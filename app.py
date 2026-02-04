import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import datetime

# --- 1. SETTING KONEKSI GOOGLE SHEETS ---
def init_connection():
    try:
        # Mengambil data dari st.secrets["gcp_service_account"]
        s = st.secrets["gcp_service_account"]
        
        # FIX PEM FILE: Mengonversi string \n menjadi baris baru yang asli
        private_key = s["private_key"].replace("\\n", "\n")
        
        info = {
            "type": s["type"],
            "project_id": s["project_id"],
            "private_key_id": s["private_key_id"],
            "private_key": private_key,
            "client_email": s["client_email"],
            "client_id": s["client_id"],
            "auth_uri": s["auth_uri"],
            "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"]
        }
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Gagal inisialisasi koneksi: {e}")
        return None

# --- 2. LOGIKA INPUT JAM (06.00 - 05.00) ---
# Membuat list jam operasional pabrik 24 jam mulai dari jam 6 pagi
jam_operasional = []
for i in range(6, 30):  # Dari 6 sampai 29 (30 tidak termasuk)
    jam_format = f"{(i % 24):02d}:00"
    jam_operasional.append(jam_format)

# --- 3. UI STREAMLIT ---
st.title("🚀 CANEMETRIX 2.0")

# Input Data
brix_teramati = st.number_input("Brix Teramati", value=8.80, step=0.01)
suhu = st.number_input("Suhu (°C)", value=28.0, step=0.1)
pol_baca = st.number_input("Pol Baca", value=11.00, step=0.01)

# Dropdown jam yang sudah diperbaiki jadi 24 jam (Mulai jam 6)
analisa_jam = st.selectbox("Analisa Jam", options=jam_operasional)

# Contoh Kalkulasi (Sesuaikan dengan rumus aslimu)
brix_akhir = brix_teramati * 10 # Contoh dummy
pol_akhir = pol_baca * 2.77 # Contoh dummy
hk = (pol_akhir / brix_akhir) * 100 if brix_akhir != 0 else 0

# Tampilan Hasil
col1, col2, col3 = st.columns(3)
col1.metric("BRIX AKHIR", f"{brix_akhir:.2f}")
col2.metric("POL AKHIR", f"{pol_akhir:.3f}")
col3.metric("HK", f"{hk:.2f}")

# --- 4. TOMBOL SIMPAN KE EXCEL ---
if st.button("🚀 SIMPAN KE EXCEL"):
    client = init_connection()
    if client:
        try:
            # GANTI NAMA SHEET SESUAI FILENAMEMU (Cek image_26e6e9.png)
            # Pastikan nama file "KKKB_250711.xlsx" atau sesuai di Drive
            sh = client.open("KKKB_250711.xlsx") 
            worksheet = sh.worksheet("INPUT") # Ganti jika nama sheet bukan INPUT
            
            # Menyiapkan data untuk dikirim
            tanggal_skrg = datetime.datetime.now().strftime("%Y-%m-%d")
            data_baru = [tanggal_skrg, analisa_jam, brix_akhir, pol_akhir, hk]
            
            # Menambah baris di paling bawah yang ada datanya
            worksheet.append_row(data_baru)
            st.success(f"Data jam {analisa_jam} berhasil masuk ke Excel! ✅")
            
        except Exception as e:
            st.error(f"Gagal Kirim ke Excel: {e}")
