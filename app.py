import streamlit as st

# --- INISIALISASI NAVIGASI ---
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- FUNGSI LOGIKA HITUNG ---
def hitung_tetes():
    st.markdown("### 🧮 Analisa Tetes (Brix & Pol)")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Input Data")
            brix_obs = st.number_input("Brix Teramati", min_value=0.0, step=0.1, format="%.2f")
            suhu = st.number_input("Suhu Teramati (°C)", min_value=20.0, max_value=40.0, value=27.5, step=0.5)
            
            # Data Koreksi Suhu sesuai tabel lo beb
            # 27 = -0.05, 28 = +0.02, 29 = +0.09, dst
            map_koreksi = {
                27.0: -0.05,
                27.5: 0.00, # Standar suhu tabel lo
                28.0: 0.02,
                29.0: 0.09,
                30.0: 0.16,
                31.0: 0.24,
                32.0: 0.31,
                33.0: 0.38,
                34.0: 0.46,
                35.0: 0.62,
                36.0: 0.70
            }
            
            # Cari koreksi, kalo suhu gak ada di list anggap 0 atau cari yang terdekat
            koreksi = map_koreksi.get(suhu, 0.0)
            
        with col2:
            st.markdown("#### Hasil Perhitungan")
            
            # Perhitungan sesuai rumus lo
            brix_pengenceran = brix_obs * 10
            brix_akhir = brix_pengenceran + koreksi
            
            # Display Box yang Eye-Catching
            st.metric("Brix Pengenceran (x10)", f"{brix_pengenceran:.2f}")
            st.metric("Koreksi Suhu (Tabel)", f"{koreksi:+.2g}")
            st.markdown(f"""
                <div style="background: rgba(38, 196, 185, 0.2); padding: 20px; border-radius: 15px; border: 2px solid #26c4b9; text-align: center;">
                    <h2 style="margin:0; color: white;">% BRIX AKHIR</h2>
                    <h1 style="margin:0; color: #26c4b9; font-size: 48px;">{brix_akhir:.2f}</h1>
                </div>
            """, unsafe_allow_html=True)

    if st.button("⬅️ Kembali ke Menu Utama"):
        st.session_state.page = 'dashboard'
        st.rerun()

# --- LOGIKA TAMPILAN ---
if st.session_state.page == 'dashboard':
    # Di sini kode Dashboard lo yang lama (Hero Section & Grid Menu)
    # Tambahin logic: kalau menu "HITUNG" diklik, jalankan:
    # st.session_state.page = 'hitung'
    
    st.title("Menu Utama (Dashboard)")
    if st.button("Buka Menu Hitung Analisa Tetes"): # Ini sementara buat ngetes
        st.session_state.page = 'hitung'
        st.rerun()

elif st.session_state.page == 'hitung':
    hitung_tetes()
