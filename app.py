import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# --- FUNGSI KONEKSI GOOGLE SHEETS (FIXED) ---
def koneksi_ke_excel():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        # Mengambil info dari Secrets Streamlit tanpa modifikasi assignment
        secret_info = st.secrets["gcp_service_account"]
        
        # Authenticate menggunakan info dari secrets
        creds = Credentials.from_service_account_info(secret_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Membuka spreadsheet berdasarkan nama file di Drive lo
        sh = client.open("KKKB_250711")
        return sh.worksheet("INPUT") 
    except Exception as e:
        st.error(f"Gagal koneksi ke Google Sheets: {e}")
        return None

# --- SIDEBAR / HEADER ---
# Tetap menggunakan desain sesuai screenshot lo
st.title("🚀 CANEMETRIX 2.0")

# --- MENU NAVIGASI (Simple Version) ---
if 'page' not in st.session_state:
    st.session_state.page = 'pilih_analisa'

def change_page(name):
    st.session_state.page = name

# --- HALAMAN UTAMA: PILIH ANALISA ---
if st.session_state.page == 'pilih_analisa':
    st.header("PILIH ANALISA")
    if st.button("🧪 ANALISA TETES", use_container_width=True):
        change_page('analisa_tetes')
    if st.button("⬅️ KEMBALI", use_container_width=False):
        pass

# --- HALAMAN: ANALISA TETES ---
elif st.session_state.page == 'analisa_tetes':
    st.header("🧪 ANALISA TETES")
    
    # Grid Input sesuai desain screenshot
    col_input_left, col_display_right = st.columns([1, 1])

    with col_input_left:
        brix_teramati = st.number_input("Brix Teramati", value=8.80, step=0.01, format="%.2f")
        suhu = st.number_input("Suhu (°C)", value=28.00, step=0.01, format="%.2f")
        pol_baca = st.number_input("Pol Baca", value=11.00, step=0.01, format="%.2f")
        analisa_jam = st.selectbox("Analisa Jam", options=[6, 14, 22], index=0)
        
        # Perhitungan (Sesuai Logika Standar yang lo pake)
        # Koreksi Suhu & BJ (Contoh logika berdasarkan screenshot lo)
        koreksi = 0.020 
        bj = 1.031242
        st.info(f"💡 Koreksi: +{koreksi:.3f} | BJ: {bj:.6f}")

    with col_display_right:
        # Kalkulasi Output
        # Ini placeholder rumus, silakan sesuaikan dengan rumus spesifik lo
        brix_akhir = 88.20 
        pol_akhir = 30.51
        hk = 34.59

        # Display Card (Box Warna-warni sesuai screenshot)
        st.markdown(f"""
            <div style="border: 2px solid #00f2ff; padding: 20px; border-radius: 10px; margin-bottom: 10px; text-align: center;">
                <h1 style="color: #00f2ff; margin: 0;">{brix_akhir:.2f}</h1>
                <p style="margin: 0;">% BRIX</p>
            </div>
            <div style="border: 2px solid #ffcc00; padding: 20px; border-radius: 10px; margin-bottom: 10px; text-align: center;">
                <h1 style="color: #ffcc00; margin: 0;">{pol_akhir:.2f}</h1>
                <p style="margin: 0;">% POL</p>
            </div>
            <div style="border: 2px solid #ff4b4b; padding: 20px; border-radius: 10px; text-align: center;">
                <h1 style="color: #ff4b4b; margin: 0;">{hk:.2f}</h1>
                <p style="margin: 0;">HK</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Tombol Aksi
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("🚀 SIMPAN KE EXCEL", type="primary"):
            sheet = koneksi_ke_excel()
            if sheet:
                try:
                    # Menyesuaikan dengan baris di Excel lo (image_25a14e.png)
                    # Lo perlu nentuin data ini masuk ke baris mana berdasarkan 'Jam'
                    # Untuk simpelnya, kita pake append_row dulu:
                    data_ke_excel = [analisa_jam, brix_teramati, suhu, pol_baca, brix_akhir, pol_akhir, hk]
                    sheet.append_row(data_ke_excel)
                    st.success("Data Berhasil Terkirim ke Excel!")
                except Exception as e:
                    st.error(f"Gagal Kirim: {e}")
                    
    with col_btn2:
        if st.button("🔙 KEMBALI KE MENU PILIHAN"):
            change_page('pilih_analisa')

# --- FOOTER ---
st.markdown("---")
st.caption("CaneMetrix v2.0 | Digitalizing Sugar Factory Analysis")
