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
    boll         →  boll.svg      nebo  boll.png
    amtra        →  amtra.svg     nebo  amtra.png
    atas         →  atas.svg      nebo  atas.png
    energy       →  energy.svg    nebo  energy.png
    ks-tools     →  ks-tools.svg  nebo  ks-tools.png
    ath-heinl    →  ath-heinl.svg nebo  ath-heinl.png
    thule        →  thule.svg     nebo  thule.png

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

U těchto značek to je na:
    castrol.com        → Media / Brand
    boll.pl            → kontakt na obchodního zástupce
    ks-tools.com       → Downloads
    thule.com          → Press room
    as-pl.com          → Downloads

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
