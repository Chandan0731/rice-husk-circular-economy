import streamlit as st
import pandas as pd
import altair as alt

# 1. Page Configuration
st.set_page_config(page_title="Advanced Optimizer", layout="wide", initial_sidebar_state="collapsed")

# 2. Modern UI CSS Injection
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

    .kpi-card {
        background: #FFFFFF; padding: 24px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); text-align: center;
        margin-bottom: 20px; border: 1px solid #E2E8F0;
    }
    .kpi-title { font-size: 14px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 32px; font-weight: 900; margin-top: 8px; color: #10B981;}
    
    .recipe-box { background-color: #FFFFFF; padding: 15px; border-radius: 8px; border-left: 5px solid #2E7D32; font-size: 16px; font-weight: bold; color: #0F172A; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 10px;}
    
    .nav-btn > button { background-color: #FFFFFF; color: #0F172A; border: 1px solid #CBD5E1; border-radius: 8px; padding: 5px 15px; font-weight: bold; }
    .nav-btn > button:hover { background-color: #F1F5F9; border-color: #94A3B8; }
</style>
""", unsafe_allow_html=True)

# 3. Navigation Header
st.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
if st.button("\u2190 Return to Kinetics Engine"):
    st.switch_page("pages/2_Microbial_Kinetics.py")
st.markdown("</div>", unsafe_allow_html=True)

st.title("Supply Chain & Sensitivity Optimizer")
st.markdown("<p>Lock in real-world supply chain constraints to calculate the optimal metabolic intervention, mapped against a sensitivity envelope to visualize biological risk margins.</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Data Dictionary
feedstocks = {
    "Rice Husk": {"yield": 0.102, "C": 37.7, "N": 0.43, "lignin": 18.6},
    "Cow Dung": {"yield": 0.207, "C": 43.3, "N": 1.73, "lignin": 11.8},
    "Food Waste": {"yield": 0.392, "C": 47.1, "N": 3.25, "lignin": 3.0},
    "Poultry Waste": {"yield": 0.174, "C": 32.2, "N": 3.88, "lignin": 7.9}
}

# 5. UI: Supply Chain Constraint Input
st.markdown("### Part 1: Define Supply Chain Constraints")
st.markdown("In industrial operations, base substrates are often fixed by daily supply. Lock your primary Rice Husk base below.")

col_mass, col_lock = st.columns([1, 2])
with col_mass:
    batch_mass_kg = st.number_input("Total Processing Batch (kg)", min_value=100.0, value=1000.0, step=100.0)
with col_lock:
    rh_fixed = st.slider("Forced Rice Husk Baseline (%)", min_value=10, max_value=80, value=50, step=5)

st.markdown("---")

# 6. The Bounded Sweep & Sensitivity Engine
with st.spinner("Calculating sensitivity matrix and isolating intervention parameters..."):
    sweep_data = []
    best_formulation = None
    best_score = -999999
    
    # We sweep the remaining allowable percentage across Cow Dung and Food Waste
    # (Poultry Waste absorbs the remainder)
    for cd in range(0, 101 - rh_fixed, 5):
        for fw in range(0, 101 - rh_fixed - cd, 5):
            pw = 100 - rh_fixed - cd - fw
            
            f_rh, f_cd, f_fw, f_pw = rh_fixed/100, cd/100, fw/100, pw/100
            
            blend_C = sum([f_rh*feedstocks["Rice Husk"]["C"], f_cd*feedstocks["Cow Dung"]["C"], f_fw*feedstocks["Food Waste"]["C"], f_pw*feedstocks["Poultry Waste"]["C"]])
            blend_N = sum([f_rh*feedstocks["Rice Husk"]["N"], f_cd*feedstocks["Cow Dung"]["N"], f_fw*feedstocks["Food Waste"]["N"], f_pw*feedstocks["Poultry Waste"]["N"]])
            blend_CN = blend_C / blend_N if blend_N > 0 else 0
            
            weighted_yield = sum([f_rh*feedstocks["Rice Husk"]["yield"], f_cd*feedstocks["Cow Dung"]["yield"], f_fw*feedstocks["Food Waste"]["yield"], f_pw*feedstocks["Poultry Waste"]["yield"]])
            methane_produced = weighted_yield * batch_mass_kg
            
            # Categorize Biological State for the Heatmap
            if fw > 40:
                state = "CRITICAL: VFA Souring"
                is_viable = False
            elif blend_CN < 15:
                state = "CRITICAL: Ammonia Toxicity"
                is_viable = False
            elif blend_CN > 35:
                state = "WARNING: Nitrogen Starvation"
                is_viable = False
            elif 25 <= blend_CN <= 30:
                state = "OPTIMAL: Peak Methanogenesis"
                is_viable = True
            else:
                state = "VIABLE: Sub-Optimal"
                is_viable = True
                
            sweep_data.append({
                "Cow Dung (%)": cd,
                "Food Waste (%)": fw,
                "Poultry Waste (%)": pw,
                "C:N Ratio": round(blend_CN, 1),
                "Methane Yield": round(methane_produced, 1),
                "Biological State": state
            })
            
            # Isolate the absolute best viable formulation
            if is_viable and methane_produced > best_score:
                best_score = methane_produced
                best_formulation = (rh_fixed, cd, fw, pw, methane_produced, blend_CN)

    df_sweep = pd.DataFrame(sweep_data)

    # 7. Output: The Golden Intervention
    st.markdown("### Part 2: Algorithmic Intervention Output")
    
    if best_formulation:
        rh_opt, cd_opt, fw_opt, pw_opt, yield_opt, cn_opt = best_formulation
        
        col_recipe, col_metrics = st.columns([1, 1])
        
        with col_recipe:
            st.markdown("<p style='color: #64748B; font-weight: bold;'>REQUIRED CO-SUBSTRATE INTERVENTION</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='recipe-box' style='border-left-color: #94A3B8;'>Locked Rice Husk Base: {rh_opt}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='recipe-box'>Add Cow Dung: {cd_opt}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='recipe-box'>Add Food Waste: {fw_opt}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='recipe-box'>Add Poultry Waste: {pw_opt}%</div>", unsafe_allow_html=True)
            
        with col_metrics:
            st.markdown("<p style='color: #64748B; font-weight: bold;'>PREDICTED PERFORMANCE</p>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="kpi-card animated-container">
                <div class="kpi-title">Optimized C:N Target</div>
                <div class="kpi-value" style="color: #2196F3;">{cn_opt:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="kpi-card animated-container" style="animation-delay: 0.1s;">
                <div class="kpi-title">Maximized Yield</div>
                <div class="kpi-value" style="color: #FF9800;">{yield_opt:,.1f} m³</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("No biologically viable formulation exists with this high of a Rice Husk baseline. Reduce the forced constraint.")

    st.markdown("---")

    # 8. Output: The Sensitivity Heatmap
    st.markdown("### Part 3: Biological Sensitivity Envelope")
    st.markdown("This matrix maps the metabolic danger zones based on your remaining flexible mixture. *Green indicates biological viability; Reds/Oranges indicate toxicity risks.*")
    
    # Custom Altair Heatmap
    heatmap = alt.Chart(df_sweep).mark_rect().encode(
        x=alt.X('Cow Dung (%):O', title='Cow Dung Addition (%)', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Food Waste (%):O', title='Food Waste Addition (%)', sort='descending'),
        color=alt.Color('Biological State:N', 
            scale=alt.Scale(
                domain=['OPTIMAL: Peak Methanogenesis', 'VIABLE: Sub-Optimal', 'WARNING: Nitrogen Starvation', 'CRITICAL: VFA Souring', 'CRITICAL: Ammonia Toxicity'],
                range=['#10B981', '#81C784', '#F59E0B', '#EF4444', '#991B1B']
            ),
            legend=alt.Legend(title="Metabolic State", orient="bottom", titleLimit=300, labelLimit=300)
        ),
        # FIX: Notice the backslash in 'C\:N Ratio' to prevent Altair from crashing
        tooltip=['Cow Dung (%)', 'Food Waste (%)', 'Poultry Waste (%)', 'C\:N Ratio', 'Methane Yield', 'Biological State']
    ).properties(
        height=500
    )
    
    st.altair_chart(heatmap, use_container_width=True)