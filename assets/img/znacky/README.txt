LOGA DODAVATELSKÝCH ZNAČEK
==========================

Sem patří loga výrobců. Nahraj sem soubor se správným názvem a logo se
na webu objeví samo — NENÍ potřeba nic přegenerovávat ani spouštět
build.py. Stačí soubor nahrát na GitHub.

NÁZVY SOUBORŮ
-------------
Musí sedět přesně, jinak se logo nenačte:

    castrol      →  castrol.svg   nebo  castrol.png
    total        →  total.svg     nebo  total.png
    elf          →  elf.svg       nebo  elf.png
    ks-tools     →  ks-tools.svg  nebo  ks-tools.png
    thule        →  thule.svg     nebo  thule.png

STAV: všech pět log je nahraných (castrol.png, total.png, elf.svg,
ks-tools.svg, thule.png). Elf a KS Tools jsou vektorové, zbylé tři
rastrové — při větším zvětšení budou o něco měkčí.

Na webu je zatím jen těchto pět — značky, které pozná i laik. Pruh
s deseti jmény, z nichž půlku nikdo nezná, nedělá dojem, spíš zmatek.
BOLL, AMTRA, ATAS, Energy a ATH Heinl zůstávají v e-shopu. Kdyby se
jejich loga někdy objevila, dopíší se do seznamu ZNACKY v build.py.

Web nejdřív zkusí .svg, pak .png. Když nenajde ani jedno, nechá na tom
místě název značky. Nic se tím nerozbije, takže můžeš doplňovat postupně.

JAKÝ FORMÁT
-----------
Nejlepší je SVG — je ostré v jakékoli velikosti a má pár kilobajtů.
Když SVG nemáš, PNG s PRŮHLEDNÝM pozadím a výškou aspoň 120 px.

Logo na bílém obdélníku nepoužívej — v nočním režimu by z pruhu svítily
bílé cedulky.

KDE LOGA VZÍT
-------------
Od obchodního zástupce dané značky, nebo z oficiálních stránek výrobce
v sekci pro partnery. Bývá pod názvem "Media kit", "Brand assets",
"Press" nebo "Ke stažení".

Nejrychlejší je brandfetch.com — napíšeš doménu značky (castrol.com,
thule.com, ks-tools.com, totalenergies.com, elf.com) a dostaneš oficiální
logo v SVG i PNG s průhledným pozadím.

Dál pak seeklogo.com, brandsoftheworld.com nebo brandeps.com. Bývají tam
i starší verze, tak porovnej s tím, co má výrobce na webu dnes.

Když se nic nenajde, napiš obchodnímu zástupci dané značky. Stačí jedna
věta o tom, že připravujete nový web a chcete uvést jejich sortiment —
často pošlou rovnou celý balíček.

Nestahuj loga z vyhledávače obrázků — bývají tam staré verze, rozmazané
výřezy a loga s vypáleným bílým pozadím.

PRÁVNÍ STRÁNKA
--------------
Majitel použití log schválil (24. 9. 2026). Opora: § 10 zákona
o ochranných známkách, vyčerpání práv u originálního zboží uvedeného
na trh v EU/EHP, stanovisko EUIPO.

Podmínka: logo smí označovat zboží, které se skutečně prodává. Nesmí
sloužit jako dekorace ani naznačovat status "oficiálního prodejce".
Na webu je pruh značek u katalogu zboží, což té podmínce odpovídá.

PŘIDÁNÍ DALŠÍ ZNAČKY
--------------------
Dopiš řádek do seznamu ZNACKY v build.py:

    ("Febi", "febi"),

a nahraj sem febi.svg. Tohle už build.py spustit vyžaduje, protože
se mění seznam, ne jen soubory.


POZNÁMKY K JEDNOTLIVÝM LOGŮM
----------------------------
thule.png   Dodaná verze byla bílá na černém (varianta pro tmavé
            pozadí). Převrácena na standardní černou verzi, jinak by
            na světlé dlaždici zmizela.

total.png   Dodaný soubor měl zapečenou šachovnici z webu, odkud
            pochází — nebyl doopravdy průhledný. Odstraněno.
            Je to STOJATÁ varianta loga (glóbus nad textem), takže
            vedle ležatých log působí menší. Kdyby se našla ležatá
            verze, bude v pruhu sedět líp.
            Pozor i na to, že Total se v roce 2021 přejmenoval na
            TotalEnergies a má nové logo — ověřit, které používat.

castrol.png Průhlednost už měl, stačil ořez. Bílý podklad uvnitř
            tahu je součást loga, ten tam patří.
