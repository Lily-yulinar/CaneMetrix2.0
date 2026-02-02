import streamlit as st

# --- 1. STATE NAVIGASI ---
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- 2. FUNGSI HALAMAN HITUNG ---
def halaman_hitung_tetes():
    st.markdown("<h2 style='text-align: center; color: #26c4b9;'>🧪 Hitung Analisa Tetes</h2>", unsafe_allow_html=True)
    
    # Bungkus dalam Container biar rapi
    with st.container():
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📥 Input Data")
            # User input brix teramati
            brix_obs = st.number_input("Masukkan Brix Teramati", min_value=0.0, step=0.01, format="%.2f")
            
            # --- DATABASE TABEL KOREKSI ---
            # Gue buat contoh mapping: Brix Teramati -> Nilai Koreksi
            # Silakan sesuaikan angka di sebelah kanan (value) dengan tabel asli lo beb
            data_tabel = {
                10.0: 0.05, 11.0: 0.06, 12.0: 0.07, 13.0: 0.08,
                14.0: 0.09, 15.0: 0.10, 16.0: 0.11, 17.0: 0.12,
                18.0: 0.13, 19.0: 0.14, 20.0: 0.15 # dst...
            }
            
            # Cari koreksi (ambil angka brix terdekat/pembulatan)
            brix_key = round(brix_obs)
            koreksi = data_tabel.get(float(brix_key), 0.0)
            
            st.info(f"💡 Berdasarkan tabel, Koreksi Brix untuk {brix_obs} adalah: **{koreksi}**")

        with col2:
            st.markdown("### 📤 Hasil Akhir")
            
            # --- EKSEKUSI RUMUS ---
            brix_x10 = brix_obs * 10
            hasil_akhir = brix_x10 + koreksi
            
            # Tampilan Metric
            st.metric("Brix Teramati x 10", f"{brix_x10:.2f}")
            st.metric("Koreksi Tabel", f"{koreksi:+.2f}")
            
            st.markdown(f"""
                <div style="background: rgba(38, 196, 185, 0.2); padding: 30px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center;">
                    <h3 style="margin:0; color: white;">% BRIX AKHIR</h3>
                    <h1 style="margin:0; color: #26c4b9; font-size: 50px; font-family: 'Orbitron';">{hasil_akhir:.2f}</h1>
                </div>
            """, unsafe_allow_html=True)

    st.write("")
    if st.button("⬅️ Kembali ke Menu Hitung"):
        st.session_state.page = 'menu_hitung'
        st.rerun()

# --- 3. LOGIKA NAVIGASI ---

if st.session_state.page == 'dashboard':
    # Di sini tampilan Dashboard Utama lo yang ada Logo & 9 Sub-menu
    st.title("Main Dashboard")
    if st.button("KLIK MENU HITUNG (Simulasi)"):
        st.session_state.page = 'menu_hitung'
        st.rerun()

elif st.session_state.page == 'menu_hitung':
    st.markdown("<h2 style='text-align: center;'>🧮 Menu Perhitungan</h2>", unsafe_allow_html=True)
    
    # Tombol Analisa Tetes
    if st.button("🧪 Analisa Tetes", use_container_width=True):
        st.session_state.page = 'analisa_tetes'
        st.rerun()
        
    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = 'dashboard'
        st.rerun()

elif st.session_state.page == 'analisa_tetes':
    halaman_hitung_tetes()
