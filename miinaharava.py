import haravasto
from haravasto import NAPIT
leveys = 800
korkeus = 600
print("Miinaharava")


haravasto.lataa_kuvat("spritet")
haravasto.luo_ikkuna(int(leveys), int(korkeus))

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
    global aika
    haravasto.piirra_tekstia(aika, leveys-leveys/10,korkeus-korkeus/10, vari=(255,0,0,255))
aika = 0    
def kello(kulunut_aika):
    global aika
    aika += 1
   
    
    
def piirra():
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    for i in range(int(leveys / 40)):
        for j in range(int((korkeus-korkeus/5) / 40)):
            haravasto.lisaa_piirrettava_ruutu(" ", i * 40, j * 40)
    haravasto.piirra_tekstia(
        str(aika), 
        leveys - leveys / 10,
        korkeus - korkeus / 10,
        vari=(255,0,0,255)
    ) 
    
    haravasto.piirra_ruudut() 
 
haravasto.aseta_raahaus_kasittelija(hiiri_kasittelija)    
haravasto.aseta_vapautus_kasittelija(vapautus_kasittelija)    
haravasto.aseta_nappain_kasittelija(nappain_kasittelija)
haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
haravasto.aseta_toistuva_kasittelija(paivitys_kasittelija, 1/60)
haravasto.aseta_toistuva_kasittelija(kello, 1)
haravasto.aseta_piirto_kasittelija(piirra)

haravasto.aloita()
