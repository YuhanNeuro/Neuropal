import datetime
import calendar
import openpyxl
from openpyxl import load_workbook

def get_month_weeks(year, month):
    # Calcule le premier et le dernier jour de chaque semaine du mois
    weeks = []
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        first_day = week[0] if week[0] != 0 else week[1]
        last_day = week[-1] if week[-1] != 0 else week[-2]
        weeks.append((first_day, last_day))
    return weeks

def main():
    # Chemin du fichier Excel
    filepath = r"C:\Users\x\Desktop\NeuroPal_Global\Base_de_donnees\4_Donnees_interface\0_calendar\Diapo_reposit_vierge.xlsx"
    
    # Charger le fichier Excel
    workbook = load_workbook(filepath)
    sheet = workbook.active
    
    # Obtenir l'année et le mois actuel
    today = datetime.date.today()
    year, month = today.year, today.month

    # Obtenir les semaines du mois
    weeks = get_month_weeks(year, month)

    # Définir les cellules où écrire
    cells = ["D29", "D31", "D33", "D35"]
    
    # Dictionnaire pour les noms de mois en français
    month_names = {
        1: "janvier", 2: "février", 3: "mars", 4: "avril",
        5: "mai", 6: "juin", 7: "juillet", 8: "août",
        9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
    }

    # Écrire dans les cellules
    for cell, (first_day, last_day) in zip(cells, weeks):
        first_date = datetime.date(year, month, first_day)
        last_date = datetime.date(year, month, last_day)
        formatted_date = f"Du {first_date.day} au {last_date.day} {month_names[month]}, {year}"
        sheet[cell] = formatted_date

    # Sauvegarder le fichier
    workbook.save(filepath)

if __name__ == "__main__":
    main()
