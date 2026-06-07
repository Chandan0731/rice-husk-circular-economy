import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# 1. Page Configuration
st.set_page_config(page_title="Kinetics Engine", layout="wide", initial_sidebar_state="collapsed")

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

    .animated-container { animation: fadeInUp 0.6s ease-out forwards; }

    .insight-card {
        background: #FFFFFF; padding: 24px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px; border: 1px solid #E2E8F0;
        border-left: 5px solid #2E7D32;
    }
    
    .insight-title { font-size: 14px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
    .insight-value { font-size: 24px; font-weight: 800; color: #0F172A; margin-top: 8px; }
    .insight-text { font-size: 14px; color: #334155; margin-top: 4px; }

    .nav-btn > button { background-color: #FFFFFF; color: #0F172A; border: 1px solid #CBD5E1; border-radius: 8px; padding: 5px 15px; font-weight: bold; }
    .nav-btn > button:hover { background-color: #F1F5F9; border-color: #94A3B8; }
</style>
""", unsafe_allow_html=True)

# 3. Navigation Header
st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
if st.button("\u2190 Return to Co-Digestion Simulator"):
    st.switch_page("pages/1_Co_Digestion_Simulator.py")
st.markdown("</div>", unsafe_allow_html=True)

st.title("Microbial Kinetics Engine")
st.markdown("<p>Time-series cumulative methane generation modeled via the Modified Gompertz Equation.</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Mathematical Basis
with st.expander("View Mathematical Basis"):
    st.markdown("The predictive engine utilizes the Modified Gompertz Equation to map biological constraints against standard stoichiometric limits:")
    st.latex(r"M(t) = P \cdot \exp\left(-\exp\left[\frac{R_m \cdot e}{P}(\lambda - t) + 1\right]\right)")
    st.markdown("""
    * **M(t)**: Cumulative methane yield at time *t*
    * **P**: Maximum methane potential (Theoretical Yield)
    * **R_m**: Maximum methane production rate (Peak Methanogenic Velocity)
    * **λ (Lambda)**: Lag phase duration (Hydrolytic Lignin Barrier)
    """)

# 5. Data Dictionary
feedstocks = {
    "Rice Husk": {"yield": 0.102, "C": 37.7, "N": 0.43, "lignin": 18.6},
    "Cow Dung": {"yield": 0.207, "C": 43.3, "N": 1.73, "lignin": 11.8},
    "Food Waste": {"yield": 0.392, "C": 47.1, "N": 3.25, "lignin": 3.0},
    "Poultry Waste": {"yield": 0.174, "C": 32.2, "N": 3.88, "lignin": 7.9}
}

# 6. UI: Inputs
st.markdown("<div class='animated-container'>", unsafe_allow_html=True)
col_batch, col_empty = st.columns([1, 3])
with col_batch:
    batch_mass_kg = st.number_input("Total Batch Mass (kg Wet Weight)", min_value=1.0, value=1000.0, step=100.0)

st.markdown("### Relative Feedstock Mix")
col1, col2, col3, col4 = st.columns(4)
with col1: rh_input = st.number_input("Rice Husk", min_value=0.0, value=70.0)
with col2: cd_input = st.number_input("Cow Dung", min_value=0.0, value=30.0)
with col3: fw_input = st.number_input("Food Waste", min_value=0.0, value=0.0)
with col4: pw_input = st.number_input("Poultry Waste", min_value=0.0, value=0.0)
st.markdown("</div>", unsafe_allow_html=True)

total_input = rh_input + cd_input + fw_input + pw_input

# 7. Kinetic Engine
if total_input == 0:
    st.info("Input batch parameters to initialize the kinetic engine.")
else:
    f_rh, f_cd, f_fw, f_pw = rh_input/total_input, cd_input/total_input, fw_input/total_input, pw_input/total_input

    blend_C = sum([f_rh*feedstocks["Rice Husk"]["C"], f_cd*feedstocks["Cow Dung"]["C"], f_fw*feedstocks["Food Waste"]["C"], f_pw*feedstocks["Poultry Waste"]["C"]])
    blend_N = sum([f_rh*feedstocks["Rice Husk"]["N"], f_cd*feedstocks["Cow Dung"]["N"], f_fw*feedstocks["Food Waste"]["N"], f_pw*feedstocks["Poultry Waste"]["N"]])
    blend_CN = blend_C / blend_N if blend_N > 0 else 0
    blend_lignin = sum([f_rh*feedstocks["Rice Husk"]["lignin"], f_cd*feedstocks["Cow Dung"]["lignin"], f_fw*feedstocks["Food Waste"]["lignin"], f_pw*feedstocks["Poultry Waste"]["lignin"]])
    
    weighted_yield = sum([f_rh*feedstocks["Rice Husk"]["yield"], f_cd*feedstocks["Cow Dung"]["yield"], f_fw*feedstocks["Food Waste"]["yield"], f_pw*feedstocks["Poultry Waste"]["yield"]])
    
    P = weighted_yield * batch_mass_kg
    lam = 1.0 + (blend_lignin * 0.4)
    cn_penalty = abs(25 - blend_CN) / 25
    base_rate = P / 15.0 
    R_m = base_rate * max(0.2, (1.0 - cn_penalty)) 

    # 8. Time Series Generation
    t_days = np.arange(0, 31, 1)
    
    if P > 0:
        methane_curve = P * np.exp(-np.exp((R_m * np.e / P) * (lam - t_days) + 1))
    else:
        methane_curve = np.zeros(31)

    # Note: We no longer set the index here so Altair can read both columns cleanly
    chart_data = pd.DataFrame({
        "Time (Days)": t_days,
        "Cumulative Methane (m³)": methane_curve
    })

    st.markdown("---")
    
    # 9. Dashboard Layout
    graph_col, insights_col = st.columns([2, 1])
    
    with graph_col:
        st.markdown("### 30-Day Accumulation Curve")
        
        # EXPLICIT ALTAIR CHART WITH FORCED AXIS LABELS AND HOVER TOOLTIPS
        kinetic_chart = alt.Chart(chart_data).mark_line(
            color="#10B981", 
            strokeWidth=4
        ).encode(
            x=alt.X('Time (Days)', title='Time (Days)', axis=alt.Axis(titleFontWeight='bold', titleFontSize=14, labelFontSize=12)),
            y=alt.Y('Cumulative Methane (m³)', title='Cumulative Methane (m³)', axis=alt.Axis(titleFontWeight='bold', titleFontSize=14, labelFontSize=12)),
            tooltip=[alt.Tooltip('Time (Days)'), alt.Tooltip('Cumulative Methane (m³)', format='.2f')]
        ).properties(
            height=400
        ).interactive() # Allows zooming and panning
        
        st.altair_chart(kinetic_chart, use_container_width=True)
        
    with insights_col:
        st.markdown("### Kinetic Parameters")
        
        st.markdown(f"""
        <div class="insight-card animated-container">
            <div class="insight-title">Lag Phase (λ)</div>
            <div class="insight-value">{lam:.1f} Days</div>
            <div class="insight-text">Time required for biological breakdown of the {blend_lignin:.1f}% Lignin matrix.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="insight-card animated-container" style="animation-delay: 0.1s; border-left-color: #2196F3;">
            <div class="insight-title">Peak Velocity (R_m)</div>
            <div class="insight-value">{R_m:.1f} m³/day</div>
            <div class="insight-text">Maximum daily production constraint based on current C:N metabolic efficiency.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-card animated-container" style="animation-delay: 0.2s; border-left-color: #FF9800;">
            <div class="insight-title">Maximum Potential (P)</div>
            <div class="insight-value">{P:.1f} m³</div>
            <div class="insight-text">Absolute limit of yield prior to substrate exhaustion.</div>
        </div>
        """, unsafe_allow_html=True)

    # Navigation Footer to Module 3
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_space, col_next = st.columns([4, 1])
    with col_next:
        if st.button("Proceed to Process Optimizer \u2192", use_container_width=True):
            st.switch_page("pages/3_Process_Optimizer.py")