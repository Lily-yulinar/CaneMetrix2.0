# --- GRID MENU (VERSI ANTI-GAGAL) ---
items = [
    ("📝", "Input Data"), ("🧮", "Hitung"), ("📅", "Database Harian"),
    ("📊", "Database Bulanan"), ("⚖️", "Rekap Stasiun"), ("📈", "Trend"),
    ("⚙️", "Pengaturan"), ("📥", "Export/Import"), ("👤", "Akun")
]

# CSS tambahan khusus buat tombol agar jadi kartu
st.markdown("""
<style>
    /* Kita desain ulang tombol streamlit biar jadi kartu menu */
    .stButton > button {
        width: 100% !important;
        height: 150px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        transition: all 0.3s ease-in-out !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
    }

    .stButton > button:hover {
        background: rgba(38, 196, 185, 0.2) !important;
        border: 1px solid #26c4b9 !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important;
    }

    /* Bikin teks di dalam tombol jadi dua baris (Icon & Label) */
    .stButton > button div p {
        font-size: 14px !important;
        font-weight: 700 !important;
        font-family: 'Poppins' !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
</style>
""", unsafe_allow_html=True)

for i in range(0, len(items), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(items):
            icon, label = items[i+j]
            with cols[j]:
                # SEKARANG KITA PAKE TOMBOL LANGSUNG
                # Kita gabung icon & label di dalam satu string
                if st.button(f"{icon}\n\n{label}", key=f"btn_{label}"):
                    if label == "Hitung":
                        st.session_state.page = 'analisa_tetes'
                        st.rerun()
