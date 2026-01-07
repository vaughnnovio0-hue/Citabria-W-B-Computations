import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- AIRCRAFT FIXED DATA ---
AIRCRAFT_NAME = "Citabria Aurora 7ECA"
MTOW = 1650.0
BEW_DEFAULT = 1060.0
BEW_ARM = 11.5
CG_LIMIT_FWD = 14.2
CG_LIMIT_AFT = 19.2
FUEL_DENSITY = 6.0  

# --- UNIFIED FUTURISTIC STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #0d1117; }

    /* The glowing pill header */
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
    }

    /* Section headers with blue left border */
    .section-box {
        border-left: 4px solid #00d4ff;
        padding-left: 15px;
        margin-top: 30px;
        margin-bottom: 20px;
        font-family: 'Orbitron', sans-serif;
        color: white;
        font-size: 18px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# --- FUTURISTIC HEADER ---
st.markdown('<div class="header-pill">⚖️ <span class="neon-text">WEIGHT & BALANCE COMPUTER</span></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="section-box">📥 LOADING MANIFEST</div>', unsafe_allow_html=True)
    unit = st.radio("System Units", ["Lbs", "Kg"], horizontal=True)
    conv = 2.20462 if unit == "Kg" else 1.0
    
    pilot = st.number_input(f"Front Seat ({unit})", value=170.0/conv) * conv
    rear = st.number_input(f"Rear Seat ({unit})", value=0.0) * conv
    baggage = st.number_input(f"Baggage ({unit})", value=0.0) * conv
    fuel_gal = st.number_input("Fuel (Gallons)", value=20.0, max_value=36.0)
    fuel_lbs = fuel_gal * FUEL_DENSITY

    with st.expander("🔢 View Calculation Formulas"):
        st.latex(r"Moment = Weight \times Arm")
        st.latex(r"CG = \frac{\sum Moments}{\sum Weights}")

with col2:
    # Calculations
    total_weight = BEW_DEFAULT + pilot + rear + baggage + fuel_lbs
    total_moment = (BEW_DEFAULT * BEW_ARM) + (pilot * 16.0) + (rear * 47.0) + (baggage * 72.0) + (fuel_lbs * 24.0)
    cg = total_moment / total_weight if total_weight > 0 else 0

    is_w_safe = total_weight <= MTOW
    is_cg_safe = CG_LIMIT_FWD <= cg <= CG_LIMIT_AFT
    is_safe = is_w_safe and is_cg_safe

    # Verdict Banner (3D Gradient Style)
    if is_safe:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1e5128, #4e9c5f); 
                    padding: 20px; border-radius: 15px; text-align: center;
                    box-shadow: inset 2px 2px 5px rgba(255,255,255,0.2), 0 10px 20px rgba(0,0,0,0.4);
                    border: 2px solid #7ed957; color: white; font-weight: bold; font-size: 24px;">
            💎 SYSTEMS NOMINAL: SAFE FOR FLIGHT
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #7b1113, #b22222); 
                    padding: 20px; border-radius: 15px; text-align: center;
                    box-shadow: inset 2px 2px 5px rgba(255,255,255,0.2), 0 10px 20px rgba(0,0,0,0.4);
                    border: 2px solid #ff4b4b; color: white; font-weight: bold; font-size: 24px;">
            🛑 CRITICAL ALERT: OUT OF ENVELOPE
        </div>
        """, unsafe_allow_html=True)

    status = "safe" if is_safe else "NOT safe"
    st.info(f"The CG is **{cg:.2f} in.** aft of datum line at **{total_weight:.1f} lbs**, therefore the aircraft is **{status}** for flight.")

    # Smart Recommendations
    if not is_safe:
        st.markdown('<div class="section-box">💡 RECOMMENDED ACTIONS</div>', unsafe_allow_html=True)
        if not is_w_safe:
            st.warning(f"👉 **Overweight:** Remove {total_weight - MTOW:.1f} lbs of baggage or fuel.")
        if cg > CG_LIMIT_AFT:
            st.warning("👉 **Too Far Aft:** Move weight forward (move items from baggage to front seat).")
        if cg < CG_LIMIT_FWD:
            st.warning("👉 **Too Far Forward:** Move weight aft (add baggage or ballast).")

    # Graph Section
    st.markdown('<div class="section-box">📊 TELEMETRY GRAPH</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')
    ax.plot([CG_LIMIT_FWD, CG_LIMIT_FWD, CG_LIMIT_AFT, CG_LIMIT_AFT, CG_LIMIT_FWD], [1000, MTOW, MTOW, 1000, 1000], 'cyan', linewidth=2)
    ax.scatter(cg, total_weight, color='#00d4ff' if is_safe else '#ff4b4b', s=250, edgecolors='white', zorder=5)
    ax.set_xlabel("CG (Inches aft of Datum)", color='white')
    ax.set_ylabel("Weight (lbs)", color='white')
    ax.tick_params(colors='white')
    st.pyplot(fig)