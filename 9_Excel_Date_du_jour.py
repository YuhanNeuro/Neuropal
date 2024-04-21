import openpyxl
from datetime import datetime
import locale

# Définition de la localité pour avoir la date en français
locale.setlocale(locale.LC_TIME, 'fr_FR')

# Chemin du fichier Excel
excel_path = r"C:\Users\x\Desktop\NeuroPal_Global\Base_de_donnees\4_Donnees_interface\0_calendar\Diapo_reposit_vierge.xlsx"

# Charger le workbook et la feuille active
workbook = openpyxl.load_workbook(excel_path)
sheet = workbook.active

# Obtenir la date du jour dans le format spécifié
today_date = datetime.now().strftime("%A %d %B %Y")

# Écrire la date dans la cellule D5
sheet['D5'] = today_date

# Sauvegarder le fichier
workbook.save(excel_path)

print("La date a été écrite avec succès dans le fichier Excel.")
