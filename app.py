import streamlit as st

# --- 1. INISIALISASI NAVIGASI (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- 2. FUNGSI HALAMAN PERHITUNGAN (Rumus lo ada di sini) ---
def halaman_analisa_tetes():
    st.markdown("<h2 style='text-align: center; color: #26c4b9;'>🧪 Hitung Analisa Tetes</h2>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Input Data")
            # Brix teramati diinput user
            brix_obs = st.number_input("Brix Teramati", min_value=0.0, step=0.1, format="%.2f")
            # Suhu teramati
            suhu = st.number_input("Suhu Teramati (°C)", min_value=20.0, max_value=40.0, value=27.5, step=0.5)
            
            # Tabel Koreksi Suhu sesuai foto lo beb
            map_koreksi = {
                27.0: -0.05, 27.5: 0.00, 28.0: 0.02, 29.0: 0.09,
                30.0: 0.16, 31.0: 0.24, 32.0: 0.31, 33.0: 0.38,
                34.0: 0.46, 35.0: 0.62, 36.0: 0.70
            }
            koreksi = map_koreksi.get(suhu, 0.0)
            
        with col2:
            st.markdown("#### 📤 Hasil Analisa")
            # Jalankan Rumus: (Brix Obs * 10) + Koreksi
            brix_pengenceran = brix_obs * 10
            brix_akhir = brix_pengenceran + koreksi
            
            st.metric("Brix Pengenceran (x10)", f"{brix_pengenceran:.2f}")
            st.metric("Koreksi Suhu (Tabel)", f"{koreksi:+.2g}")
            
            st.markdown(f"""
                <div style="background: rgba(38, 196, 185, 0.1); padding: 20px; border-radius: 15px; border: 2px solid #26c4b9; text-align: center;">
                    <h3 style="margin:0; color: white; font-family: 'Poppins';">% BRIX AKHIR</h3>
                    <h1 style="margin:0; color: #26c4b9; font-family: 'Orbitron'; font-size: 45px;">{brix_akhir:.2f}</h1>
                </div>
            """, unsafe_allow_html=True)

    st.write("")
    if st.button("⬅️ Kembali ke Menu Hitung"):
        st.session_state.page = 'menu_hitung'
        st.rerun()

# --- 3. LOGIKA NAVIGASI UTAMA ---

# A. HALAMAN DASHBOARD (UTAMA)
if st.session_state.page == 'dashboard':
    # --- Kode Dashboard (Hero & Grid Menu) taruh di sini ---
    # Contoh simpel pas lo klik tombol "HITUNG" di grid:
    st.title("CaneMetrix Dashboard")
    if st.button("🧮 GOTO MENU HITUNG"): # Ini simulasi klik card 'HITUNG'
        st.session_state.page = 'menu_hitung'
        st.rerun()

# B. SUB-MENU HITUNG (Pilihan Analisa)
elif st.session_state.page == 'menu_hitung':
    st.markdown("<h2 style='text-align: center;'>Pilih Analisa</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧪 Hitung Analisa Tetes", use_container_width=True):
            st.session_state.page = 'analisa_tetes'
            st.rerun()
    with col_b:
        if st.button("💎 Hitung Analisa Kristal (Soon)", use_container_width=True):
            pass

    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

# C. HALAMAN RUMUS ANALISA TETES
elif st.session_state.page == 'analisa_tetes':
    halaman_analisa_tetes()
