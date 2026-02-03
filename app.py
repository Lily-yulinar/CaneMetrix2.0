# --- 5. GRID MENU (BAGIAN INI AJA YG DIUPDATE BEB) ---
items = [
    ("📝", "Input Data"), ("🧮", "Hitung"), ("📅", "Database Harian"),
    ("📊", "Database Bulanan"), ("⚖️", "Rekap Stasiun"), ("📈", "Trend"),
    ("⚙️", "Pengaturan"), ("📥", "Export/Import"), ("👤", "Akun")
]

for i in range(0, len(items), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(items):
            icon, text = items[i+j]
            with cols[j]:
                # Visual Tetap Sama Persis kayak kemauan lo
                st.markdown(f"""
                    <div class="menu-card">
                        <div style="font-size: 50px; margin-bottom: 10px;">{icon}</div>
                        <div style="font-size: 16px; font-weight: 700; letter-spacing: 1px;">{text.upper()}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # INI KUNCINYA: Tombol transparan ditaruh di atas visual biar navigasi jalan
                # Kita kasih jarak minus biar dia naik menimpa kotak menu-card
                st.markdown('<div style="margin-top: -180px;">', unsafe_allow_html=True)
                if st.button("", key=f"btn_{text}", help=f"Klik untuk {text}"):
                    if text == "Hitung":
                        st.session_state.page = 'analisa_tetes'
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                # --- LOGIKA PINDAH HALAMAN ---
if st.session_state.page == 'analisa_tetes':
    # Hapus tampilan dashboard dan munculkan kalkulator
    st.empty() 
    
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📥 INPUT")
        bx_obs = st.number_input("Brix Teramati", value=8.80, format="%.2f")
        suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, format="%.1f")
        
        # Fungsi interpolasi yang kita buat tadi
        koreksi = hitung_interpolasi(suhu_obs)
        st.success(f"Koreksi: {koreksi:+.3f}")
        
    with c2:
        st.markdown("### 📤 HASIL")
        bx_akhir = (bx_obs * 10) + koreksi
        st.markdown(f"""
            <div style="background: rgba(38, 196, 185, 0.2); padding: 20px; border-radius: 15px; border: 2px solid #26c4b9; text-align: center;">
                <h4 style="margin:0; color:white;">% BRIX AKHIR</h4>
                <h1 style="margin:0; color:#26c4b9; font-family:Orbitron; font-size:45px;">{bx_akhir:.3f}</h1>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI KE MENU"):
        st.session_state.page = 'dashboard'
        st.rerun()
