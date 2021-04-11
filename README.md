# Reseptisovellus
Aineopintojen harjoitustyö: Tietokantasovellus, Tietojenkäsittelytieteen osasto, Helsingin yliopisto, kevät 2021.

Sovelluksen tilanne 11.4.2021

Testiversio löytyy osoitteesta [https://morning-beach-58885.herokuapp.com/](https://morning-beach-58885.herokuapp.com/)

## Toiminnallisuudet tällä hetkellä

* Käyttäjä -valikon kautta voi luoda tunnuksen sovellukseen, kirjautua sisään tai ulos ja tarkistaa itse luomansa reseptit
* sovellukseen voi jättää uuden reseptin
* Reseptit -valikon alta voi selailla sovellukseen luotuja reseptejä
* reseptin voi em. valikosta klikata tarkempaan tarkasteluun, jolloin näkyy reseptiin kuuluvat ainesosat ja niiden tiedot
* reseptiin voi myös lisätä kommentteja ja lukea muiden jättämiä kommentteja

Tietojen tallentamiseen käytetään PostgreSQL -tietokantaa.

## Selkeimmät puutteet ja lopulliseen versioon tulossa olevat ominaisuudet

* uuden reseptin syöttämisessä ei ole mitään validaatioita (eikä oikeastaan missään muussakaan lomakkeessa) -> esim. jonkin ainesosa-kentän jättäminen tyhjäksi tai jonkin muun kuin kokonaisluvun kirjaaminen määrä-kohtaan johtaa virhetilanteeseen
* uuden reseptin ainesosakenttiä pitäisi pystyä myös poistamaan (tällä hetkellä vain lisäysnappi)
* käyttäjä voi ilman kirjautumista yrittää jättää kommenttia tai lisätä uuden reseptin -> virhetilanne
* ulkoasu on kaikin puolin vielä kesken (html, css, javascript eivät juuri entuudestaan ole tuttua, niin asiassa riittää opeteltavaa)
* lisäominaisuuksiksia olisi tarkoitus tulla ainakin jotain näistä: ostoslistan luonti, mahdollisuus muokata itse luomiaan reseptejä, suosikkireseptien tallentaminen, reseptiarviot, käyttäjäryhmien luonti (yksityiset reseptipankit ja kommentoinnit)

### Alkuperäinen info/kehitysajatus alla

Sovelluksen avulla voi (sen valmistuttua) tallentaa ja tarkastella ruokareseptejä. Lisäksi tarkoitus on, että sovelluksessa voisi valita reseptejä sekä syöjien määrän ja näillä tiedoilla luoda valmiin ostoslistan.

Sovelluksen ominaisuuksia on tarkoitus olla ainakin:

* Käyttäjä voi kirjautua sisään ja ulos
* Käyttäjä voi lisätä uuden reseptin
* Käyttäjä voi muokata aiemmin luomaansa reseptiä tai poistaa sen
* Käyttäjä voi tarkastella muiden lisäämiä reseptejä
* Käyttäjä voi arvioida reseptejä tai antaa niihin kommentteja
* Käyttäjät näkevät muiden antamat arviot tai kommentit
* Käyttäjä voi generoida ostoslistan valittujen reseptien mukaisesti

Lisäksi harkitsen, että sovelluksessa olisi mahdollisuus luoda ryhmiä, joilla näkyisi yleisten reseptien lisäksi "yksityisiä" reseptejä ja niiden arviot/kommentit. Yhtenä ydinajatuksena sovelluksessa olisi helpottaa esim. kaveriporukan mökkireissujen ostosten suunnittelua, jolloin osa resepteistä ja niihin liittyvä keskustelu voisi pysyä yksityisenä.

Suurin haaste kehityksessä on mahdollisesti ostoslistan toteutus hyvin. Ruokareseptien yhteydessä voi vaatia tiedoiksi annosmäärän ja eri aineksiin (riittävän) tarkat määrät (esim. grammoina ja millilitroina), jolloin eri reseptien tiedot on helpohkoa yhdistää ostoslistaan. Olisi kuitenkin myös mielekästä yhdistellä eri reseptien ainesosat listassa yhteen - esim. jos useampaan reseptiin on merkitty ketsuppi, niin listassa ei tarvitsisi olla ketsuppi 100g ja ketsuppi 150g - mutta täytyy miettiä miten tämän toteuttaisi, sillä aineksilla voi olla eri kirjoitusasu (ketsuppi, ketsuppia) ja yhdistely ei siten ihan helposti onnistu. Lisäksi kaikista aineista ei ole mielekästä tai mahdollista antaa tarkkoja määriä (esim. suola ja mustapippuri "maun mukaan") ja mahdollisesti kaikkia perusmausteita ei tarvita ostoslistaan mukaan.
