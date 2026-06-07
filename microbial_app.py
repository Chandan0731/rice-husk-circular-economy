import streamlit as st

# 1. Page Configuration (Must be the first command)
st.set_page_config(
    page_title="Microbial Biorefinery Modeling",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom CSS for Professional Branding
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #F5F9F6;
    }
    
    /* Typography & Headers */
    h1, h2, h3, h4 {
        color: #2E7D32;
        font-family: 'Arial', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 2px solid #81C784;
    }
    
    /* Call to Action Button */
    .stButton>button {
        background-color: #4CAF50;
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2E7D32;
        color: #FFFFFF;
    }
    
    /* Info Box Styling */
    .sci-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-left: 5px solid #4CAF50;
        border-radius: 5px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# 3. Main Page Content
st.title("Microbial Biorefinery Modeling")
st.subheader("Sustainable Valorization of Rice Husk via Anaerobic Co-Digestion")

st.markdown("---")

# 4. Scientific Overview Layout
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
        <p>This simulator utilizes a stoichiometric mass-balance engine to model the introduction of nitrogen-rich co-substrates (Cow Dung, Food Waste, Poultry Waste). By simulating various feedstock ratios, we can mathematically identify the optimal parameters required to neutralize ammonia toxicity risks and achieve an ideal 25:1 C:N metabolic environment.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 5. Project Architecture & Navigation
st.markdown("### System Modules")
st.markdown("""
* **Module 1: Co-Digestion Simulator** - A decision-support tool predicting methane yields while actively screening for volatile fatty acid (VFA) souring.
* **Module 2: Microbial Kinetics** - Time-series projections utilizing kinetic constraints to visualize metabolic lag phases.
* **Module 3: Process Optimizer** - Algorithmic sweeps to isolate maximum economic viability under strict biological safety thresholds.
""")

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Prompt
st.info("Please use the left sidebar navigation panel to initialize the core simulator modules.")