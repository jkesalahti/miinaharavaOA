import random
import haravasto
from haravasto import NAPIT
import json
from datetime import datetime

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
    vapaat_ruudut = []

    for rivi in range(tila["korkeus"]):
        for sarake in range(tila["leveys"]):
            vapaat_ruudut.append((rivi, sarake))

    for _ in range(tila["miinoja"]):

        indeksi = random.randint(
            0,
        len(vapaat_ruudut) - 1
        )
        rivi, sarake = vapaat_ruudut.pop(indeksi)
        tila["kentta"][rivi][sarake] = "X"

#MIINOJEN LASKEMINEN RUUDUN YMPÄRILLÄ
def laske_miinat_ruudun_ymparilla(rivi, sarake):
    miinoja = 0

    for r in range (rivi -1, rivi + 2):
        for s in range(sarake -1, sarake +2):

            if(
                0 <= r <= tila["korkeus"] - 1
                and
                0 <= s <= tila["leveys"] - 1
            ):
                if r == rivi and s == sarake:
                    continue

                if tila["kentta"][r][s] == "X":
                    miinoja += 1

    return miinoja

#VIEREISTEN MIINOJEN LASKEMINEN
def laske_viereiset_miinat():
    for rivi in range(tila["korkeus"]):
        for sarake in range(tila["leveys"]):

            if tila["kentta"][rivi][sarake] == "X":
                continue

            miinojen_maara = laske_miinat_ruudun_ymparilla(
                rivi, 
                sarake
            )

            tila["kentta"][rivi][sarake] = str(miinojen_maara)

def flood_fill(rivi, sarake):
    kasiteltavat = [(rivi, sarake)]

    while kasiteltavat:
        rivi, sarake = kasiteltavat.pop()

        tila["nakyva_kentta"][rivi][sarake] = (
            tila["kentta"][rivi][sarake]
        )

        if tila["kentta"][rivi][sarake] != "0":
            continue

        for r in range(rivi - 1, rivi + 2):
            for s in range(sarake - 1, sarake + 2):

                if (
                    0 <= r < tila["korkeus"]
                    and
                    0 <= s < tila["leveys"]
                ):
                    if (
                        tila["nakyva_kentta"][r][s]
                        ==
                        tila["kentta"][r][s]
                    ):
                        continue
                    kasiteltavat.append((r, s))          

#TARKISTETAAN VOITTO
def tarkista_voitto():
    avattuja = 0

    for rivi in range(tila["korkeus"]):
        for sarake in range(tila["leveys"]):

            if (
                tila["kentta"][rivi][sarake] != "X"
                and
                tila["nakyva_kentta"][rivi][sarake]
                ==
                tila["kentta"][rivi][sarake]
            ):
                avattuja += 1


    turvallisia =(
            tila["leveys"]
            * tila["korkeus"]
            - tila["miinoja"]
        )

    if avattuja == turvallisia:
        tila["voitto"] = True
        tallenna_tilasto("voitto")
        print("Voitit pelin!")

#TILASTOJEN NÄYTTÄMINEN
def nayta_tilastot():
    try:
        with open(
            "tilastot.json",
            "r",
            encoding="utf-8"
        ) as tiedosto:
            tilastot = json.load(tiedosto)
    except FileNotFoundError:
        print("Tilastoja ei ole vielä.")
        return

    print("\n=== TILASTOT ===\n")
    for peli in tilastot:
        print(
            f"{peli["aika"]} | "
            f"{peli["tulos"]} | "
            f"{peli["leveys"]}x{peli["korkeus"]} | "
            f"miinoja {peli["miinoja"]} | "
            f"vuorot {peli["vuorot"]} | "
            f"kesto {peli["kesto"]} s"
        )

#TILASTOJEN TALLENTAMINEN
def tallenna_tilasto(tulos):
    uusi_tilasto = {
        "aika": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "kesto": tila["aika"],
        "vuorot": tila["vuorot"],
        "tulos": tulos,
        "leveys": tila["leveys"],
        "korkeus": tila["korkeus"],
        "miinoja": tila["miinoja"]
    }

    try:
        with open("tilastot.json", "r", encoding="utf-8") as tiedosto:
            tilastot = json.load(tiedosto)
    except (FileNotFoundError, json.JSONDecodeError):
        tilastot = []

    tilastot.append(uusi_tilasto)

    with open("tilastot.json", "w", encoding="utf-8") as tiedosto:
        json.dump(
            tilastot,
            tiedosto,
            indent=4,
            ensure_ascii=False
        )

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

    if tila["havio"] or tila["voitto"]:
        return

    sarake = int(x // 40)
    rivi = tila["korkeus"]- 1 - int(y // 40)
    if(
        rivi < 0
        or rivi >= tila["korkeus"]
        or sarake < 0
        or sarake >= tila["leveys"]
    ):
        return

    tila ["vuorot"] += 1

    if tila["kentta"][rivi][sarake] == "0":
        flood_fill(rivi, sarake)
    else:
        tila["nakyva_kentta"][rivi][sarake] =(
            tila["kentta"][rivi][sarake]
        )

    if tila["kentta"][rivi][sarake] == "X":
        tila["havio"] = True

        tallenna_tilasto("häviö")

        for r in range(tila["korkeus"]):
            for s in range(tila["leveys"]):
                if tila["kentta"][r][s] == "X":
                    tila["nakyva_kentta"][r][s] = "X"

        print("Hävisit pelin!")
    else:
        tarkista_voitto()
    
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
    if not tila["havio"] and not tila["voitto"]:
        tila["aika"] += 1

#RUUDUN PIIRTÄMINEN
def piirra():
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()

    for rivi in range(len(tila["nakyva_kentta"])):
        for sarake in range(len(tila["nakyva_kentta"][rivi])):
            haravasto.lisaa_piirrettava_ruutu(
                tila["nakyva_kentta"][rivi][sarake],
                sarake * 40,
                (tila["korkeus"] - 1 - rivi) * 40
            )
    haravasto.piirra_tekstia(
        str(tila["aika"]), 
        tila["leveys"] * 40 - 80,
        tila["korkeus"] * 40 + 20,
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
    
    #MIINOITETAAN KENTTÄ
    miinoita_kentta()
    laske_viereiset_miinat()

    haravasto.lataa_kuvat("spritet")
    '''
    ikkunan_leveys = max(
        tila["leveys"] * 40,
        300
    )
    
    ikkunan_korkeus = max(
        tila["korkeus"] * 40 + 80,
        250
    )     
    '''
    haravasto.luo_ikkuna(
        tila["leveys"] * 40,
        tila["korkeus"] * 40 + 80
        )

    haravasto.aseta_raahaus_kasittelija(raahaus_kasittelija)    
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


   
    
    







    


