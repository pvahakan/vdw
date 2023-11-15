# Laskentakoodin kuvaus

Tarkoitus on tehdä laskentakoodi, jolla pystytään määrittämään eri kaasuille paine tilavuuden funktiona käyttäen ideaalikaasun tilanyhtälöä sekä van der Waals -tilanyhtälöä.

# Tehtävänanto

1. Laske kaasun tilavuus 1-1000 atm:n paineessa ideaalikaasumallilla sekä vdw-mallilla.
2. Ota tuloksesta paine ja tilavuus, piirrä kuvaaja (P, PV)-koordinaatistoon ja vertaile eri mallien antamia tuloksia.
3. Toista laskenta CO2 ja H2 -kaasuille.

# Teoreettista taustaa

## Ideaalikaasu

Ideaalikaasu on eräs tapa mallintaa kaasujen käyttäytymistä. Ideaalikaasussa kaikki molekyylit ovat pistemäisiä, etenevät suoraviivaisesti ja törmäilevät toisiin atomeihin kimmoisasti. Ideaalikaasun tila voidaan määrittää ideaalikaasun tilanyhtälöstä

$$pV=nRT$$

## van der Waals -tilanyhtälö

Van der Waals -tilanyhtälö on kehittyneempi malli ideaalikaasusta. Se ottaa huomioon molekyylien koon sekä molekyylien välisiä vuorovaikutuksia. Van der Waals -tilanyhtälö on muotoa

$$\left[ p + a \left( \frac{n}{V} \right)^2 \right] \left( \frac{V}{n} - b \right) = RT$$

missä vakiot $a$ ja $b$ ovat kokeellisesti eri kaasuille määrättyjä vakioita. Vakio $a$ on korjauskerroin, joka ottaa huomioon molekyylien sisäisiä voimia. Vakio $b$ puolestaan on korjauskerroin molekyylin koolle.

Tästä yhtälösta paineen ratkaisu onnistuu analyyttisesti suhteellisen helposti, mutta tilavuuden kanssa tulee ongelmia. Niimpä tilavuus ratkaistaan numeerisesti.
