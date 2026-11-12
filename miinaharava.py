import random
import haravasto
from haravasto import NAPIT

#PELIN TILA
tila = {}

#KENTÄN KÄSITTELY

#KENTÄN LUOMINEN
def luo_kentta(leveys, korkeus):
    kentta = []

    for _ in range(korkeus):
        rivi = []

        for _ in range(leveys):
            rivi.append(" ")

        kentta.append(rivi)
    return kentta

#KENTÄN MIINOITTAMINEN
def miinoita_kentta():
    pass

#VIEREISTEN MIINOJEN LASKEMINEN
def laske_viereiset_miinat():
    pass

#TARKISTETAAN VOITTO
def tarkista_voitto():
    pass

#TILASTOT

#TILASTOJEN NÄYTTÄMINEN
def nayta_tilastot():
    '''
    try:
        with open("tilastot.txt", "r") as tiedosto:
            tilastot = tiedosto.readlines()
            if not tilastot:
                print("Ei tilastoja.")
                return
            print("\n=== Tilastot ===")
            for rivi in tilastot:
                print(rivi.strip())
    except FileNotFoundError:
        print("Tilastotiedostoa ei löytynyt.")
    '''
    print("\n"* 100)  # Tyhjennetään konsoli
    print("Tilastoja ei ole vielä toteutettu.")

#TILASTOJEN TALLENTAMINEN
def tallenna_tilasto():
    pass

#ARVOJEN KYSYMINEN
def kysy_positiivinen_luku(teksti):
    while True:
        try:
            arvo = int(input(teksti))
            if arvo > 0:
                return arvo
            else:
                print("Syötä positiivinen kokonaisluku.")
        except ValueError:
            print("Virheellinen syöte. Yritä uudelleen.")


#MIINOJEN MÄÄRÄN KYSYMINEN
def kysy_miinojen_maara(leveys, korkeus):
    maksimi_miinat = leveys * korkeus - 1
    while True:
        miinoja = kysy_positiivinen_luku(
            "Syötä miinojen lukumäärä: "
        )
        if miinoja <= maksimi_miinat:
            tila["miinoja"] = miinoja
            break
        else:
            print(
                f"Miinoja voi olla enintään {maksimi_miinat}. Yritä uudelleen."
            )

#HARAVASTON KÄSITTELIJÄT
def hiiri_kasittelija(x, y, nappi, muokkausnapit):
    pass
def raahaus_kasittelija(x, y, dx, dy, nappi, muokkausnapit):
    pass

def vapautus_kasittelija(x, y, nappi, muokkausnapit):
    pass

def nappain_kasittelija(symboli, muokkausnapit):
    if symboli == NAPIT.ESCAPE:
        haravasto.lopeta()

def paivitys_kasittelija(kulunut_aika):
    pass
def kello(kulunut_aika):
    tila["aika"] += 1

def piirra():
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    for rivi in range(len(tila["nakyva_kentta"])):
        for sarake in range(len(tila["nakyva_kentta"][rivi])):
            haravasto.lisaa_piirrettava_ruutu(
                tila["nakyva_kentta"][rivi][sarake],
                sarake * 40,
                rivi * 40
            )
    haravasto.piirra_tekstia(
        str(tila["aika"]), 
        tila["leveys"] * 40,
        tila["korkeus"] * 40,
        vari=(255,0,0,255)
    ) 
    
    haravasto.piirra_ruudut() 


#UUDEN PELIN KÄYNNISTÄMINEN
def uusi_peli():
    global tila
    tila = {
        "kentta": [],
        "nakyva_kentta": [],
        "leveys": 0,
        "korkeus": 0,
        "miinoja": 0,
        "vuorot": 0,
        "aika": 0,
        "voitto": False,
        "havio": False
    }
    tila["leveys"] = kysy_positiivinen_luku(
        "Syötä kentän leveys (ruutuina): "
    )
    tila["korkeus"] = kysy_positiivinen_luku(
        "Syötä kentän korkeus (ruutuina): "
    )
    kysy_miinojen_maara(
        tila["leveys"], tila["korkeus"]
        )
    
    tila["kentta"] = luo_kentta(
        tila["leveys"], 
        tila["korkeus"]
    )

    tila["nakyva_kentta"] = luo_kentta(
        tila["leveys"], 
        tila["korkeus"]
    )

    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(
        tila["leveys"] * 40, 
        tila["korkeus"] * 40 + 80
        )

    haravasto.aseta_raahaus_kasittelija(hiiri_kasittelija)    
    haravasto.aseta_vapautus_kasittelija(vapautus_kasittelija)    
    haravasto.aseta_nappain_kasittelija(nappain_kasittelija)
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    haravasto.aseta_toistuva_kasittelija(paivitys_kasittelija, 1/60)
    haravasto.aseta_toistuva_kasittelija(kello, 1)
    haravasto.aseta_piirto_kasittelija(piirra)

    #ALOITETAAN PELI
    haravasto.aloita()


#ALKUVALIKKO
def nayta_valikko():
    while True:
        print("\n=== Miinaharava ===")
        print("(U)usi peli")
        print("(T)ilastot")
        print("(L)opeta peli")
        valinta = input("Valitse toiminto: ").strip().lower()
        if valinta == "u":
            uusi_peli()
        elif valinta == "t":
            nayta_tilastot()
        elif valinta == "l":
            print("Lopetetaan peli")
            break
        else:
            print("\n" * 100)  # Tyhjennetään konsoli
            print("Virheellinen valinta. Yritä uudelleen.")


#PÄÄOHJELMA 
if __name__ == "__main__":           
    nayta_valikko()


   
    
    







    


