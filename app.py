import streamlit as st
import os
import json
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
import io

st.set_page_config(page_title="Stundenübersicht", page_icon="⏱️", layout="centered")

st.title("⏱️ Stundenübersicht")

# --- بخش ورود / نام پرسنل در منوی کناری ---
st.sidebar.header("🔐 Anmeldung")
username = st.sidebar.text_input("Name des Mitarbeiters:")

if not username:
    st.warning("⚠️ Bitte geben Sie Ihren Namen in der Seitenleiste ein, um fortzufahren.")
    st.stop()

st.success(f"Willkommen, **{username}**! Sie können jetzt Ihre Arbeitszeiten erfassen.")

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
