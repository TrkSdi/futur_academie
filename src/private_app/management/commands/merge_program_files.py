import pandas as pd
import numpy as np
import csv

scraped_data = pd.read_csv("./2024-01-17-donnéesparcoursup.csv", delimiter="#")
downloaded_data = pd.read_json("./fr-esr-parcoursup.json")

description_data = pd.read_csv(
    "./2024-01-20-infoparcoursup.csv",
    delimiter="$",
    quoting=3,
    engine="python",
    encoding="UTF-8",
)

# description_data["cod_aff_form"] = description_data["cod_aff_form"].astype(int)
merged_data = pd.merge(scraped_data, downloaded_data, on="cod_aff_form")

all_data = pd.merge(merged_data, description_data, on="cod_aff_form")


selected_columns = [
    "cod_aff_form",
    "lib_for_voe_ins",
    "select_form",
    "g_olocalisation_des_formations",
    "ville_etab",
    "cod_uai",
    "place_dispo",
    "taux_acces",
    "nombre_voeux",
    "pourcentage_boursiers",
    "candidats_hors_secteur",
    "taux_passage_L2",
    "taux_diplome_temps_prevu",
    "description",
    "job_prospects",
    "contrat_etab",
    "g_ea_lib_vx",
]

selected_data = (
    all_data[selected_columns].drop_duplicates(subset=["cod_aff_form"]).copy()
)
selected_data = selected_data.rename(
    columns={
        "lib_for_voe_ins": "program_name",
        "select_form": "selectivity",
        "g_olocalisation_des_formations": "geolocation",
        "ville_etab": "city",
        "place_dispo": "available_places",
        "taux_acces": "percent_admitted",
        "nombre_voeux": "number_applicants",
        "pourcentage_boursiers": "percent_scholarship",
        "candidats_hors_secteur": "out_of_sector_candidates",
        "taux_passage_L2": "L2_continuation_rate",
        "taux_diplome_temps_prevu": "diploma_earned_ontime",
        "contrat_etab": "school_type",
        "g_ea_lib_vx": "school_name",
    }
)


selected_data.to_json("./study_program_data.json", orient="records", lines=True)
print("json created")
print(selected_data.head())
# # stat_columns = [
#     "diploma_earned_ontime",
#     "percent_scholarship",
#     "out_of_sector_candidates",
#     "L2_continuation_rate",
#     "diploma_earned_ontime",
# ]
# # stats = (
#     selected_data[stat_columns]
#     .quantile(q=[0.25, 0.5, 0.75], numeric_only=True)
#     .transpose()
# )
# stats.to_csv("studyprogram_stats.csv", index=True, sep="#")


# merged_data.to_csv("merged_studyprogram_data.csv", index=False, sep="#")
# print(
#     "Data exported to CSV! Includes: scraped statistics, scraped descriptions and location/school info from original CSV."
# )

# diploma_earned_ontime = [47.6,58.7,66.8]
# percent_scholarship = [12.0,17.0,23.0]
# out_of_sector_candidates=[18.0,40.0,50.0]
# diploma_earned_ontime=[47.6,58.7,66.8]
# use these stats to set quartile on object creation

# new_data = []
# data_source = "./2024-01-18-formation-description.csv"
# with open(data_source, "r", encoding="UTF-8", errors="replace") as csvfile:
#     data = csv.reader(csvfile, delimiter="§")
#     total_short = 0
#     for line in data:
#         if len(line) == 2:
#             line.append("None")
#             total_short += 1
#         elif len(line) == 1:
#             line.append("None")
#             line.append("None")
#             total_short += 1
#         new_data.append(line)
# with open("./2024-01-18-infoparcoursup_edited.csv", "w", errors="replace") as csvfile:
#     writer = csv.writer(csvfile, delimiter="#")
#     writer.writerows(new_data)
#
