# Otázky pro majitele GCAR

Seznam věcí, které jsem při předělávce webu nedokázal ověřit. Dokud na ně
nebude odpověď, není na webu žádné tvrzení, které by je předjímalo.

---

## A. Tvrzení, která jsem z webu SMAZAL, protože je nemám ověřená

Napsal jsem je do dřívější verze sám. Nejsou nikde na gcar.cz.
Pokud platí, vrátíme je zpět — a budou to nejsilnější argumenty, které web má.

| # | Tvrzení | Otázka |
|---|---|---|
| A1 | ~~Vlastní rozvoz~~ | **POTVRZENO majitelem** — vozí vlastními auty. Na webu je to teď v horní liště i v pruhu s fakty. |
| A2 | „Rozvoz na Kroměřížsku a Uherskohradišťsku" | Jaký je skutečný dojezd? Kam všude jezdíte? |
| A3 | „Objednejte do X hodin a máte to týž den" | Existuje nějaký deadline pro objednávku na stejný den? Jak často rozvoz jezdí? |
| A4 | Autoservis | **PRAVDĚPODOBNĚ VYŘEŠENO** — katalogy (ekatalog.cz, firmy.cz) vedou autoservis, pneuservis i montáže LPG/CNG pod stejným IČO **26946840**, tedy pod GCAR services, s.r.o. Nechat potvrdit. |
| A5 | „Prodej i montáž autoskel a tažných zařízení" | Montujete, nebo jen prodáváte? |
| A6 | „Přezutí a vyvážení pneumatik u nás" | Děláte pneuservis? |
| A10 | ~~„Najdeme díl podle VIN"~~ | **OVĚŘENO** — e-shop má „VIN + ACI katalog" a vyhledávání podle KÓD / TEXT / VOZIDLO. Můžeme to na webu tvrdit. |
| A7 | Podmínky půjčovny (kauce, doklad totožnosti, rezervace) | Jak to u vás doopravdy chodí? |
| A8 | Podmínky výprodeje (záruka, trvalá sleva) | Platí u výprodejového zboží standardní záruka? |
| A9 | „Velkoobchod i prodej koncovým zákazníkům" | Prodáváte i běžným lidem z ulice, nebo jen firmám? |

---

## B. Věci, které na webu chybí a měly by tam být

| # | Co | Proč |
|---|---|---|
| B1 | **Loga dodavatelských značek** | Z e-shopu už víme o **CASTROL, TOTAL, ELF, BOLL, AMTRA, ATAS, ENERGY, KS Tools, ATH Heinl, Thule**. Castrol, Total a Elf mají v patičce e-shopu vlastní sekci, takže jsou asi klíčoví. Které další vedete a od kterých smíte použít logo? |
| B8 | **TecDoc** | E-shop běží na databázi TecDoc. To je pro mechanika silný signál (kompletní katalog dílů podle vozu). Na prezentačním webu o tom není ani slovo — může tam být? |
| B9 | **Katalogy ke stažení** | E-shop odkazuje na Mazací plán CASTROL, katalog chemie BOLL, katalog startérů a alternátorů a tažná zařízení. Servisy tyhle PDF používají — patří i na web? **Potřebuju konkrétní URL těch odkazů z patičky e-shopu.** |
| B10 | **Souhlas s použitím log značek** | Na webu je zatím jen textový výpis značek. Loga bych přidal, ale u některých výrobců je jejich použití vázané na smlouvu s distributorem. Máte to ošetřené? |
| B2 | **Konkrétní čísla o rozvozu** | Viz A1–A3. Tohle je jediná věc, kterou e-shop z internetu nedokáže nabídnout. |
| B3 | **Vlastní fotky** — sklad, regály, prodejna, lidi za pultem | Web nemá jedinou fotku. Vlastní fotka skladu udělá pro důvěru víc než jakýkoli text. Stocková fotka rozmazaného motoru je horší než žádná. |
| B4 | **Jak dlouho firma existuje, kolik má lidí** | Nic z toho na webu není. |
| B5 | **Kdo je ten „obchodní partner jedné z největších firem na evropském trhu"** | Když to jde napsat jménem, je to desetkrát silnější než anonymní věta. |
| B6 | **Hlavní sklad** | E-shop rozlišuje dostupnost KM / Pobočky / **Hlavní sklad**. Kde je hlavní sklad a co to znamená pro dodací dobu? Na webu o něm není ani slovo. |
| B7 | **Ceny na webu byly zastaralé** | Stahovák pružin ENG NE00016: gcar.cz uváděl 4 846 Kč, e-shop má 2 900,80 Kč bez DPH. Proto na novém webu ceny nejsou vůbec a odkazuje se do e-shopu. |

---

## C. Technické věci k ověření

### Nesrovnalosti mezi gcar.cz a e-shopem

| # | Co | Otázka |
|---|---|---|
| C9 | ~~Dva různé e-maily~~ | **ZODPOVĚZENO 16. 9. 2026** — hlavní je `gcar@gcar.cz`. (`info@gcar.cz` v e-shopu zůstává, na web nedáváme.) |
| C10 | ~~602 721 994 telefon nebo fax?~~ | **ZODPOVĚZENO** — je to **telefon**. Patička e-shopu ho označuje jako fax chybně; stojí za to ji opravit. |
| C11 | ~~Adresa~~ | **ZODPOVĚZENO** — správně je **Hulínská 2351/28E**. Na starém gcar.cz je překlep (298E) — opravit i tam, než se web vypne. |
| C12 | **Právní stránky chybí** | E-shop má Obchodní podmínky, Reklamační řád, Ochranu osobních údajů a Cookies. Nový prezentační web nemá nic. **Pošli mi URL těch stránek z e-shopu** a odkážu na ně z patičky. |
| C13 | ~~Fonty z Google~~ | **VYŘEŠENO** — písma se hostují z `/assets/fonts/`, web už nikam ven nesahá. |
| C14 | **Newsletter** | E-shop sbírá e-maily na akční nabídky. Má být přihlášení i na webu? |


| # | Co | Stav |
|---|---|---|
| C1 | ~~URL vyhledávání~~ | **VYŘEŠENO** — `/cs/hledani/5/-1/{dotaz}`. Vyhledávací pole na webu je napojené. |
| C2 | ~~Ceny s DPH nebo bez?~~ | **ZODPOVĚZENO** — e-shop ukazuje obojí, hlavní cena bez DPH, pod ní s DPH. |
| C3 | **Logo v SVG** | Mám jen PNG 200×65. Na retina displeji je měkké. Potřebuju i inverzní variantu pro tmavé pozadí (teď ji generuju přebarvením pixelů, což není ideální). |
| C4 | **Odkazy na mapy** obou poboček | Na mapy.cz najít pobočku → Sdílet → Vložit na web. Styl `.maps` v CSS je hotový, chybí jen odkazy. |
| C5 | **Kontaktní formulář nikam neodesílá** | Otevře poštovní klienta přes `mailto`. Na ostro potřebuje endpoint (Formspree nebo serverless funkce). Na který e-mail mají poptávky chodit? |
| C6 | ~~Otevírací doba~~ | **ČÁSTEČNĚ** — majitel potvrdil **8:00–17:00**. Portál řidiče má 7:00–17:30 chybně, nechat opravit. **VYŘEŠENO** — Firmy.cz má rozepsáno Po–Pá 8:00–17:00, **So 9:00–10:00**, Ne zavřeno. Na webu upraveno. |
| C7 | **Sociální sítě** | Na současném webu jsou v patičce tři ikony s prázdným odkazem (`href="#"`). Máte Facebook/Instagram, nebo je vypustit? |
| C8 | **Texty podstránek** | gcar.cz blokuje automatické stahování (robots.txt), takže jsem podstránky nikdy neviděl. Zkopíruj mi prosím text z `/o-nas/`, `/sortiment/*`, `/akce/`, `/vyprodej/`, `/pujcovna/`. |

---

## E. Nové zjištění: firma dělá víc, než co je na webu

> **ZMĚNA KONCEPCE (16. 9. 2026):** GCAR není prodejna dílů se službami navrch —
> je to střecha nad vším: autodíly, autoservis i LPG/CNG. Web je proto
> přestavěný na tři rovnocenné pilíře na první obrazovce a servis i LPG
> mají vlastní stránky **/autoservis/** a **/lpg/**.
>
> **POZOR:** Text těch stránek s autoservisem, pneuservisem
> a montážemi LPG/CNG. Ten text je poskládaný z veřejných katalogů, **ne od
> firmy**. Než web pustíme ven, musí ho majitel přečíst slovo po slovu —
> zvlášť tvrzení o náhradním vozidle po dobu montáže a o rozsahu servisu
> klimatizací a geometrie. (Splátky na montáž LPG už byly odstraněny —
> nenabízejí se.)

Z veřejných katalogů (firmy.cz, ekatalog.cz, zivefirmy.cz) vychází, že pod
IČO **26946840** běží toho podstatně víc, než co gcar.cz zmiňuje. Ověřit
u majitele a rozhodnout, co z toho na web patří.

| # | Co | Otázka |
|---|---|---|
| E1 | **Montáže LPG a CNG — UŽ JE NA WEBU, POTVRDIT TEXT** | Samostatný web **lpg-kromeriz.cz**, montáže, přestavby, revize, servis a diagnostika LPG/CNG, LPG na splátky, roční revize, výměny nádrží, náhradní vozidlo po dobu montáže. Na gcar.cz o tom není ani slovo. Má to tam být, nebo to má zůstat oddělené? |
| E2 | **Pneuservis — UŽ JE NA WEBU, POTVRDIT TEXT** | Katalogy uvádějí „autoservis s pneuservisem", měření geometrie, servis klimatizací. Tím padá moje pochybnost, jestli přezouváte — asi ano. Potvrdit. |
| E3 | **Pevná linka 573 334 052** | Na webu není. Má tam být? |
| E4 | **Firma vznikla v roce 2004** | Na webu bylo teď „Od roku 2004" — potvrdit, ať tam nemáme špatný rok. |
| E5 | **Jednatel Vladimír Hauk** | Je to majitel, se kterým se řeší tento web? |
| E8 | **Mají se weby sloučit?** | Teď jsou tři: gcar.cz, autoserviskromeriz.cz, lpg-kromeriz.cz. gcar.cz na zbylé dva odkazuje. Má to tak zůstat, nebo mají obsah těch dvou postupně přejít pod gcar.cz a domény se jen přesměrovat? Tři weby znamenají trojí údržbu a rozdrobené pozice ve vyhledávání. |
| E6 | ~~Adresa ve Starém Městě~~ | **POTVRZENO** — **Brněnská 1395**. Údaj „Za Špicí 1798" na ekatalog.cz je špatně, nechat opravit. |
| E7 | **Záznamy na Firmy.cz** | Firma tam má **několik samostatných zápisů** („GCAR services", „LPG - GCAR", „Prodej náhradních dílů - GCAR", „GCAR"), každý s jinými údaji a jinou otevírací dobou. Stojí za to je pročistit — pro místní vyhledávání to má větší dopad než půlka webu. |

---

## D. Co jsem z původního webu vyhodil schválně

| # | Co | Proč |
|---|---|---|
| D1 | Sekce **„Proč s námi? 01–04"** | Čtyři obecné fráze bez jediného konkrétního údaje. Nikoho nepřesvědčí. Nahradit fakty z bodů A1–A3 a B1–B4. |
| D2 | `© 2020` v patičce | Působí jako opuštěný web. Teď se doplňuje automaticky. |
| D3 | Ikony sociálních sítí vedoucí na `#` | Viz C7. |
