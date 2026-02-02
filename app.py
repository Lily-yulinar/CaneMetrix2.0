# --- GRID SUB-MENU (Urutan Baru) ---
st.write("") # Kasih nafas dikit
m1, m2, m3 = st.columns(3)

# Susunan menu sesuai request lo
items = [
    ("📝", "Input Data"), 
    ("🧮", "Hitung"), 
    ("📅", "Database Harian"),
    ("📊", "Database Bulanan"), 
    ("⚖️", "Rekap Stasiun"), 
    ("📈", "Trend"),
    ("⚙️", "Pengaturan"), 
    ("📥", "Export/Import Data"), 
    ("👤", "Akun")
]

for i, (icon, text) in enumerate(items):
    # Logika buat bagi kolom otomatis
    with [m1, m2, m3][i % 3]:
        st.markdown(f"""
            <div class="menu-card">
                <div style="font-size: 60px; margin-bottom: 15px;">{icon}</div>
                <div style="font-size: 18px; font-weight: 700; letter-spacing: 2px;">{text.upper()}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("") # Spacer biar rapi di tampilan mobile
