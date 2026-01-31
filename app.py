import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Sayfa yapılandırması
st.set_page_config(page_title="SRAL Disiplin", page_icon="🛡️")

# Google Sheets Bağlantı Fonksiyonu
def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(st.secrets["sheet_id"]).sheet1

# Öğrenci Listesini Yükle
@st.cache_data
def load_students():
    return pd.read_excel("ogrenciler.xlsx")

df = load_students()

st.title("🛡️ SRAL Disiplin Takip")

# Öğretmen Bilgisi
with st.sidebar:
    ogretmen = st.text_input("Öğretmen Ad Soyad")
    ders = st.selectbox("Ders Saati", list(range(1, 10)))

# Uygulama Ana Ekranı
ogr_no = st.number_input("Öğrenci Numarası", min_value=1, step=1, value=None)

if ogr_no:
    ogrenci = df[df['Öğrenci No'] == ogr_no]
    
    if not ogrenci.empty:
        ad_soyad = ogrenci.iloc[0]['Ad Soyad']
        sinif = ogrenci.iloc[0]['Sınıf']
        st.success(f"👤 **{ad_soyad}** ({sinif})")
        
        # İSTENEN 4 ANA BAŞLIK
        secenekler = st.multiselect(
            "İhlal Türlerini İşaretleyin:",
            ["Saç-Sakal", "Kıyafet", "Makyaj", "Takı"]
        )
        notlar = st.text_input("Ek Not (İsteğe bağlı)")
        
        if st.button("KAYDET"):
            if not ogretmen:
                st.error("Lütfen adınızı girin!")
            elif not secenekler:
                st.error("En az bir ihlal seçmelisiniz!")
            else:
                try:
                    sheet = connect_to_gsheet()
                    tarih = datetime.now().strftime("%d/%m/%Y %H:%M")
                    # Veriyi Google Sheets'e gönder
                    sheet.append_row([tarih, ogretmen, ders, ogr_no, ad_soyad, sinif, ", ".join(secenekler), notlar])
                    st.success("Kayıt başarıyla gönderildi!")
                except Exception as e:
                    st.error(f"Bağlantı Hatası: {e}")
    else:
        st.warning("Bu numara listede yok!")
