import streamlit as st
from datetime import datetime
import os
import pandas as pd

EXCEL_FILE = "stunden_daten.xlsx"

# تنظیمات صفحه
st.set_page_config(page_title="Stundenübersicht", page_icon="⏱️", layout="centered")

st.title("⏱️ Zeiterfassung für Mitarbeiter")

# --- بخش ورود / انتخاب نام کاربر ---
st.sidebar.header("🔐 Anmeldung")
username = st.sidebar.text_input("Vor- und Nachname eingeben:")

if not username:
    st.warning("⚠️ Bitte geben Sie Ihren Namen in der Seitenleiste ein, um fortzufahren.")
    st.stop()

st.success(f"Willkommen, **{username}**! Sie können jetzt Ihre Arbeitszeiten erfassen.")

# --- فرم ثبت ساعات کاری ---
st.subheader("📝 Neue Arbeitsstunden erfassen")

with st.form("stunden_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Datum", datetime.today())
    with col2:
        hours = st.number_input("Arbeitsstunden", min_value=1.0, max_value=16.0, value=8.0, step=0.5)
    
    description = st.text_area("Beschreibung (z.B. Kabelverlegung, Steckdosen montieren)")
    
    submitted = st.form_submit_button("Stunden speichern")
    
    if submitted:
        new_data = pd.DataFrame([{
            "Mitarbeiter": username,
            "Datum": str(date),
            "Stunden": hours,
            "Beschreibung": description,
            "Eingetragen am": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        
        # ذخیره در فایل اکسل
        if os.path.exists(EXCEL_FILE):
            df_existing = pd.read_excel(EXCEL_FILE)
            df_final = pd.concat([df_existing, new_data], ignore_index=True)
        else:
            df_final = new_data
            
        df_final.to_excel(EXCEL_FILE, index=false)
        st.success(f"✅ Arbeitsstunden für **{username}** erfolgreich gespeichert!")

# --- نمایش گزارش‌ها ---
st.divider()
st.subheader("📊 Bisherige Erfassungen")

if os.path.exists(EXCEL_FILE):
    df_all = pd.read_excel(EXCEL_FILE)
    st.dataframe(df_all, use_container_width=True)
    
    # دکمه دانلود فایل اکسل
    with open(EXCEL_FILE, "rb") as f:
        st.download_button(
            label="📥 Excel-Liste herunterladen",
            data=f,
            file_name="stunden_uebersicht.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Noch keine Einträge vorhanden.")
