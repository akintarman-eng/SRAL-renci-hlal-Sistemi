{\rtf1\ansi\ansicpg1254\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
from datetime import datetime\
import os\
\
# Sayfa yap\uc0\u305 land\u305 rmas\u305 \
st.set_page_config(page_title="Okul Disiplin Takip", layout="centered")\
\
# Verileri y\'fckle\
@st.cache_data\
def load_data():\
    return pd.read_excel("ogrenciler.xlsx")\
\
df = load_data()\
\
# Kay\uc0\u305 tlar\u305 n tutulaca\u287 \u305  dosya\
log_file = "ihlal_kayitlari.csv"\
\
# Aray\'fcz\
st.title("\uc0\u55357 \u57057 \u65039  Okul Kontrol Sistemi")\
\
# 1. B\'f6l\'fcm: \'d6\uc0\u287 retmen Bilgileri\
with st.expander("\uc0\u55357 \u56424 \u8205 \u55356 \u57323  \'d6\u287 retmen ve Ders Bilgisi", expanded=True):\
    col1, col2 = st.columns(2)\
    with col1:\
        ogretmen = st.text_input("Ad\uc0\u305 n\u305 z Soyad\u305 n\u305 z")\
    with col2:\
        ders_saati = st.selectbox("Ders Saati", [1,2,3,4,5,6,7,8])\
\
# 2. B\'f6l\'fcm: \'d6\uc0\u287 renci ve \u304 hlal Giri\u351 i\
st.subheader("\uc0\u55357 \u56541  \u304 hlal Giri\u351 i")\
ogr_no = st.number_input("\'d6\uc0\u287 renci No Girin", min_value=1, step=1, value=None)\
\
if ogr_no:\
    ogrenci = df[df['\'d6\uc0\u287 renci No'] == ogr_no]\
    \
    if not ogrenci.empty:\
        ad_soyad = ogrenci.iloc[0]['Ad Soyad']\
        sinif = ogrenci.iloc[0]['S\uc0\u305 n\u305 f']\
        st.info(f"**\'d6\uc0\u287 renci:** \{ad_soyad\} | **S\u305 n\u305 f:** \{sinif\}")\
        \
        ihlaller = st.multiselect("\uc0\u304 hlal T\'fcr\'fc", ["K\u305 l\u305 k-K\u305 yafet", "Sa\'e7-Sakal", "Tak\u305 -Makyaj", "Ge\'e7 Kalma", "Di\u287 er"])\
        notlar = st.text_input("Notlar (Opsiyonel)")\
        \
        if st.button("KAYDET"):\
            if ogretmen == "":\
                st.warning("L\'fctfen \'f6\uc0\u287 retmen ad\u305 n\u305  girin!")\
            else:\
                yeni_veri = pd.DataFrame([\{\
                    "Tarih": datetime.now().strftime("%d/%m/%Y %H:%M"),\
                    "\'d6\uc0\u287 retmen": ogretmen,\
                    "Ders": ders_saati,\
                    "No": ogr_no,\
                    "Ad Soyad": ad_soyad,\
                    "S\uc0\u305 n\u305 f": sinif,\
                    "\uc0\u304 hlaller": ", ".join(ihlaller),\
                    "Notlar": notlar\
                \}])\
                \
                # Veriyi dosyaya ekle\
                yeni_veri.to_csv(log_file, mode='a', index=False, header=not os.path.exists(log_file), encoding='utf-8-sig')\
                st.success("Kay\uc0\u305 t Ba\u351 ar\u305 l\u305 !")\
    else:\
        st.error("Bu numaral\uc0\u305  bir \'f6\u287 renci bulunamad\u305 .")\
\
# 3. B\'f6l\'fcm: \uc0\u304 dare Paneli (Basit Raporlama)\
st.divider()\
if st.checkbox("\uc0\u55357 \u56522  \u304 dare Paneli (Haftal\u305 k Kontrol)"):\
    sifre = st.text_input("Giri\uc0\u351  \u350 ifresi", type="password")\
    if sifre == "idare123": # Buray\uc0\u305  de\u287 i\u351 tirebilirsiniz\
        if os.path.exists(log_file):\
            log_df = pd.read_csv(log_file)\
            st.write("### T\'fcm \uc0\u304 hlal Kay\u305 tlar\u305 ")\
            st.dataframe(log_df)\
            \
            st.write("### 3'ten Fazla \uc0\u304 hlali Olanlar")\
            ozet = log_df['Ad Soyad'].value_counts()\
            limit_asanlar = ozet[ozet >= 3] # Buradan limiti de\uc0\u287 i\u351 tirebilirsiniz\
            st.warning(limit_asanlar)\
        else:\
            st.write("Hen\'fcz kay\uc0\u305 t yap\u305 lmam\u305 \u351 .")}