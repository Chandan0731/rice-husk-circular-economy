import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# 1. Page Configuration
st.set_page_config(page_title="Kinetics Engine", layout="wide", initial_sidebar_state="collapsed")

# 2. Professional CSS Injection
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

    .info-block {
        background-color: #FFFFFF; padding: 24px; border-radius: 8px;
        border: 1px solid #E2E8F0; border-top: 4px solid #0F172A;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px;
    }
    .info-title { font-size: 18px; font-weight: 800; color: #0F172A; margin-bottom: 10px; }
    .info-text { font-size: 14px; color: #475569; line-height: 1.6; }
    
    .sig-block {
        background-color: #F0FDF4; padding: 20px; border-radius: 8px;
        border-left: 5px solid #16A34A; margin-top: 15px;
    }
    .sig-title { font-size: 15px; font-weight: 800; color: #166534; text-transform: uppercase; margin-bottom: 5px;}
    .sig-text { font-size: 14px; color: #15803D; font-weight: 600; line-height: 1.5;}

    .insight-card {
        background: #FFFFFF; padding: 24px; border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #E2E8F0;
        border-left: 5px solid #2E7D32; text-align: center;
    }
    .insight-title { font-size: 13px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
    .insight-value { font-size: 28px; font-weight: 900; color: #0F172A; margin-top: 8px; }
    
    .nav-btn > button { background-color: #FFFFFF; color: #0F172A; border: 1px solid #CBD5E1; border-radius: 6px; padding: 4px 12px; font-weight: bold; }
    .nav-btn > button:hover { background-color: #F1F5F9; border-color: #94A3B8; }
</style>
""", unsafe_allow_html=True)

# 3. Navigation Header
st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
if st.button("Return to Co-Digestion Simulator"):
    st.switch_page("pages/1_Co_Digestion_Simulator.py")
st.markdown("</div>", unsafe_allow_html=True)

st.title("Microbial Kinetics Engine")
st.markdown("---")

# 4. State Management validation
if 'f_rh' not in st.session_state:
    st.warning("Awaiting Configuration: Please return to the Co-Digestion Simulator and configure your batch.")
    st.stop()

# Silently load variables mapped perfectly from Page 1
batch_mass_kg = st.session_state['batch_mass_kg']
f_rh = st.session_state['f_rh']
f_cd = st.session_state['f_cd']
f_fw = st.session_state['f_fw']
f_pw = st.session_state['f_pw']

# Data Dictionary
feedstocks = {
    "Rice Husk": {"yield": 0.102, "C": 37.7, "N": 0.43, "lignin": 18.6},
    "Cow Dung": {"yield": 0.207, "C": 43.3, "N": 1.73, "lignin": 11.8},
    "Food Waste": {"yield": 0.392, "C": 47.1, "N": 3.25, "lignin": 3.0},
    "Poultry Waste": {"yield": 0.174, "C": 32.2, "N": 3.88, "lignin": 7.9}
}

# 5. Kinetic Math Engine
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

t_days = np.arange(0, 61, 1)

if P > 0:
    methane_curve = P * np.exp(-np.exp((R_m * np.e / P) * (lam - t_days) + 1))
else:
    methane_curve = np.zeros(61)

chart_data = pd.DataFrame({
    "Time (Days)": t_days,
    "Cumulative Methane (m³)": methane_curve
})

# 6. Top Layout: Graph (Left) & Information (Right)
col_graph, col_info = st.columns([1.6, 1])

with col_graph:
    st.markdown("<div class='animated-container'>", unsafe_allow_html=True)
    kinetic_chart = alt.Chart(chart_data).mark_line(
        color="#10B981", strokeWidth=4
    ).encode(
        x=alt.X('Time (Days)', title='Digestion Time (60 Days)', axis=alt.Axis(titleFontWeight='bold', titleFontSize=13, grid=False)),
        y=alt.Y('Cumulative Methane (m³)', title='Cumulative Yield (m³)', axis=alt.Axis(titleFontWeight='bold', titleFontSize=13)),
        tooltip=[alt.Tooltip('Time (Days)'), alt.Tooltip('Cumulative Methane (m³)', format='.1f')]
    ).properties(height=420).interactive()
    
    st.altair_chart(kinetic_chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_info:
    st.markdown("<div class='animated-container'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-block">
        <div class="info-title">The Modified Gompertz Model</div>
        <div class="info-text">
            This graph simulates biological methanogenesis over a 60-day operational cycle. Rather than a simple linear progression, microbial gas production follows a strict <b>Sigmoidal (S-Curve)</b> pathway defined by three distinct phases:
            <br><br>
            <b>1. Hydrolytic Lag:</b> Initial flat period where microbes break down complex lignin.<br>
            <b>2. Exponential Growth:</b> Rapid upward curve driven by optimal C:N ratios.<br>
            <b>3. Substrate Exhaustion:</b> The top plateau where potential yield is maxed out.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sig-block">
        <div class="sig-title">Industrial Significance</div>
        <div class="sig-text">
            This predictive curve allows plant operators to schedule energy distribution. By identifying the exact day the reactor hits the "Exponential Plateau," operators know precisely when to harvest the biogas and flush the reactor for the next batch, minimizing downtime.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 7. Bottom Layout: Kinetic Parameters
st.markdown("### Process Kinetic Parameters")
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(f"""
    <div class="insight-card animated-container">
        <div class="insight-title">Lag Phase Barrier (λ)</div>
        <div class="insight-value">{lam:.1f} Days</div>
        <div style="font-size: 13px; color: #64748B; margin-top: 5px;">Time required to penetrate the {blend_lignin:.1f}% Lignin matrix.</div>
    </div>
    """, unsafe_allow_html=True)
    
with k2:
    st.markdown(f"""
    <div class="insight-card animated-container" style="animation-delay: 0.1s; border-left-color: #2196F3;">
        <div class="insight-title">Peak Velocity (R_m)</div>
        <div class="insight-value">{R_m:.1f} m³/day</div>
        <div style="font-size: 13px; color: #64748B; margin-top: 5px;">Max rate constrained by current C:N metabolic efficiency.</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="insight-card animated-container" style="animation-delay: 0.2s; border-left-color: #FF9800;">
        <div class="insight-title">Maximum Potential (P)</div>
        <div class="insight-value">{P:.0f} m³</div>
        <div style="font-size: 13px; color: #64748B; margin-top: 5px;">Absolute yield limit prior to total substrate exhaustion.</div>
    </div>
    """, unsafe_allow_html=True)

# Navigation Footer
st.markdown("<br><br>", unsafe_allow_html=True)
col_space, col_next = st.columns([4, 1])
with col_next:
    if st.button("Proceed to Process Optimizer \u2192", use_container_width=True):
        st.switch_page("pages/3_Process_Optimizer.py")