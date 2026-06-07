import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Microbial Biorefinery",
    layout="wide",
    initial_sidebar_state="collapsed" # We collapse the sidebar so they use your new animated buttons!
)

# 2. Modern CSS Injection with Motion Graphics (@keyframes)
st.markdown("""
<style>
    /* Clean Slate Background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* High-Contrast Typography */
    h1, h2, h3, h4 {
        color: #0F172A !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
    }
    p {
        color: #334155;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* MOTION GRAPHIC 1: Fade In and Slide Up */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Animated Info Cards */
    .animated-card {
        animation: fadeInUp 0.8s ease-out forwards;
        background: #FFFFFF;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #10B981; /* Accent Green */
        margin-bottom: 20px;
    }
    
    /* MOTION GRAPHIC 2: Interactive Module Buttons */
    div.stButton > button {
        animation: fadeInUp 1s ease-out forwards;
        width: 100%;
        height: 100px;
        background: #FFFFFF;
        color: #0F172A;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Hover Lift Physics */
    div.stButton > button:hover {
        border-color: #10B981;
        color: #047857;
        transform: translateY(-8px);
        box-shadow: 0 12px 20px -3px rgba(16, 185, 129, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# 3. Header Section (Animated)
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Microbial Biorefinery Modeling</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #64748B !important; margin-top: 0; margin-bottom: 40px;'>Sustainable Valorization of Rice Husk via Anaerobic Co-Digestion</h4>", unsafe_allow_html=True)

# 4. Animated Scientific Overview
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="animated-card">
        <h3 style="color: #047857 !important;">The Biological Bottleneck</h3>
        <p>Rice husk possesses an immensely high Carbon-to-Nitrogen (C:N) ratio (~88.8) and a dense lignocellulosic matrix (18.6% Lignin). In mono-digestion, this crystalline shield prevents hydrolytic enzymatic binding, while the severe lack of nitrogen starves methanogenic archaea of essential nutrients for cell synthesis.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="animated-card" style="animation-delay: 0.2s;">
        <h3 style="color: #047857 !important;">The Co-Digestion Solution</h3>
        <p>This simulator utilizes a stoichiometric mass-balance engine to model the introduction of nitrogen-rich co-substrates. By simulating various feedstock ratios, we mathematically identify the exact parameters required to neutralize ammonia toxicity risks and achieve an ideal 25:1 C:N metabolic environment.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Interactive Navigation Modules (Direct Page Switching)
st.markdown("### Select System Module")
nav1, nav2, nav3 = st.columns(3)

with nav1:
    if st.button("Module 1: Co-Digestion Simulator"):
        st.switch_page("pages/1_Co_Digestion_Simulator.py")
        
with nav2:
    if st.button("Module 2: Microbial Kinetics"):
        st.switch_page("pages/2_Microbial_Kinetics.py") # We will build this next!
        
with nav3:
    if st.button("Module 3: Process Optimizer"):
        st.switch_page("pages/3_Process_Optimizer.py") # We will build this later!