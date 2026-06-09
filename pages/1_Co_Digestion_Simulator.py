import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Co-Digestion Simulator", layout="wide", initial_sidebar_state="collapsed")

# 2. Strict Professional CSS Injection
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    h1, h2, h3, h4 { color: #0F172A !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 800; }
    p, label { color: #334155 !important; font-weight: 600; }
    
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .kpi-card {
        animation: fadeInUp 0.6s ease-out forwards;
        background: #FFFFFF; padding: 20px; border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); text-align: center;
        margin-bottom: 20px; border: 1px solid #E2E8F0; transition: transform 0.2s ease;
    }
    .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.08); }
    .kpi-title { font-size: 13px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 28px; font-weight: 900; margin-top: 5px; }

    .card-methane { border-bottom: 4px solid #FF9800; } .val-methane { color: #FF9800; }
    .card-energy { border-bottom: 4px solid #2196F3; } .val-energy { color: #2196F3; }
    .card-carbon { border-bottom: 4px solid #4CAF50; } .val-carbon { color: #4CAF50; }
    .card-revenue { border-bottom: 4px solid #9C27B0; } .val-revenue { color: #9C27B0; }

    .diag-container { animation: fadeInUp 0.5s ease-out forwards; margin-top: 15px; margin-bottom: 25px; }
    .alert-box { padding: 16px 20px; border-radius: 6px; font-weight: 700; font-size: 16px; margin-bottom: 12px; border: 1px solid #E2E8F0; }
    .alert-green { background-color: #F0FDF4; border-left: 6px solid #16A34A; color: #166534; }
    .alert-red { background-color: #FEF2F2; border-left: 6px solid #DC2626; color: #991B1B; }
    .alert-yellow { background-color: #FFFBEB; border-left: 6px solid #D97706; color: #92400E; }
    
    .back-btn > button { background-color: #FFFFFF; color: #0F172A; border: 1px solid #CBD5E1; border-radius: 6px; padding: 4px 12px; font-weight: bold; }
    .back-btn > button:hover { background-color: #F1F5F9; border-color: #94A3B8; }
    
    .ratio-box { background-color: #FFFFFF; padding: 10px; border-radius: 6px; text-align: center; font-size: 14px; font-weight: 800; color: #0F172A; border: 1px solid #E2E8F0; }
    .db-tag { font-size: 11px; color: #4CAF50; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: -10px; display: block;}
</style>
""", unsafe_allow_html=True)

# 3. Navigation Header
st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
if st.button("Return to Overview"):
    st.switch_page("microbial_app.py")
st.markdown("</div>", unsafe_allow_html=True)

st.title("Co-Digestion Stoichiometric Simulator")
st.markdown("<p>Define demographic origins and feedstock ratios to execute a biological mass-balance prediction.</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Agricultural Database Integration
try:
    df_rice = pd.read_csv("rice_varieties_india.csv")
except FileNotFoundError:
    st.error("Database Error: 'rice_varieties_india.csv' not found. Please ensure it is in the root directory.")
    st.stop()

# Biological Stoichiometry Baseline
feedstocks = {
    "Rice Husk": {"yield": 0.102, "C": 37.7, "N": 0.43, "lignin": 18.6},
    "Cow Dung": {"yield": 0.207, "C": 43.3, "N": 1.73, "lignin": 11.8},
    "Food Waste": {"yield": 0.392, "C": 47.1, "N": 3.25, "lignin": 3.0},
    "Poultry Waste": {"yield": 0.174, "C": 32.2, "N": 3.88, "lignin": 7.9}
}

# 5. UI: Demographics
st.markdown("<span class='db-tag'>Live Database Query Active</span>", unsafe_allow_html=True)
st.markdown("### 1. Location Demographics")

states = df_rice['State'].unique().tolist()
col_state, col_reg, col_var, col_batch = st.columns(4)

with col_state:
    selected_state = st.selectbox("State", states)
    
regions = df_rice[df_rice['State'] == selected_state]['Region'].unique().tolist()
with col_reg:
    selected_region = st.selectbox("Agricultural Region", regions)

varieties = df_rice[(df_rice['State'] == selected_state) & (df_rice['Region'] == selected_region)]['Variety'].tolist()
with col_var:
    selected_variety = st.selectbox("Rice Variety", varieties)

with col_batch:
    batch_mass_kg = st.number_input("Batch Mass (kg Wet)", min_value=1.0, value=1000.0, step=100.0)

trait = df_rice[(df_rice['Variety'] == selected_variety)]['Trait'].values[0]
st.caption(f"Database Record Found: **{selected_variety}** is characterized as *{trait}*.")
st.markdown("---")

# 6. UI: Sliders for Relative Feedstock Mix
st.markdown("### 2. Formulate Substrate Mixture")
st.markdown("<p style='font-size: 14px; color: #64748B !important;'>Adjust the sliders to define relative proportions.</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: rh_input = st.slider("Rice Husk", min_value=0, max_value=100, value=70, step=5)
with col2: cd_input = st.slider("Cow Dung", min_value=0, max_value=100, value=30, step=5)
with col3: fw_input = st.slider("Food Waste", min_value=0, max_value=100, value=0, step=5)
with col4: pw_input = st.slider("Poultry Waste", min_value=0, max_value=100, value=0, step=5)

total_input = rh_input + cd_input + fw_input + pw_input

# --- REAL-TIME SESSION STATE SAVING ---
if total_input > 0:
    st.session_state['batch_mass_kg'] = batch_mass_kg
    st.session_state['f_rh'] = rh_input / total_input
    st.session_state['f_cd'] = cd_input / total_input
    st.session_state['f_fw'] = fw_input / total_input
    st.session_state['f_pw'] = pw_input / total_input

# 7. Action Button
st.markdown("<br>", unsafe_allow_html=True)
col_btn, col_empty = st.columns([1, 3])
with col_btn:
    predict_triggered = st.button("Generate Predictive Result", type="primary", use_container_width=True)

# 8. Execution Engine
if predict_triggered:
    if total_input == 0:
        st.error("Please assign a value to at least one substrate slider before executing the prediction.")
    else:
        st.markdown("---")
        
        f_rh = st.session_state['f_rh']
        f_cd = st.session_state['f_cd']
        f_fw = st.session_state['f_fw']
        f_pw = st.session_state['f_pw']

        st.markdown("### Normalized Substrate Composition")
        st.markdown(f"""
        <div style='display: flex; gap: 10px; margin-bottom: 20px;'>
            <div class='ratio-box' style='flex: 1; border-bottom: 4px solid #81C784;'>Rice Husk: {f_rh*100:.1f}%</div>
            <div class='ratio-box' style='flex: 1; border-bottom: 4px solid #795548;'>Cow Dung: {f_cd*100:.1f}%</div>
            <div class='ratio-box' style='flex: 1; border-bottom: 4px solid #FFB74D;'>Food Waste: {f_fw*100:.1f}%</div>
            <div class='ratio-box' style='flex: 1; border-bottom: 4px solid #9E9E9E;'>Poultry Waste: {f_pw*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        blend_C = sum([f_rh*feedstocks["Rice Husk"]["C"], f_cd*feedstocks["Cow Dung"]["C"], f_fw*feedstocks["Food Waste"]["C"], f_pw*feedstocks["Poultry Waste"]["C"]])
        blend_N = sum([f_rh*feedstocks["Rice Husk"]["N"], f_cd*feedstocks["Cow Dung"]["N"], f_fw*feedstocks["Food Waste"]["N"], f_pw*feedstocks["Poultry Waste"]["N"]])
        blend_CN = blend_C / blend_N if blend_N > 0 else 0
        
        weighted_yield = sum([f_rh*feedstocks["Rice Husk"]["yield"], f_cd*feedstocks["Cow Dung"]["yield"], f_fw*feedstocks["Food Waste"]["yield"], f_pw*feedstocks["Poultry Waste"]["yield"]])
        
        methane_produced = weighted_yield * batch_mass_kg
        energy_kwh = methane_produced * 10
        co2_saved = methane_produced * 2
        revenue = energy_kwh * 8

        st.markdown("<div class='diag-container'>", unsafe_allow_html=True)
        st.markdown("### Biochemical Health Diagnostics")
        
        if (f_fw * 100) > 40:
            st.markdown("<div class='alert-box alert-red'>CRITICAL WARNING: High Food Waste (>40%). Imminent risk of rapid Acidogenesis causing Volatile Fatty Acid (VFA) accumulation and Methanogen souring.</div>", unsafe_allow_html=True)
        
        if 25 <= blend_CN <= 30:
            st.markdown(f"<div class='alert-box alert-green'>OPTIMAL ENVIRONMENT ({blend_CN:.1f} C:N Ratio) <br><span style='font-size:14px; font-weight:500;'>The stoichiometric balance is ideal for methanogenic cell synthesis and rapid digestion.</span></div>", unsafe_allow_html=True)
        elif blend_CN < 15:
            st.markdown(f"<div class='alert-box alert-red'>TOXICITY RISK ({blend_CN:.1f} C:N Ratio) <br><span style='font-size:14px; font-weight:500;'>Ratio is too low. High probability of free ammonia (NH3) toxicity completely inhibiting methanogenic archaea.</span></div>", unsafe_allow_html=True)
        elif blend_CN > 35:
            st.markdown(f"<div class='alert-box alert-yellow'>NITROGEN STARVATION ({blend_CN:.1f} C:N Ratio) <br><span style='font-size:14px; font-weight:500;'>Ratio is too high. Microbes lack sufficient nitrogen for enzyme synthesis. Process will be severely delayed.</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-box alert-yellow'>SUB-OPTIMAL ENVIRONMENT ({blend_CN:.1f} C:N Ratio) <br><span style='font-size:14px; font-weight:500;'>Digestion is biologically viable but will not operate at peak kinetic efficiency.</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"### Predictive Yield Analysis (Based on {batch_mass_kg:,.0f} kg Input)")
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
                <div class="kpi-value val-carbon">{co2_saved:,.0f} kg</div>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="kpi-card card-revenue" style="animation-delay: 0.3s;">
                <div class="kpi-title">Projected Revenue</div>
                <div class="kpi-value val-revenue">₹ {revenue:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

# Navigation Footer
st.markdown("<br><br>", unsafe_allow_html=True)
col_space, col_next = st.columns([4, 1])
with col_next:
    if st.button("Proceed to Kinetics Engine \u2192", use_container_width=True):
        st.switch_page("pages/2_Microbial_Kinetics.py")