import streamlit as st
import datetime
import pytz
import base64
import os
import gspread # Tambahan
from google.oauth2.service_account import Credentials # Tambahan

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# --- FUNGSI KONEKSI EXCEL (UBAH DISINI) ---
def init_connection():
    try:
        s = st.secrets["gcp_service_account"]
        # Fix PEM file error dengan replace newline
        private_key = s["private_key"].replace("\\n", "\n")
        info = {
            "type": s["type"], "project_id": s["project_id"],
            "private_key_id": s["private_key_id"], "private_key": private_key,
            "client_email": s["client_email"], "client_id": s["client_id"],
            "auth_uri": s["auth_uri"], "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"]
        }
        creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Gagal koneksi ke Excel: {e}")
        return None

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- [BAGIAN LOGO, DATA TABEL, DAN CSS TETAP SAMA - TIDAK DIUBAH] ---
# ... (kode get_base64_logo, data_koreksi, data_bj, data_tsai, hitung_interpolasi, CSS kamu) ...

# --- 6. LOGIKA HALAMAN ---
# ... (kode dashboard dan pilih_analisa kamu tetap sama) ...

elif st.session_state.page == 'analisa_lab':
    # --- ANALISA TETES ---
    if st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                bx_in = st.number_input("Brix Teramati", value=8.80, format="%.2f")
                sh_in = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
                pol_baca = st.number_input("Pol Baca", value=11.00, format="%.2f")
                
                # --- FIX JAM 24 JAM (06.00 - 05.00) ---
                list_jam = [f"{(i % 24):02d}:00" for i in range(6, 30)]
                analisa_jam = st.selectbox("Analisa Jam", options=list_jam)
                
                kor = hitung_interpolasi(sh_in, data_koreksi); bj = hitung_interpolasi(bx_in, data_bj)
                brix_akhir = (bx_in + kor) * 10; pol_akhir = (0.286 * pol_baca) / bj * 10
                hk = (pol_akhir / brix_akhir * 100) if brix_akhir != 0 else 0
                st.info(f"💡 Koreksi: {kor:+.3f} | BJ: {bj:.6f}")
                
                # --- TOMBOL SIMPAN KE EXCEL ---
                if st.button("🚀 SIMPAN KE EXCEL", use_container_width=True):
                    gc = init_connection()
                    if gc:
                        try:
                            # Sesuaikan nama file Google Sheet kamu
                            sh = gc.open("KKKB_250711.xlsx") 
                            worksheet = sh.worksheet("INPUT")
                            tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d")
                            worksheet.append_row([tanggal, analisa_jam, brix_akhir, pol_akhir, hk])
                            st.success(f"Data jam {analisa_jam} Berhasil Disimpan! ✅")
                        except Exception as e:
                            st.error(f"Gagal Kirim Data: {e}")

            with cy:
                st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-family:Orbitron; margin:0;">{brix_akhir:.3f}</h1><p style="color:white;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0;">{pol_akhir:.3f}</h1><p style="color:white;">% POL AKHIR</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0;">{hk:.2f}</h1><p style="color:white;">HK</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- [OD TETES, TSAI, ICUMSA TETEP SAMA - TIDAK DIUBAH] ---
