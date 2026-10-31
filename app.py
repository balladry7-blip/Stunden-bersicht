import streamlit as st
from datetime import datetime

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
        st.success(f"✅ Arbeitsstunden für **{username}** erfolgreich gespeichert!")
        st.write(f"- Datum: {date}")
        st.write(f"- Stunden: {hours}")
        st.write(f"- Beschreibung: {description}")
