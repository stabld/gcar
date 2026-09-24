# gcar.cz

Statický web GCAR services, s.r.o. Bez frameworku, bez node_modules, bez build pipeline.

## Struktura

```
build.py                  generátor — hlavička, patička, menu a obsah stránek
assets/css/style.css      všechny styly
assets/css/fonts.css      @font-face — generované, needitovat ručně
assets/fonts/             písma hostovaná u nás (ne Google Fonts)
assets/js/main.js         mobilní menu, živý stav otevírací doby, formulář
assets/img/               logo (světlá i inverzní varianta)
index.html                ⟵ generované, needitovat ručně
o-nas/, sortiment/, …     ⟵ generované, needitovat ručně
sitemap.xml, robots.txt   ⟵ generované
```

## Jak upravit obsah

1. Otevři `build.py`
2. Nahoře jsou firemní údaje (`FIRMA`, `POBOCKY`, `OTEVIRACI_DOBA`, `NAV`) — telefon se změní na jednom místě a promítne se všude
3. Níž je text jednotlivých stránek (`HOME`, `O_NAS`, `KAT_PNEU`, …)
4. Spusť `python3 build.py`
5. `git add -A && git commit -m "…" && git push`

HTML soubory **needituj ručně** — další běh `build.py` je přepíše.

## Lokální náhled

```bash
python3 -m http.server 8000
```

Pak http://localhost:8000. Obyčejné otevření souboru v prohlížeči (`file://`)
nebude fungovat správně, protože cesty k CSS a JS začínají lomítkem.

## Nasazení

Vercel: Add New → Project → import repozitáře. Framework Preset **Other**,
Build Command i Output Directory nechat prázdné. `vercel.json` už řeší
hezké adresy a cache hlavičky.

## Obsah

Na webu je **jen text, který doopravdy stojí na gcar.cz** — nic domyšleného.
Podstránky jsou proto zatím hubené: gcar.cz blokuje automatické stahování
(`robots.txt`), takže jejich původní texty zatím nemám.

Seznam všeho, co je potřeba doplnit nebo ověřit u majitele, je v **[OTAZKY.md](OTAZKY.md)**.


## Poznámka k logu

`assets/img/logo.svg` a `logo-inverse.svg` nejsou originál od grafika —
vznikly **obtažením** z původního `logo.png` (200 × 65 px). Tvarově sedí
a na rozdíl od rastru jsou ostré v jakékoli velikosti, ale zuby ozubeného
kola jsou o chlup zakulacenější než v předloze.

Z téhož obtahu vychází i ikona v záložce a náhledový obrázek pro sdílení.

Až se objeví originální vektor od grafika (.svg, .ai nebo .pdf), stačí
ho nahradit — názvy souborů zůstanou stejné. `logo.png` zůstává, používá
se ve strukturovaných datech pro Google, kde se rastr preferuje.
