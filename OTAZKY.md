# Otázky pro majitele GCAR

Seznam věcí, které jsem při předělávce webu nedokázal ověřit. Dokud na ně
nebude odpověď, není na webu žádné tvrzení, které by je předjímalo.

---

## A. Tvrzení, která jsem z webu SMAZAL, protože je nemám ověřená

Napsal jsem je do dřívější verze sám. Nejsou nikde na gcar.cz.
Pokud platí, vrátíme je zpět — a budou to nejsilnější argumenty, které web má.

| # | Tvrzení | Otázka |
|---|---|---|
| A1 | „Vlastní rozvoz do servisů" | Rozvážíte vlastními auty, nebo posíláte přepravní službou? Web říká jen „distribuce do autoservisů a obchodů". |
| A2 | „Rozvoz na Kroměřížsku a Uherskohradišťsku" | Jaký je skutečný dojezd? Kam všude jezdíte? |
| A3 | „Objednejte do X hodin a máte to týž den" | Existuje nějaký deadline pro objednávku na stejný den? Jak často rozvoz jezdí? |
| A4 | „Sortiment testujeme ve vlastní dílně" | Je autoservis (autoserviskromeriz.cz) vaše firma, nebo jen partner? |
| A5 | „Prodej i montáž autoskel a tažných zařízení" | Montujete, nebo jen prodáváte? |
| A6 | „Přezutí a vyvážení pneumatik u nás" | Děláte pneuservis? |
| A7 | Podmínky půjčovny (kauce, doklad totožnosti, rezervace) | Jak to u vás doopravdy chodí? |
| A8 | Podmínky výprodeje (záruka, trvalá sleva) | Platí u výprodejového zboží standardní záruka? |
| A9 | „Velkoobchod i prodej koncovým zákazníkům" | Prodáváte i běžným lidem z ulice, nebo jen firmám? |

---

## B. Věci, které na webu chybí a měly by tam být

| # | Co | Proč |
|---|---|---|
| B1 | **Loga dodavatelských značek** (Bosch, Febi, Sachs, TRW…) | Pro autoservis je to nejrychlejší důkaz kvality. Které značky vedete? |
| B2 | **Konkrétní čísla o rozvozu** | Viz A1–A3. Tohle je jediná věc, kterou e-shop z internetu nedokáže nabídnout. |
| B3 | **Vlastní fotky** — sklad, regály, prodejna, lidi za pultem | Web nemá jedinou fotku. Vlastní fotka skladu udělá pro důvěru víc než jakýkoli text. Stocková fotka rozmazaného motoru je horší než žádná. |
| B4 | **Jak dlouho firma existuje, kolik má lidí** | Nic z toho na webu není. |
| B5 | **Kdo je ten „obchodní partner jedné z největších firem na evropském trhu"** | Když to jde napsat jménem, je to desetkrát silnější než anonymní věta. |

---

## C. Technické věci k ověření

| # | Co | Stav |
|---|---|---|
| C1 | **Skutečná URL vyhledávání v e-shopu** | V `build.py` je `ESHOP_SEARCH` = můj odhad. Vyhledej něco v e-shopu a pošli výslednou adresu. |
| C2 | **Ceny v e-shopu — s DPH nebo bez?** | Zatím u cen na webu nepíšeme nic. |
| C3 | **Logo v SVG** | Mám jen PNG 200×65. Na retina displeji je měkké. Potřebuju i inverzní variantu pro tmavé pozadí (teď ji generuju přebarvením pixelů, což není ideální). |
| C4 | **Odkazy na mapy** obou poboček | Na mapy.cz najít pobočku → Sdílet → Vložit na web. Styl `.maps` v CSS je hotový, chybí jen odkazy. |
| C5 | **Kontaktní formulář nikam neodesílá** | Otevře poštovní klienta přes `mailto`. Na ostro potřebuje endpoint (Formspree nebo serverless funkce). Na který e-mail mají poptávky chodit? |
| C6 | **Otevírací doba — rozpor** | Na gcar.cz je Po–Pá 8:00–17:00, na Portálu řidiče 7:00–17:30. Co platí? Je doba stejná na obou pobočkách? |
| C7 | **Sociální sítě** | Na současném webu jsou v patičce tři ikony s prázdným odkazem (`href="#"`). Máte Facebook/Instagram, nebo je vypustit? |
| C8 | **Texty podstránek** | gcar.cz blokuje automatické stahování (robots.txt), takže jsem podstránky nikdy neviděl. Zkopíruj mi prosím text z `/o-nas/`, `/sortiment/*`, `/akce/`, `/vyprodej/`, `/pujcovna/`. |

---

## D. Co jsem z původního webu vyhodil schválně

| # | Co | Proč |
|---|---|---|
| D1 | Sekce **„Proč s námi? 01–04"** | Čtyři obecné fráze bez jediného konkrétního údaje. Nikoho nepřesvědčí. Nahradit fakty z bodů A1–A3 a B1–B4. |
| D2 | `© 2020` v patičce | Působí jako opuštěný web. Teď se doplňuje automaticky. |
| D3 | Ikony sociálních sítí vedoucí na `#` | Viz C7. |
