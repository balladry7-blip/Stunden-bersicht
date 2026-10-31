import streamlit as st
import os
import json
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import io

st.set_page_config(page_title="Stundenübersicht", page_icon="⏱️", layout="centered")

st.title("⏱️ Stundenübersicht")
st.write("Erfassung der Arbeitsstunden - Abbas Jahmedolati")

# دریافت تاریخ
today = datetime.now()
date_input = st.date_input("Datum (TT.MM.JJJJ)", value=today)
datum_str = date_input.strftime("%d.%m.%Y")
jahr_str = str(date_input.year)
monat_int = date_input.month

# انتخاب پروژه
project_type = st.selectbox("Text / Projekt:", ["Bitte wählen", "Erftland", "Auftrag"])

detail_val = ""
if project_type == "Erftland":
    detail_val = st.text_input("Adresse eingeben:")
elif project_type == "Auftrag":
    detail_val = st.text_input("Auftragsnummer eingeben:")

# ساعات استراحت و کار
pause_input = st.text_input("Pause (z.B. 0,0):", value="0,0")
hours_input = st.text_input("Geleistete Std (z.B. 00:00):", value="00:00")

def format_hours_four_digits(val_str, is_hours_field=False):
    if not val_str or val_str.strip() == "":
        return "00:00" if is_hours_field else "0,0"
    val_str = val_str.strip().replace(".", ",")
    if "," in val_str:
        parts = val_str.split(",")
        integer_part = parts[0] if parts[0] else "0"
        decimal_part = parts[1] if len(parts) > 1 else ""
        if len(decimal_part) == 1:
            decimal_part += "0"
        elif len(decimal_part) == 0:
            decimal_part = "00"
        else:
            decimal_part = decimal_part[:2]
        if is_hours_field:
            if len(integer_part) == 1:
                integer_part = "0" + integer_part
            return f"{integer_part}:{decimal_part}"
        return f"{integer_part},{decimal_part}"
    else:
        if is_hours_field:
            if len(val_str) == 1:
                val_str = "0" + val_str
            return f"{val_str}:00"
        return f"{val_str},0"

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_filenames(jahr, monat):
    base_name = f"stunden_{int(monat):02d}_{int(jahr)}"
    excel_path = os.path.join(DATA_DIR, f"{base_name}.xlsx")
    json_path = os.path.join(DATA_DIR, f"{base_name}.json")
    return excel_path, json_path

def generate_excel_bytes(jahr, monat):
    excel_path, json_path = get_filenames(jahr, monat)
    records_dict = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data_list = json.load(f)
                for rec in data_list:
                    d_str = rec.get("datum", "")
                    if d_str:
                        day_num = int(d_str.split(".")[0])
                        records_dict[day_num] = rec
        except:
            records_dict = {}

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stundenübersicht"
    
    font_title = Font(name="Calibri", size=14, bold=True)
    font_header = Font(name="Calibri", size=11, bold=True)
    thin_border = Border(left=Side(style='thin', color='000000'), right=Side(style='thin', color='000000'), top=Side(style='thin', color='000000'), bottom=Side(style='thin', color='000000'))
    
    ws['A1'] = "Stundenübersicht : Abbas Jahmedolati"
    ws['A1'].font = font_title
    ws.row_dimensions[1].height = 30
    
    ws['A3'] = "Datum"
    ws['B3'] = "Jahr"
    ws['C3'] = "Text"
    ws['E3'] = "Pause"
    ws['F3'] = "geleistete Std"
    
    for col in ['A', 'B', 'C', 'E', 'F']:
        cell = ws[f'{col}3']
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    ws['A4'] = "Datum"
    ws['B4'] = "Jahr"
    ws['C4'] = "Projekt"
    ws['D4'] = "Monteur"
    ws['E4'] = ""
    ws['F4'] = "Pause"
    ws['G4'] = "0,00"
    
    for col_idx, col_letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 1):
        cell = ws.cell(row=4, column=col_idx)
        cell.font = font_header
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for day_idx in range(1, 32):
        r = 4 + day_idx
        ws.row_dimensions[r].height = 18
        if day_idx in records_dict:
            rec = records_dict[day_idx]
            ws.cell(row=r, column=1, value=str(rec.get("datum", "")))
            ws.cell(row=r, column=2, value=str(rec.get("jahr", str(jahr))))
            ws.cell(row=r, column=3, value=str(rec.get("text", "")))
            ws.cell(row=r, column=6, value=str(rec.get("pause", "0,0")))
            ws.cell(row=r, column=7, value=str(rec.get("hours", "00:00")))
        else:
            ws.cell(row=r, column=1, value=f"{day_idx:02d}.{int(monat):02d}.{jahr}")
            ws.cell(row=r, column=2, value=str(jahr))
            ws.cell(row=r, column=3, value="")
            ws.cell(row=r, column=6, value="0,0")
            ws.cell(row=r, column=7, value="00:00")
        
        for col_idx, col_letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 1):
            cell = ws.cell(row=r, column=col_idx)
            cell.border = thin_border
            if col_letter in ['A', 'B', 'F']:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_letter == 'G':
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    row_flex = 36
    row_summe = 37
    row_end = 39
    ws[f'C{row_flex}'] = "Flex Vormonat"
    ws[f'A{row_summe}'] = "Summe :"
    ws[f'A{row_end}'] = "Endbestand :"
    
    for r in [row_flex, row_summe, row_end]:
        ws.row_dimensions[r].height = 20
        for col_letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            cell = ws[f'{col_letter}{r}']
            cell.border = thin_border
            if r == row_summe and col_letter == 'G':
                cell.value = "0,00"
            if r == row_end and col_letter == 'G':
                cell.value = "-174,00"

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

# دکمه ذخیره
if st.button("Eintrag speichern", type="primary"):
    if project_type == "Bitte wählen":
        st.error("Bitte wählen Sie Erftland oder Auftrag aus!")
    elif not detail_val:
        msg = "Bitte geben Sie die Adresse ein!" if project_type == "Erftland" else "Bitte geben Sie die Auftragsnummer ein!"
        st.error(msg)
    else:
        text_result = f"{project_type}: {detail_val}"
        _, json_path = get_filenames(jahr_str, monat_int)
        
        records = []
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except:
                records = []

        updated = False
        for rec in records:
            if rec.get("datum") == datum_str:
                rec["jahr"] = jahr_str
                rec["text"] = text_result
                rec["pause"] = format_hours_four_digits(pause_input, False)
                rec["hours"] = format_hours_four_digits(hours_input, True)
                updated = True
                break

        if not updated:
            new_record = {
                "datum": datum_str,
                "jahr": jahr_str,
                "text": text_result,
                "pause": format_hours_four_digits(pause_input, False),
                "hours": format_hours_four_digits(hours_input, True)
            }
            records.append(new_record)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=4)

        st.success("Der Eintrag wurde erfolgreich gespeichert!")

st.divider()

# بخش دانلود اکسل
st.subheader("Excel-Datei herunterladen")
sel_monat = st.selectbox("Monat wählen:", list(range(1, 13)), index=datetime.now().month - 1)
sel_jahr = st.selectbox("Jahr wählen:", [2024, 2025, 2026, 2027], index=2)

excel_data = generate_excel_bytes(sel_jahr, sel_monat)
st.download_button(
    label="📥 Excel-Datei herunterladen",
    data=excel_data,
    file_name=f"stunden_{sel_monat:02d}_{sel_jahr}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)