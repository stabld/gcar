#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GCAR — generátor statického webu.

Spuštění:  python3 build.py
Výsledek:  hotové .html soubory vedle build.py (přepíše je).

Hlavička, patička a menu jsou definované jednou, tady. Obsah stránek
je dole ve struktuře PAGES. Po každé změně spusť build.py znovu.
"""

import hashlib
import os
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://gcar.cz"
ESHOP = "https://eshop.gcar.cz/cs"
ESHOP_SEARCH = "https://eshop.gcar.cz/cs/hledani/5/-1/"  # cestová URL: .../hledani/5/-1/{dotaz}
SERVIS = "http://autoserviskromeriz.cz"

# Kam chodí poptávky z kontaktního formuláře.
# Prázdné = formulář otevře poštovního klienta (záložní režim).
# Po založení formuláře na formspree.io sem vlož jeho adresu,
# např. "https://formspree.io/f/xayzbwkd", a spusť build.py.
FORM_ENDPOINT = "https://formspree.io/f/xnpnzzre"

# Právní dokumenty — společné s e-shopem, proto na ně jen odkazujeme.
PRAVNI = [
    ("Obchodní podmínky", "https://eshop.gcar.cz/cs/clanek/obchodni-podminky-cz"),
    ("Reklamační řád", "https://eshop.gcar.cz/cs/clanek/reklamacni-rad-cz"),
    ("Ochrana osobních údajů", "https://eshop.gcar.cz/cs/pravni-informace/ochrana-osobnich-udaju"),
    ("Používání cookies", "https://eshop.gcar.cz/cs/pravni-informace/pouzivani-cookies"),
]

# Katalogy výrobců. Vedou mimo gcar.cz — slouží k dohledání dílu,
# objednává se pak u nás. Proto jsou označené jako externí.
KATALOGY_VYROBCU = {
    "chemie": [
        ("Castrol — výběr oleje podle vozu",
         "https://www.castrol.com/cs_cz/czech_republic/home/product-finder.html",
         "Zadáte značku a model a Castrol ukáže, který olej do vozu patří."),
        ("BOLL — katalog chemie",
         "https://www.boll.pl/cz/produkty/",
         "Kompletní sortiment autochemie BOLL."),
    ],
    "nahradni-dily": [
        ("AS-PL — katalog startérů a alternátorů",
         "https://as-pl.com/cs/index",
         "Vyhledávání startérů, alternátorů a jejich dílů podle vozu i čísla."),
        ("Tažná zařízení",
         "https://eshop.gcar.cz/cs/katalog/univerzalni-dily",
         "Nabídka tažných zařízení v našem e-shopu. Montáž zajistíme v servisu."),
    ],
}
def _ic(body):
    return ('<svg class="ico" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % body

IKONY = {
    # brzdový kotouč se třmenem
    "nahradni-dily": _ic('<circle cx="11" cy="12" r="8"/><circle cx="11" cy="12" r="2.5"/><path d="M11 4v3M11 17v3M3 12h3M16 12h3M5.3 6.3l2.1 2.1M14.6 15.6l2.1 2.1M5.3 17.7l2.1-2.1"/><path d="M19 6c1.6 1.6 2.5 3.7 2.5 6s-.9 4.4-2.5 6"/>'),
    # pneumatika
    "pneumatiky": _ic('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/><path d="M12 3v4.5M12 16.5V21M3 12h4.5M16.5 12H21"/>'),
    # klíč
    "vybaveni-servisu": _ic('<path d="M14.5 4.5a4.5 4.5 0 0 0-4.2 6.1L3.5 17.4V20.5h3.1l1-1.6 1.6-.4.4-1.7 1.6-.4 1.4-1.4a4.5 4.5 0 0 0 5.9-5.6l-2.8 2.8-2.4-.6-.6-2.4 2.8-2.8a4.5 4.5 0 0 0-2-.4z"/>'),
    # kanystr / kapka oleje
    "chemie": _ic('<path d="M12 3.5c3 3.8 5.5 6.6 5.5 9.6a5.5 5.5 0 0 1-11 0c0-3 2.5-5.8 5.5-9.6z"/><path d="M9.5 14a2.6 2.6 0 0 0 2.5 2.4"/>'),
    # rukavice / štít
    "ochranne-prostredky": _ic('<path d="M12 3l7.5 2.8v5.6c0 4.4-3 7.9-7.5 9.6-4.5-1.7-7.5-5.2-7.5-9.6V5.8z"/><path d="M8.6 12.2l2.3 2.3 4.5-4.7"/>'),
}

FORM_MAIL = "gcar@gcar.cz"
LPG = "https://www.lpg-kromeriz.cz"

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
        # Potvrzeno majitelem: 28E (ne 298E, jak uvádí starý gcar.cz)
        "ulice": "Hulínská 2351/28E",
        "psc": "767 01 Kroměříž",
        "poznamka": "areál bývalé masny",
        # Potvrzeno majitelem 16. 9. 2026: 602 721 994 je telefon (ne fax),
        # přestože patička e-shopu ho uvádí jako fax. Hlavní číslo na web.
        "tel": ["+420602721994", "+420608501994"],
        "mail": "gcar@gcar.cz",
        "mapa": "https://frame.mapy.cz/s/hodukacale",
    },
    {
        "key": "uh",
        "nazev": "Staré Město",
        # Potvrzeno: Brněnská 1395 (ne "Za Špicí 1798", jak uvádí ekatalog.cz)
        "ulice": "Brněnská 1395",
        "psc": "686 03 Staré Město",
        "poznamka": "",
        "tel": ["+420777141994", "+420774721884"],
        "mail": "obchod.uh@gcar.cz",
        "mapa": "https://frame.mapy.cz/s/nubelolavo",
    },
]

OTEVIRACI_DOBA = "Po–Pá 8:00–17:00 · So 9:00–10:00 · Neděle a svátky zavřeno"

NAV = [
    ("/", "Domů", "index"),
    ("/o-nas/", "O nás", "o-nas"),
    ("/sortiment/", "Autodíly", "sortiment"),
    ("https://www.autoserviskromeriz.cz", "Autoservis", "autoservis"),
    ("https://www.lpg-kromeriz.cz", "LPG", "lpg"),
    ("/pujcovna/", "Půjčovna", "pujcovna"),
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


def asset(path):
    """Přidá k adrese otisk obsahu: /assets/css/style.css?v=a1b2c3d4.
    Bez toho by prohlížeč po změně souboru dál používal starou verzi
    z cache — přesně na tom se web zasekl 15. 9. 2026."""
    full = os.path.join(ROOT, path.lstrip("/"))
    try:
        with open(full, "rb") as f:
            h = hashlib.md5(f.read()).hexdigest()[:8]
        return "%s?v=%s" % (path, h)
    except OSError:
        return path


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
        '\n      <a href="%s"%s%s>%s</a>' % (
            url, ' aria-current="page"' if key == active else "",
            ' target="_blank" rel="noopener"' if url.startswith("http") else "", label)
        for url, label, key in NAV
    )
    mob_items = "".join(
        '\n    <a href="%s"%s>%s</a>' % (
            url, ' target="_blank" rel="noopener"' if url.startswith("http") else "", label)
        for url, label, key in NAV
    )
    return """<a class="skip" href="#obsah">Přeskočit na obsah</a>

<div class="util">
  <div class="wrap">
    <span>Autodíly · Autoservis · LPG</span>
    <span class="sep">Po–Pá 8:00–17:00</span>
    <a href="mailto:gcar@gcar.cz">gcar@gcar.cz</a>
  </div>
</div>

<header>
  <div class="wrap">
    <a class="brand" href="/" aria-label="GCAR — domů">
      <img class="logo-light" src="/assets/img/logo.svg" alt="GCAR" width="200" height="65">
      <img class="logo-dark" src="/assets/img/logo-inverse.svg" alt="" width="200" height="65" aria-hidden="true">
      <em>Jistá cesta k úspěchu</em>
    </a>
    <nav class="main" aria-label="Hlavní navigace">%s
    </nav>
    <a class="btn btn-red nav-cta" href="%s">E-shop</a>
    <button class="theme-toggle" id="theme-toggle" type="button" aria-label="Přepnout noční režim">
      <svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
        <circle cx="12" cy="12" r="4.2"/>
        <path d="M12 2.2v2.4M12 19.4v2.4M2.2 12h2.4M19.4 12h2.4M5.1 5.1l1.7 1.7M17.2 17.2l1.7 1.7M18.9 5.1l-1.7 1.7M6.8 17.2l-1.7 1.7"/>
      </svg>
      <svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M20.5 14.3A8.6 8.6 0 0 1 9.7 3.5a8.6 8.6 0 1 0 10.8 10.8z"/>
      </svg>
    </button>
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
        <div style="color:var(--band-text);font-weight:600;margin-bottom:4px">%s</div>
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

    pravni_html = "".join(
        '<a href="%s" rel="noopener">%s</a>' % (url, nazev) for nazev, url in PRAVNI)

    return """
<div class="volani" id="volani">
  <div class="volani-panel" id="volani-panel" hidden>
    <a href="tel:%s"><b>Kroměříž</b><span>%s</span></a>
    <a href="tel:%s"><b>Staré Město</b><span>%s</span></a>
  </div>
  <button class="volani-btn" id="volani-btn" type="button"
          aria-expanded="false" aria-controls="volani-panel" aria-label="Zavolat na pobočku">
    <svg class="ik-tel" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .3 1.9.6 2.8a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.5 2.8.6a2 2 0 0 1 1.7 2z"/>
    </svg>
    <svg class="ik-krizek" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"
         stroke-linecap="round" aria-hidden="true">
      <path d="M6 6l12 12M18 6L6 18"/>
    </svg>
  </button>
</div>

<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <img src="/assets/img/logo-inverse.svg" alt="GCAR">
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
          <li><a href="https://www.autoserviskromeriz.cz" target="_blank" rel="noopener">Autoservis</a></li>
          <li><a href="https://www.lpg-kromeriz.cz" target="_blank" rel="noopener">LPG</a></li>
          <li><a href="%s">E-shop</a></li>
        </ul>
      </div>
      <div>
        <h4>Kontakt</h4>%s
      </div>
    </div>
    <div class="fpravni">%s</div>
    <div class="fbottom">
      <span>%s · IČO %s · DIČ %s</span>
      <span class="sep"><a href="/kontakt/">Kontakt</a></span>
      <span>Jistá cesta k úspěchu</span>
      <span>© %d GCAR.cz</span>
    </div>
  </div>
</footer>
""" % (POBOCKY[0]["tel"][0], fmt_tel(POBOCKY[0]["tel"][0]),
       POBOCKY[1]["tel"][0], fmt_tel(POBOCKY[1]["tel"][0]),
       kat_html, ESHOP,
       pobocky_html, pravni_html,
       FIRMA["nazev"], FIRMA["ico"], FIRMA["dic"], date.today().year)


def schema_org():
    """Strukturovaná data — díky nim Google zobrazí adresu, otevírací dobu
    a telefon přímo ve výsledcích vyhledávání. Pro místní firmu je to
    nejcennější technická věc na celém webu."""
    import json
    pobocky = []
    for p in POBOCKY:
        pobocky.append({
            "@type": "AutoPartsStore",
            "name": "GCAR " + p["nazev"],
            "image": DOMAIN + "/assets/img/share.png",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": p["ulice"],
                "addressLocality": p["psc"].split(" ", 2)[-1],
                "postalCode": " ".join(p["psc"].split(" ")[:2]),
                "addressCountry": "CZ",
            },
            "telephone": p["tel"][0],
            "email": p["mail"],
            "url": DOMAIN + "/kontakt/",
            "openingHoursSpecification": [
                {"@type": "OpeningHoursSpecification",
                 "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                 "opens": "08:00", "closes": "17:00"},
                {"@type": "OpeningHoursSpecification",
                 "dayOfWeek": "Saturday", "opens": "09:00", "closes": "10:00"},
            ],
        })

    data = {
        "@context": "https://schema.org",
        "@graph": [{
            "@type": "Organization",
            "@id": DOMAIN + "/#organizace",
            "name": FIRMA["nazev"],
            "alternateName": "GCAR",
            "url": DOMAIN,
            "logo": DOMAIN + "/assets/img/logo.png",
            "email": POBOCKY[0]["mail"],
            "telephone": POBOCKY[0]["tel"][0],
            "vatID": FIRMA["dic"],
            "taxID": FIRMA["ico"],
            "sameAs": [ESHOP, SERVIS, LPG],
        }] + pobocky,
    }
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(data, ensure_ascii=False, separators=(",", ":")))


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
<meta property="og:url" content="%s%s">
<meta property="og:site_name" content="GCAR">
<meta property="og:image" content="%s/assets/img/share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1A243D">
<script>
/* Nastaví režim dřív, než se stránka vykreslí — jinak by při načtení
   probliklo světlé pozadí. Proto je tenhle skript v hlavičce a ne v main.js. */
(function(){try{var t=localStorage.getItem("gcar-theme");
if(t!=="dark"&&t!=="light"){t=window.matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light";}
document.documentElement.setAttribute("data-theme",t);}catch(e){}})();
</script>
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/img/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
%s
<link rel="preload" href="/assets/fonts/archivo-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%s">
<link rel="stylesheet" href="%s">
</head>
<body>
%s
<main id="obsah">
%s
</main>
%s
<script src="%s" defer></script>
</body>
</html>
""" % (title, desc, DOMAIN, canonical, title, desc,
       DOMAIN, canonical, DOMAIN, schema_org(),
       asset("/assets/css/fonts.css"), asset("/assets/css/style.css"),
       header(active), body, footer(), asset("/assets/js/main.js"))


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
      <p style="color:var(--band-muted);font-size:14.5px;margin-top:18px">%s</p>
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
  <a class="btn btn-ghost" href="/kontakt/">Kontakty poboček</a>
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

# Katalogy, které e-shop doopravdy má (z horního menu eshop.gcar.cz).
# CHYBI: přímé URL jednotlivých katalogů — zatím vedou na hlavní stranu e-shopu.
KATALOGY = [
    ("Autodíly", "Katalog náhradních dílů na osobní a užitkové vozy.",
     "https://eshop.gcar.cz/cs/katalog/tecdoc/osobni"),
    ("VIN + ACI katalog", "Vyhledání dílu podle VIN kódu vozidla.",
     "https://eshop.gcar.cz/cs/katalog/aci-embedded"),
    ("Uni díly", "Univerzální díly, nářadí a vybavení dílny.",
     "https://eshop.gcar.cz/cs/katalog/univerzalni-dily"),
    ("Vybavení autoservisu", "Samostatný katalog technologií pro autoservisy.",
     "https://narzedzia.moto-profil.pl"),
]


def katalogy_grid():
    return "".join("""
      <a class="katalog" href="%s" target="_blank" rel="noopener">
        <h3>%s</h3>
        <p>%s</p>
      </a>""" % (u, n, p) for n, p, u in KATALOGY)


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
      <h1>Všechno kolem auta na jednom místě</h1>
      <p class="lede"><strong>Prodej náhradních dílů na osobní a dodávkové vozy do 3,5 t, včetně pneumatik, autoskel a autodoplňků.</strong> K tomu autoservis s pneuservisem a montáže LPG. Díly dovážíme a distribuujeme, servisům a obchodům je rozvážíme vlastními vozy.</p>

      <form class="finder" id="hledani" data-base="__SEARCH__" role="search">
        <input name="q" type="search" placeholder="Hledat díl, značku nebo katalogové číslo" aria-label="Hledat v e-shopu" required>
        <button type="submit">Hledat</button>
      </form>
      <noscript><p class="finder-note"><a href="__ESHOP__">Přejít do e-shopu a hledat tam</a></p></noscript>
      <p class="finder-note">Hledat můžete podle kódu, textu i vozidla — e-shop má i VIN katalog. Nevíte si rady? <a href="tel:__TEL__">Zavolejte na __TELF__</a>.</p>
      <p class="hero-cta">
        <a class="btn btn-line btn-video" href="#video" id="hero-video">
          <span class="ikona-prehrat" aria-hidden="true"></span>Jak k nám trefíte
        </a>
        <a class="btn btn-ghost" href="/o-nas/">Více o nás</a>
      </p>
    </div>

    <div class="branches" id="pobocky">__BRANCHES__
      <div class="hours"><b>Po–Pá 8:00–17:00</b> · So 9:00–10:00 · Neděle a svátky zavřeno</div>
    </div>
  </div>
</div>

<section class="pillars">
  <div class="wrap">
    <div class="pillar-grid">
      <a class="pillar" href="/sortiment/">
        <b>01</b>
        <h2>Autodíly</h2>
        <p>Náhradní díly na osobní a užitkové vozy i na moto, pneumatiky, oleje, chemie, nářadí a vybavení servisů. Objednáte do 16:45, druhý den to máte u sebe.</p>
        <span class="go">Sortiment a e-shop</span>
      </a>
      <a class="pillar" href="https://www.autoserviskromeriz.cz" target="_blank" rel="noopener">
        <b>02</b>
        <h2>Autoservis</h2>
        <p>Oleje, brzdy, převodovky, pneumatiky a 3D geometrie, klimatizace, karosářské a elektrikářské práce. Ceník máme zveřejněný.</p>
        <span class="go">Co v servisu uděláme</span>
      </a>
      <a class="pillar" href="https://www.lpg-kromeriz.cz" target="_blank" rel="noopener">
        <b>03</b>
        <h2>LPG</h2>
        <p>Montáže a přestavby na plynový pohon, pravidelné revize, servis a diagnostika, výměny nádrží.</p>
        <span class="go">Přestavba na plyn</span>
      </a>
    </div>
  </div>
</section>

__VIDEO__

<div class="strip">
  <div class="wrap">
    <div class="stat"><b>Objednávka do 16:45</b><span>druhý den máte zboží k dispozici</span></div>
    <div class="stat"><b>2 pobočky</b><span>Kroměříž a Staré Město</span></div>
    <div class="stat"><b>TecDoc</b><span>díl dohledáte podle vozu, VIN i katalogového čísla</span></div>
    <div class="stat"><b>Od roku 1997</b><span>GCAR services, s.r.o.</span></div>
  </div>
</div>

<section class="about" id="o-nas">
  <div class="wrap">
    <div><h2>Kdo jsme</h2></div>
    <div>
      <p>Firma dováží a distribuuje náhradní díly na osobní a užitkové vozy světových značek. Zajišťujeme rozvoz servisům a obchodům. Široký sortiment náhradních dílů od světových výrobců nás řadí k největším prodejcům v regionu. Jsme obchodním partnerem jedné z největších firem na evropském trhu.</p>
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
        __IKONA_nahradni-dily__<h3>Náhradní díly</h3>
        <p>Originální i aftermarketové díly na osobní a užitkové vozy.</p>
      </a>
      <a class="cat" href="/sortiment/pneumatiky/">
        __IKONA_pneumatiky__<h3>Pneumatiky</h3>
      </a>
      <a class="cat" href="/sortiment/vybaveni-servisu/">
        __IKONA_vybaveni-servisu__<h3>Vybavení servisů</h3>
      </a>
      <a class="cat" href="/sortiment/chemie/">
        __IKONA_chemie__<h3>Chemie a oleje</h3>
      </a>
      <a class="cat" href="/sortiment/ochranne-prostredky/">
        __IKONA_ochranne-prostredky__<h3>Ochranné prostředky</h3>
      </a>
    </div>
  </div>
</section>

__ROZVOZ__

<section id="katalogy" class="on-paper">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <h2>Katalogy v e-shopu</h2>
        <p class="lede">Ceny, skladová dostupnost i fotky jsou vždy v e-shopu — tam se to aktualizuje průběžně.</p>
      </div>
      <a class="more" href="__ESHOP__">Do e-shopu</a>
    </div>
    <div class="katalogy">__KATALOGY__</div>
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
    <p class="brands-note">A řada dalších. Kompletní nabídku najdete v e-shopu.</p>
  </div>
</section>

<section id="sluzby">
  <div class="wrap">
    <div class="sec-head"><div><h2>A ještě</h2></div></div>
    <div class="svc">
      <a href="/pujcovna/"><h3>Půjčovna</h3><p>Střešní autoboxy od 80 Kč za den.</p></a>
      <a href="/akce/"><h3>Akce</h3><p>Aktuální akční nabídky v e-shopu.</p></a>
      <a href="/o-nas/"><h3>O nás</h3><p>Kdo jsme a kde nás najdete.</p></a>
    </div>
  </div>
</section>

__KONTAKT__
"""

# --------------------------------------------------------------------------
O_NAS = """<div class="split">
  <div class="prose">
    <p>Firma dováží a distribuuje náhradní díly na osobní a užitkové vozy světových značek. Zajišťujeme rozvoz servisům a obchodům. Široký sortiment náhradních dílů od světových výrobců nás řadí k největším prodejcům v regionu a jsme obchodním partnerem jedné z největších firem na evropském trhu.</p>

    <h2>Všechno kolem auta pod jednou firmou</h2>
    <p>GCAR není jen prodejna dílů. Pod stejnou firmou běží i <a href="https://www.autoserviskromeriz.cz" target="_blank" rel="noopener">autoservis s pneuservisem</a> a <a href="https://www.lpg-kromeriz.cz" target="_blank" rel="noopener">montáže plynových pohonů</a>. Pro zákazníka to znamená, že díl, opravu i přestavbu na LPG vyřídí na jednom místě a s jedním telefonním číslem.</p>
    <p>Pro servis to znamená ještě něco navíc: nářadí, chemii a vybavení, které prodáváme, denně používáme ve vlastní dílně.</p>

    <h2>Jak to u nás vypadá</h2>
  </div>
  <div></div>
</div>

__FOTKY__

<div class="split">
  <div class="prose">
    <h2>Kde nás najdete</h2>
    <p>
      <strong>Kroměříž</strong> — Hulínská 2351/28E, 767 01 Kroměříž, areál bývalé masny<br>
      <strong>Staré Město</strong> — Brněnská 1395, 686 03 Staré Město
    </p>
    <p>Otevřeno máme v pracovní dny 8:00–17:00 a v sobotu 9:00–10:00. Podrobné kontakty na obě pobočky jsou na <a href="/kontakt/">stránce Kontakt</a>.</p>

    <h2>Fakturační údaje</h2>
    <p>
      GCAR services, s.r.o.<br>
      IČO 26946840<br>
      DIČ CZ26946840<br>
      Bankovní účet: 35-4227050297/0100 (KB Kroměříž)<br>
      Datová schránka: qfkpmws
    </p>
  </div>
  __ASIDE__
</div>

<div class="historie">
  <h2>Historie naší firmy</h2>
  <ol>
    <li><span class="rok">1997</span><div><h3>Založení</h3><p>Firma byla založena roku 1997. Začínalo se v garáži v centru historické Kroměříže.</p></div></li>
    <li><span class="rok">2000</span><div><h3>První stěhování</h3><p>V roce 2000 se firma přestěhovala do větších prostor v témže domě.</p></div></li>
    <li><span class="rok">2001</span><div><h3>Otevření servisu</h3><p>V roce 2001 byl otevřen servis v pronajatých prostorách na Hulínské ulici v Kroměříži.</p></div></li>
    <li><span class="rok">2003</span><div><h3>Nová pobočka</h3><p>V roce 2003 jsme otevřeli pobočku v Uherském Hradišti, na Moravním nábřeží.</p></div></li>
    <li><span class="rok">2004</span><div><h3>Stěhování prodejny</h3><p>V roce 2004 se do budovy servisu v Kroměříži přestěhoval i obchod, kterému byly prostory v centru Kroměříže znovu malé. Bylo jasné, že toto stěhování nebylo poslední, neboť firma rychle expandovala a rozvíjela se.</p></div></li>
    <li><span class="rok">2004</span><div><h3>Stěhování do vlastního</h3><p>Na podzim roku 2004 se firmě nabídla neopakovatelná příležitost: koupě bývalé výrobní haly v areálu Masny Kroměříž o rozloze 530 m². V srpnu roku 2005, po náročné rekonstrukci, se celá firma, včetně servisu, přestěhovala do vlastních prostor.</p></div></li>
    <li><span class="rok">2007</span><div><h3>Stěhování do Starého Města</h3><p>V roce 2007 se přestěhovala pobočka Uherské Hradiště do větších prostor ve Starém Městě.</p></div></li>
    <li><span class="rok">2011</span><div><h3>E-shop</h3><p>V květnu 2011 jsme rozjeli vlastní e-shop na bázi celoevropského TecDocu.</p></div></li>
    <li><span class="rok">2013</span><div><h3>Nová identita</h3><p>V lednu 2013 představila společnost GCAR services, s.r.o. nové logo společnosti.</p></div></li>
    <li><span class="rok">2016</span><div><h3>Stěhování prodejny ve Starém Městě</h3><p>Dne 28. listopadu 2016 se pobočka ve Starém Městě přestěhovala do vlastního objektu na rušném průtahu Starým Městem, na ulici Brněnská. Moderní stavba s vlastním parkováním ve dvoře z ulice U Školky zajišťuje pohodlí pro naše klienty.</p></div></li>
  </ol>
</div>
"""

# --------------------------------------------------------------------------
SORTIMENT = """<div class="prose" style="margin-bottom:36px">
  <p>Kompletní sortiment náhradních dílů na osobní vozy.</p>
</div>

<div class="chips" style="margin-bottom:40px">__CHIPS__</div>

<div class="cats" style="margin-bottom:40px">
  <a class="cat is-wide" href="/sortiment/nahradni-dily/">
    __IKONA_nahradni-dily__<h3>Náhradní díly</h3>
    <p>Originální i aftermarketové díly na osobní a užitkové vozy.</p>
  </a>
  <a class="cat" href="/sortiment/pneumatiky/">__IKONA_pneumatiky__<h3>Pneumatiky</h3></a>
  <a class="cat" href="/sortiment/vybaveni-servisu/">__IKONA_vybaveni-servisu__<h3>Vybavení servisů</h3></a>
  <a class="cat" href="/sortiment/chemie/">__IKONA_chemie__<h3>Chemie a oleje</h3></a>
  <a class="cat" href="/sortiment/ochranne-prostredky/">__IKONA_ochranne-prostredky__<h3>Ochranné prostředky</h3></a>
</div>

__ROZVOZ_INLINE__
"""

# --------------------------------------------------------------------------
# Podstránky sortimentu.
# CHYBI: skutečné texty z gcar.cz/sortiment/*. Zatím jen to, co se dá
# doložit z homepage a z e-shopu.
# --------------------------------------------------------------------------
KAT_DILY = """<div class="split">
  <div class="prose">
    <p>Dodáváme jen to nejlepší, co na trhu existuje. Sortiment originálních náhradních dílů se samozřejmě dostává i na pulty aftermarketu — jen v jiné krabičce, než ji znáte ze značkového servisu.</p>
    <h2>Co vedeme</h2>
    <div class="chips">__CHIPS__</div>
  </div>
  __ASIDE__
</div>

<details class="dily-seznam">
  <summary>Kompletní přehled dílů, které prodáváme</summary>
  <ul>
    <li><strong>Brzdy</strong> — brzdové kotouče, brzdové destičky, třmeny, brzdové hadice a válečky</li>
    <li><strong>Filtry</strong> — olejové, vzduchové, palivové a kabinové filtry</li>
    <li><strong>Zapalování a žhavení</strong> — zapalovací svíčky, žhavicí svíčky, zapalovací cívky</li>
    <li><strong>Podvozek</strong> — tlumiče, pružiny, silentbloky, ramena, kulové čepy, tyčky stabilizátoru, ložiska kol</li>
    <li><strong>Řízení</strong> — spojovací tyče, hlavice řízení, řídicí převody</li>
    <li><strong>Spojka a převodovka</strong> — spojkové sady, dvouhmotové setrvačníky, ložiska, poloosy, homokinetické klouby a manžety</li>
    <li><strong>Rozvody a pohon</strong> — rozvodové sady, rozvodové řemeny, drážkové řemeny, napínáky, vodní čerpadla</li>
    <li><strong>Motor</strong> — těsnění, pístní kroužky, ventily, olejová čerpadla, hydraulická zdvihátka, turbodmychadla</li>
    <li><strong>Palivová soustava</strong> — palivová čerpadla, vstřikovače, palivové filtry</li>
    <li><strong>Chlazení, topení a klimatizace</strong> — chladiče, termostaty, ventilátory, kompresory klimatizace, kondenzátory, sušiče</li>
    <li><strong>Výfuk a emise</strong> — tlumiče výfuku, katalyzátory, filtry pevných částic, lambda sondy</li>
    <li><strong>Elektrika</strong> — alternátory, startéry, autobaterie, žárovky, senzory a čidla</li>
    <li><strong>Karoserie a osvětlení</strong> — světlomety, zpětná zrcátka, stěrače, nárazníky, autoskla</li>
    <li><strong>Pneumatiky a kola</strong> — letní, zimní a celoroční pneumatiky osobní a dodávkové</li>
    <li><strong>Oleje a chemie</strong> — motorové a převodové oleje, chladicí a brzdové kapaliny, autochemie</li>
    <li><strong>Autodoplňky</strong> — střešní nosiče a boxy, koberce, potahy, doplňky do vozu</li>
    <li><strong>Díly na moto</strong> — náhradní díly pro motocykly a skútry</li>
  </ul>
  <p>Hledáte něco, co tu není? Zavolejte nebo napište, díl vám obstaráme.</p>
</details>

__KATALOGY_VYROBCU__

__ESHOPBOX__
"""

KAT_PNEU = """<div class="split">
  <div class="prose">
    <p>Pneumatiky na osobní a užitkové vozy i na motocykly — letní, zimní i celoroční.</p>

    <h2>Jaký rozměr potřebujete</h2>
    <p>Rozměr je vypsaný na boku stávající pneumatiky, například <span style="font-family:var(--mono);white-space:nowrap">205/55 R16 91V</span>. Čte se takto:</p>
    <ul>
      <li><strong>205</strong> — šířka v milimetrech</li>
      <li><strong>55</strong> — výška boční stěny v procentech šířky</li>
      <li><strong>R16</strong> — průměr ráfku v palcích</li>
      <li><strong>91</strong> — index nosnosti (kolik kilogramů pneumatika unese)</li>
      <li><strong>V</strong> — rychlostní index (do jaké rychlosti je určená)</li>
    </ul>
    <p>Index nosnosti ani rychlosti nesmí být nižší, než uvádí technický průkaz vozu. Vyšší být může.</p>

    <h2>Zimní, letní, nebo celoroční</h2>
    <p>V Česku jsou <strong>zimní pneumatiky povinné od 1. listopadu do 31. března</strong>, pokud je na silnici souvislá vrstva sněhu, led nebo námraza — anebo se to dá vzhledem k počasí předpokládat. Zákon zároveň vyžaduje u zimních pneumatik <strong>minimální hloubku dezénu 4 mm</strong>, u letních 1,6 mm.</p>
    <p>Celoroční pneumatika je kompromis. Dává smysl při malém nájezdu a jízdě hlavně po městě. Kdo jezdí hodně po dálnici nebo pravidelně do kopců v zimě, vyjde líp se dvěma sadami.</p>

    <h2>Když si nejste jistí</h2>
    <p>Zavolejte a řekněte nám rozměr z boku pneumatiky, značku a model vozu a jak s autem jezdíte — město, dálnice, tahání přívěsu. Doporučíme konkrétní modely v několika cenových hladinách a vysvětlíme, v čem se liší.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

KAT_VYBAVENI = """<div class="split">
  <div class="prose">
    <p>Prakticky vše, co servis potřebuje. Od klíčů, přípravků, stahováků, dílenského nábytku po hevery! Vše najdete v našem e-shopu v záložce UNI DÍLY A DÍLNA a ještě víc v KATALOG VYBAVENÍ SERVISU.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

KAT_CHEMIE = """<div class="split">
  <div class="prose">
    <p>Motorové a převodové oleje, maziva, provozní kapaliny a autochemie.</p>

    <h2>U oleje nerozhoduje jen viskozita</h2>
    <p>Označení jako <span style="font-family:var(--mono)">5W-30</span> říká, jak olej teče za studena a za provozní teploty. Samo o sobě ale nestačí. Důležitější je <strong>schválení výrobce vozu</strong> — například VW 504.00/507.00, MB 229.51, BMW Longlife-04 nebo PSA B71 2290.</p>
    <p>Rozdíl není kosmetický. Olej bez správného schválení může u motoru s filtrem pevných částic filtr postupně zanést popelem, i když viskozita sedí. Oprava pak stojí násobně víc než ta správná nádoba oleje.</p>

    <h2>Co se mění a jak často</h2>
    <ul>
      <li><strong>Motorový olej</strong> — podle servisního intervalu vozu, u krátkých jízd po městě raději dřív.</li>
      <li><strong>Brzdová kapalina</strong> — obvykle po dvou letech. Postupně na sebe váže vlhkost, tím klesá bod varu a při prudkém brzdění může brzda „změknout".</li>
      <li><strong>Chladicí kapalina</strong> — řídí se typem (G11, G12, G12+, G13). Míchat je dohromady se nemá, u některých kombinací se sráží.</li>
      <li><strong>Převodový olej</strong> — u manuálních převodovek podle nájezdu, u automatů podle předpisu výrobce.</li>
    </ul>

    __FOTKA_OLEJE__

    <h2>Poradíme se specifikací</h2>
    <p>Řekněte nám značku, model, rok výroby a motorizaci — nebo rovnou VIN — a vybereme olej, který do vozu patří. Vedeme i aditiva, maziva, montážní spreje a autokosmetiku.</p>
  </div>
  __ASIDE__
</div>

__KATALOGY_VYROBCU__

__ESHOPBOX__
"""

KAT_OOPP = """<div class="split">
  <div class="prose">
    <p>Ochranné pracovní prostředky — oděvy, obuv, rukavice, masky a respirátory. Pro autoservisy i pro provozy mimo automobilový obor.</p>

    <h2>Podle čeho vybírat</h2>
    <p>U ochranných pomůcek nejde o značku, ale o normu. Ta je vyražená přímo na výrobku a říká, co pomůcka skutečně vydrží.</p>
    <ul>
      <li><strong>Obuv — EN ISO 20345.</strong> Třída <span style="font-family:var(--mono)">S1</span> má ochrannou špici a antistatickou podešev, <span style="font-family:var(--mono)">S2</span> navíc odolává vodě, <span style="font-family:var(--mono)">S3</span> má ještě podešev odolnou proti propíchnutí. Do dílny obvykle stačí S1P nebo S3.</li>
      <li><strong>Rukavice — EN 388.</strong> Čtyři až pět znaků za piktogramem udává odolnost proti oděru, proříznutí, roztržení a propíchnutí. Čím vyšší číslo, tím lepší. Na manipulaci s plechem se hodí vyšší odolnost proti proříznutí.</li>
      <li><strong>Ochrana zraku — EN 166.</strong> Brýle a štíty. Při broušení je potřeba odolnost proti nárazu, při práci s chemií těsnicí brýle.</li>
      <li><strong>Ochrana dýchání.</strong> <span style="font-family:var(--mono)">FFP2</span> a <span style="font-family:var(--mono)">FFP3</span> na prach a částice, masky s výměnnými filtry na výpary a rozpouštědla — typ filtru se volí podle látky.</li>
    </ul>

    <h2>Pro firmy</h2>
    <p>Potřebujete vystrojit celou dílnu nebo pravidelně doplňovat spotřební pomůcky — rukavice, respirátory, čisticí pasty? Ozvěte se a domluvíme se na pravidelném odběru.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

# --------------------------------------------------------------------------
# CHYBI: potvrzení od majitele. Rozsah služeb je poskládaný z veřejných
# katalogů (firmy.cz, ekatalog.cz) pod IČO 26946840, ne z gcar.cz.
# Služby převzaté z autoserviskromeriz.cz (vlastní web servisu, stejná firma).
AUTOSERVIS = """<div class="split">
  <div class="prose">
    <p>Nabízíme kompletní služby autoservisu, abyste se na cestách cítili bezpečněji. Servis provozujeme v Kroměříži pod stejnou firmou jako prodejnu dílů — díly, které do vozu montujeme, máme na vlastním skladě a nečeká se na dodavatele.</p>
  </div>
  <div></div>
</div>

<div class="list-grid">
  <div><h4>Výměna oleje</h4><p>Častější výměna oleje prodlužuje životnost motoru.</p></div>
  <div><h4>Brzdy</h4><p>Destičky, kotouče, kapaliny — brzdy řešíme celé, ne jen to, co je vidět.</p></div>
  <div><h4>Opravy převodovek</h4><p>Manuální i automatické, včetně výměny olejů.</p></div>
  <div><h4>Pneumatiky a 3D geometrie</h4><p>Správný vzorek a geometrie zlepšují jízdní vlastnosti.</p></div>
  <div><h4>Klimatizace a dezinfekce</h4><p>Udržujte klimatizaci čistou. Čistý vzduch bez bakterií.</p></div>
  <div><h4>Sezónní prohlídky</h4><p>Udržujte auto v kondici pravidelnými letními a zimními kontrolami.</p></div>
  <div><h4>Diagnostika a zjištění závady</h4><p>Než něco vyměníme, zjistíme, co je opravdu špatně.</p></div>
  <div><h4>Karosářské a elektrikářské práce</h4><p>Od plechu po kabeláž.</p></div>
  <div><h4>Montáž tažného zařízení</h4><p>Klasická elektroinstalace i check control.</p></div>
</div>

<div class="split">
  <div class="prose">
    __FOTKA_DILNA__

    <h2>Ceník máme zveřejněný</h2>
    <p>Nemusíte volat, abyste se dozvěděli, kolik co stojí. Kompletní ceník servisních prací — mechanika, pneuservis, klimatizace, provozní kapaliny i tažná zařízení — je na webu servisu. Ceny jsou uvedené s DPH.</p>
    <p>Na provedené práce platí zákonná záruka 6 měsíců.</p>
    <p><a class="btn btn-red" href="__SERVIS__">Zobrazit ceník servisních prací</a></p>

    <h2>Objednání</h2>
    <p>Termín si domluvte telefonicky. Řekněte nám značku, model a rok výroby vozu a o co jde — poradíme, co bude potřeba.</p>
  </div>
  __ASIDE__
</div>
"""

LPG_STRANKA = """<div class="split">
  <div class="prose">
    <p>Montáže a přestavby vozů na LPG děláme v Kroměříži. Používáme systémy od světových výrobců a staráme se i o následný servis a povinné revize.</p>

    <h2>Co zajišťujeme</h2>
    <ul>
      <li>Montáže a přestavby na LPG</li>
      <li>Pravidelné roční revize</li>
      <li>Servis a diagnostika plynových systémů</li>
      <li>Výměny tlakových nádrží</li>
      <li>Seřízení vozů na plyn</li>
    </ul>

    <h2>Máte zájem o přestavbu?</h2>
    <p>Zavolejte a řekněte nám značku, model a rok výroby vozu. Řekneme vám, jestli je přestavba možná, co obnáší a kolik bude stát.</p>
    <p><a class="btn btn-line" href="__LPG__">Přejít na lpg-kromeriz.cz</a></p>
  </div>
  __ASIDE__
</div>
"""

# --------------------------------------------------------------------------
AKCE = """<div class="split">
  <div class="prose">
    <p>Akční nabídky a sezónní ceny vedeme v e-shopu. Má to důvod: ceny i skladová dostupnost se mění průběžně a na jednom místě jsou vždy platné. Kdybychom je přepisovali i sem, dřív nebo později by se jedno z těch dvou míst rozešlo s realitou.</p>

    <h2>Kdy se vyplatí sledovat</h2>
    <ul>
      <li><strong>Před sezónou.</strong> Zimní i letní pneumatiky bývají nejvýhodnější dřív, než po nich sáhnou všichni ostatní.</li>
      <li><strong>Při akcích dodavatelů.</strong> Výrobci olejů, chemie a nářadí vypisují akce v vlnách — když zrovna běží, promítá se to do ceny.</li>
      <li><strong>Když se uvolní skladové zásoby.</strong> To už ale patří spíš do <a href="/vyprodej/">výprodeje</a>.</li>
    </ul>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

VYPRODEJ = """<div class="split">
  <div class="prose">
    <p>Zboží za snížené ceny. Nejde o vadné ani použité kusy — jsou to skladové zbytky, doběhové položky a zboží z ukončených řad.</p>

    <h2>Proč bývá zlevněné</h2>
    <ul>
      <li><strong>Doběh řady.</strong> Výrobce model nahradil novým, i když ten starý funguje stejně dobře.</li>
      <li><strong>Zbytek ze skladu.</strong> Zůstal poslední kus nebo dva a už se nebude doobjednávat.</li>
      <li><strong>Změna obalu nebo značení.</strong> Obsah zůstává stejný.</li>
    </ul>

    <h2>Co z toho plyne</h2>
    <p>Množství je omezené tím, co zbylo — co se prodá, už nedoplníme. Vyplatí se proto koukat pravidelně, nabídka se mění podle toho, co se zrovna uvolní.</p>
    <p>Část výprodejového zboží, zvlášť jednotlivé kusy nářadí a vybavení dílny, leží na pobočce a nemusí být v e-shopu vidět. Když hledáte něco konkrétního, zavolejte.</p>
  </div>
  __ASIDE__
</div>

__ESHOPBOX__
"""

PUJCOVNA = """<div class="split">
  <div class="prose">
    <p>Nejlevnější a nejlepší autobox je ten, který si vůbec nekoupíte. Půjčujeme střešní autoboxy, střešní nosiče a nosič na kola na tažné zařízení.</p>

    <h2>Nabízíme</h2>
    <ul>
      <li><strong>Střešní autoboxy</strong> — čtyři kusy, dva úzké a dva široké, všechny kolem 230 cm dlouhé. Úzký nechá na střeše víc místa vedle sebe, široký pobere víc nákladu.</li>
      <li><strong>Střešní nosiče</strong> — některé typy, na které se boxy upevňují.</li>
      <li><strong>Nosič na kola</strong> — na tažné zařízení.</li>
    </ul>

    <h2>Za kolik</h2>
    <table class="ceny">
      <thead><tr><th></th><th>Za týden</th><th>Za den</th></tr></thead>
      <tbody>
        <tr><th scope="row">Střešní autobox</th><td>400 Kč</td><td>80 Kč</td></tr>
        <tr><th scope="row">Střešní nosič</th><td>200 Kč</td><td>30 Kč</td></tr>
        <tr><th scope="row">Nosič na kola na tažné zařízení</th><td>750 Kč</td><td>150 Kč</td></tr>
      </tbody>
    </table>
    <p class="ceny-pozn">Cena za den platí při kratším zapůjčení.</p>

    <h2>Jak si půjčit</h2>
    <ul>
      <li><strong>Zavolejte a domluvte si termín.</strong> Půjčování probíhá na základě telefonické dohody. V létě a o prázdninách bývají boxy zamluvené dopředu.</li>
      <li><strong>Řekněte nám značku a model vozu.</strong> Podle typu střechy a nosiče poradíme, co na něj sedne.</li>
      <li><strong>Při vyzvednutí se podepisuje zápůjční smlouva.</strong></li>
    </ul>
  </div>
  __ASIDE__
</div>
"""


# --------------------------------------------------------------------------
VIDEO_MINI = """
      <figure class="prehravac is-mini" id="prehravac">
        <video id="video-gcar" poster="/assets/video/poster.jpg" preload="none"
               muted playsinline data-src="/assets/video/video-gcar.mp4"
               aria-label="Video: cesta k pobočce GCAR v Kroměříži a prohlídka provozu">
          <source data-src="/assets/video/video-gcar.mp4" type="video/mp4">
        </video>
        <button class="prehrat" id="prehrat" type="button" aria-controls="video-gcar">
          <span class="sipka" aria-hidden="true"></span>
          <span class="popis">Přehrát video<small>50 s · cesta k nám</small></span>
        </button>
      </figure>"""


def kontakt_body():
    cards = ""
    for p in POBOCKY:
        pozn = "<br>" + p["poznamka"] if p["poznamka"] else ""
        info = """
      <div class="cinfo">
        <h3>%s</h3>
        <address>%s, %s%s</address>
        <div class="tels">%s</div>
        <a class="mail" href="mailto:%s">%s</a>
      </div>""" % (p["nazev"], p["ulice"], p["psc"], pozn,
                   "".join(tel_link(t) for t in p["tel"]), p["mail"], p["mail"])
        if "Kroměříž" in p["nazev"]:
            # video k pobočce v Kroměříži — stejné ID jako na homepage, obslouží ho main.js
            info += VIDEO_MINI
            cards += '\n    <div class="ccard is-light has-video">%s\n    </div>' % info
        else:
            cards += '\n    <div class="ccard is-light">%s\n    </div>' % info

    # CHYBI: odkazy na mapy. Až budou, vloží se sem iframe (styl .maps je hotový).
    return """<div class="kontakt-sloupec">
  <div>
    %s
    <div style="background:var(--zinc-light);border-radius:4px;padding:18px 22px">
      <strong style="font-size:15px">Otevírací doba</strong>
      <p style="margin:6px 0 0;font-size:15px;color:var(--ink-soft)">%s</p>
    </div>

    <div style="margin-top:28px">%s</div>

    <div class="prose" style="margin-top:28px">
      <h2>Fakturační údaje</h2>
      <p>GCAR services, s.r.o.<br>IČO 26946840<br>DIČ CZ26946840<br>Bankovní účet: 35-4227050297/0100 (KB Kroměříž)<br>Datová schránka: qfkpmws</p>
    </div>
  </div>

</div>
""" % (cards, OTEVIRACI_DOBA,
       fotka("prijezd", "Příjezd k pobočce v Kroměříži"),
       )


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
# Na webu jsou jen značky, které pozná i laik — pruh s deseti jmény,
# z nichž půlku nikdo nezná, nedělá dojem, spíš zmatek. Ostatní
# (BOLL, AMTRA, ATAS, Energy, ATH Heinl) zůstávají v e-shopu.
# Druhá položka je název souboru s logem ve složce /assets/img/znacky/.
# Dokud soubor neexistuje, vypíše se místo loga název — web se nerozbije.
# Nejlepší je SVG, jinak PNG s průhledným pozadím, výška aspoň 120 px.
ZNACKY = [
    ("Castrol", "castrol"),
    ("Total", "total"),
    ("Elf", "elf"),
    ("KS Tools", "ks-tools"),
    ("Thule", "thule"),
]


def znacky_row():
    """Pruh značek.

    Když soubor existuje při sestavení, odkáže se rovnou na něj.
    Když ne, prohlížeč zkusí .svg, pak .png a nakonec nechá název —
    takže stačí logo nahrát do /assets/img/znacky/ a objeví se samo.
    """
    zaloha = ("var p=this.parentNode;"
              "if(this.src.indexOf('.svg')>-1){"
              "this.src=this.src.replace('.svg','.png');}"
              "else{p.className='znacka is-text';p.textContent=this.alt;}")
    out = ""
    for nazev, slug in ZNACKY:
        cesta = None
        for pripona in (".svg", ".png"):
            kandidat = "/assets/img/znacky/" + slug + pripona
            if os.path.exists(os.path.join(ROOT, kandidat.lstrip("/"))):
                cesta = asset(kandidat)
                break
        if cesta:
            out += ('<span class="znacka"><img src="%s" alt="%s" '
                    'loading="lazy"></span>') % (cesta, nazev)
        else:
            out += ('<span class="znacka">'
                    '<img src="/assets/img/znacky/%s.svg" alt="%s" loading="lazy" '
                    'onerror="%s"></span>') % (slug, nazev, zaloha)
    return out

def fotka(soubor, popisek):
    """Jedna fotka z provozu. Rozměry v HTML, aby stránka při načítání neposkakovala."""
    return ('<figure class="fotka fotka-sama">'
            '<img src="/assets/img/foto/%s.jpg" alt="%s" width="1400" height="788" loading="lazy">'
            '<figcaption>%s</figcaption></figure>') % (soubor, popisek, popisek)


def fotky_provoz():
    """Trojice fotek z pobočky v Kroměříži (snímky z videa)."""
    polozky = [
        ("prodejna-zvenku", "Areál pobočky v Kroměříži"),
        ("prodejna", "Prodejna náhradních dílů"),
        ("dilna", "Autoservis s vlastní dílnou"),
    ]
    return '<div class="fotky">%s</div>' % "".join(
        '<figure class="fotka">'
        '<img src="/assets/img/foto/%s.jpg" alt="%s" width="1400" height="788" loading="lazy">'
        '<figcaption>%s</figcaption></figure>' % (s, p, p) for s, p in polozky)

def video_sekce():
    """Video prohlídka pobočky.

    Soubor se nestahuje při načtení stránky — do <video> se dosadí až
    po kliknutí. Do té doby je vidět jen plakát, tedy jeden obrázek.
    Bez toho by si každý návštěvník stáhl 7,8 MB, i kdyby video nespustil.
    """
    return """<section class="video-sekce" id="video">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <h2>Podívejte se k nám</h2>
        <p class="lede">Necelá minuta o tom, jak k nám do Kroměříže trefíte a co u nás najdete — prodejnu, sklad i dílnu.</p>
      </div>
      <a class="more" href="/kontakt/">Adresa a otevírací doba</a>
    </div>

    <figure class="prehravac" id="prehravac">
      <video id="video-gcar" poster="/assets/video/poster.jpg" preload="none"
             muted playsinline data-src="/assets/video/video-gcar.mp4"
             aria-label="Video: cesta k pobočce GCAR v Kroměříži a prohlídka provozu">
        <source data-src="/assets/video/video-gcar.mp4" type="video/mp4">
      </video>
      <button class="prehrat" id="prehrat" type="button" aria-controls="video-gcar">
        <span class="sipka" aria-hidden="true"></span>
        <span class="popis">Přehrát video<small>50 sekund · bez komentáře</small></span>
      </button>
    </figure>
  </div>
</section>"""

def rozvoz_sekce(uvnitr_sekce=False):
    """Údaje o rozvozu. Používá se na homepage i na stránce Autodíly,
    proto je to jedno místo — změna ceny nebo času se promítne na obou."""
    telo = """    <div class="sec-head">
      <div>
        <h2>Rozvoz do servisů a obchodů</h2>
        <p class="lede">Nemusíte pro díl jezdit ani čekat na přepravní službu. Objednejte do 16:45 a druhý den máte zboží připravené. Můžete si ho vyzvednout, nebo vám ho dovezeme.</p>
      </div>
    </div>

    <div class="rozvoz-grid is-2">
      <div class="rozvoz-card">
        <b>Do 16:45</b>
        <p>Poslední objednávka je do 16:45, zboží je druhý den připravené.</p>
      </div>
      <div class="rozvoz-card">
        <b>Kroměříž – Staré Město a okolí do 30 km</b>
        <p>Díly rozvážíme vlastními vozy servisům a obchodům.</p>
      </div>
    </div>

    <p class="rozvoz-note">Trasy se řídí tím, kde máme zákazníky. Pokud sídlíte kousek za uvedeným okruhem, zavolejte — často se to dá domluvit.</p>"""

    if uvnitr_sekce:
        # na podstránce už jsme uvnitř <section><div class="wrap">
        return '<div class="rozvoz is-inline">\n%s\n</div>' % telo
    return '<section class="rozvoz">\n  <div class="wrap">\n%s\n  </div>\n</section>' % telo


def katalogy_vyrobcu(klic):
    """Odkazy na katalogy výrobců u příslušné kategorie sortimentu."""
    polozky = KATALOGY_VYROBCU.get(klic)
    if not polozky:
        return ""
    sablona = ('\n    <a class="vyrobce" href="%s" rel="noopener">'
                '\n      <b>%s</b>'
                '\n      <span>%s</span>'
                '\n    </a>')
    radky = "".join(sablona % (url, nazev, popis)
                    for nazev, url, popis in polozky)
    return ('<div class="vyrobci">'
            '\n  <h2>Kde si díl dohledat</h2>'
            '\n  <p class="vyrobci-lede">Katalogy výrobců, ve kterých najdete přesné '
            'označení dílu. Objednat ho pak můžete u nás.</p>'
            '\n  <div class="vyrobci-grid">%s\n  </div>'
            '\n</div>') % radky


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

add("autoservis/index.html", "Autoservis a pneuservis Kroměříž | GCAR",
    "Autoservis v Kroměříži — výměny oleje, brzdy, opravy převodovek, pneumatiky a 3D geometrie, servis klimatizací a sezónní prohlídky.",
    AUTOSERVIS, "autoservis",
    page_head("Autoservis", "Kompletní služby autoservisu, abyste se na cestách cítili bezpečněji.",
              [(None, "Autoservis")]))

add("lpg/index.html", "Montáže LPG Kroměříž | GCAR",
    "Montáže a přestavby vozů na LPG v Kroměříži, pravidelné revize, servis plynových systémů a výměny nádrží.",
    LPG_STRANKA, "lpg",
    page_head("LPG", "Montáže a přestavby na plynový pohon, revize a servis.",
              [(None, "LPG")]))

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
    kat_klic = page["path"].split("/")[1] if page["path"].startswith("sortiment/") else ""
    body = body.replace("__KATALOGY_VYROBCU__", katalogy_vyrobcu(kat_klic))
    body = body.replace("__ESHOPBOX__", eshop_box(
        "Aktuální nabídku, ceny a skladovou dostupnost najdete v našem e-shopu."))
    body = body.replace("__VIDEO__", video_sekce())
    body = body.replace("__FOTKY__", fotky_provoz())
    for _slug, _svg in IKONY.items():
        body = body.replace("__IKONA_%s__" % _slug, _svg)
    body = body.replace("__FOTKA_AREAL__", fotka("prodejna-zvenku", "Areál pobočky v Kroměříži"))
    body = body.replace("__FOTKA_DILNA__", fotka("dilna", "Dílna autoservisu v Kroměříži"))
    body = body.replace("__FOTKA_OLEJE__", fotka("oleje", "Část sortimentu olejů a autochemie na prodejně"))
    body = body.replace("__ROZVOZ_INLINE__", rozvoz_sekce(uvnitr_sekce=True))
    body = body.replace("__ROZVOZ__", rozvoz_sekce())
    body = body.replace("__CHIPS__", chips(DILY_CHIPS))
    body = body.replace("__ZNACKY__", znacky_row())
    body = body.replace("__KATALOGY__", katalogy_grid())
    body = body.replace("__BRANCHES__", branches_panel())
    body = body.replace("__KONTAKT__", kontakt_sekce())
    body = body.replace("__ASIDE__", aside_pomoc())
    body = body.replace("__SEARCH__", ESHOP_SEARCH)
    body = body.replace("__ESHOP__", ESHOP)
    body = body.replace("__SERVIS__", SERVIS)
    body = body.replace("__LPG__", LPG)
    body = body.replace("__TELF__", fmt_tel(POBOCKY[0]["tel"][0]).replace(" ", "&nbsp;"))
    body = body.replace("__TEL__", POBOCKY[0]["tel"][0])

    if page["head"]:
        body = page["head"] + '\n<section>\n  <div class="wrap">\n' + body + "\n  </div>\n</section>\n"

    html = layout(page["title"], page["desc"], body, page["active"],
                  "/" + page["path"].replace("index.html", ""))
    if page["path"] in SKRYTE:
        html = html.replace('<meta name="description"', '<meta name="robots" content="noindex, nofollow">\n<meta name="description"', 1)
    return html


SKRYTE = {"autoservis/index.html", "lpg/index.html"}   # zatím schované: bez odkazů, noindex


def sitemap():
    today = date.today().isoformat()
    urls = "".join(
        "  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n"
        % (DOMAIN + "/" + p["path"].replace("index.html", ""), today)
        for p in PAGES if p["path"] != "404.html" and p["path"] not in SKRYTE)
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
