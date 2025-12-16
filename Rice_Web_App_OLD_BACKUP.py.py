import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Rice Husk Circular Economy Simulator",
    page_icon="🌾",
    layout="wide"
)

# --- 2. CSS STYLING (To make it look Modern) ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MATH ENGINE (From your Paper) ---
def calculate(area, paddy_yield, gasifier_eff):
    # Constants from SATEM-2025 Paper
    HUSK_RATIO = 0.22      # Ref [5]
    LHV = 13.5             # MJ/kg Ref [6]
    GEN_EFF = 0.30         # Ref [8]
    BIOCHAR_YIELD = 0.20   # Ref [10]
    EF_FLOODED = 30        # kg CH4/ha
    EF_AWD = 16            # kg CH4/ha
    PRICE_ELEC = 7.0       # INR/kWh
    PRICE_CHAR = 15.0      # INR/kg
    CAPEX_PER_KW = 80000   # INR

    # Calculations
    total_paddy = area * paddy_yield
    total_husk = total_paddy * HUSK_RATIO
    
    # Energy (Eq 2)
    energy_mj = total_husk * LHV * gasifier_eff * GEN_EFF
    energy_kwh = energy_mj / 3.6
    
    # Biochar (Eq 3)
    biochar_kg = total_husk * BIOCHAR_YIELD
    
    # Methane (Eq 1)
    ch4_saved = area * (EF_FLOODED - EF_AWD)
    co2_eq = ch4_saved * 28
    
    # Economics (Eq 4)
    capacity_kw = energy_kwh / 1000
    capex = max(capacity_kw, 5) * CAPEX_PER_KW
    revenue = (energy_kwh * PRICE_ELEC) + (biochar_kg * PRICE_CHAR)
    opex = capex * 0.10
    profit = revenue - opex
    
    if profit > 0:
        payback = capex / profit
    else:
        payback = 0
        
    return energy_kwh, biochar_kg, co2_eq, revenue, payback

# --- 4. THE INTERFACE ---
st.title("🌾 Rice Husk Circular Economy Simulator")
st.markdown("### Interactive Model based on SATEM-2025 Methodology")
st.markdown("---")

# Two Columns: Left for Controls, Right for Results
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.header("⚙️ Input Parameters")
    st.info("Adjust the sliders below to simulate different scenarios.")
    
    area = st.slider("Farm Area (Hectares)", 1, 100, 50)
    paddy_yield = st.slider("Paddy Yield (kg/ha)", 2000, 8000, 4500)
    eff = st.slider("Gasifier Efficiency (%)", 40, 90, 70) / 100
    
    st.markdown("---")
    st.caption("**Model Reference:** Mathematical Modelling for Conversion of Rice Husk into Energy mitigate methane gas emission.")

with col2:
    st.header("📊 Simulation Results")
    
    # Run the Math
    en, char, co2, rev, pb = calculate(area, paddy_yield, eff)
    
    # Row 1: Key Metrics
    c1, c2 = st.columns(2)
    c1.metric(label="⚡ Net Energy Output", value=f"{int(en):,} kWh")
    c2.metric(label="🌱 Biochar Produced", value=f"{int(char):,} kg")
    
    # Row 2: Environmental & Economic
    c3, c4 = st.columns(2)
    c3.metric(label="🌍 CO2 Equivalent Avoided", value=f"{int(co2):,} kg", delta="Positive Impact")
    c4.metric(label="💰 Annual Revenue", value=f"₹ {int(rev):,}")
    
    # Payback Highlight
    st.success(f"**📉 Estimated Payback Period:** {pb:.1f} Years")
    
    # Simple Chart
    st.bar_chart({
        "Energy (kWh)": en,
        "Biochar (kg)": char,
        "CO2 Saved (kg)": co2
    })