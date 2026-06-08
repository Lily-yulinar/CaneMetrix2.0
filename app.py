import streamlit as st
import gspread
import pandas as pd
from datetime import datetime

# ==========================================
# 1. SETTING HALAMAN & CONFIG
# ==========================================
st.set_page_config(
    page_title="CaneMetrix 2.0",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. FUNGSI KONEKSI GOOGLE SECRETS (TOML)
# ==========================================
def init_connection():
    try:
        # Membaca kredensial dari Streamlit Cloud Secrets
        credentials = st.secrets["gcp_service_account"]
        return gspread.service_account_from_dict(credentials)
    except Exception as e:
        return None

# Jalankan koneksi
gc = init_connection()

# ==========================================
# 3. KONDISI OFFLINE / ONLINE CHECK
# ==========================================
if gc is None:
    # --- TAMPILAN JIKA OFFLINE ---
    st.error("⚠️ Peringatan: Aplikasi berjalan mode offline. Google Sheets belum terhubung. Cek Google Secrets lo beb!")
    
    st.title("CANE METRIX 2.0")
    st.subheader("Accelerating QA Performance")
    st.write("Aplikasi gagal membaca kredensial keamanan. Silakan periksa kembali pengisian TOML di dashboard Streamlit Secrets lo.")

else:
    # --- TAMPILAN JIKA ONLINE (SUKSES CONNECT) ---
    try:
        # Membuka Spreadsheet Utama Lo
        nama_spreadsheet = "Analisa Khusus SG10 2026"
        sh = gc.open(nama_spreadsheet)
        
        # Sidebar Navigasi Menu
        st.sidebar.title("CaneMetrix Navigasi")
        menu = st.sidebar.radio("Pilih Menu:", ["DASHBOARD", "INPUT DATA", "COCKPIT", "KURVA BRIX"])
        
        # ------------------------------------------
        # MENU: DASHBOARD
        # ------------------------------------------
        if menu == "DASHBOARD":
            st.title("CANE METRIX")
            st.caption("ACCELERATING QA PERFORMANCE")
            
            # Menampilkan Tanggal & Jam Live di Dashboard
            col_tgl, col_jam = st.columns(2)
            with col_tgl:
                st.metric("Tanggal Operasi", datetime.now().strftime("%d %B %Y"))
            with col_jam:
                st.metric("Waktu Sistem WIB", datetime.now().strftime("%H:%M:%S"))
                
            st.success("⚡ Sistem Terkoneksi Lancar dengan Google Sheets!")
            st.info("Silakan pilih menu di sidebar sebelah kiri untuk mulai melakukan input atau kalkulasi analisa khusus.")
            
        # ------------------------------------------
        # MENU: INPUT DATA (STASIUN GILINGAN)
        # ------------------------------------------
        elif menu == "INPUT DATA":
            st.title("📥 Input Data Analisa")
            
            st.subheader("Stasiun Gilingan")
            
            # Input parameter tanggal untuk nentuin sheet harian (Format: 0106, 0806, dll)
            tgl_pilihan = st.date_input("Pilih Tanggal Operasi:", datetime.now())
            nama_sheet_harian = tgl_pilihan.strftime("%d%m") # Mengubah ke format ddmm (misal: 0806)
            
            # Pilihan Jam Kerja / Pengamatan
            jam_pilihan = st.selectbox("Pilih Jam Pengamatan:", [
                "07.00", "08.00", "09.00", "10.00", "11.00", "12.00", 
                "13.00", "14.00", "15.00", "16.00", "17.00", "18.00",
                "19.00", "20.00", "21.00", "22.00", "23.00", "00.00",
                "01.00", "02.00", "03.00", "04.00", "05.00", "06.00"
            ])
            
            st.markdown("---")
            st.subheader("Form Analisa NPP (Nira Perasan Pertama)")
            
            # Form Input Data Teknis
            col1, col2, col3 = st.columns(3)
            with col1:
                brix_baca = st.number_input("Brix Baca NPP:", min_value=0.0, max_value=30.0, value=18.0, step=0.1)
            with col2:
                suhu_npp = st.number_input("Suhu NPP (°C):", min_value=0.0, max_value=100.0, value=28.0, step=0.1)
            with col3:
                pol_baca = st.number_input("Pol Baca NPP:", min_value=0.0, max_value=25.0, value=14.0, step=0.1)
                
            # Tombol Tembak Data ke Google Sheets
            if st.button("🚀 TEMBAK DATA NPP", type="primary"):
                try:
                    # Buka sub-sheet berdasarkan tanggal (misal: "0806")
                    ws = sh.worksheet(nama_sheet_harian)
                    
                    # Mencari baris jam yang sesuai di Kolom A
                    list_jam = ws.col_values(1) # Mengambil semua data di Kolom A (Jam)
                    
                    if jam_pilihan in list_jam:
                        # Dapatkan indeks baris (ditambah 1 karena indeks gspread dimulai dari 1)
                        baris_target = list_jam.index(jam_pilihan) + 1
                        
                        # Jalankan Kalkulasi Rumus Brix Akhir di Python sebelum ditembak
                        # Contoh rumus penyesuaian brix berdasarkan suhu/faktor koreksi (bisa disesuaikan nanti)
                        brix_koreksi = brix_baca * (1 + (suhu_npp - 27.5) * 0.0003) 
                        pol_akhir = pol_baca * 0.95
                        
                        # Tembak data ke Kolom B (Baris jam tersebut)
                        # Kolom 2 = Kolom B (misal untuk data % Sac / Brix Akhir)
                        ws.update_cell(baris_target, 2, round(brix_koreksi, 2))
                        ws.update_cell(baris_target, 3, round(pol_akhir, 2))
                        
                        st.success(f"🎉 Sukses! Data Jam {jam_pilihan} berhasil ditembak ke sheet '{nama_sheet_harian}' Baris {baris_target}!")
                    else:
                        st.error(f"❌ Format jam '{jam_pilihan}' tidak ditemukan di Kolom A sheet {nama_sheet_harian}. Cek format titik/koma di Excel lo beb.")
                        
                except gspread.exceptions.WorksheetNotFound:
                    st.error(f"❌ Sheet dengan nama '{nama_sheet_harian}' belum dibuat di Google Sheets lo beb! Tolong bikin dulu sheet-nya.")
                except Exception as error:
                    st.error(f"🚨 Terjadi eror teknis: {error}")
                    
        # ------------------------------------------
        # MENU: COCKPIT / MONITORING DATA
        # ------------------------------------------
        elif menu == "COCKPIT":
            st.title("🎛️ Cockpit Monitoring")
            st.write("Fitur monitoring visual realtime parameter pabrik gula.")
            # Nanti lo tinggal tambahin chart atau tabel rekap di sini beb
            
        # ------------------------------------------
        # MENU: KURVA BRIX
        # ------------------------------------------
        elif menu == "KURVA BRIX":
            st.title("📈 Kurva Brix & Progress")
            st.write("Grafik tren perkembangan Brix harian stasiun masakan dan penguapan.")

    except Exception as e:
        st.error(f"⚠️ Gagal membuka Spreadsheet. Pastiin email bot sudah di-share ke Google Sheets sebagai 'Editor' ya beb! Eror: {e}")
