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

# --- STYLING & ANIMATIONS ---
# FIXED: changed unsafe_content_type to unsafe_allow_html
st.markdown("""
<style>
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.02); opacity: 1; }
        100% { transform: scale(1); opacity: 0.9; }
    }
    .safe-banner {
        font-size: 24px; font-weight: bold; color: #155724;
        background-color: #d4edda; border-radius: 10px; padding: 20px;
        text-align: center; border: 2px solid #c3e6cb;
        animation: pulse 2s infinite;
    }
    .danger-banner {
        font-size: 24px; font-weight: bold; color: #721c24;
        background-color: #f8d7da; border-radius: 10px; padding: 20px;
        text-align: center; border: 2px solid #f5c6cb;
        animation: pulse 1s infinite;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ Weight & Balance Calculator")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("📥 Loading Inputs")
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

    # Verdict Banner
    # Replace your old Banner logic with this:
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

    # Verdict Statement
    status = "safe" if is_safe else "NOT safe"
    st.info(f"The CG is **{cg:.2f} in.** aft of datum line at **{total_weight:.1f} lbs**, therefore the aircraft is **{status}** for flight.")

    # Smart Recommendations
    if not is_safe:
        st.subheader("💡 Solutions")
        if not is_w_safe:
            st.warning(f"👉 **Overweight:** Remove {total_weight - MTOW:.1f} lbs of baggage or fuel.")
        if cg > CG_LIMIT_AFT:
            st.warning("👉 **Too Far Aft:** Move weight forward (move items from baggage to front seat).")
        if cg < CG_LIMIT_FWD:
            st.warning("👉 **Too Far Forward:** Move weight aft (add baggage or ballast).")

    # Graph
    fig, ax = plt.subplots()
    ax.plot([CG_LIMIT_FWD, CG_LIMIT_FWD, CG_LIMIT_AFT, CG_LIMIT_AFT, CG_LIMIT_FWD], [1000, MTOW, MTOW, 1000, 1000], 'g-')
    ax.scatter(cg, total_weight, color='blue' if is_safe else 'red', s=250, edgecolors='white', zorder=5)
    ax.set_xlabel("CG (Inches aft of Datum)")
    ax.set_ylabel("Weight (lbs)")
    st.pyplot(fig)