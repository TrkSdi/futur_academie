import pandas as pd
import numpy as np
import csv

# Original data with most statistics
# scraped_data = pd.read_csv("./2024-01-17-donnéesparcoursup.csv", delimiter="#")
# # Downloaded CSV with info such as GPS location
# downloaded_data = pd.read_json("./fr-esr-parcoursup.json")
# # Scraping results including program description and job prospects description
# description_data = pd.read_csv(
#     "./2024-01-20-infoparcoursup.csv",
#     delimiter="$",
#     quoting=3,
#     engine="python",
#     encoding="UTF-8",
# )

# # Combine the first two documents
# merged_data = pd.merge(scraped_data, downloaded_data, on="cod_aff_form")

# # Add the third document
# all_data = pd.merge(merged_data, description_data, on="cod_aff_form")

# # Select only the necessary columns
# selected_columns = [
#     "cod_aff_form",
#     "lib_for_voe_ins",
#     "select_form",
#     "g_olocalisation_des_formations",
#     "ville_etab",
#     "cod_uai",
#     "place_dispo",
#     "taux_acces",
#     "nombre_voeux",
#     "pourcentage_boursiers",
#     "candidats_hors_secteur",
#     "taux_passage_L2",
#     "taux_diplome_temps_prevu",
#     "description",
#     "job_prospects",
#     "contrat_etab",
#     "g_ea_lib_vx",
# ]
# selected_data = (
#     all_data[selected_columns].drop_duplicates(subset=["cod_aff_form"]).copy()
# )

# # Rename columns to clearer names
# selected_data = selected_data.rename(
#     columns={
#         "lib_for_voe_ins": "program_name",
#         "select_form": "selectivity",
#         "g_olocalisation_des_formations": "geolocation",
#         "ville_etab": "city",
#         "place_dispo": "available_places",
#         "taux_acces": "percent_admitted",
#         "nombre_voeux": "number_applicants",
#         "pourcentage_boursiers": "percent_scholarship",
#         "candidats_hors_secteur": "out_of_sector_candidates",
#         "taux_passage_L2": "L2_continuation_rate",
#         "taux_diplome_temps_prevu": "diploma_earned_ontime",
#         "contrat_etab": "school_type",
#         "g_ea_lib_vx": "school_name",
#     }
# )

# selected_data["L2_continuation_rate"] = (
#     selected_data["L2_continuation_rate"]
#     .str.replace(",", ".")
#     .str.replace("ns", "NaN")
#     .astype("float")
# )

# # Write the result to JSON, note that we will need to manually convert it to a list after export
# selected_data.to_json("./study_program_data.json", orient="records", lines=True)
# print("json created")

selected_data = pd.read_json("./study_program_data.json", encoding="UTF-8")

stat_columns = [
    "percent_admitted",
    "percent_scholarship",
    "out_of_sector_candidates",
    "L2_continuation_rate",
    "diploma_earned_ontime",
]
# selected_data[stat_columns].replace(to_replace=["None"], value=np.nan, inplace=True)
stats = selected_data[stat_columns].quantile(q=[0.25, 0.5, 0.75]).transpose()

# print(selected_data["L2_continuation_rate"].dtypes)
print(stats)
stats.to_csv("studyprogram_stats.csv", index=True, sep="#")
print("CSV created")

# # diploma_earned_ontime = [47.6,58.7,66.8]
# # percent_scholarship = [12.0,17.0,23.0]
# # out_of_sector_candidates=[18.0,40.0,50.0]
# # diploma_earned_ontime=[47.6,58.7,66.8]
# # use these stats to set quartile on object creation
