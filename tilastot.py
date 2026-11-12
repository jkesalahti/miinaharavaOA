import json
from datetime import datetime

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
            f"{peli['aika']} | "
            f"{peli['tulos']} | "
            f"{peli['leveys']}x{peli['korkeus']} | "
            f"miinoja {peli['miinoja']} | "
            f"vuorot {peli['vuorot']} | "
            f"kesto {peli['kesto']} s"
        )

#TILASTOJEN TALLENTAMINEN
def tallenna_tilasto(tulos, tila):
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

#TILASTOJEN TYHJENTÄMINEN
def tyhjenna_tilastot():
    with open(
        "tilastot.json",
        "w",
        encoding="utf-8"
    ) as tiedosto:
        json.dump([], tiedosto)