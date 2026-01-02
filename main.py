import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- AIRCRAFT FIXED DATA ---
AIRCRAFT = "Citabria Aurora 7ECA"
MTOW = 1650.0          
BEW_DEFAULT = 1060.0           
BEW_ARM = 11.5         
CG_FWD = 14.2          
CG_AFT = 19.2          
FUEL_DENSITY = 6.0     # lbs/gal
KG_TO_LBS = 2.20462    

st.set_page_config(page_title=f"{AIRCRAFT} W&B", layout="wide")

# --- UI HEADER ---
st.title(f"✈️ {AIRCRAFT} Weight & Balance")
st.markdown("### Professional Multi-Unit Pre-Flight Tool")
st.divider()

col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("1. Input Data")
    
    # Unit Toggle
    weight_unit = st.radio("Weight Input Unit", ["Pounds (lbs)", "Kilograms (kg)"], horizontal=True)
    w_conv = KG_TO_LBS if weight_unit == "Kilograms (kg)" else 1.0
    w_label = "kg" if weight_unit == "Kilograms (kg)" else "lbs"

    # Weight Inputs
    bew = st.number_input(f"Basic Empty Weight ({w_label})", value=BEW_DEFAULT/w_conv) * w_conv
    pilot = st.number_input(f"Front Seat Occupant ({w_label})", value=170.0/w_conv) * w_conv
    rear = st.number_input(f"Rear Seat Occupant ({w_label})", value=0.0) * w_conv
    bags = st.number_input(f"Baggage/Cargo ({w_label})", value=0.0, help="Manufacturer standard limit is 100 lbs") * w_conv
    
    st.divider()
    
    # Fuel Inputs
    fuel_unit = st.radio("Fuel Input Unit", ["Gallons", "Pounds (lbs)"], horizontal=True)
    if fuel_unit == "Gallons":
        fuel_qty = st.number_input("Fuel Quantity (Gallons)", value=20.0, max_value=36.0)
        fuel_lbs = fuel_qty * FUEL_DENSITY
    else:
        fuel_lbs = st.number_input("Fuel Weight (lbs)", value=120.0, max_value=216.0)

with col2:
    st.header("2. Safety Status")
    
    # Math Engine
    data = [
        {"Station": "Basic Empty Weight", "Weight": bew, "Arm": BEW_ARM},
        {"Station": "Front Seat", "Weight": pilot, "Arm": 16.0},
        {"Station": "Rear Seat", "Weight": rear, "Arm": 47.0},
        {"Station": "Baggage", "Weight": bags, "Arm": 72.0},
        {"Station": "Fuel", "Weight": fuel_lbs, "Arm": 24.0},
    ]
    df = pd.DataFrame(data)
    df['Moment'] = df['Weight'] * df['Arm']
    
    total_weight = df['Weight'].sum()
    total_moment = df['Moment'].sum()
    cg = total_moment / total_weight if total_weight > 0 else 0

    # Safety Logic
    is_weight_safe = total_weight <= MTOW
    is_cg_safe = CG_FWD <= cg <= CG_AFT
    is_bag_safe = bags <= 100.0
    
    if is_weight_safe and is_cg_safe and is_bag_safe:
        st.success("✅ SAFE FOR FLIGHT")
    elif is_weight_safe and is_cg_safe and not is_bag_safe:
        st.warning("⚠️ WITHIN ENVELOPE - BAGGAGE STRUCTURAL LIMIT EXCEEDED")
    else:
        st.error("❌ NOT SAFE FOR FLIGHT")

    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Weight", f"{total_weight:.1f} lbs", f"{MTOW - total_weight:.1f} lbs rem", delta_color="normal")
    m2.metric("C.G. Location", f"{cg:.2f} in")
    m3.metric("Max Gross", f"{MTOW} lbs")

    # --- PLOT ---
    fig, ax = plt.subplots(figsize=(6, 4))
    env_x = [CG_FWD, CG_FWD, CG_AFT, CG_AFT, CG_FWD]
    env_y = [1000, MTOW, MTOW, 1000, 1000]
    ax.plot(env_x, env_y, 'g-', label="Normal Envelope")
    ax.scatter(cg, total_weight, color='red' if not (is_weight_safe and is_cg_safe) else 'blue', s=100)
    ax.set_xlabel("C.G. (Inches Aft of Datum)")
    ax.set_ylabel("Weight (lbs)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

# --- TABLE ---
st.header("3. Loading Manifest")

st.table(df.style.format({"Weight": "{:.2f}", "Arm": "{:.2f}", "Moment": "{:.2f}"}))
