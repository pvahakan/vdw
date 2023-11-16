# ComPhy

Tällä laskentakoodilla pystyy määrittämään eri kaasuille tilavuuden paineen funktiona. Koodi muodostaa 20 paineen arvoa annetulta väliltä ja laskee jokaista painetta vastaavan tilavuuden. Koodille annetaan tiedoksi mitä kaasua tutkitaan, kuinka paljon ja missä lämpötilassa.

ComPhy pystyy laskemaan kaasun tilavuuden kahdella eri kaasumallilla: ideaalikaasun tilanyhtälön avulla sekä van der Waals -tilanyhtälön avulla. Van der Waals -tilanyhtälöä varten täytyy määrittää mitä kaasua tutkitaan, koska vdw-malli vaatii kullekin kaasulle ominaiset parametrit $a$:n ja $b$:n.

## Input ja output -tiedostot

Laskennassa käytettävä malli kuvataan .inp -päätteiseen tekstitiedostoon. Tiedoston nimeämisessä kannattaa käyttää johdonmukaista mallia, koska useimmiten pitää laskea esimerkiksi usealla eri kaasulla samoilla paineen arvoilla. Jos kaasu tai jokin muu parametri vaihtuu, täytyy tehdä uusi input-tiedosto ja suorittaa laskenta sen pohjalta.

Kun input-tiedosto on tehty ja laskenta suoritettu, kirjoittaa koodi tuloksen output-tiedostoon. Output-tiedostolla on sama nimi kuin input-tiedostolla, mutta tiedostopääte on .out. Jos saman nimisellä input-tiedostolla suoritetaan laskenta useaan kertaan, output-tiedosto ylikirjoitetaan jokaisella suorituskerralla. Luo siis jokaista laskentaa varten uusi input-tiedosto, jotta vanha data ei häviä. Output-tiedoston alkuun tulostuu tieto laskennassa käytetyistä parametreista sekä varsinainen laskun tulos, joka on kutakin paineen arvoa vastaava tilavuuden arvo.

Input-tiedostossa kuvataan kaikki tarvittavat parametrit laskennan suorittamiseksi. Niitä ovat käytettävä kaasumalli, kaasu, laskettava suure, kaasun lämpötila, kaasun massa ja kaasun paine. Input-tiedosto koostuu avainsanasta ja sen perässä olevasta arvosta. Avainsana ja arvo erotetaan toisistaan kaksoispisteellä. Alla on esimerkki input-tiedoston muodosta.

```
%model
type : "vdw"
calculation : "vol"
gas : "CO2" # Muita mahdollisia: H2O, CO2, HE

%values
temp : 270 # Kaasun lämpötila kelvineinä
mass : 12 # Kaasun massa grammoina
pressure : 1-1000 # Laskee kaasun tilavuuden, kun paine on 1-100 atm
```

Kaikki risuaidan (#) jälkeiset tekstit ovat kommentteja eikä niitä huomioida input-tiedoston lukemisessa. Alla on listattu kaikki tällä hetkellä käytössä olevat avainsanojen arvot.

- type: "vdw" ja "ideal". Viittaavat käytettävään malliin, missä "vdw" tarkoittaa van der Waals -tilanyhtälöä ja "ideal" ideaalikaasun tilanyhtälöä.
- calculation: "vol". Kertoo mikä suure lasketaan. "vol" tarkoittaa, että lasketaan tilavuus.
- gas: "CO2", "H2O", "HE". Kertoo mikä kaasu on kyseessä. Tässä hiilidioksidi, vesihöyry ja helium.
- temp: Kaasun lämpötila kelvinasteina.
- mass: Kaasun massa grammoina.
- pressure: Painealue, jossa tilavuus halutaan laskea. Koodi muodostaa 20 arvoa annetulta väliltä. Väli annetaan muodossa alaraja-yläraja. Paineen yksikkönä on ilmakehän paine (atm).

Yllä olevia tietoja soveltamalla pystyy input-tiedostoa muokkaamaan halutunlaiseksi. **Huom!** Aina kun muutat input-tiedostoa, vaihda myös tiedoston nimi, jotta vanhan laskun tulokset eivät häviä! Kun koodi suoritetaan, vanha .out -tiedosto ylikirjoitetaan, mikäli sillä on tiedostopäätettä lukuunottamatta sama nimi kuin input-tiedostolla.

## Laskentakoodin ajaminen

Laskentakoodi suoritetaan komentoriviltä. Mene komentorivillä siihen hakemistoon jossa laskentakoodi on (main.py). Kun olet tässä hakemistossa, suorita komento

```bash
./main.py tiedostonimesi.inp
```

Komentoriville saattaa tulostua jotakin varoituksia, mutta niistä ei tarvitse välittää. Mikäli kaikki meni putkeen, samassa kansiossa on nyt tiedosto ``tiedostonimesi.out``, joka sisältää laskennan tuloksen. Voit avata tiedoston jollakin tekstieditorilla (komentorivillä esim. ``less tiedostonimesi.out``).

Mikäli komentoriville tulostuu virheitä, eikä output-tiedostoa ole tai se ei sisällä oikeaa tietoa, tarkista ensin että input-tiedosto on täsmälleen ylempänä olevan esimerkin kaltainen. Tarkista, että sanat ovat kirjoitettu oikein, pienet ja isot kirjaimet ovat kuten esimerkeissä sekä heittomerkit ja kaksoispisteet ovat kohdallaan. Input-tiedoston tulee olla juuri oikean muotoinen, jotta koodi ymmärtää mitä se pitää sisällään.

# Teoreettista taustaa

## Ideaalikaasu

Ideaalikaasu on eräs tapa mallintaa kaasujen käyttäytymistä. Ideaalikaasussa kaikki molekyylit ovat pistemäisiä, etenevät suoraviivaisesti ja törmäilevät toisiin atomeihin kimmoisasti. Ideaalikaasun tila voidaan määrittää ideaalikaasun tilanyhtälöstä

$$pV=nRT$$

## van der Waals -tilanyhtälö

Van der Waals -tilanyhtälö on kehittyneempi malli ideaalikaasusta. Se ottaa huomioon molekyylien koon sekä molekyylien välisiä vuorovaikutuksia. Van der Waals -tilanyhtälö on muotoa

$$\left[ p + a \left( \frac{n}{V} \right)^2 \right] \left( \frac{V}{n} - b \right) = RT$$

missä vakiot $a$ ja $b$ ovat kokeellisesti eri kaasuille määrättyjä vakioita. Vakio $a$ on korjauskerroin, joka ottaa huomioon molekyylien sisäisiä voimia. Vakio $b$ puolestaan on korjauskerroin molekyylin koolle.

Tästä yhtälösta paineen ratkaisu onnistuu analyyttisesti suhteellisen helposti, mutta tilavuuden kanssa tulee ongelmia. Niimpä tilavuus ratkaistaan numeerisesti.

# Tehtävänanto

1. Laske kaasun tilavuus 1-1000 atm:n paineessa ideaalikaasumallilla sekä vdw-mallilla.
2. Ota tuloksesta paine ja tilavuus, piirrä kuvaaja (P, PV)-koordinaatistoon ja vertaile eri mallien antamia tuloksia.
3. Toista laskenta CO2 ja H2 -kaasuille.