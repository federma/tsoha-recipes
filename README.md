# Reseptisovellus
Aineopintojen harjoitustyö: Tietokantasovellus, Tietojenkäsittelytieteen osasto, Helsingin yliopisto, kevät 2021.

Sovelluksen tilanne 25.4.2021 (välipalautus III)

Testiversio löytyy osoitteesta [https://morning-beach-58885.herokuapp.com/](https://morning-beach-58885.herokuapp.com/)

Tietojen tallentamiseen käytetään PostgreSQL -tietokantaa.

## Toiminnallisuudet tällä hetkellä

* käyttäjä voi luoda tunnuksen, kirjautua sisään tai ulos
* käyttäjä näkee profiilisivultaan itse luomansa reseptit
* sovellukseen voi jättää uuden reseptin
* jättämäänsä reseptiä voi muokata
* sovellukseen jätettyjä reseptejä voi selailla, hakea nimen perusteella ja järjestellä
* reseptin ohjetta voi tarkistella
* reseptiin voi lisätä kommentteja ja lukea muiden jättämiä kommentteja
* reseptin voi lisätä ostoslistalle tai poistaa sieltä
* ostoslistalla voi valita annosten lukumäärän ja ainesosat skaalautuvat
* ostoslistan voi tyhjentää kokonaan

## Kehityksessä olevat keskeneräiset asiat

* ulkoasuun on takoitus panostaa kurssin loppuvaiheessa lisää
* lomakkeiden syötteiden validaatiot ovat kesken, esim. syötteiden pituutta ei vielä tarkisteta
* CSRF-haavoittuvuuden paikkaaminen
* reseptin ainesosien syötteessä täytyy paremmin huomioida, jos tarkkaa määrää ei voi antaa (nyt voi valita yksiköksi "maun mukaan", mutta täytyy silti antaa jokin määrä)
* ostoslista täytyy muuttaa selkeämmäksi tulosteiden osalta ja jotenkin huomioida erikseen ainesosat, joille ei ole määriä (joita siten ei voi skaalata eri annoskokoihin)
* koodia on tarkoitus siivota (esim. poistaa käyttämättömät metodit)
* mahdollisuus lisätä/poistaa reseptiä ostoslistalta suoraan reseptien selailusivulle ja ostoslista-sivulle
* timestamp täytyy korjata, ei näytä olevan Suomen aikavyöhyke asetettu
* jos jää aikaa tai on kurssin jälkeen intoa kehittää, niin voisi lisäillä suosikkireseptien ja usean ostoslistan tallenusmahdollisuuden, käyttäjäryhmät (yksityiset reseptipankit ja kommentoinnit), admin-näkymän, valmistusajat resepteille

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
