import streamlit as st

# --- 1. INISIALISASI NAVIGASI ---
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- 2. FUNGSI HALAMAN HITUNG ANALISA TETES ---
def halaman_hitung_tetes():
    st.markdown("<h2 style='text-align: center; color: #26c4b9;'>🧪 Hitung Analisa Tetes</h2>", unsafe_allow_html=True)
    
    # Card Putih untuk Form
    st.markdown("""
        <style>
        .form-container {
            background: rgba(255, 255, 255, 0.05);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📥 Input Data Lab")
            brix_teramati = st.number_input("Brix Teramati", min_value=0.0, step=0.01, format="%.2f")
            suhu = st.selectbox("Suhu Teramati (°C)", [27, 28, 29, 30, 31, 32, 33, 34, 35, 36])
            
            # Database Koreksi Suhu (Sesuai Tabel ICUMSA lo Beb)
            tabel_koreksi = {
                27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24,
                32: 0.31, 33: 0.38, 34: 0.46, 35: 0.62, 36: 0.70
            }
            koreksi = tabel_koreksi.get(suhu, 0.0)

        with col2:
            st.subheader("📤 Hasil Perhitungan")
            
            # Rumus: (Brix Teramati * 10) + Koreksi Suhu
            brix_pengenceran = brix_teramati * 10
            brix_akhir = brix_pengenceran + koreksi
            
            # Tampilan Hasil
            st.write(f"Brix Pengenceran (x10): **{brix_pengenceran:.2f}**")
            st.write(f"Koreksi Suhu ({suhu}°C): **{koreksi:+.2f}**")
            
            st.markdown(f"""
                <div style="background: #26c4b9; padding: 20px; border-radius: 12px; text-align: center; margin-top: 10px;">
                    <span style="color: #000; font-weight: bold; font-size: 18px;">% BRIX AKHIR</span><br>
                    <span style="color: #000; font-size: 40px; font-weight: 900; font-family: 'Orbitron';">{brix_akhir:.2f}</span>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("⬅️ Kembali ke Pilihan Analisa"):
        st.session_state.page = 'menu_hitung'
        st.rerun()

# --- 3. LOGIKA NAVIGASI ---

# A. DASHBOARD UTAMA
if st.session_state.page == 'dashboard':
    # Simulasi Klik Sub-menu 'HITUNG' (Urutan ke-2)
    st.title("CaneMetrix 2.0")
    if st.button("Buka Menu HITUNG"):
        st.session_state.page = 'menu_hitung'
        st.rerun()

# B. SUB-MENU HITUNG (PILIHAN)
elif st.session_state.page == 'menu_hitung':
    st.markdown("<h2 style='text-align: center;'>Pilih Jenis Analisa</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        # Tombol masuk ke Analisa Tetes
        if st.button("🧪 Hitung Analisa Tetes", use_container_width=True):
            st.session_state.page = 'hitung_tetes'
            st.rerun()
            
    with col_b:
        st.button("💎 Hitung Analisa Kristal (Soon)", use_container_width=True, disabled=True)

    if st.button("⬅️ Kembali ke Dashboard Utama"):
        st.session_state.page = 'dashboard'
        st.rerun()

# C. HALAMAN PERHITUNGAN TETES
elif st.session_state.page == 'hitung_tetes':
    halaman_hitung_tetes()
