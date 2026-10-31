import streamlit as st
from datetime import datetime

# تنظیمات صفحه
st.set_page_config(page_title="سیستم ثبت ساعات کاری", page_icon="⏱️", layout="centered")

st.title("⏱️ سیستم ثبت ساعات کاری پرسنل")

# --- بخش ورود / انتخاب نام کاربر ---
st.sidebar.header("🔐 ورود به سیستم")
username = st.sidebar.text_input("نام و نام خانوادگی خود را وارد کنید:")

if not username:
    st.warning("⚠️ لطفاً برای شروع، نام خود را از منوی سمت راست وارد کنید.")
    st.stop()

st.success( خوش آمدید، **{username}** عزیز! شما اکنون می‌توانید ساعات کاری خود را ثبت کنید.")

# --- فرم ثبت ساعات کاری ---
st.subheader("📝 ثبت ساعت جدید")

with st.form("stunden_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("تاریخ", datetime.today())
    with col2:
        hours = st.number_input("تعداد ساعت کاری", min_value=1.0, max_value=16.0, value=8.0, step=0.5)
    
    description = st.text_area("توضیحات کار (مثلاً: کابل‌کشی، نصب پریز و کلید)")
    
    submitted = st.form_submit_button("ثبت ساعت")
    
    if submitted:
        # اینجا می‌توانید اطلاعات را ذخیره کنید (مثلاً در فایل اکسل یا لیست)
        st.success(f"✅ ساعت کاری با موفقیت برای **{username}** ثبت شد!")
        # نمایش اطلاعات ثبت شده به عنوان نمونه
        st.write(f"- تاریخ: {date}")
        st.write(f"- ساعت: {hours}")
        st.write(f"- توضیحات: {description}")
