import streamlit as st
import datetime

# 1. Konfigurasi Halaman
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# 2. CSS untuk Background Gambar Lab dan Styling Menu
st.markdown("""
    <style>
    /* Mengatur background utama dengan gambar lab */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
        url("https://images.unsplash.com/photo-1581093588401-fbb62a02f120?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Header styling */
    .header-container {
        background-color: #1a4a7a;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        position: relative;
    }
    
    /* Card/Kotak Menu styling */
    .menu-card {
        background-color: #7ab8e1;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 20px;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s;
        cursor: pointer;
    }
    
    .menu-card:hover {
        transform: scale(1.05);
        background-color: #5ba4d6;
    }
    
    .dark-card {
        background-color: #3d7fb3;
    }
    
    /* Info Bar di bawah */
    .info-bar {
        background-color: #26c4b9;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section (Nama, Tanggal, Shift)
today = datetime.datetime.now().strftime("%d %B %Y")
st.markdown(f"""
    <div class="header-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="text-align: left;">Welcome, Planters!</div>
            <div style="text-align: right;">{today} <br> <span style="background:#26c4b9; padding:2px 10px; border-radius:5px;">SHIFT I</span></div>
        </div>
        <h1 style="margin:10px 0; letter-spacing: 8px; font-family: sans-serif;">CANE METRIX</h1>
        <p style="margin:0; font-style: italic;">Accelerating QA Performance</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Grid Menu 3x3
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="menu-card">📋<br>Input Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-card dark-card">⚖️<br>Rekap Stasiun</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-card">📈<br>Trend</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="menu-card dark-card">📅<br>Database Harian</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-card">🧮<br>Hitung</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-card">⚙️<br>Pengaturan</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="menu-card">📊<br>Database Bulanan</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-card">👤<br>Akun</div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-card dark-card">📥<br>Export/Import Data</div>', unsafe_allow_html=True)

st.write("") # Spasi

# 5. Footer / Status Sampel
st.markdown('<div class="info-bar">Jumlah sampel masuk hari ini: *45</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: right; color: gray; margin-top:10px;'>Status Server: <span style='color: green;'>● OK</span></p>", unsafe_allow_html=True)
