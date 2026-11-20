import random
import haravasto
import ikkunasto
from haravasto import NAPIT
import json
from datetime import datetime
from kentta import (
    luo_kentta,
    miinoita_kentta,
    laske_viereiset_miinat,
    taytto,
    tarkista_voitto
)
from tilastot import (
    tallenna_tilasto,
    nayta_tilastot,
    tyhjenna_tilastot
)

#PELIN TILA
tila = {}


#LASKETAAN LIPPUJEN MÄÄRÄ
def laske_liput():

    liput = 0

    for rivi in tila["nakyva_kentta"]:
        for ruutu in rivi:

            if ruutu == "f":
                liput += 1

    return liput

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
    #PELIN LOPPUMISEN JÄLKEEN POISTUMINEN
    if tila["havio"] or tila["voitto"]:
        if nappi == haravasto.HIIRI_VASEN:
            haravasto.lopeta()
        return
    #KENTTÄ JAETAAN RUUTUIHIN
    sarake = int(x // 40)
    rivi = tila["korkeus"] - 1 - int(y // 40)
    if(
        rivi < 0
        or rivi >= tila["korkeus"]
        or sarake < 0
        or sarake >= tila["leveys"]
    ):
        return
    #LIPUN LISÄYS
    if nappi == haravasto.HIIRI_OIKEA:
        if tila["nakyva_kentta"][rivi][sarake] == " ":
            if laske_liput() < tila["miinoja"]:
                tila["nakyva_kentta"][rivi][sarake] = "f"
        elif tila["nakyva_kentta"][rivi][sarake] == "f":
            tila["nakyva_kentta"][rivi][sarake] = " "
        return 
    #VARMISTETAAN ETTEI LIPUTETTUA RUUTUA AVATA
    if tila["nakyva_kentta"][rivi][sarake] == "f":
        return
    tila ["vuorot"] += 1
    #RUUDUN AVAAMINEN
    if nappi == haravasto.HIIRI_VASEN:
        if tila["kentta"][rivi][sarake] == "0":
            taytto(rivi, sarake, tila)
        else:
            tila["nakyva_kentta"][rivi][sarake] =(
                tila["kentta"][rivi][sarake]
            )

    #MIINAN AVAAMINEN
    if tila["kentta"][rivi][sarake] == "X":
        tila["havio"] = True

        tallenna_tilasto("häviö", tila)
        #PALJASTETAAN LOPUT MIINAT
        for r in range(tila["korkeus"]):
            for s in range(tila["leveys"]):
                if tila["kentta"][r][s] == "X":
                    tila["nakyva_kentta"][r][s] = "X"

        print("Hävisit pelin!")
    else:
        if tarkista_voitto(tila):
            tila["voitto"] = True
            tallenna_tilasto("voitto", tila)
            print("Voitit pelin!")

def raahaus_kasittelija(x, y, dx, dy, nappi, muokkausnapit):
    pass

def vapautus_kasittelija(x, y, nappi, muokkausnapit):
    pass

def nappain_kasittelija(symboli, muokkausnapit):
    if symboli == NAPIT.ESCAPE:
        haravasto.lopeta()

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

    #KELLON PIIRTÄMINEN
    haravasto.piirra_tekstia(
        str(tila["aika"]), 
        tila["leveys"] * 20 + tila["leveys"] * 10,
        tila["korkeus"] * 40 + 20,
        vari=(255,0,0,255)
    )
    #LIPPUMITTARIN PIIRTÄMINEN
    haravasto.piirra_tekstia(
        str(tila["miinoja"] - laske_liput()), 
        tila["leveys"] * 20 - tila["leveys"] * 10,
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

    def aloita_peli():
        tila["leveys"] = int(ikkunasto.lue_kentan_sisalto(
                leveyskentta
            ))
        tila["korkeus"] = int(ikkunasto.lue_kentan_sisalto(
                korkeuskentta
            ))
        tila["miinoja"] = int(ikkunasto.lue_kentan_sisalto(
                miinakentta
                ))
            
        tila["kentta"] = luo_kentta(
            tila["leveys"], 
            tila["korkeus"]
            )
        
        tila["nakyva_kentta"] = luo_kentta(
            tila["leveys"], 
            tila["korkeus"]
            )
            
        #MIINOITETAAN KENTTÄ
        miinoita_kentta(tila)
        laske_viereiset_miinat(tila)
        haravasto.luo_ikkuna(
                    tila["leveys"] * 40,
                    tila["korkeus"] * 40 + 80
                    )
        

        haravasto.aseta_raahaus_kasittelija(raahaus_kasittelija)    
        haravasto.aseta_vapautus_kasittelija(vapautus_kasittelija)                
        haravasto.aseta_nappain_kasittelija(nappain_kasittelija)            
        haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
        haravasto.aseta_toistuva_kasittelija(kello, 1)
        haravasto.aseta_piirto_kasittelija(piirra)
        haravasto.lataa_kuvat("spritet")
        
        
        haravasto.aloita()
        
            

    #LUODAAN IKKUNA KENTÄN KOON JA MIINOJEN KYSYMISEEN
    kyselyikkuna = ikkunasto.luo_ali_ikkuna("Uusi peli")
    kyselykehys = ikkunasto.luo_kehys(kyselyikkuna)

    ikkunasto.luo_tekstirivi(kyselykehys, "Anna kentän leveys")
    leveyskentta = ikkunasto.luo_tekstikentta(kyselykehys)
    ikkunasto.luo_tekstirivi(kyselykehys, "Anna kentän korkeus")
    korkeuskentta = ikkunasto.luo_tekstikentta(kyselykehys)
    ikkunasto.luo_tekstirivi(kyselykehys, "Anna miinojen määrä")
    miinakentta = ikkunasto.luo_tekstikentta(kyselykehys)
    ikkunasto.luo_vaakaerotin(kyselykehys, 5)
    pelin_aloitus = ikkunasto.luo_nappi(kyselykehys,"Aloita peli", aloita_peli)

    

    
    


#LUODAAN ALKUVALIKON IKKUNA
def luo_ikkuna():
    ikkuna = ikkunasto.luo_ikkuna("Miinaharava")
    nappikehys = ikkunasto.luo_kehys(ikkuna)
    ikkunasto.luo_vaakaerotin(nappikehys, 5)
    uusi_peli_nappi = ikkunasto.luo_nappi(
        nappikehys,"Uusi peli", uusi_peli
        )
    ikkunasto.luo_vaakaerotin(nappikehys, 2)
    tilastot_nappi = ikkunasto.luo_nappi(
        nappikehys, "Tilastot", nayta_tilastot
        )
    ikkunasto.luo_vaakaerotin(nappikehys, 2)
    tyhjenna_nappi = ikkunasto.luo_nappi(
        nappikehys, "Tyhjennä tilastot", tyhjenna_tilastot
        )
    ikkunasto.luo_vaakaerotin(nappikehys, 2)
    lopeta_nappi = ikkunasto.luo_nappi(
        nappikehys, "Lopeta peli", ikkunasto.lopeta
        )
    ikkunasto.luo_vaakaerotin(nappikehys, 5)
    ikkunasto.kaynnista()

#ALKUVALIKKO
def nayta_valikko():
    luo_ikkuna()
    
    
    """
    while True:
        print("\n=== Miinaharava ===")
        print("(U)usi peli")
        print("(T)ilastot")
        print("(P)oista tilastot")
        print("(L)opeta peli")
        valinta = input("Valitse toiminto: ").strip().lower()
        if valinta == "u":
            uusi_peli()
        elif valinta == "t":
            nayta_tilastot()
        elif valinta == "l":
            print("Lopetetaan peli")
            break
        elif valinta == "p":
            tyhjenna_tilastot()
        else:
            print("\n" * 100)  # Tyhjennetään konsoli
            print("Virheellinen valinta. Yritä uudelleen.")
    """

#PÄÄOHJELMA 
if __name__ == "__main__":           
    nayta_valikko()


   
    
    







    


