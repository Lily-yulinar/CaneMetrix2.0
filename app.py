import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import datetime

# --- KONEKSI GOOGLE SHEETS ---
def init_gsheet():
    # Mengambil rahasia yang tadi lo simpan di Secrets
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    # Pastikan ID di bawah ini adalah ID Spreadsheet lo
    return client.open_by_key("1yQ2DbMy0ip_du1gqJ16jWwaWK8Psv6AB").worksheet("INPUT")

# --- TAMPILAN APLIKASI ---
st.title("🏭 STASIUN PEMURNIAN - CANEMETRIX")

# Pilihan Sampel & Jam
col1, col2 = st.columns(2)
with col1:
    sampel = st.selectbox("Pilih Sampel", ["Nira Encer", "Nira Kental", "Nira Kotor"])
with col2:
    # Jam 6 pagi sampai jam 5 pagi besoknya
    jam_pilihan = st.selectbox("Analisa Jam", list(range(6, 24)) + list(range(0, 6)))

# Input Data
bx_baca = st.number_input("Brix Teramati", format="%.2f")
pol_baca = st.number_input("Pol Baca", format="%.2f")
icumsa = st.number_input("Icumsa (Jika Ada)", format="%.3f", value=0.0)

if st.button("🚀 KIRIM KE EXCEL"):
    try:
        sheet = init_gsheet()
        
        # HITUNG BARIS: Jam 06:00 = Baris 124
        # Kalau jam 6-23: baris = 124 + (jam - 6)
        # Kalau jam 0-5: baris = 124 + (jam + 18)
        if jam_pilihan >= 6:
            baris_target = 124 + (jam_pilihan - 6)
        else:
            baris_target = 124 + (jam_pilihan + 18)
            
        # MAPPING KOLOM (Sesuai Gambar Excel Lo)
        mapping = {
            "Nira Encer": {"Brix": "C", "Pol": "D", "Icumsa": "I"},
            "Nira Kental": {"Brix": "K", "Pol": "L", "Icumsa": "N"},
            "Nira Kotor": {"Brix": "S", "Pol": "T"}
        }
        
        # Kirim Brix
        sheet.update_acell(f"{mapping[sampel]['Brix']}{baris_target}", str(bx_baca))
        # Kirim Pol
        sheet.update_acell(f"{mapping[sampel]['Pol']}{baris_target}", str(pol_baca))
        # Kirim Icumsa (khusus nira encer & kental)
        if "Icumsa" in mapping[sampel] and icumsa > 0:
            sheet.update_acell(f"{mapping[sampel]['Icumsa']}{baris_target}", str(icumsa))
            
        st.success(f"✅ Mantap Beb! Data {sampel} Jam {jam_pilihan}:00 Berhasil Masuk ke Baris {baris_target}!")
    except Exception as e:
        st.error(f"Waduh Gagal: {e}")
