import requests
from bs4 import BeautifulSoup
import datetime
import time
import json
import random

date = datetime.date.today()
start = time.time()

# chemin du fichier json où extraire les cod aff form pour les adresses url qui seront stockés dans list_cod_aff_form
file_path = "./fr-esr-parcoursup.json"
list_cod_aff_form = []

with open(file_path, "r") as f:
    # Load the data
    data = json.load(f)
    # Loop through programs to add the code to the list:
    for program in data:
        program_code = program["cod_aff_form"]
        list_cod_aff_form.append(program_code)

# short list pour éviter les requêtes trop longues et faire tests
list_cod_aff_form_short = random.sample(list_cod_aff_form, 10)

# variables permettant de voir l'avancer lors des requêtes
num_page = 0
longueur_table = len(list_cod_aff_form_short)

# ajoute l'entête au csv
entete = "index§info"
with open(f"{date}-infoparcoursup.csv", "a") as fichier_extract:
    fichier_extract.write(entete + "\n")


# bouclage sur l'ensemble des adresses url présent dans le fichier parcourssup
for index, program in enumerate(list_cod_aff_form_short):
    # affichage de l'avancement des requêtes
    actual_time = time.time()
    print(
        f"page n°{index} sur {longueur_table} ({round(100*num_page/longueur_table,2)} %) - Temps d'exécution : {int(actual_time - start)} sec"
    )

    # différentes variables pour le scrap => index prendra les valeurs cod aff form
    url = f"https://dossier.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_ta_cod={program}"
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    except:
        list_cod_aff_form.append(program)

    soup = BeautifulSoup(html.content, "html.parser")

    # deux principales balise à "souper" dans lequelles on fera un find_all pour aller chercher les résultats
    infos_presentation = soup.find(
        "div", {"class": "fr-col-sm-12 fr-col-lg-6 fr-pt-3w"}
    )

    # echape l'erreur si jamais les balises ne sont pas présentes
    try:
        div_elements = infos_presentation.find_all(
            "div", {"class": "word-break-break-word"}
        )
    except:
        div_elements = []

    # dico sera les données renvoyées dans le CV à chaque boucle avec le cod aff form en premier
    dico = [program]

    for div in div_elements:
        result = div.get_text()
        dico.append(result)

    # on change la liste en string avec chaque valeur séparée par un #
    transfert_csv = "§".join(map(str, dico))

    # on écrit dans le fichier csv avant de reboucler
    with open(f"{date}-infoparcoursup.csv", "a") as fichier_extract:
        fichier_extract.write(f"{transfert_csv}\n")
    num_page += 1
