# Napojení kontaktního formuláře

**HOTOVO — formulář je napojený.**

    Endpoint:  https://formspree.io/f/xnpnzzre
    Nastaveno v build.py na řádku FORM_ENDPOINT

## Zbývá: přesměrovat poptávky na gcar@gcar.cz

Formulář teď posílá na adresu, která byla při zakládání vybraná v poli
„Send emails to". Cíl je **gcar@gcar.cz**. Formspree neumí posílat na
adresu, kterou si nikdo nepotvrdil, takže:

1. Na formspree.io → **Account** → **Linked Emails** → přidat `gcar@gcar.cz`
2. Formspree pošle na tu adresu potvrzovací e-mail — **musí na odkaz
   kliknout někdo, kdo má do té schránky přístup**
3. Pak ve **Forms → Poptávky gcar.cz → Settings** přepnout příjemce

**Adresa formuláře se tím nemění**, takže na webu se nic přepisovat nebude
a není potřeba znovu nic nahrávat.

## Otestovat po nasazení

Odeslat přes formulář zkušební zprávu a ověřit, že dorazila. Formspree
u prvních zpráv občas posílá potvrzovací krok — když zpráva nedorazí,
podívat se do schránky příjemce i do spamu.

## Co se stane po odeslání

- **Povedlo se:** pod tlačítkem se zobrazí „Děkujeme, poptávku máme."
  a formulář se vyprázdní. Člověk zůstane na stránce.
- **Nepovedlo se:** „Odeslání se nepovedlo. Zkuste to prosím znovu, nebo
  nám zavolejte." — ať zpráva nezmizí do prázdna.
- **Chybí povinné pole:** web řekne konkrétně které.

## Ochrana proti robotům

Ve formuláři je skryté pole (`_gotcha`), které člověk nevidí, ale roboti
ho vyplňují. Když je vyplněné, odeslání se tiše zahodí. Formspree má
navíc vlastní filtr.

## Limity zdarma

Formspree dává v bezplatném tarifu 50 zpráv měsíčně. Kdyby to nestačilo,
placený tarif stojí kolem 10 USD měsíčně — nebo se dá formulář přepojit
na vlastní funkci na Vercelu.
