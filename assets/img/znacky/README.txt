LOGA DODAVATELSKÝCH ZNAČEK
==========================

Sem patří loga výrobců. Web si je vezme sám — stačí nakopírovat soubor
se správným názvem a spustit `python3 build.py`.

Očekávané názvy souborů:

    castrol.svg
    total.svg
    elf.svg
    boll.svg
    amtra.svg
    atas.svg
    energy.svg
    ks-tools.svg
    ath-heinl.svg
    thule.svg

Dokud soubor chybí, vypíše se místo loga název značky. Web se nerozbije,
jen tam bude text.

FORMÁT
------
Nejlepší je SVG — je ostré v jakékoli velikosti a má pár kilobajtů.
Když SVG není, PNG s průhledným pozadím a výškou aspoň 120 px.
Logo na bílém obdélníku nepoužívat, v nočním režimu by svítilo.

Místo .svg lze použít i .png — jen změň příponu v seznamu ZNACKY
v souboru build.py.

KDE LOGA VZÍT
-------------
Od obchodního zástupce dané značky, nebo z oficiálních stránek výrobce
v sekci pro partnery (bývá jako "Media kit", "Brand assets", "Ke stažení").
Nestahovat z vyhledávače obrázků — bývají tam staré verze log
a rozmazané výřezy.

PŘIDÁNÍ DALŠÍ ZNAČKY
--------------------
Dopiš řádek do seznamu ZNACKY v build.py, například:

    ("Febi", "febi.svg"),

a nakopíruj sem febi.svg.
