import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Rice Husk Circular Economy", layout="wide")

# --- CUSTOM CSS (Styles for Top Cards Only) ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #4CAF50;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-label { font-size: 16px; font-weight: 600; color: #666; margin-bottom: 5px; }
    .metric-value { font-size: 28px; font-weight: 700; color: #222; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.header("🚜 Farm Parameters")
area = st.sidebar.slider("Farm Area (Hectares)", 1, 50, 5)
yield_per_ha = st.sidebar.slider("Paddy Yield (kg/ha)", 2000, 8000, 4500)

st.sidebar.header("⚙️ Tech Parameters")
efficiency = st.sidebar.slider("Gasifier Efficiency (%)", 40, 90, 70) / 100
season_days = st.sidebar.number_input("Season Length (Days)", value=120)

# --- SCIENTIFIC CONSTANTS ---
EF_FLOODED = 1.30  # kg CH4/ha/day
EF_AWD = 0.75      # kg CH4/ha/day
CV_HUSK = 14       # MJ/kg
BIOCHAR_YIELD = 0.25 
PRICE_ELEC = 7.0   # INR/kWh
PRICE_CHAR = 15.0  # INR/kg
PRICE_CARBON_CREDIT = 2500 # INR per ton CO2e

# --- CALCULATIONS ---
# 1. Mass Balance
total_paddy = area * yield_per_ha
husk_mass = total_paddy * 0.22 

# 2. Energy Model
energy_mj = husk_mass * CV_HUSK * efficiency
energy_kwh = energy_mj / 3.6

# 3. Biochar Model
biochar_mass = husk_mass * BIOCHAR_YIELD

# 4. Methane & Carbon Credit Model
methane_flooded = EF_FLOODED * area * season_days
methane_awd = EF_AWD * area * season_days
methane_avoided = methane_flooded - methane_awd  # kg CH4
co2_eq_tons = (methane_avoided * 28) / 1000      # GWP = 28
revenue_carbon = co2_eq_tons * PRICE_CARBON_CREDIT

# 5. Financials
revenue_elec = energy_kwh * PRICE_ELEC
revenue_char = biochar_mass * PRICE_CHAR
total_revenue = revenue_elec + revenue_char + revenue_carbon

# --- DASHBOARD HEADER ---
st.title("🌾 Rice Husk Circular Economy Simulator")
st.markdown("### Integrated Bio-Energy & Carbon Mitigation System")
st.markdown("---")

# --- ROW 1: KEY IMPACT METRICS (The Cards) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚡ Net Energy Output</div>
        <div class="metric-value">{int(energy_kwh):,} kWh</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 6px solid #FFD700;">
        <div class="metric-label">🔥 Biochar Yield</div>
        <div class="metric-value">{int(biochar_mass):,} kg</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 6px solid #FF4B4B;">
        <div class="metric-label">💨 Methane Avoided</div>
        <div class="metric-value">{int(methane_avoided):,} kg</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 6px solid #1E90FF;">
        <div class="metric-label">💰 Total Revenue</div>
        <div class="metric-value">₹ {int(total_revenue):,}</div>
    </div>""", unsafe_allow_html=True)

# --- ROW 2: GRAPHS WITH EXPLANATIONS ---
col_left, col_right = st.columns(2)

# GRAPH 1: Flooded vs AWD
with col_left:
    st.subheader("📉 Emissions Analysis")
    fig, ax = plt.subplots(figsize=(5,3.5))
    labels = ['Flooded (Conventional)', 'AWD (Proposed)']
    values = [methane_flooded, methane_awd]
    colors = ['#ff9999', '#66b3ff']
    
    ax.bar(labels, values, color=colors, width=0.6)
    ax.set_ylabel('Methane Emissions (kg)')
    ax.set_title(f'Reduction Potential (Season: {season_days} days)')
    
    # Labels
    for i, v in enumerate(values):
        ax.text(i, v + (max(values)*0.02), f"{int(v)} kg", ha='center', fontweight='bold')
    
    st.pyplot(fig)
    
    # Explanation Box
    st.info("""
    **Analysis:** The blue bar (AWD) shows the reduced emissions compared to the red bar (Flooded).
    """)

# GRAPH 2: Scalability
with col_right:
    st.subheader("📈 Scalability & Revenue")
    
    areas_range = np.arange(1, 51, 5) 
    savings_range = (EF_FLOODED - EF_AWD) * areas_range * season_days * 28 / 1000 
    revenue_range = (areas_range * yield_per_ha * 0.22 * CV_HUSK * efficiency / 3.6 * PRICE_ELEC)
    
    fig2, ax2 = plt.subplots(figsize=(5,3.5))
    ax2.plot(areas_range, savings_range, marker='o', label='CO2 Offset (Tons)', color='green', linewidth=2)
    
    ax3 = ax2.twinx()
    ax3.plot(areas_range, revenue_range, marker='s', linestyle='--', label='Revenue (INR)', color='blue', linewidth=2)
    
    ax2.set_xlabel('Farm Area (Hectares)')
    ax2.set_ylabel('CO2 Offset (Tons)', color='green', fontweight='bold')
    ax3.set_ylabel('Revenue (INR)', color='blue', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    st.pyplot(fig2)
    
    # Explanation Box
    st.info("""
    **Analysis:** As farm area increases, both Carbon Savings (Green) and Revenue (Blue) increase linearly.
    """)

st.markdown("---")

# --- ROW 3: STANDARD SUMMARY REPORT (Clean Table) ---
st.subheader("📋 Project Impact Report")

# Create a simple, clean dictionary for the data
data = {
    "Metric": [
        "Input Biomass (Rice Husk)",
        "Clean Energy Generated", 
        "Biochar Produced",
        "Methane (CH4) Avoided",
        "CO2 Equivalent Saved",
        "Carbon Credit Revenue",
        "Electricity Revenue",
        "Biochar Revenue",
        "TOTAL SEASONAL PROFIT"
    ],
    "Value": [
        f"{husk_mass:,.0f}",
        f"{energy_kwh:,.2f}",
        f"{biochar_mass:,.0f}",
        f"{methane_avoided:,.0f}",
        f"{co2_eq_tons:,.3f}",
        f"₹ {revenue_carbon:,.2f}",
        f"₹ {revenue_elec:,.2f}",
        f"₹ {revenue_char:,.2f}",
        f"₹ {total_revenue:,.2f}"
    ],
    "Unit": [
        "kg",
        "kWh",
        "kg",
        "kg",
        "Tons",
        "INR",
        "INR",
        "INR",
        "INR"
    ]
}

# Convert to DataFrame
df_report = pd.DataFrame(data)

# Display as a static table (Looks like a printed report)
st.table(df_report)

# Footer
st.caption("Simulation powered by Python & Streamlit | Data Source: Standard Emission Factors (IPCC 2019)")