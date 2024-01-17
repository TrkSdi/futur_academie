import requests
from bs4 import BeautifulSoup
import datetime
import time
import json
import random

date = datetime.date.today()
start = time.time()

#chemin du fichier json où extraire les cod aff form pour les adresses url qui seront stockés dans list_cod_aff_form
file_path = './fr-esr-parcoursup.json'
list_cod_aff_form = []

with open(file_path, "r") as f:
    # Load the data
    data = json.load(f)
    # Loop through programs to add the code to the list:
    for program in data:
            program_code= program["cod_aff_form"]
            list_cod_aff_form.append(program_code)

#short list pour éviter les requêtes trop longues et faire tests
list_cod_aff_form_short = random.sample(list_cod_aff_form, 50)

#variables permettant de voir l'avancer lors des requêtes
num_page = 0
longueur_table = len(list_cod_aff_form)

#ajoute l'entête au csv
entete = "index#place dispo#taux d'acces a la formation#Nombre de voeux formules#Pourcentage de lyceens boursiers#candidats hors secteur#Taux de passage en deuxieme annee#Taux de reussite a 2/4 ans"
with open(f"{date}-donnéesparcoursup.csv", "a") as fichier_extract:
    fichier_extract.write(entete + "\n")

#bouclage sur l'ensemble des adresses url présent dans le fichier parcourssup
for index in list_cod_aff_form:
    #affichage de l'avancement des requêtes
    actual_time = time.time()
    print(f"page n°{num_page} sur {longueur_table} ({round(100*num_page/longueur_table,2)} %) - Temps d'exécution : {int(actual_time - start)} sec")
    
    #différentes variables pour le scrap => index prendra les valeurs cod aff form
    url = f"https://dossier.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_ta_cod={index}"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    
    #deux principales balise à "souper" dans lequelles on fera un find_all pour aller chercher les résultats
    infos = soup.find("div", {"id": "tabpanel-4-panel"})
    encar1 = soup.find("ul", {"class": "list-unstyled"})
    
    #echape l'erreur si jamais les balises ne sont pas présentes
    try:
        span_elements = infos.find_all("span", {"class": "fr-h6 fr-mb-0"})
    except:
        pass
    try :
        div_elements = infos.find_all("div", {"class": "psup-carte-texte-cle fr-mb-1w fr-mr-1w"})
    except :
        pass
    try:
        span_elements_encar = encar1.find_all("span", {"class": "fr-h6 fr-mb-0"})
    except:
        pass
    
    #dico sera les données renvoyées dans le CV à chaque boucle avec le cod aff form en premier
    dico =[index]
    
    for span in span_elements_encar:
        result = span.get_text()
        if result.isdigit() or (result.endswith('%') and result[:-1].isdigit()): #test si c'est un nombre ou si cela finit par un %
            if result.endswith('%'):
                result = result.strip('%') #on enlève le pourcentage pour traitement plus facile à posteriori
            dico.append(result)
        
    for span in span_elements:
        result = span.get_text()
        if result.isdigit() or (result.endswith('%') and result[:-1].isdigit()):
            if result.endswith('%'):
                result = result.strip('%')
            dico.append(result)
    
    #on complète les valeurs non trouvées par des None au besoin (on ne travaille plus sur les <span> mais des <div>)
    if len(dico) < 6:
        for i in range(6 - len(dico)):
            dico.append(None)
            
    for div in div_elements:
        
        div_result = div.get_text().strip()
        
        # on cherche s'il y a "Taux de réussite en 3 ou 4 ans" pour aller chercher la valeur après
        if "Taux de réussite en 3 ou 4 ans" in div_result:
            taux_value = div_result.split("Taux de réussite en 3 ou 4 ans")[1].strip().split(" ")[0]
            if taux_value.endswith('%'):
                taux_value = taux_value.strip('%')
            if taux_value == "Donnée":
                taux_value = None
            dico.append(taux_value)
        
        # idem, c'est soit l'un ou l'autre    
        elif "Taux de réussite en 2 ou 3 ans" in div_result:
            taux_value = div_result.split("Taux de réussite en 2 ou 3 ans")[1].strip().split(" ")[0]
            if taux_value.endswith('%'):
                taux_value = taux_value.strip('%')
            if taux_value == "Donnée":
                taux_value = None
            dico.append(taux_value)
        
        #on cherche s'il y a "Taux :" pour aller chercher la valeur après  
        if "Taux :" in div_result:
            taux_accept = div_result.split("Taux :")[1].strip().split(" ")[0]
            if taux_accept.endswith('%'):
                taux_accept = taux_accept.strip('%')
            if not taux_accept.strip():
                taux_accept = None
            dico.append(taux_accept)
    
    #on complète les valeurs non trouvées par des None au besoin
    if len(dico) < 9:
        for i in range(8 - len(dico)):
            dico.append(None)
    
    #on change la liste en string avec chaque valeur séparée par un #     
    transfert_csv = '#'.join(map(str, dico))
    
    #on écrit dans le fichier csv avant de reboucler
    with open(f"{date}-donnéesparcoursup.csv", "a") as fichier_extract:
        fichier_extract.write(f"{transfert_csv}\n")
    num_page +=1