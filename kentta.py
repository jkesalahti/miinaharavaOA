import random



#KENTÄN LUOMINEN
def luo_kentta(leveys, korkeus):
    kentta = []

    for rivi in range(korkeus):
        kentta.append([])

        for _ in range(leveys):
            kentta[rivi].append(" ")

    return kentta

#KENTÄN MIINOITTAMINEN
def miinoita_kentta(tila):
    vapaat_ruudut = []

    for rivi in range(tila["korkeus"]):
        for sarake in range(tila["leveys"]):
            vapaat_ruudut.append((rivi, sarake))

    for _ in range(tila["miinoja"]):

        i = random.randint(
            0,
        len(vapaat_ruudut) - 1
        )
        rivi, sarake = vapaat_ruudut.pop(i)
        tila["kentta"][rivi][sarake] = "X"

#VIEREISTEN MIINOJEN LASKEMINEN
def laske_viereiset_miinat(tila):
    for rivi in range(tila["korkeus"]):
        for sarake in range(tila["leveys"]):

            if tila["kentta"][rivi][sarake] == "X":
                continue

            miinoja = 0

            for r in range(rivi - 1, rivi + 2):
                for s in range(sarake - 1, sarake + 1):
                    if (0 <= r < tila["korkeus"]
                    and
                    0 <= s < tila["leveys"]
                    ):
                        if tila["kentta"][r][s] == "X":
                            miinoja += 1
            tila["kentta"][rivi][sarake] = str(miinoja)

def taytto(rivi, sarake, tila):
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
    turvallisia = 0
    avattuja = 0

    for rivi in range(tila["korkeus"]):
        for sarake in range(tila["leveys"]):

            if tila["kentta"][rivi][sarake] != "X":
                turvallisia += 1

                if tila["nakyva_kentta"][rivi][sarake] != "X":
                    turvallisia += 1

                    if tila["nakyva_kentta"][rivi][sarake] == tila["kentta"][rivi][sarake]:
                        avattuja += 1
    return avattuja == turvallisia