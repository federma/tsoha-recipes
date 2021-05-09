# Reseptisovellus
Aineopintojen harjoitustyö: Tietokantasovellus, Tietojenkäsittelytieteen osasto, Helsingin yliopisto, kevät 2021.

Sovelluksen tilanne 9.5.2021

Testiversio löytyy osoitteesta [https://morning-beach-58885.herokuapp.com/](https://morning-beach-58885.herokuapp.com/).

Sovelluksen sujuva toiminta edellyttää, että selaimessa on JavaScript päällä. Sovellusta voi käyttää myös ilman JS:ä, mutta uusiin resepteihin ei pääse lisäämään ainesosarivejä ja lomakkeiden virheisiin reagointi on vähemmän käyttäjäystävällistä.

Tietojen tallentamiseen käytetään taustalla PostgreSQL -tietokantaa.

## Toiminnallisuudet tällä hetkellä

* käyttäjä voi luoda tunnuksen, kirjautua sisään tai ulos
* käyttäjä näkee profiilisivultaan itse luomansa reseptit
* sovellukseen voi jättää uuden reseptin
* jättämäänsä reseptiä voi muokata
* sovellukseen jätettyjä reseptejä voi selailla, hakea nimen perusteella ja järjestellä
* reseptin ohjetta voi tarkistella
* reseptiin voi lisätä kommentteja ja lukea muiden jättämiä kommentteja
* reseptin voi lisätä ostoslistalle tai poistaa sieltä (toiminto reseptin omalla sivulla)
* ostoslistalla voi valita annosten lukumäärän ja ainesosat skaalautuvat
* ostoslistan voi tyhjentää kokonaan

## Oikeuksien ja syötteiden hallinta

* tietokannan osoite ja sovelluksen käyttämä salainen avain on tallennettu yksityiseen ympäristömuuttujaan
* käyttäjien salasanat tallennetaan selkokielesen sanan sijaan hajautusarvona
* kirjautuneiden käyttäjien tunnistamiseen käytetään Flask:in session-oliota
* istuntoon (session) tallennetaan myös satunnainen tieto (csrf-token), jolla estetetään CSRF-haavoittuvuus
* käyttäjän antamia syötteitä ei näytetä sivuilla tai tallenneta tietokantaa sellaisenaan (estetään XSS-haavoittuvuus ja SQL-injektio)
* lomakkeiden syötteitä (lähinnä pituus) tarkistetaan HTML:n sekä JavaScriptin avulla
* jos JS ei ole käytössä, niin syötteet varmuuden vuoksi tarkistetaan myös Python -koodissa

## Sovelluksen puutteet / kehitysajatukset

* ulkoasuun ei ole löytynyt aikaa panostaa riittävästi, käytössä on toistaiseksi kohtalaisen vakioasetuksilla Bootstrap -elementtejä
* reseptin ainesosien ja erityisesti määrien suhteen tahtoisin rakentaa paremman ratkaisun siihen, että miten huomioidaan ainesosat, joille ei ole antaa tarkkoja määriä. Mietin, että käyttäjä voisi syöttää esim. erikseen ainesosat, joille voi antaa tarkan määrän ja sitten olisi erillinen listaus esim. mausteille tai määrien vapaamuotoista määrittelyä varten. Nyt sovellus yksinkertaisesti muuttaa määrän lukuarvoon 0, jos käyttäjä on antanut kyseiseen kohtaan sanallisen kuvauksen tai epäkelpoja merkkejä.
* ostoslistan ulkoasua ja toiminnallisuutta tahtoisin hioa (erityisesti suorat linkit resepteihin, mahdollisuus poistaa suoraan yksittäisiä reseptejä, tulostus tekstitiedostona)
* lisäksi mielessä on ollut suosikkireseptien ja usean ostoslistan tallennusmahdollisuuden, käyttäjäryhmät (yksityiset reseptipankit ja kommentoinnit), admin-näkymän, valmistusajat resepteille

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
