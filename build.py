#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GCAR — generátor statického webu.

Spuštění:  python3 build.py
Výsledek:  hotové .html soubory vedle build.py (přepíše je).

Hlavička, patička a menu jsou definované jednou, tady. Obsah stránek
je dole ve struktuře PAGES. Po každé změně spusť build.py znovu.
"""

import os
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://gcar.cz"
ESHOP = "https://eshop.gcar.cz/cs"
ESHOP_SEARCH = "https://eshop.gcar.cz/cs/hledani/5/-1/"  # cestová URL: .../hledani/5/-1/{dotaz}
SERVIS = "http://autoserviskromeriz.cz"

# --------------------------------------------------------------------------
# Firemní údaje — jediné místo, kde jsou. Změna telefonu se promítne všude.
# --------------------------------------------------------------------------
FIRMA = {
    "nazev": "GCAR services, s.r.o.",
    "ico": "26946840",
    "dic": "CZ26946840",
}

POBOCKY = [
    {
        "key": "km",
        "nazev": "Kroměříž",
        "ulice": "Hulínská 2351/298E",
        "psc": "767 01 Kroměříž",
        "poznamka": "areál bývalé masny",
        "tel": ["+420602721994", "+420608501994"],
        "mail": "gcar@gcar.cz",
        "mapa": "https://frame.mapy.cz/s/hodukacale",
    },
    {
        "key": "uh",
        "nazev": "Staré Město",
        "ulice": "Brněnská 1395",
        "psc": "686 03 Staré Město",
        "poznamka": "",
        "tel": ["+420777141994", "+420774721884"],
        "mail": "obchod.uh@gcar.cz",
        "mapa": "https://frame.mapy.cz/s/nubelolavo",
    },
]

OTEVIRACI_DOBA = "Po–Pá 8:00–17:00 · So po domluvě (obvykle 9:00–10:00) · Neděle a svátky zavřeno"

NAV = [
    ("/", "Domů", "index"),
    ("/o-nas/", "O firmě", "o-nas"),
    ("/sortiment/", "Sortiment", "sortiment"),
    ("/akce/", "Akce", "akce"),
    ("/vyprodej/", "Výprodej", "vyprodej"),
    ("/pujcovna/", "Půjčovna", "pujcovna"),
    (SERVIS, "Servis", "servis"),
    ("/kontakt/", "Kontakt", "kontakt"),
]

KATEGORIE = [
    ("nahradni-dily", "Náhradní díly",
     "Originální i aftermarketové díly na osobní a užitkové vozy."),
    ("pneumatiky", "Pneumatiky",
     "Letní, zimní i celoroční pneumatiky na osobní, užitkové vozy a motocykly."),
    ("vybaveni-servisu", "Vybavení servisů",
     "Nářadí, přípravky, hevery, zvedáky, vyvažovačky a dílenský nábytek."),
    ("chemie", "Chemie a oleje",
     "Motorové a převodové oleje, maziva, aditiva, provozní kapaliny, autokosmetika."),
    ("ochranne-prostredky", "Ochranné prostředky",
     "Pracovní oděvy, obuv, rukavice, masky a respirátory."),
]


def tel_link(t):
    """+420602721994 -> odkaz s hezky formátovaným číslem"""
    n = t.replace("+420", "")
    return '<a href="tel:%s">%s %s %s</a>' % (t, n[0:3], n[3:6], n[6:9])


def fmt_tel(t):
    n = t.replace("+420", "")
    return "%s %s %s" % (n[0:3], n[3:6], n[6:9])


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

def header(active):
    nav_items = "".join(
        '\n      <a href="%s"%s>%s</a>' % (
            url, ' aria-current="page"' if key == active else "", label)
        for url, label, key in NAV
    )
    mob_items = "".join(
        '\n    <a href="%s">%s</a>' % (url, label) for url, label, key in NAV
    )
    return """<a class="skip" href="#obsah">Přeskočit na obsah</a>

<div class="util">
  <div class="wrap">
    <span>Prodej náhradních dílů · Kroměříž a Staré Město</span>
    <span class="sep">Po–Pá 8:00–17:00</span>
    <a href="mailto:gcar@gcar.cz">gcar@gcar.cz</a>
  </div>
</div>

<header>
  <div class="wrap">
    <a class="brand" href="/" aria-label="GCAR — domů">
      <img src="/assets/img/logo.png" alt="GCAR" width="200" height="65">
      <em>náhradní díly</em>
    </a>
    <nav class="main" aria-label="Hlavní navigace">%s
    </nav>
    <a class="btn btn-red nav-cta" href="%s">E-shop</a>
    <button class="burger" id="burger" aria-label="Otevřít menu" aria-expanded="false" aria-controls="mobmenu">
      <span class="bars" aria-hidden="true"><i></i><i></i><i></i></span>
    </button>
  </div>
</header>

<div class="mobmenu" id="mobmenu" hidden>
  <nav aria-label="Hlavní menu">%s
  </nav>
  <a class="btn btn-red btn-lg" href="%s" style="width:100%%">E-shop</a>
</div>
""" % (nav_items, ESHOP, mob_items, ESHOP)


def footer():
    pobocky_html = ""
    for p in POBOCKY:
        pobocky_html += """
      <div style="margin-bottom:18px">
        <div style="color:#fff;font-weight:600;margin-bottom:4px">%s</div>
        <div>%s, %s</div>
        <div style="margin-top:6px">%s</div>
        <div><a href="mailto:%s">%s</a></div>
      </div>""" % (
            p["nazev"], p["ulice"], p["psc"],
            " · ".join('<a href="tel:%s">%s</a>' % (t, fmt_tel(t)) for t in p["tel"]),
            p["mail"], p["mail"])

    kat_html = "".join(
        '\n        <li><a href="/sortiment/%s/">%s</a></li>' % (slug, nazev)
        for slug, nazev, _ in KATEGORIE)

    return """
<div class="callbar" aria-label="Rychlý kontakt">
  <a class="c-km" href="tel:%s">Zavolat<small>Kroměříž</small></a>
  <a class="c-uh" href="tel:%s">Zavolat<small>Staré Město</small></a>
</div>

<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <img src="/assets/img/logo-inverse.png" alt="GCAR">
        <p style="margin:0">Dovoz náhradních dílů pro osobní a užitkové vozy světových značek a jejich distribuce do autoservisů a obchodů.</p>
      </div>
      <div>
        <h4>Sortiment</h4>
        <ul>%s
        </ul>
      </div>
      <div>
        <h4>Firma</h4>
        <ul>
          <li><a href="/o-nas/">O firmě</a></li>
          <li><a href="/akce/">Akce</a></li>
          <li><a href="/vyprodej/">Výprodej</a></li>
          <li><a href="/pujcovna/">Půjčovna</a></li>
          <li><a href="%s">Autoservis</a></li>
          <li><a href="%s">E-shop</a></li>
        </ul>
      </div>
      <div>
        <h4>Kontakt</h4>%s
      </div>
    </div>
    <div class="fbottom">
      <span>%s · IČO %s · DIČ %s</span>
      <span class="sep"><a href="/kontakt/">Kontakt</a></span>
      <span>© %d GCAR.cz</span>
    </div>
  </div>
</footer>
""" % (POBOCKY[0]["tel"][0], POBOCKY[1]["tel"][0], kat_html, SERVIS, ESHOP,
       pobocky_html, FIRMA["nazev"], FIRMA["ico"], FIRMA["dic"], date.today().year)


def layout(title, desc, body, active, canonical):
    return """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="website">
<meta property="og:locale" content="cs_CZ">
<link rel="icon" href="/assets/img/logo.png">
<link rel="preload" href="/assets/fonts/archivo-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
%s
<main id="obsah">
%s
</main>
%s
<script src="/assets/js/main.js" defer></script>
</body>
</html>
""" % (title, desc, DOMAIN, canonical, title, desc, header(active), body, footer())


def page_head(h1, lede, crumbs=None):
    c = ""
    if crumbs:
        parts = ['<a href="/">Domů</a>']
        for url, label in crumbs:
            parts.append('<a href="%s">%s</a>' % (url, label) if url else "<span>%s</span>" % label)
        c = '<p class="crumbs">%s</p>' % '<span>/</span>'.join(parts)
    return """<div class="page-head">
  <div class="wrap">
    %s
    <h1>%s</h1>
    <p class="lede">%s</p>
  </div>
</div>""" % (c, h1, lede)


def kontakt_sekce():
    cards = ""
    for p in POBOCKY:
        pozn = "<br>" + p["poznamka"] if p["poznamka"] else ""
        cards += """
      <div class="ccard">
        <h3>%s</h3>
        <address>%s, %s%s</address>
        <div class="tels">%s</div>
        <a class="mail" href="mailto:%s">%s</a>
      </div>""" % (
            p["nazev"], p["ulice"], p["psc"], pozn,
            "".join(tel_link(t) for t in p["tel"]),
            p["mail"], p["mail"])

    return """<section class="contact" id="kontakt">
  <div class="wrap">
    <div>
      <h2>Ozvěte se</h2>
      <p class="lede">Máme dvě pobočky — v Kroměříži a ve Starém Městě.</p>
      <p style="margin-top:22px"><a class="btn btn-red btn-lg" href="tel:%s">Zavolat %s</a></p>
      <p style="color:#7E88A5;font-size:14.5px;margin-top:18px">%s</p>
    </div>
    <div>%s
    </div>
  </div>
</section>""" % (POBOCKY[0]["tel"][0], fmt_tel(POBOCKY[0]["tel"][0]), OTEVIRACI_DOBA, cards)


def aside_pomoc():
    return """<aside class="aside-card">
  <h3>Zeptejte se nás</h3>
  <p>Nevíte si rady s výběrem, nebo hledáte konkrétní díl? Zavolejte nám.</p>
  <a class="btn btn-red" href="tel:%s">Zavolat %s</a>
  <a class="btn btn-ghost" href="/kontakt/">Napsat poptávku</a>
</aside>""" % (POBOCKY[0]["tel"][0], fmt_tel(POBOCKY[0]["tel"][0]))



# ==========================================================================
# OBSAH STRÁNEK
#
# PRAVIDLO: tady je JEN text, který doopravdy stojí na gcar.cz.
# Nic jsem si nedomyslel. Místa, kde obsah chybí, jsou označená
# komentářem CHYBI a v README je seznam otázek pro majitele.
# ==========================================================================

# Seznam ze sekce "Co nabízíme?" na současné homepage — doslova.
DILY_CHIPS = ["Brzdy", "Spojky", "Tlumiče", "Filtry", "Řemeny", "Kladky", "Ložiska",
              "Výfuky", "Čepy", "Startéry", "Alternátory", "Karosářské díly",
              "Vybavení servisu", "Oleje", "Chladiče", "Poloosy"]

# Doporučené zboží — odkazy do e-shopu.
# Ceny tu ZÁMĚRNĚ nejsou: na starém gcar.cz byly zastaralé (stahovák pružin
# 4 846 Kč vs. 2 900,80 Kč v e-shopu). Cena patří na jedno místo — do e-shopu.
ZBOZI = [
    ("ATH HEINL · ATH-150031", "Vyvažovačka kol ATH W 42 LED 2D", "64 800 Kč", "3049631",
     ESHOP + "/katalog/detail-zbozi/vyvazovacka-kol-ath-w-42-led-2d/ath-heinl/ath-150031/3049631/"),
    ("KS TOOLS · KST-BT153207", "Nářaďový vozík KS Tools, kompletně vybavený", "18 207 Kč", "4779125",
     ESHOP + "/katalog/detail-zbozi/naradovy-vozik-ks-tools-perfektne/ks-tools/kst-bt153207/4779125/"),
    ("THULE · THU-12185", "Nosič kol na tažné zařízení Thule VeloCompact, 3 kola", "13 990 Kč", "3898539",
     ESHOP + "/katalog/detail-zbozi/nosic-kol-na-tz-thule-velocompact-3-kol/thule/thu-12185/3898539/"),
    ("ENERGY · ENG-NE00016", "Stahovák pružin", "4 846 Kč", "222424",
     ESHOP + "/katalog/detail-zbozi/stahovak-pruzin-skvely-pomer-cena-provedeni/energy/eng-ne00016/222424/"),
    ("ENERGY · ENG-NE00118", "Sada kleští na stahovací pásky, 9 ks", "1 666 Kč", "949262",
     ESHOP + "/katalog/detail-zbozi/sada-klesti-na-stahov-pasky-9ks/energy/eng-ne00118/949262/"),
    ("ENERGY · ENG-NE00314", "Přísavky na manipulaci s okny, trojité", "270 Kč", "949651",
     ESHOP + "/katalog/detail-zbozi/prisavky-na-manimulaci-s-okny-triangl/energy/eng-ne00314/949651/"),
]


def zbozi_grid():
    out = ""
    for kod, nazev, cena, img, url in ZBOZI:
        out += """
      <a class="good" href="%s">
        <span class="ph"><img src="https://eshop.gcar.cz/Image.ashx?type=3&amp;id=%s" alt="" loading="lazy" onerror="this.replaceWith(Object.assign(document.createElement('span'),{textContent:'FOTO'}))"></span>
        <span class="code">%s</span>
        <h3>%s</h3>
        <span class="price"><span>Cena a dostupnost v e-shopu</span></span>
      </a>""" % (url, img, kod, nazev)
    return out


def branches_panel():
    out = ""
    for p in POBOCKY:
        out += """
      <div class="branch" data-branch="%s">
        <div class="branch-top">
          <span class="dot"></span>
          <h3>%s</h3>
          <span class="status">—</span>
        </div>
        <address>%s, %s</address>
        <div class="tels">%s</div>
      </div>""" % (p["key"], p["nazev"], p["ulice"], p["psc"],
                   "".join(tel_link(t) for t in p["tel"]))
    return out


def eshop_box(text, popisek="Zobrazit v e-shopu"):
    return """<div class="note">
  <p>%s</p>
  <p style="margin-top:14px"><a class="btn btn-red" href="__ESHOP__">%s</a></p>
</div>""" % (text, popisek)


# --------------------------------------------------------------------------
# HOMEPAGE
# H1 i podtitulek doslova podle současného webu.
# --------------------------------------------------------------------------
HOME = """<div class="hero">
  <div class="wrap">
    <div>
      <h1>Prodej náhradních dílů</h1>
      <p class="lede">Zaměřujeme se na dovoz náhradních dílů pro osobní a užitkové vozy světových značek a jejich distribuci do autoservisů a obchodů.</p>

      <form class="finder" id="hledani" data-base="__SEARCH__" role="search">
        <input name="q" type="search" placeholder="Hledat díl, značku nebo katalogové číslo" aria-label="Hledat v e-shopu" required>
        <button type="submit">Hledat</button>
      </form>
      <noscript><p class="finder-note"><a href="__ESHOP__">Přejít do e-shopu a hledat tam</a></p></noscript>
      <p class="finder-note">Hledat můžete podle kódu, textu i vozidla — e-shop má i VIN katalog. Nevíte si rady? <a href="tel:__TEL__">Zavolejte na __TELF__</a>.</p>
      <p class="hero-cta" style="margin:22px 0 0"><a class="btn btn-ghost" href="/o-nas/">Více o nás</a></p>
    </div>

    <div class="branches" id="pobocky">__BRANCHES__
      <div class="hours"><b>Po–Pá 8:00–17:00</b> · So po domluvě (obvykle 9:00–10:00) · Neděle a svátky zavřeno</div>
    </div>
  </div>
</div>

<section class="about" id="o-nas">
  <div class="wrap">
    <div><h2>Kdo jsme</h2></div>
    <div>
      <p>Firma dováží a distribuuje náhradní díly pro osobní a užitkové vozy. Široký sortiment náhradních dílů od světových výrobců nás řadí k největším prodejcům v regionu. Jsme obchodním partnerem jedné z největších firem na evropském trhu.</p>
      <p style="margin:0"><a class="btn btn-line" href="/o-nas/">Více o nás</a></p>
    </div>
  </div>
</section>

<section id="sortiment">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <h2>Co nabízíme</h2>
        <p class="lede">Kompletní sortiment náhradních dílů na osobní vozy.</p>
      </div>
      <a class="more" href="/sortiment/">Celý sortiment</a>
    </div>

    <div class="chips" style="margin-bottom:34px">__CHIPS__</div>

    <div class="cats">
      <a class="cat is-wide" href="/sortiment/nahradni-dily/">
        <h3>Náhradní díly</h3>
        <p>Originální i aftermarketové díly na osobní a užitkové vozy.</p>
      </a>
      <a class="cat" href="/sortiment/pneumatiky/">
        <h3>Pneumatiky</h3>
      </a>
      <a class="cat" href="/sortiment/vybaveni-servisu/">
        <h3>Vybavení servisů</h3>
      </a>
      <a class="cat" href="/sortiment/chemie/">
        <h3>Chemie a oleje</h3>
      </a>
      <a class="cat" href="/sortiment/ochranne-prostredky/">
        <h3>Ochranné prostředky</h3>
      </a>
    </div>
  </div>
</section>

<section id="zbozi" class="delivery">
  <div class="wrap">
    <div class="sec-head">
      <div><h2>Doporučené zboží</h2></div>
      <a class="more" href="__ESHOP__">Do e-shopu</a>
    </div>
    <div class="goods">__ZBOZI__</div>
  </div>
</section>

<section class="brands">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <h2>Značky, které u nás najdete</h2>
        <p class="lede">Katalog dílů v e-shopu běží na databázi TecDoc — díl dohledáte podle vozu, VIN nebo katalogového čísla.</p>
      </div>
      <a class="more" href="__ESHOP__">Prohlédnout katalog</a>
    </div>
    <div class="brandrow">__ZNACKY__</div>
  </div>
</section>

<section id="sluzby">
  <div class="wrap">
    <div class="sec-head"><div><h2>Další služby</h2></div></div>
    <div class="svc">
      <a href="__SERVIS__"><h3>Autoservis</h3><p>Provozujeme autoservis v Kroměříži.</p></a>
      <a href="/pujcovna/"><h3>Půjčovna</h3><p>Půjčovna autodoplňků.</p></a>
      <a href="/vyprodej/"><h3>Výprodej</h3><p>Zboží za snížené ceny.</p></a>
      <a href="/akce/"><h3>Akce</h3><p>Aktuální akční nabídky.</p></a>
    </div>
  </div>
</section>

__KONTAKT__
"""

# --------------------------------------------------------------------------
O_NAS = """<div class="split">
  <div class="prose">
    <p>Zaměřujeme se na dovoz náhradních dílů pro osobní a užitkové vozy světových značek a jejich distribuci do autoservisů a obchodů.</p>
    <p>Firma dováží a distribuuje náhradní díly pro osobní a užitkové vozy. Široký sortiment náhradních dílů od světových výrobců nás řadí k největším prodejcům v regionu. Jsme obchodním partnerem jedné z největších firem na evropském trhu.</p>

    <h2>Pobočky</h2>
    <p>
      <strong>Kroměříž</strong> — Hulínská 2351/298E, 767 01 Kroměříž<br>
      <strong>Staré Město</strong> — Brněnská 1395, 686 03 Staré Město
    </p>

    <h2>Fakturační údaje</h2>
    <p>
      GCAR services, s.r.o.<br>
      IČO 26946840<br>
      DIČ CZ26946840
    </p>
  </div>
  __ASIDE__
</div>
"""

# --------------------------------------------------------------------------
SORTIMENT = """<div class="prose" style="margin-bottom:36px">
  <p>Kompletní sortiment náhradních dílů na osobní vozy.</p>
</div>

<div class="chips" style="margin-bottom:40px">__CHIPS__</div>

<div class="cats" style="margin-bottom:40px">
  <a class="cat is-wide" href="/sortiment/nahradni-dily/">
    <h3>Náhradní díly</h3>
    <p>Originální i aftermarketové díly na osobní a užitkové vozy.</p>
  </a>
  <a class="cat" href="/sortiment/pneumatiky/"><h3>Pneumatiky</h3></a>
  <a class="cat" href="/sortiment/vybaveni-servisu/"><h3>Vybavení servisů</h3></a>
  <a class="cat" href="/sortiment/chemie/"><h3>Chemie a oleje</h3></a>
  <a class="cat" href="/sortiment/ochranne-prostredky/"><h3>Ochranné prostředky</h3></a>
</div>
"""

# --------------------------------------------------------------------------
# Podstránky sortimentu.
# CHYBI: skutečné texty z gcar.cz/sortiment/*. Zatím jen to, co se dá
# doložit z homepage a z e-shopu.
# --------------------------------------------------------------------------
KAT_DILY = """<div class="split">
  <div class="prose">
    <p>Originální i aftermarketové díly na osobní a užitkové vozy. Sortiment originálních dílů se dostává i na pulty aftermarketu — jen v jiné krabičce, než ji znáte ze značkového servisu.</p>
    <h2>Co vedeme</h2>
    <div class="chips">__CHIPS__</div>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

KAT_PNEU = """<div class="split">
  <div class="prose">
    <p>Pneumatiky na osobní a užitkové vozy i na motocykly.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

KAT_VYBAVENI = """<div class="split">
  <div class="prose">
    <p>Vybavení pro autoservisy a dílny — nářadí, přípravky, zvedací technika, vybavení pneuservisu a dílenský nábytek.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

KAT_CHEMIE = """<div class="split">
  <div class="prose">
    <p>Motorové a převodové oleje, maziva, provozní kapaliny a autochemie.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

KAT_OOPP = """<div class="split">
  <div class="prose">
    <p>Ochranné pracovní prostředky — oděvy, obuv, rukavice, masky a respirátory.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

# --------------------------------------------------------------------------
AKCE = """<div class="split">
  <div class="prose">
    <p>Aktuální akční nabídky najdete v našem e-shopu, kde jsou vždy platné ceny a skladová dostupnost.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

VYPRODEJ = """<div class="split">
  <div class="prose">
    <p>Zboží za snížené ceny. Aktuální výprodejovou nabídku najdete v e-shopu.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

PUJCOVNA = """<div class="split">
  <div class="prose">
    <p>Provozujeme půjčovnu autodoplňků. Dostupnost na konkrétní termín a podmínky výpůjčky vám sdělíme telefonicky.</p>
  </div>
  __ASIDE__
</div>
"""


# --------------------------------------------------------------------------
def kontakt_body():
    cards = ""
    for p in POBOCKY:
        pozn = "<br>" + p["poznamka"] if p["poznamka"] else ""
        cards += """
    <div class="ccard" style="border-color:var(--zinc);background:#fff;color:var(--ink)">
      <h3 style="color:var(--ink)">%s</h3>
      <address style="color:var(--ink-soft)">%s, %s%s</address>
      <div class="tels" style="margin-bottom:12px">%s</div>
      <a class="mail" href="mailto:%s" style="color:var(--ink)">%s</a>
    </div>""" % (p["nazev"], p["ulice"], p["psc"], pozn,
                 "".join(tel_link(t) for t in p["tel"]), p["mail"], p["mail"])

    # CHYBI: odkazy na mapy. Až budou, vloží se sem iframe (styl .maps je hotový).
    return """<div class="split">
  <div>
    %s
    <div style="background:var(--zinc-light);border-radius:4px;padding:18px 22px">
      <strong style="font-size:15px">Otevírací doba</strong>
      <p style="margin:6px 0 0;font-size:15px;color:var(--ink-soft)">%s</p>
    </div>

    <div class="prose" style="margin-top:28px">
      <h2>Fakturační údaje</h2>
      <p>GCAR services, s.r.o.<br>IČO 26946840<br>DIČ CZ26946840</p>
    </div>
  </div>

  <div>
    <form class="form" id="kontaktni-formular" novalidate>
      <h3 style="margin-bottom:14px">Napište nám</h3>
      <div class="row">
        <div class="field">
          <label for="f-jmeno">Jméno a příjmení *</label>
          <input id="f-jmeno" name="jmeno" type="text" required autocomplete="name">
        </div>
        <div class="field">
          <label for="f-firma">Firma</label>
          <input id="f-firma" name="firma" type="text" autocomplete="organization">
        </div>
      </div>
      <div class="row">
        <div class="field">
          <label for="f-tel">Telefon *</label>
          <input id="f-tel" name="telefon" type="tel" required autocomplete="tel" inputmode="tel">
        </div>
        <div class="field">
          <label for="f-mail">E-mail</label>
          <input id="f-mail" name="email" type="email" autocomplete="email" inputmode="email">
        </div>
      </div>
      <div class="field">
        <label for="f-vozidlo">Vozidlo nebo VIN</label>
        <input id="f-vozidlo" name="vozidlo" type="text">
      </div>
      <div class="field">
        <label for="f-zprava">Zpráva *</label>
        <textarea id="f-zprava" name="zprava" required></textarea>
      </div>
      <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn-red btn-lg" type="submit" style="width:100%%">Odeslat</button>
    </form>
  </div>
</div>
""" % (cards, OTEVIRACI_DOBA)


CTYRISTOCTYRI = """<div class="prose" style="text-align:center;margin:0 auto;padding:60px 0">
  <h2>Tuhle stránku jsme nenašli</h2>
  <p>Možná se přesunula, nebo je v odkazu překlep.</p>
  <p style="margin-top:24px">
    <a class="btn btn-red" href="/">Na hlavní stránku</a>
    <a class="btn btn-ghost" href="/sortiment/">Sortiment</a>
  </p>
</div>
"""


# ==========================================================================
# Značky doložené z e-shopu (patička + produktové karty).
# CHYBI: úplný seznam a souhlas s použitím log — zatím jen text, ne loga.
ZNACKY = ["CASTROL", "TOTAL", "ELF", "BOLL", "AMTRA", "ATAS",
          "ENERGY", "KS TOOLS", "ATH HEINL", "THULE"]


def znacky_row():
    return "".join('<span>%s</span>' % z for z in ZNACKY)


def chips(items):
    return "".join('<i class="chip">%s</i>' % i for i in items)


PAGES = []


def add(path, title, desc, body, active, head=None):
    PAGES.append({"path": path, "title": title, "desc": desc,
                  "body": body, "active": active, "head": head})


add("index.html",
    "GCAR — prodej náhradních dílů | Kroměříž, Staré Město",
    "Dovoz náhradních dílů pro osobní a užitkové vozy světových značek a jejich distribuce do autoservisů a obchodů. Pobočky Kroměříž a Staré Město.",
    HOME, "index")

add("o-nas/index.html",
    "O nás | GCAR",
    "GCAR services, s.r.o. — dovoz a distribuce náhradních dílů pro osobní a užitkové vozy. Pobočky v Kroměříži a ve Starém Městě.",
    O_NAS, "o-nas",
    page_head("O nás",
              "Dovoz náhradních dílů pro osobní a užitkové vozy světových značek a jejich distribuce do autoservisů a obchodů.",
              [(None, "O nás")]))

add("sortiment/index.html",
    "Sortiment | GCAR",
    "Náhradní díly, pneumatiky, vybavení servisů, chemie a oleje a ochranné pracovní prostředky.",
    SORTIMENT, "sortiment",
    page_head("Sortiment", "Kompletní sortiment náhradních dílů na osobní vozy.",
              [(None, "Sortiment")]))

KAT_BODY = {
    "nahradni-dily": (KAT_DILY, "Náhradní díly | GCAR",
        "Originální i aftermarketové náhradní díly na osobní a užitkové vozy.",
        "Náhradní díly", "Originální i aftermarketové díly na osobní a užitkové vozy."),
    "pneumatiky": (KAT_PNEU, "Pneumatiky | GCAR",
        "Pneumatiky na osobní a užitkové vozy i na motocykly.",
        "Pneumatiky", "Pneumatiky na osobní a užitkové vozy i na motocykly."),
    "vybaveni-servisu": (KAT_VYBAVENI, "Vybavení servisů | GCAR",
        "Nářadí, přípravky, zvedací technika a dílenský nábytek pro autoservisy.",
        "Vybavení servisů", "Nářadí, přípravky, zvedací technika a dílenský nábytek."),
    "chemie": (KAT_CHEMIE, "Chemie a oleje | GCAR",
        "Motorové a převodové oleje, maziva, provozní kapaliny a autochemie.",
        "Chemie a oleje", "Oleje, maziva, provozní kapaliny a autochemie."),
    "ochranne-prostredky": (KAT_OOPP, "Ochranné prostředky | GCAR",
        "Ochranné pracovní prostředky — oděvy, obuv, rukavice, masky a respirátory.",
        "Ochranné prostředky", "Oděvy, obuv, rukavice, masky a respirátory."),
}

for slug, nazev, _ in KATEGORIE:
    body, title, desc, h1, lede = KAT_BODY[slug]
    add("sortiment/%s/index.html" % slug, title, desc, body, "sortiment",
        page_head(h1, lede, [("/sortiment/", "Sortiment"), (None, nazev)]))

add("akce/index.html", "Akce | GCAR", "Aktuální akční nabídky GCAR.",
    AKCE, "akce", page_head("Akce", "Aktuální akční nabídky.", [(None, "Akce")]))

add("vyprodej/index.html", "Výprodej | GCAR", "Zboží za snížené ceny.",
    VYPRODEJ, "vyprodej", page_head("Výprodej", "Zboží za snížené ceny.", [(None, "Výprodej")]))

add("pujcovna/index.html", "Půjčovna | GCAR", "Půjčovna autodoplňků.",
    PUJCOVNA, "pujcovna", page_head("Půjčovna", "Půjčovna autodoplňků.", [(None, "Půjčovna")]))

add("kontakt/index.html", "Kontakt | GCAR",
    "Kontakty na pobočky GCAR v Kroměříži a ve Starém Městě — adresy, telefony, e-maily a otevírací doba.",
    kontakt_body(), "kontakt",
    page_head("Kontakt", "Dvě pobočky — Kroměříž a Staré Město.", [(None, "Kontakt")]))

add("404.html", "Stránka nenalezena | GCAR", "Požadovaná stránka nebyla nalezena.",
    CTYRISTOCTYRI, "")


# ==========================================================================
def render(page):
    body = page["body"]
    body = body.replace("__ESHOPBOX__", eshop_box(
        "Aktuální nabídku, ceny a skladovou dostupnost najdete v našem e-shopu."))
    body = body.replace("__CHIPS__", chips(DILY_CHIPS))
    body = body.replace("__ZNACKY__", znacky_row())
    body = body.replace("__ZBOZI__", zbozi_grid())
    body = body.replace("__BRANCHES__", branches_panel())
    body = body.replace("__KONTAKT__", kontakt_sekce())
    body = body.replace("__ASIDE__", aside_pomoc())
    body = body.replace("__SEARCH__", ESHOP_SEARCH)
    body = body.replace("__ESHOP__", ESHOP)
    body = body.replace("__SERVIS__", SERVIS)
    body = body.replace("__TELF__", fmt_tel(POBOCKY[0]["tel"][0]).replace(" ", "&nbsp;"))
    body = body.replace("__TEL__", POBOCKY[0]["tel"][0])

    if page["head"]:
        body = page["head"] + '\n<section>\n  <div class="wrap">\n' + body + "\n  </div>\n</section>\n"

    return layout(page["title"], page["desc"], body, page["active"],
                  "/" + page["path"].replace("index.html", ""))


def sitemap():
    today = date.today().isoformat()
    urls = "".join(
        "  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n"
        % (DOMAIN + "/" + p["path"].replace("index.html", ""), today)
        for p in PAGES if p["path"] != "404.html")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls


def main():
    for page in PAGES:
        out = os.path.join(ROOT, page["path"])
        os.makedirs(os.path.dirname(out) or ROOT, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(render(page))
        print("  ✓ /%s" % page["path"])
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap())
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN)
    print("\nHotovo — %d stránek" % len(PAGES))


if __name__ == "__main__":
    main()
