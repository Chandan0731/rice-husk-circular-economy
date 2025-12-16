import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Rice Husk Circular Economy", layout="wide")

# --- CUSTOM CSS (Styles) ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .metric-label { font-size: 14px; font-weight: bold; color: #555; }
    .metric-value { font-size: 24px; font-weight: bold; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.header("🚜 Farm Parameters")
area = st.sidebar.slider("Farm Area (Hectares)", 1, 50, 5)
yield_per_ha = st.sidebar.slider("Paddy Yield (kg/ha)", 2000, 8000, 4500)

st.sidebar.header("⚙️ Tech Parameters")
efficiency = st.sidebar.slider("Gasifier Efficiency (%)", 40, 90, 70) / 100
season_days = st.sidebar.number_input("Season Length (Days)", value=120)

# --- TEAMMATE'S SCIENTIFIC CONSTANTS ---
EF_FLOODED = 1.30  # kg CH4/ha/day
EF_AWD = 0.75      # kg CH4/ha/day
CV_HUSK = 14       # MJ/kg (Updated from 13.5)
BIOCHAR_YIELD = 0.25 # 25% (Updated from 20%)
PRICE_ELEC = 7.0   # INR/kWh
PRICE_CHAR = 15.0  # INR/kg
PRICE_CARBON_CREDIT = 2500 # INR per ton CO2e

# --- CALCULATIONS ---
# 1. Mass Balance
total_paddy = area * yield_per_ha
husk_mass = total_paddy * 0.22  # 22% of paddy is husk

# 2. Energy Model
energy_mj = husk_mass * CV_HUSK * efficiency
energy_kwh = energy_mj / 3.6

# 3. Biochar Model
biochar_mass = husk_mass * BIOCHAR_YIELD

# 4. Methane & Carbon Credit Model (New!)
methane_flooded = EF_FLOODED * area * season_days
methane_awd = EF_AWD * area * season_days
methane_avoided = methane_flooded - methane_awd  # kg CH4
co2_eq_tons = (methane_avoided * 28) / 1000      # GWP of Methane is 28
revenue_carbon = co2_eq_tons * PRICE_CARBON_CREDIT

# 5. Financials
revenue_elec = energy_kwh * PRICE_ELEC
revenue_char = biochar_mass * PRICE_CHAR
total_revenue = revenue_elec + revenue_char + revenue_carbon

# --- DASHBOARD LAYOUT ---
st.title("🌾 Rice Husk Circular Economy Simulator")
st.markdown("### Real-time Impact Assessment with AWD Integration")

# Row 1: Key Impacts
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">⚡ Net Energy Output</div>
        <div class="metric-value">{int(energy_kwh):,} kWh</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card" style="border-left: 5px solid #FFD700;">
        <div class="metric-label">🔥 Biochar Production</div>
        <div class="metric-value">{int(biochar_mass):,} kg</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card" style="border-left: 5px solid #FF4B4B;">
        <div class="metric-label">💨 Methane Avoided</div>
        <div class="metric-value">{int(methane_avoided):,} kg</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card" style="border-left: 5px solid #1E90FF;">
        <div class="metric-label">💰 Total Revenue</div>
        <div class="metric-value">₹ {int(total_revenue):,}</div>
        <small>Includes Carbon Credits</small>
    </div>""", unsafe_allow_html=True)

st.divider()

# --- GRAPHS SECTION ---
col_left, col_right = st.columns(2)

# GRAPH 1: Flooded vs AWD Comparison
with col_left:
    st.subheader("📉 Emissions Comparison")
    fig, ax = plt.subplots()
    labels = ['Flooded Field', 'AWD Practice']
    values = [methane_flooded, methane_awd]
    colors = ['#ff9999', '#66b3ff']
    
    ax.bar(labels, values, color=colors)
    ax.set_ylabel('Methane Emissions (kg)')
    ax.set_title(f'Emission Reduction for {area} Ha Farm')
    
    # Add labels on top of bars
    for i, v in enumerate(values):
        ax.text(i, v + (max(values)*0.01), f"{int(v)} kg", ha='center')
        
    st.pyplot(fig)

# GRAPH 2: Sensitivity Analysis (Scalability)
with col_right:
    st.subheader("📈 Scalability Analysis (1-50 Ha)")
    
    # Generate data for 1 to 50 hectares based on current sliders
    areas_range = np.arange(1, 51, 5) 
    # Logic: For each area step, calculate savings
    savings_range = (EF_FLOODED - EF_AWD) * areas_range * season_days * 28 / 1000 # Tons CO2eq
    revenue_range = (areas_range * yield_per_ha * 0.22 * CV_HUSK * efficiency / 3.6 * PRICE_ELEC)
    
    fig2, ax2 = plt.subplots()
    ax2.plot(areas_range, savings_range, marker='o', label='CO2 Offset (Tons)', color='green')
    
    # Create a second y-axis for Revenue to show both on one chart
    ax3 = ax2.twinx()
    ax3.plot(areas_range, revenue_range, marker='s', linestyle='--', label='Revenue (INR)', color='blue')
    
    ax2.set_xlabel('Farm Area (Hectares)')
    ax2.set_ylabel('CO2 Offset (Tons)', color='green')
    ax3.set_ylabel('Potential Revenue (INR)', color='blue')
    ax2.grid(True, alpha=0.3)
    
    st.pyplot(fig2)

# --- DETAILED DATA TABLE ---
st.markdown("### 📋 Detailed Simulation Data")
st.dataframe({
    "Parameter": ["Total Paddy", "Husk Quantity", "Methane Reduction", "Carbon Credits Earned"],
    "Value": [f"{total_paddy:,.0f} kg", f"{husk_mass:,.0f} kg", f"{methane_avoided:,.0f} kg", f"₹ {revenue_carbon:,.2f}"],
    "Unit": ["kg", "kg", "kg CH4", "INR"]
})