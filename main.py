import streamlit as st
import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load 3D animations
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Futuristic Header Code
st.markdown("""
<style>
    .futuristic-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        padding: 25px;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
        margin-bottom: 20px;
        text-align: center;
    }
    .neon-text {
        color: #00d4ff;
        text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff;
        font-size: 35px;
        font-weight: bold;
        letter-spacing: 2px;
    }
</style>
<div class="futuristic-card">
    <div class="neon-text">🚀 CITABRIA FLIGHT INTERFACE</div>
</div>
""", unsafe_allow_html=True)

# Add a 3D animated airplane icon
lottie_air = load_lottieurl("https://lottie.host/82542037-1601-4475-9b24-733333333333/your_json_here.json") # Example URL
if lottie_air:
    st_lottie(lottie_air, height=200)
# Page Configuration
st.set_page_config(
    page_title="Citabria 7ECA Home",
    page_icon="✈️",
    layout="wide"
)

# Custom Styling for the Home Page
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #0E1117;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 20px;
        color: #555;
        text-align: center;
        margin-top: 0px;
        margin-bottom: 30px;
    }
    .spec-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">✈️ Citabria Aurora 7ECA Flight Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Official Pre-Flight Weight & Balance Planning Tool</div>', unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([1.5, 1])

with col1:
    st.header("About the Aircraft")
    st.write("""
    The **Citabria Aurora 7ECA** is a two-seat, fixed-gear utility aircraft designed for flight training, 
    touring, and light aerobatics. Known for its rugged steel-tube fuselage and wooden-spar wings, 
    the Citabria is a favorite among tailwheel pilots.
    
    Because the 7ECA is often used for training and aerobatics, maintaining a precise 
    **Weight and Balance** is critical for both control authority and structural integrity.
    """)
    
    st.info("💡 **Ready to calculate?** Select 'Calculator' from the sidebar menu to begin your manifest.")

with col2:
    st.markdown('<div class="spec-card">', unsafe_allow_html=True)
    st.subheader("🛠️ Design Specs")
    st.write("**Engine:** Lycoming O-235 (115 HP)")
    st.write("**Max Gross Weight:** 1,650 lbs")
    st.write("**Fuel Capacity:** 36 Gallons (Standard)")
    st.write("**Vso (Stall):** 51 MPH")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Instructional Section
st.subheader("How to Use This Tool")
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