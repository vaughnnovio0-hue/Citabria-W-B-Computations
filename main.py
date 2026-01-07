import streamlit as st
from streamlit_lottie import st_lottie
import requests

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Citabria 7ECA Home",
    page_icon="✈️",
    layout="wide"
)

# 2. LOAD ANIMATIONS
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# 3. MASTER FUTURISTIC STYLING
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* Dark Theme Background */
    .stApp { background-color: #0d1117; }

    /* --- SIDEBAR IMPROVEMENTS --- */
    
    /* Target the first link (main) */
    [data-testid="stSidebarNav"] ul li:nth-child(1) span {
        visibility: hidden;
    }
    [data-testid="stSidebarNav"] ul li:nth-child(1) span::after {
        content: "🏠 Home";
        visibility: visible;
        color: #00d4ff;
        text-shadow: 0 0 10px #00d4ff;
        font-family: 'Orbitron', sans-serif;
        font-size: 16px;
    }

    /* Target the second link (calculator) */
    [data-testid="stSidebarNav"] ul li:nth-child(2) span {
        visibility: hidden;
    }
    [data-testid="stSidebarNav"] ul li:nth-child(2) span::after {
        content: "⚖️ W&B Calculator";
        visibility: visible;
        color: #00d4ff;
        text-shadow: 0 0 10px #00d4ff;
        font-family: 'Orbitron', sans-serif;
        font-size: 16px;
    }

    /* Sidebar Hover Glow */
    [data-testid="stSidebarNav"] ul li:hover {
        background-color: rgba(0, 212, 255, 0.1);
        border-radius: 10px;
        transition: 0.3s;
    }

    /* --- END SIDEBAR IMPROVEMENTS --- */

    /* Futuristic Pill Header */
    .header-pill {
        display: flex;
        align-items: center;
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid #00d4ff;
        border-radius: 50px;
        padding: 10px 25px;
        width: fit-content;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
        margin-bottom: 30px;
    }

    .neon-text {
        color: #00d4ff;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px #00d4ff;
        font-size: 22px;
        font-weight: bold;
        margin-left: 15px;
        letter-spacing: 1px;
    }

    /* Section Headers */
    .section-box {
        border-left: 4px solid #00d4ff;
        padding-left: 15px;
        margin-top: 30px;
        margin-bottom: 15px;
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .spec-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        box-shadow: inset 0 0 10px rgba(0, 212, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# 4. MAIN HEADER
st.markdown('<div class="header-pill">🚀 <span class="neon-text">CITABRIA FLIGHT INTERFACE</span></div>', unsafe_allow_html=True)

# (Rest of your original code follows...)
lottie_air = load_lottieurl("https://lottie.host/82542037-1601-4475-9b24-733333333333/your_json_here.json") 
if lottie_air:
    st_lottie(lottie_air, height=200)

st.divider()

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown('<div class="section-box">ℹ️ ABOUT THE AIRCRAFT</div>', unsafe_allow_html=True)
    st.write("""
    The **Citabria Aurora 7ECA** is a two-seat, fixed-gear utility aircraft designed for flight training, 
    touring, and light aerobatics. Known for its rugged steel-tube fuselage and wooden-spar wings, 
    the Citabria is a favorite among tailwheel pilots.
    """)
    st.info("💡 **Ready to calculate?** Select 'W&B Calculator' from the sidebar menu to begin.")

with col2:
    st.markdown('<div class="spec-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-family: Orbitron; color: #00d4ff; margin-bottom:10px;">🛠️ DESIGN SPECS</div>', unsafe_allow_html=True)
    st.write("**Engine:** Lycoming O-235 (115 HP)")
    st.write("**Max Gross Weight:** 1,650 lbs")
    st.write("**Fuel Capacity:** 36 Gallons (Standard)")
    st.write("**Vso (Stall):** 51 MPH")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.markdown('<div class="section-box">🕹️ HOW TO USE THIS TOOL</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 1️⃣ Enter Weights")
    st.write("Input the weights for the pilot, passenger, baggage, and fuel load in either Lbs or Kg.")

with c2:
    st.markdown("### 2️⃣ Check the Graph")
    st.write("The animated envelope will show you exactly where your Center of Gravity (CG) sits.")

with c3:
    st.markdown("### 3️⃣ Follow Advice")
    st.write("If you are out of balance, the app will suggest how to fix your load before takeoff.")

st.warning("⚠️ **Disclaimer:** This tool is for educational purposes. Always verify calculations using the official POH for your specific tail number.")