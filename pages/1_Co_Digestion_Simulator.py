import streamlit as st
import pandas as pd

st.set_page_config(page_title="Co-Digestion Simulator", layout="wide")

# --- CSS INJECTION FOR CUSTOM KPI CARDS ---
st.markdown("""
<style>
    .stApp { background-color: #F5F9F6; }
    h1, h2, h3 { color: #2E7D32 !important; }
    
    /* KPI Card Styles */
    .kpi-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .kpi-title { font-size: 16px; font-weight: bold; color: #555555; text-transform: uppercase; }
    .kpi-value { font-size: 32px; font-weight: bold; margin-top: 10px; }
    
    /* Specific Colors requested by user */
    .color-methane { color: #FF9800; }
    .color-energy { color: #2196F3; }
    .color-carbon { color: #4CAF50; }
    .color-revenue { color: #9C27B0; }
    
    /* Alert Styles */
    .alert-green { background-color: #E8F5E9; border-left: 5px solid #4CAF50; padding: 15px; border-radius: 4px; color: #2E7D32; font-weight: bold;}
    .alert-red { background-color: #FFEBEE; border-left: 5px solid #F44336; padding: 15px; border-radius: 4px; color: #C62828; font-weight: bold;}
    .alert-yellow { background-color: #FFF8E1; border-left: 5px solid #FFC107; padding: 15px; border-radius: 4px; color: #F57F17; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- DATA DICTIONARY (From Cleaned Master) ---
# Format: [Methane Yield, Carbon %, Nitrogen %, Lignin %]
feedstocks = {
    "Rice Husk": {"yield": 0.102, "C": 37.7, "N": 0.43, "lignin": 18.6},
    "Cow Dung": {"yield": 0.207, "C": 43.3, "N": 1.73, "lignin": 11.8},
    "Food Waste": {"yield": 0.392, "C": 47.1, "N": 3.25, "lignin": 3.0},
    "Poultry Waste": {"yield": 0.174, "C": 32.2, "N": 3.88, "lignin": 7.9}
}

st.title("Co-Digestion Stoichiometric Simulator")
st.markdown("Adjust feedstock ratios to optimize microbial metabolic conditions and predict output.")

# --- UI: SLIDERS ---
st.markdown("### Feedstock Composition (%)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    rh_pct = st.number_input("Rice Husk", min_value=0, max_value=100, value=70)
with col2:
    cd_pct = st.number_input("Cow Dung", min_value=0, max_value=100, value=30)
with col3:
    fw_pct = st.number_input("Food Waste", min_value=0, max_value=100, value=0)
with col4:
    pw_pct = st.number_input("Poultry Waste", min_value=0, max_value=100, value=0)

total_pct = rh_pct + cd_pct + fw_pct + pw_pct

# --- VALIDATION AND CALCULATION BLOCK ---
if total_pct != 100:
    st.error(f"Total composition must equal 100%. Current total: {total_pct}%")
else:
    # Fractions
    f_rh, f_cd, f_fw, f_pw = rh_pct/100, cd_pct/100, fw_pct/100, pw_pct/100

    # 1. Biological Mass Balance Calculations
    blend_C = (f_rh * feedstocks["Rice Husk"]["C"] + f_cd * feedstocks["Cow Dung"]["C"] + 
               f_fw * feedstocks["Food Waste"]["C"] + f_pw * feedstocks["Poultry Waste"]["C"])
    
    blend_N = (f_rh * feedstocks["Rice Husk"]["N"] + f_cd * feedstocks["Cow Dung"]["N"] + 
               f_fw * feedstocks["Food Waste"]["N"] + f_pw * feedstocks["Poultry Waste"]["N"])
    
    blend_CN = blend_C / blend_N if blend_N > 0 else 0
    blend_lignin = (f_rh * feedstocks["Rice Husk"]["lignin"] + f_cd * feedstocks["Cow Dung"]["lignin"] + 
                    f_fw * feedstocks["Food Waste"]["lignin"] + f_pw * feedstocks["Poultry Waste"]["lignin"])

    # 2. Linear Performance Model
    weighted_yield = (f_rh * feedstocks["Rice Husk"]["yield"] + 
                      f_cd * feedstocks["Cow Dung"]["yield"] + 
                      f_fw * feedstocks["Food Waste"]["yield"] + 
                      f_pw * feedstocks["Poultry Waste"]["yield"])
    
    feedstock_mass_kg = 1000 # Base assumption
    methane_produced = weighted_yield * feedstock_mass_kg
    energy_kwh = methane_produced * 10
    co2_saved = methane_produced * 2
    revenue = energy_kwh * 8

    # --- BIOCHEMICAL VALIDATION LAYER (The Core Defense) ---
    st.markdown("### Microbial Health Diagnostics")
    
    # Check 1: VFA Souring (Food Waste Limit)
    if fw_pct > 40:
        st.markdown("<div class='alert-red'>CRITICAL WARNING: High Food Waste (>40%). Imminent risk of rapid Acidogenesis causing Volatile Fatty Acid (VFA) accumulation and Methanogen souring.</div>", unsafe_allow_html=True)
    
    # Check 2: C:N Stoichiometry
    if 25 <= blend_CN <= 30:
        st.markdown(f"<div class='alert-green'>OPTIMAL C:N RATIO ({blend_CN:.1f}): The stoichiometric environment is perfectly balanced for methanogenic cell synthesis.</div>", unsafe_allow_html=True)
    elif blend_CN < 15:
        st.markdown(f"<div class='alert-red'>TOXICITY RISK ({blend_CN:.1f} C:N): Ratio is too low. High probability of free ammonia (NH3) toxicity inhibiting methanogenic archaea.</div>", unsafe_allow_html=True)
    elif blend_CN > 35:
        st.markdown(f"<div class='alert-yellow'>NITROGEN STARVATION ({blend_CN:.1f} C:N): Ratio is too high. Microbes lack sufficient nitrogen for enzyme synthesis. Digestion will be severely prolonged.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='alert-yellow'>SUB-OPTIMAL C:N RATIO ({blend_CN:.1f}): Digestion is biologically viable but will not operate at peak kinetic efficiency.</div>", unsafe_allow_html=True)

    st.markdown("---")

    # --- OUTPUT KPIs (Custom Colors) ---
    st.markdown("### Predictive Outputs (per 1,000 kg Feedstock)")
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Methane Yield</div>
            <div class="kpi-value color-methane">{methane_produced:.1f} m³</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Energy Output</div>
            <div class="kpi-value color-energy">{energy_kwh:.0f} kWh</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Carbon Reduction</div>
            <div class="kpi-value color-carbon">{co2_saved:.0f} kg CO2</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Revenue Generated</div>
            <div class="kpi-value color-revenue">₹ {revenue:.0f}</div>
        </div>
        """, unsafe_allow_html=True)