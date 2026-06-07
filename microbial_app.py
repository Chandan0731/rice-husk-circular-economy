import streamlit as st

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Microbial Biorefinery Modeling",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Professional Biotech CSS Injection
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #F5F9F6;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 2px solid #81C784;
    }
    
    /* Typography */
    h1, h2, h3, h4 {
        color: #2E7D32 !important;
        font-family: 'Arial', sans-serif;
    }
    
    /* Information Boxes */
    .sci-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-left: 5px solid #4CAF50;
        border-radius: 5px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

# 3. Content
st.title("Microbial Biorefinery Modeling")
st.subheader("Sustainable Valorization of Rice Husk via Anaerobic Co-Digestion")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="sci-box">
        <h4>The Biological Bottleneck</h4>
        <p>Rice husk possesses an immensely high Carbon-to-Nitrogen (C:N) ratio (~88.8) and a dense lignocellulosic matrix (18.6% Lignin). In mono-digestion, this crystalline shield prevents hydrolytic enzymatic binding, while the lack of nitrogen starves methanogenic archaea of essential nutrients for cell synthesis.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="sci-box">
        <h4>The Co-Digestion Solution</h4>
        <p>This simulator utilizes a stoichiometric mass-balance engine to model the introduction of nitrogen-rich co-substrates. By simulating various feedstock ratios, we mathematically identify the optimal parameters required to neutralize ammonia toxicity risks and achieve an ideal 25:1 C:N metabolic environment.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### System Modules")
st.markdown("""
* **Module 1: Co-Digestion Simulator** - A decision-support tool predicting methane yields while actively screening for volatile fatty acid (VFA) souring.
* **Module 2: Microbial Kinetics** - Time-series projections utilizing kinetic constraints to visualize metabolic lag phases.
* **Module 3: Process Optimizer** - Algorithmic sweeps to isolate maximum economic viability under strict biological safety thresholds.
""")

st.info("Please use the left sidebar navigation panel to initialize the core simulator modules.")