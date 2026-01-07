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

# --- INITIALIZE HISTORY IN SESSION STATE ---
if 'calc_history' not in st.session_state:
    st.session_state.calc_history = [] 

# --- UNIFIED FUTURISTIC STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #0d1117; }

    /* --- SIDEBAR IMPROVEMENTS --- */
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

    [data-testid="stSidebarNav"] ul li:hover {
        background-color: rgba(0, 212, 255, 0.1);
        border-radius: 10px;
        transition: 0.3s;
    }
    /* --- END SIDEBAR IMPROVEMENTS --- */

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
    
    # DEFAULTED AT 0 VALUE
    pilot = st.number_input(f"Front Seat ({unit})", value=0.0, step=1.0) * conv
    rear = st.number_input(f"Rear Seat ({unit})", value=0.0, step=1.0) * conv
    baggage = st.number_input(f"Baggage ({unit})", value=0.0, step=1.0) * conv
    fuel_gal = st.number_input("Fuel (Gallons)", value=0.0, max_value=36.0, step=1.0)
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

    # HISTORY LOGGER BUTTON
    if st.button("💾 LOG TELEMETRY DATA"):
        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "weight": f"{total_weight:.1f} lbs",
            "cg": f"{cg:.2f} in",
            "safe": "✅" if is_safe else "🛑"
        }
        st.session_state.calc_history.append(entry)
        st.toast("Telemetry logged to session history!")

    if not is_safe:
        st.markdown('<div class="section-box">💡 RECOMMENDED ACTIONS</div>', unsafe_allow_html=True)
        if not is_w_safe:
            st.warning(f"👉 **Overweight:** Remove {total_weight - MTOW:.1f} lbs of baggage or fuel.")
        if cg > CG_LIMIT_AFT:
            st.warning("👉 **Too Far Aft:** Move weight forward.")
        if cg < CG_LIMIT_FWD:
            st.warning("👉 **Too Far Forward:** Move weight aft.")

# --- SIDEBAR HISTORY PANEL ---
with st.sidebar:
    st.markdown('<div class="neon-text" style="font-size:18px;">📜 SESSION HISTORY</div>', unsafe_allow_html=True)
    if st.session_state.calc_history:
        for item in reversed(st.session_state.calc_history):
            st.markdown(f"**{item['time']}** | {item['weight']} | {item['safe']}")
            st.caption(f"CG: {item['cg']}")
            st.divider()
    else:
        st.info("No logs found. Values reset to 0 for new session.")

# --- ENHANCED FUTURISTIC GRAPH SECTION ---
st.markdown('<div class="section-box">📊 LIVE TELEMETRY: LOADING ENVELOPE</div>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(12, 7)) 
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0a0e14')

# Corrected Manual Limits from image
norm_x = [14.2, 14.2, 19.2, 19.2, 14.2]
norm_y = [1325, 1650, 1650, 1325, 1325]
acro_x = [14.2, 14.2, 17.5, 17.5, 14.2]
acro_y = [1325, 1650, 1650, 1325, 1325]

ax.plot(norm_x, norm_y, color='#00d4ff', linewidth=3, alpha=0.8, label='Normal Category')
ax.fill(norm_x, norm_y, color='#00d4ff', alpha=0.05) 
ax.plot(acro_x, acro_y, color='#ff00ff', linestyle='--', linewidth=2, alpha=0.6, label='Acrobatic/Utility')
ax.fill(acro_x, acro_y, color='#ff00ff', alpha=0.08) 

ax.grid(True, linestyle=':', alpha=0.2, color='#00d4ff')

state_color = '#00d4ff' if is_safe else '#ff4b4b'
ax.scatter(cg, total_weight, color=state_color, s=1000, alpha=0.15, zorder=4)
ax.scatter(cg, total_weight, color=state_color, s=400, alpha=0.3, zorder=5)
ax.scatter(cg, total_weight, color='white', s=100, edgecolors=state_color, linewidth=2, zorder=6, label='Current State')

ax.set_xlabel("CG POSITION (INCHES AFT DATUM)", color='#00d4ff', fontsize=10, fontname='Orbitron')
ax.set_ylabel("GROSS WEIGHT (LBS)", color='#00d4ff', fontsize=10, fontname='Orbitron')
ax.set_xlim(12, 22)
ax.set_ylim(1100, 1750)
ax.tick_params(colors='#00d4ff', labelsize=9)

leg = ax.legend(facecolor='#0d1117', edgecolor='#00d4ff')
for text in leg.get_texts():
    text.set_color("white")
    text.set_fontname('Orbitron')

st.pyplot(fig)