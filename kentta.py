import random

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
def miinoita_kentta(tila):
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
def laske_miinat_ruudun_ymparilla(rivi, sarake, tila):
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
def laske_viereiset_miinat(tila):
    for rivi in range(tila["korkeus"]):
        for sarake in range(tila["leveys"]):

            if tila["kentta"][rivi][sarake] == "X":
                continue

            miinojen_maara = laske_miinat_ruudun_ymparilla(
                rivi, 
                sarake,
                tila
            )

            tila["kentta"][rivi][sarake] = str(miinojen_maara)

def flood_fill(rivi, sarake, tila):
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
def tarkista_voitto(tila):
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
        return True
    return False