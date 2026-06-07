import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Co-Digestion Simulator", layout="wide", initial_sidebar_state="collapsed")

# 2. Modern UI & Motion Graphics CSS Injection
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    h1, h2, h3, h4 { color: #0F172A !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 800; }
    p, label { color: #334155 !important; font-weight: 500; }
    
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .kpi-card {
        animation: fadeInUp 0.6s ease-out forwards;
        background: #FFFFFF; padding: 24px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); text-align: center;
        margin-bottom: 20px; border: 1px solid #E2E8F0; transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .kpi-card:hover { transform: translateY(-5px); }
    
    .kpi-title { font-size: 14px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 36px; font-weight: 900; margin-top: 8px; }

    .card-methane:hover { box-shadow: 0 10px 20px -5px rgba(255, 152, 0, 0.3); border-bottom: 4px solid #FF9800; }
    .val-methane { color: #FF9800; }
    .card-energy:hover { box-shadow: 0 10px 20px -5px rgba(33, 150, 243, 0.3); border-bottom: 4px solid #2196F3; }
    .val-energy { color: #2196F3; }
    .card-carbon:hover { box-shadow: 0 10px 20px -5px rgba(76, 175, 80, 0.3); border-bottom: 4px solid #4CAF50; }
    .val-carbon { color: #4CAF50; }
    .card-revenue:hover { box-shadow: 0 10px 20px -5px rgba(156, 39, 176, 0.3); border-bottom: 4px solid #9C27B0; }
    .val-revenue { color: #9C27B0; }

    .alert-box { animation: fadeInUp 0.5s ease-out forwards; padding: 16px 20px; border-radius: 8px; font-weight: 600; margin-bottom: 15px; }
    .alert-green { background-color: #ECFDF5; border-left: 5px solid #10B981; color: #065F46; }
    .alert-red { background-color: #FEF2F2; border-left: 5px solid #EF4444; color: #991B1B; }
    .alert-yellow { background-color: #FFFBEB; border-left: 5px solid #F59E0B; color: #92400E; }
    
    .back-btn > button { background-color: #FFFFFF; color: #0F172A; border: 1px solid #CBD5E1; border-radius: 8px; padding: 5px 15px; font-weight: bold; }
    .back-btn > button:hover { background-color: #F1F5F9; border-color: #94A3B8; }
    
    .ratio-box { background-color: #E2E8F0; padding: 10px; border-radius: 6px; text-align: center; font-size: 14px; font-weight: bold; color: #334155; }
</style>
""", unsafe_allow_html=True)

# 3. Navigation Header
st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
if st.button("⬅ Return to Overview"):
    st.switch_page("microbial_app.py")
st.markdown("</div>", unsafe_allow_html=True)

st.title("Co-Digestion Stoichiometric Simulator")
st.markdown("<p>Define your total batch size and input relative feedstock amounts. The system automatically normalizes the ratios based on Wet Mass.</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Data Dictionary (Stoichiometric Baseline)
feedstocks = {
    "Rice Husk": {"yield": 0.102, "C": 37.7, "N": 0.43, "lignin": 18.6},
    "Cow Dung": {"yield": 0.207, "C": 43.3, "N": 1.73, "lignin": 11.8},
    "Food Waste": {"yield": 0.392, "C": 47.1, "N": 3.25, "lignin": 3.0},
    "Poultry Waste": {"yield": 0.174, "C": 32.2, "N": 3.88, "lignin": 7.9}
}

# 5. UI: Master Inputs
col_batch, col_empty = st.columns([1, 3])
with col_batch:
    batch_mass_kg = st.number_input("Total Batch Mass (kg Wet Weight)", min_value=1.0, value=1000.0, step=100.0)

st.markdown("### Relative Feedstock Mix")
st.markdown("<p style='font-size: 14px; color: #64748B !important;'>Enter any values. ", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: rh_input = st.number_input("Rice Husk (Relative)", min_value=0.0, value=70.0)
with col2: cd_input = st.number_input("Cow Dung (Relative)", min_value=0.0, value=30.0)
with col3: fw_input = st.number_input("Food Waste (Relative)", min_value=0.0, value=0.0)
with col4: pw_input = st.number_input("Poultry Waste (Relative)", min_value=0.0, value=0.0)

total_input = rh_input + cd_input + fw_input + pw_input

# 6. Auto-Normalization Engine
if total_input == 0:
    st.info("Please input at least one feedstock value to begin the simulation.")
else:
    # Calculate exact fractions seamlessly
    f_rh, f_cd, f_fw, f_pw = rh_input/total_input, cd_input/total_input, fw_input/total_input, pw_input/total_input

    # Display the calculated actual percentages to the user so they see the result
    st.markdown(f"""
    <div style='display: flex; gap: 10px; margin-bottom: 20px;'>
        <div class='ratio-box' style='flex: 1; border-bottom: 3px solid #81C784;'>🌾 {f_rh*100:.1f}% Rice Husk</div>
        <div class='ratio-box' style='flex: 1; border-bottom: 3px solid #795548;'>🐄 {f_cd*100:.1f}% Cow Dung</div>
        <div class='ratio-box' style='flex: 1; border-bottom: 3px solid #FFB74D;'>🍎 {f_fw*100:.1f}% Food Waste</div>
        <div class='ratio-box' style='flex: 1; border-bottom: 3px solid #E0E0E0;'>🐔 {f_pw*100:.1f}% Poultry Waste</div>
    </div>
    """, unsafe_allow_html=True)

    # Mass Balance Calculations
    blend_C = sum([f_rh*feedstocks["Rice Husk"]["C"], f_cd*feedstocks["Cow Dung"]["C"], f_fw*feedstocks["Food Waste"]["C"], f_pw*feedstocks["Poultry Waste"]["C"]])
    blend_N = sum([f_rh*feedstocks["Rice Husk"]["N"], f_cd*feedstocks["Cow Dung"]["N"], f_fw*feedstocks["Food Waste"]["N"], f_pw*feedstocks["Poultry Waste"]["N"]])
    blend_CN = blend_C / blend_N if blend_N > 0 else 0
    
    # Linear Performance Model mapped to actual user batch size
    weighted_yield = sum([f_rh*feedstocks["Rice Husk"]["yield"], f_cd*feedstocks["Cow Dung"]["yield"], f_fw*feedstocks["Food Waste"]["yield"], f_pw*feedstocks["Poultry Waste"]["yield"]])
    
    methane_produced = weighted_yield * batch_mass_kg
    energy_kwh = methane_produced * 10
    co2_saved = methane_produced * 2
    revenue = energy_kwh * 8

    # 7. Biochemical Validation Layer
    st.markdown("### Microbial Health Diagnostics")
    
    if (f_fw * 100) > 40:
        st.markdown("<div class='alert-box alert-red'>CRITICAL WARNING: High Food Waste (>40%). Imminent risk of rapid Acidogenesis causing Volatile Fatty Acid (VFA) accumulation and Methanogen souring.</div>", unsafe_allow_html=True)
    
    if 25 <= blend_CN <= 30:
        st.markdown(f"<div class='alert-box alert-green'>OPTIMAL C:N RATIO ({blend_CN:.1f}): The stoichiometric environment is perfectly balanced for methanogenic cell synthesis.</div>", unsafe_allow_html=True)
    elif blend_CN < 15:
        st.markdown(f"<div class='alert-box alert-red'>TOXICITY RISK ({blend_CN:.1f} C:N): Ratio is too low. High probability of free ammonia (NH3) toxicity inhibiting methanogenic archaea.</div>", unsafe_allow_html=True)
    elif blend_CN > 35:
        st.markdown(f"<div class='alert-box alert-yellow'>NITROGEN STARVATION ({blend_CN:.1f} C:N): Ratio is too high. Microbes lack sufficient nitrogen for enzyme synthesis. Digestion will be prolonged.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='alert-box alert-yellow'>SUB-OPTIMAL C:N RATIO ({blend_CN:.1f}): Digestion is biologically viable but will not operate at peak kinetic efficiency.</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 8. Output KPIs
    st.markdown(f"### Predictive Outputs (Yield for {batch_mass_kg:,.0f} kg Batch)")
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
        <div class="kpi-card card-methane">
            <div class="kpi-title">Methane Yield</div>
            <div class="kpi-value val-methane">{methane_produced:,.1f} m³</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card card-energy" style="animation-delay: 0.1s;">
            <div class="kpi-title">Energy Output</div>
            <div class="kpi-value val-energy">{energy_kwh:,.0f} kWh</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card card-carbon" style="animation-delay: 0.2s;">
            <div class="kpi-title">Carbon Reduction</div>
            <div class="kpi-value val-carbon">{co2_saved:,.0f} kg CO₂</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card card-revenue" style="animation-delay: 0.3s;">
            <div class="kpi-title">Revenue Generated</div>
            <div class="kpi-value val-revenue">₹ {revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
       
        # --- NAVIGATION FOOTER ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_space, col_next = st.columns([4, 1])
    with col_next:
        if st.button("Proceed to Kinetics Engine \u2192", use_container_width=True):
            st.switch_page("pages/2_Microbial_Kinetics.py")