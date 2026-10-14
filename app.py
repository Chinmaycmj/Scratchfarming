import streamlit as st
import json
import io
from PIL import Image
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
from core.reasoner import call_gemini_multimodal, answer_curveball_query, load_knowledge

# Page Configuration
st.set_page_config(
    page_title="Scratch Farming | Soil Diagnostics & Crop Planning",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Visual Design System: Agricultural Technology Theme
# Primary: #173F2A (Forest Green)
# Secondary: #32804A (Botanical Green)
# Background: #F8FAF6 (Warm Off-White)
# Soft Accent: #EAF3E8 (Sage)
# Text: #24352B (Dark Charcoal-Green)
# Border: #DCE6DA
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');
    
    /* Global App Container */
    .stApp {
        background-color: #F8FAF6;
        color: #24352B;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Headings & Typography */
    h1, h2, h3, h4 {
        color: #173F2A !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    p, span, label, div {
        color: #24352B;
    }
    
    /* Header Banner */
    .app-header {
        background: #FFFFFF;
        border: 1px solid #DCE6DA;
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 2px 10px rgba(23, 63, 42, 0.04);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    
    .app-title-group h1 {
        margin: 0;
        font-size: 26px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .app-subtitle {
        margin: 4px 0 0 0;
        color: #556B5B;
        font-size: 13.5px;
        font-weight: 500;
    }
    
    /* Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 600;
        margin-left: 6px;
    }
    .badge-sage {
        background: #EAF3E8;
        color: #173F2A;
        border: 1px solid #CFDDD0;
    }
    .badge-forest {
        background: #173F2A;
        color: #FFFFFF;
    }
    .badge-botanical {
        background: #E8F5EE;
        color: #2D7A4D;
        border: 1px solid #B8E2CB;
    }
    
    /* Card Containers */
    .agri-card {
        background: #FFFFFF;
        border: 1px solid #DCE6DA;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(23, 63, 42, 0.03);
    }
    
    .agri-card-header {
        border-bottom: 1px solid #EAF3E8;
        padding-bottom: 12px;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Metric Cards */
    .metric-box {
        background: #FFFFFF;
        border: 1px solid #DCE6DA;
        border-radius: 10px;
        padding: 16px 18px;
        text-align: center;
        box-shadow: 0 1px 4px rgba(23, 63, 42, 0.02);
    }
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        color: #556B5B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #173F2A;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-delta {
        font-size: 11.5px;
        color: #32804A;
        font-weight: 500;
        margin-top: 2px;
    }
    
    /* Crop Card */
    .crop-card {
        background: #FFFFFF;
        border: 1px solid #DCE6DA;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(23, 63, 42, 0.03);
        border-top: 4px solid #32804A;
    }
    
    /* Protocol Card */
    .remedy-card {
        background: #FFFFFF;
        border: 1px solid #DCE6DA;
        border-left: 4px solid #32804A;
        border-radius: 8px;
        padding: 16px 18px;
        margin-bottom: 12px;
    }
    
    /* Empty State Box */
    .empty-state-box {
        background: #FFFFFF;
        border: 1.5px dashed #CFDDD0;
        border-radius: 12px;
        padding: 36px 24px;
        text-align: center;
        margin-top: 10px;
    }
    
    /* Primary Action Buttons */
    .stButton>button {
        background-color: #173F2A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #32804A !important;
        box-shadow: 0 4px 12px rgba(50, 128, 74, 0.25) !important;
    }
    
    /* Secondary/Preset Buttons */
    .preset-btn button {
        background-color: #EAF3E8 !important;
        color: #173F2A !important;
        border: 1px solid #CFDDD0 !important;
        font-size: 13px !important;
        padding: 6px 14px !important;
    }
    .preset-btn button:hover {
        background-color: #DCE6DA !important;
    }
    
    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #EAF3E8;
        padding: 6px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 7px;
        padding: 8px 16px;
        color: #556B5B;
        font-weight: 600;
        font-size: 13.5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #173F2A !important;
        box-shadow: 0 1px 4px rgba(23, 63, 42, 0.08);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F1F5EF !important;
        border-right: 1px solid #DCE6DA;
    }
</style>
""", unsafe_allow_html=True)

# Preset Scenario Catalog
PRESET_SCENARIOS = {
    "Arid Desert Basin": {
        "title": "Hyper-Arid Sandy Basin (pH 8.4, 0% Retention)",
        "text": (
            "Hyper-arid sand dunes with intense solar radiation (>45°C). Soil has over 90% coarse sand with zero organic matter. "
            "Poured water drains straight through in seconds. Highly alkaline with trace boron contamination. Survivor needs emergency calories."
        ),
        "icon": "🏜️"
    },
    "Coastal Saline Marsh": {
        "title": "Coastal Sodic Shoreline (EC 7.8 dS/m, Dispersed Clay)",
        "text": (
            "Low-lying coastal marshland subjected to saltwater intrusion. Electrical conductivity reaches 7.8 dS/m. "
            "Soil exhibits heavy sodium dispersion and surface white salt crusting. Normal seeds fail to germinate due to osmotic drought."
        ),
        "icon": "🌊"
    },
    "Acidic Tropical Laterite": {
        "title": "Acidic Tropical Clay (pH 4.5, Toxic Soluble Al3+)",
        "text": (
            "Deep reddish heavy clay terrain in an abandoned tropical clear-cut. Soil test reveals severe acidity at pH 4.5. "
            "High soluble aluminum (Al3+) causing immediate root stunting. Phosphorus is chemically locked into insoluble clay matrices."
        ),
        "icon": "🌋"
    },
    "Rocky Mountain Slope": {
        "title": "Degraded Alpine Rocky Slope (<10cm Topsoil)",
        "text": (
            "Steep mountainous slope subject to harsh winds, high altitude UV, and cold nights. Topsoil horizon is skeletal and under 10cm. "
            "Torrential rains cause immediate topsoil sheet erosion. Severe nitrogen and carbon depletion."
        ),
        "icon": "⛰️"
    },
    "Waterlogged Peat Marsh": {
        "title": "Saturated Silt Wetland (Rhizosphere Anoxia)",
        "text": (
            "Saturated silt wetland basin with high water table right at surface. Complete lack of oxygen (rhizosphere anoxia) causing sulfur smells. "
            "Fungal root rot is prevalent. Soil temperature is cold and organic matter decomposition is severely retarded."
        ),
        "icon": "🌾"
    }
}

# Session State Initialization
if "result_data" not in st.session_state:
    st.session_state.result_data = None
if "active_scenario_text" not in st.session_state:
    st.session_state.active_scenario_text = ""
if "last_preset_selected" not in st.session_state:
    st.session_state.last_preset_selected = "Custom Field Input"

# Sidebar: Controls & System Info
with st.sidebar:
    st.markdown("### 🌱 Scratch Farming")
    st.caption("Agricultural Soil Diagnostics & Crop Planning Platform")
    st.markdown("---")
    
    st.markdown("#### ⚙️ Configuration")
    api_key_input = st.text_input(
        "Google Gemini API Key (Optional)",
        type="password",
        help="Optional API key for live multimodal vision reasoning. If left blank, the deterministic First-Principles Agronomic Engine executes locally with zero external latency."
    )
    
    if api_key_input:
        st.success("API Key detected: Multimodal Cloud Reasoning active.", icon="☁️")
    else:
        st.info("Local Engine: First-principles deterministic agronomy active.", icon="💻")
    
    st.markdown("---")
    st.markdown("#### 📚 Agricultural Reference")
    with st.expander("5 Core Soil Archetypes", expanded=False):
        st.markdown("""
        - **Arid Sandy:** Leached, low CEC, high drainage -> *Biochar, mulch, millet*.
        - **Coastal Saline:** High EC, sodium toxicity -> *Gypsum, leaching, barley*.
        - **Acidic Clay:** pH < 5.0, Al³⁺ toxicity -> *Lime ($CaCO_3$), cassava*.
        - **Rocky Slope:** Thin topsoil, erosion -> *Swales, vetiver grass, amaranth*.
        - **Wetland Peat:** Anoxia, fungal rot -> *French drains, ridges, taro*.
        """)
    
    st.markdown("---")
    st.caption("Scratch Farming OS v2.4 | Production Edition")

# Application Header Banner
st.markdown("""
<div class="app-header">
    <div class="app-title-group">
        <h1>🌱 Scratch Farming</h1>
        <p class="app-subtitle">Intelligent Soil Diagnostics, Chemical Remediation & Survival Crop Viability System</p>
    </div>
    <div>
        <span class="badge-pill badge-forest">System Online</span>
        <span class="badge-pill badge-sage">First-Principles Core</span>
        <span class="badge-pill badge-botanical">Multimodal Vision</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Workspace Layout
st.markdown("### 📋 Field Input & Soil Characterization Console")
st.markdown("Input field soil observations or choose a calibrated reference archetype to evaluate limiting factors and generate a full crop deployment plan.")

# Input Card
with st.container():
    st.markdown('<div class="agri-card">', unsafe_allow_html=True)
    
    # Preset Selector Row
    p_col1, p_col2 = st.columns([3, 1])
    with p_col1:
        preset_options = ["Custom Field Input"] + [f"{v['icon']} {k}" for k, v in PRESET_SCENARIOS.items()]
        selected_option = st.selectbox(
            "Quick Reference Scenarios (Pre-calibrated archetypes):",
            preset_options,
            index=0,
            help="Select a benchmark terrain archetype to immediately populate field observations."
        )
    with p_col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Load Preset", use_container_width=True):
            if selected_option != "Custom Field Input":
                raw_name = selected_option.split(" ", 1)[1]
                st.session_state.active_scenario_text = PRESET_SCENARIOS[raw_name]["text"]
                st.session_state.last_preset_selected = raw_name
                st.rerun()

    col_narrative, col_imagery = st.columns([3, 2], gap="large")
    
    with col_narrative:
        scenario_input = st.text_area(
            "Field Soil Observations & Geological Constraints:",
            value=st.session_state.active_scenario_text,
            height=165,
            placeholder="Describe soil appearance, texture (sand, clay, silt), drainage behavior, observed vegetative stress, or laboratory readings (e.g. pH 4.5, high salinity, standing water)...",
            help="Provide descriptive terrain observations. The system extracts limiting chemical, physical, and biological constraints."
        )
        # Update session state on text change
        st.session_state.active_scenario_text = scenario_input
    
    with col_imagery:
        uploaded_image = st.file_uploader(
            "Terrain / Soil Surface Photo (Optional, Rule 19):",
            type=["jpg", "jpeg", "png"],
            help="Upload an image of the ground surface. Multimodal vision evaluates color, cracking, salt crust, and slope."
        )
        
        image_bytes = None
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Analyzed Terrain Surface Feed", use_container_width=True)
            img_buffer = io.BytesIO()
            image.save(img_buffer, format="JPEG")
            image_bytes = img_buffer.getvalue()
    
    # Action Row
    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #EAF3E8;'/>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_spacer = st.columns([2, 1, 3])
    
    with btn_col1:
        analyze_clicked = st.button("🚀 Analyze Soil & Generate Plan", use_container_width=True)
    with btn_col2:
        if st.button("Reset Console", use_container_width=True):
            st.session_state.result_data = None
            st.session_state.active_scenario_text = ""
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Processing Logic
if analyze_clicked:
    if not scenario_input.strip() and not image_bytes:
        st.error("Please provide field observations in the text console or upload an image to begin soil characterization.")
    else:
        with st.spinner("Analyzing soil physics, evaluating limiting factors, and computing agronomic remediation protocols..."):
            result = call_gemini_multimodal(
                scenario_text=scenario_input,
                image_bytes=image_bytes,
                api_key=api_key_input
            )
            st.session_state.result_data = result
            st.toast("Soil characterization & crop plan successfully generated!", icon="🌱")

# =============================================================================
# RESULTS DISPLAY OR EMPTY STATE
# =============================================================================

if st.session_state.result_data:
    data = st.session_state.result_data
    sc_analysis = data.get("scenario_analysis", {})
    metrics = sc_analysis.get("soil_metrics", {})
    remediation = data.get("remediation_protocol", [])
    crops = data.get("recommended_crops", [])
    roadmap = data.get("survival_harvest_roadmap", [])
    
    # Archetype Highlight Banner
    st.markdown(f"""
    <div class="agri-card" style="border-left: 6px solid #173F2A; background: #FFFFFF; padding: 18px 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span class="metric-label" style="color: #32804A;">Identified Terrain Archetype</span>
                <h2 style="margin: 2px 0 0 0; font-size: 22px;">{sc_analysis.get('identified_archetype', 'Uncharted Ground')}</h2>
            </div>
            <div>
                <span class="badge-pill badge-forest">Fertility Index: {metrics.get('fertility_index', 50)}/100</span>
                <span class="badge-pill badge-sage">Target pH: {metrics.get('target_ph', 6.5):.1f}</span>
            </div>
        </div>
        {f"<p style='margin: 10px 0 0 0; font-size: 13px; color: #556B5B;'><strong>Visual Inspection Notes:</strong> {sc_analysis.get('visual_findings')}</p>" if sc_analysis.get('visual_findings') else ""}
    </div>
    """, unsafe_allow_html=True)

    # 5 KPI Metric Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Soil pH</div>
            <div class="metric-value">{metrics.get('ph', 7.0):.1f}</div>
            <div class="metric-delta">Target: {metrics.get('target_ph', 6.5):.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Salinity (EC)</div>
            <div class="metric-value">{metrics.get('salinity_ec_ds_m', 0.5):.1f} <span style="font-size: 13px; font-weight: normal;">dS/m</span></div>
            <div class="metric-delta">Optimal: &lt;1.5 dS/m</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Moisture Retention</div>
            <div class="metric-value">{metrics.get('moisture_pct', 50):.0f}%</div>
            <div class="metric-delta">Field Capacity: 60%</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Organic Matter</div>
            <div class="metric-value">{metrics.get('organic_matter_pct', 1.0):.1f}%</div>
            <div class="metric-delta">Healthy: &gt;3.0%</div>
        </div>
        """, unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Fertility Score</div>
            <div class="metric-value">{metrics.get('fertility_index', 50)} <span style="font-size: 14px; font-weight: normal;">/100</span></div>
            <div class="metric-delta">Computed Biocapacity</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Structured Tabs Navigation
    tab_diag, tab_remedy, tab_crops, tab_roadmap, tab_simulator = st.tabs([
        "📊 Soil Diagnostics & Radar",
        "🧪 Remediation Protocol",
        "🌾 Crop Selection & Viability",
        "🗺️ Seasonal Harvest Roadmap",
        "⚡ Adaptive Field Simulator"
    ])

    # ---------------- TAB 1: DIAGNOSTICS & RADAR ----------------
    with tab_diag:
        st.markdown("#### Comprehensive Soil Telemetry & Limiting Factors")
        col_t1_left, col_t1_right = st.columns([1, 1], gap="large")
        
        with col_t1_left:
            st.markdown('<div class="agri-card">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top: 0;'>⚠️ Critical Limiting Factors Identified</h4>", unsafe_allow_html=True)
            st.caption("Primary physiological barriers preventing normal crop emergence in raw soil:")
            
            for factor in sc_analysis.get("limiting_factors", ["General nutrient deficiency"]):
                st.markdown(f"""
                <div style="background: #FEF3E2; border-left: 3px solid #D97706; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px;">
                    <span style="color: #92400E; font-size: 13px; font-weight: 600;">• {factor}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="margin-top: 16px; padding: 12px; background: #EAF3E8; border-radius: 8px;">
                <p style="margin: 0; font-size: 12.5px; color: #173F2A;">
                    <strong>Agronomic Principle:</strong> Fertilizer application is ineffective until fundamental chemical barriers (such as severe acidity or extreme osmotic salinity) are neutralized.
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_t1_right:
            st.markdown('<div class="agri-card">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top: 0;'>📈 Soil Balance Radar (Baseline vs Target)</h4>", unsafe_allow_html=True)
            
            categories = ['pH Balance', 'Low Salinity', 'Water Retention', 'Organic Matter', 'Biocapacity']
            raw_ph_score = max(10, 100 - abs(6.5 - metrics.get('ph', 7.0)) * 25)
            raw_sal_score = max(10, 100 - metrics.get('salinity_ec_ds_m', 0.5) * 12)
            raw_moist_score = min(100, max(15, metrics.get('moisture_pct', 50)))
            raw_om_score = min(100, metrics.get('organic_matter_pct', 1.0) * 25)
            raw_bio_score = metrics.get('fertility_index', 40)

            if HAS_PLOTLY:
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=[raw_ph_score, raw_sal_score, raw_moist_score, raw_om_score, raw_bio_score],
                    theta=categories,
                    fill='toself',
                    name='Raw Baseline Soil',
                    line_color='#C05621',
                    fillcolor='rgba(192, 86, 33, 0.15)'
                ))
                fig.add_trace(go.Scatterpolar(
                    r=[92, 95, 85, 88, 90],
                    theta=categories,
                    fill='toself',
                    name='Remediated Target',
                    line_color='#173F2A',
                    fillcolor='rgba(23, 63, 42, 0.25)'
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], color="#556B5B", gridcolor="#DCE6DA"),
                        bgcolor="#FFFFFF"
                    ),
                    paper_bgcolor="#FFFFFF",
                    font=dict(color="#24352B", family="Inter, sans-serif"),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(l=30, r=30, t=10, b=30),
                    height=290
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.bar_chart({
                    "Parameter": categories,
                    "Raw Baseline": [raw_ph_score, raw_sal_score, raw_moist_score, raw_om_score, raw_bio_score],
                    "Remediated Target": [92, 95, 85, 88, 90]
                }, x="Parameter")
            
            st.caption("Normalized index comparing baseline soil health parameters against optimal agricultural benchmarks.")
            st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- TAB 2: REMEDIATION PROTOCOL ----------------
    with tab_remedy:
        st.markdown("#### Sequential Soil Conditioning & Chemical Amendments")
        st.caption("Calculated dosages formulated to neutralize active toxicities and restore structural soil porosity:")
        
        for step in remediation:
            st.markdown(f"""
            <div class="remedy-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span class="badge-pill badge-sage" style="margin-left: 0;">{step.get('phase', 'Action Step')}</span>
                    <strong style="color: #173F2A; font-family: 'JetBrains Mono', monospace; font-size: 13px;">⚖️ Dosage: {step.get('dosage', 'Determined by area')}</strong>
                </div>
                <h4 style="margin: 4px 0 6px 0; color: #173F2A;">{step.get('amendment', 'Amendment')}</h4>
                <p style="margin: 0; font-size: 13px; color: #4A5D50; line-height: 1.5;">
                    <strong>Scientific Rationale:</strong> {step.get('scientific_rationale', 'Neutralizes limiting condition.')}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ---------------- TAB 3: CROP SELECTION ----------------
    with tab_crops:
        st.markdown("#### Two-Tier Survival Crop Matchmaker")
        st.caption("Biological matching pairs emergency fast-yielding foliage for rapid survival with high-density caloric staples:")
        
        crop_cols = st.columns(len(crops)) if crops else [st.container()]
        for col, crop in zip(crop_cols, crops):
            with col:
                st.markdown(f"""
                <div class="crop-card">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <h3 style="margin: 0; font-size: 19px; color: #173F2A;">{crop.get('crop_name')}</h3>
                            <span class="badge-pill badge-botanical">{crop.get('viability_score', 85)}% Match</span>
                        </div>
                        <div style="font-size: 11.5px; font-weight: 600; color: #32804A; margin: 4px 0 10px 0;">
                            {crop.get('tier', 'Primary Crop')}
                        </div>
                        <div style="background: #F8FAF6; border: 1px solid #EAF3E8; border-radius: 8px; padding: 10px 12px; margin-bottom: 12px;">
                            <div style="font-size: 12.5px; margin-bottom: 3px;">⏱️ <strong>Full Harvest:</strong> {crop.get('days_to_harvest')} Days</div>
                            <div style="font-size: 12.5px; margin-bottom: 3px;">🥗 <strong>First Edible:</strong> {crop.get('emergency_days', 20)} Days</div>
                            <div style="font-size: 12.5px;">⚡ <strong>Energy:</strong> {crop.get('calories', '150 kcal/100g')}</div>
                        </div>
                        <p style="font-size: 12.5px; color: #4A5D50; line-height: 1.45; margin-bottom: 10px;">
                            <strong>Why Viable:</strong> {crop.get('why_viable')}
                        </p>
                    </div>
                    <div style="background: #EAF3E8; border-radius: 6px; padding: 8px 12px; font-size: 11.5px; color: #173F2A;">
                        🛡️ <strong>Care Note:</strong> {crop.get('failure_mitigation')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(crop.get('viability_score', 85) / 100)

    # ---------------- TAB 4: HARVEST ROADMAP ----------------
    with tab_roadmap:
        st.markdown("#### Chronological Harvest Timeline (From Bare Soil to Sustained Harvest)")
        st.caption("Actionable, phase-by-phase field deployment schedule:")
        
        for idx, r in enumerate(roadmap):
            with st.expander(f"📌 {r.get('stage')}", expanded=(idx < 2)):
                for act in r.get("actions", []):
                    st.markdown(f"- **{act}**")

    # ---------------- TAB 5: ADAPTIVE SIMULATOR ----------------
    with tab_simulator:
        st.markdown("#### Adaptive Crisis Simulator & Agronomic Advisor")
        st.caption("Test system responsiveness against extreme meteorological or biological disruptions (e.g. unseasonal frost, flash flood, insect pressure):")
        
        col_q1, col_q2 = st.columns([4, 1])
        with col_q1:
            challenge_query = st.text_input(
                "Simulate Field Crisis / Challenge Query:",
                placeholder="e.g. A torrential flash flood washes away surface mulch on Day 18. What tactical adjustments are needed?",
                label_visibility="collapsed"
            )
        with col_q2:
            simulate_btn = st.button("Simulate Crisis", use_container_width=True)
        
        if simulate_btn and challenge_query.strip():
            with st.spinner("Calculating biological impact and adaptive countermeasures..."):
                response_text = answer_curveball_query(
                    question=challenge_query,
                    context=data,
                    api_key=api_key_input
                )
                st.markdown(f"""
                <div class="agri-card" style="border-left: 4px solid #32804A; background: #FFFFFF; margin-top: 16px;">
                    <h4 style="margin-top: 0; color: #173F2A;">🛰️ Tactical Agronomic Adaptation Protocol</h4>
                    <div style="font-size: 13.5px; color: #24352B; line-height: 1.6;">
                        {response_text.replace(chr(10), '<br/>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

else:
    # =========================================================================
    # EMPTY STATE: USER GUIDE & WORKFLOW ONBOARDING
    # =========================================================================
    st.markdown("""
    <div class="empty-state-box">
        <h3 style="color: #173F2A; margin: 0 0 6px 0;">Welcome to Scratch Farming</h3>
        <p style="color: #556B5B; max-width: 620px; margin: 0 auto 24px auto; font-size: 14px;">
            A decision-support system designed to guide agricultural planning from raw, degraded, or uncharted soil to a resilient harvest.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_w1, col_w2, col_w3 = st.columns(3, gap="medium")
    
    with col_w1:
        st.markdown("""
        <div class="agri-card" style="text-align: center; height: 100%;">
            <div style="font-size: 28px; margin-bottom: 8px;">🔬</div>
            <h4 style="margin: 0 0 6px 0; font-size: 16px;">1. Soil Diagnostics</h4>
            <p style="color: #556B5B; font-size: 13px; line-height: 1.45;">
                Extracts physical limiting factors (pH reaction, electrical conductivity, moisture retention) from field notes and surface photographs.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_w2:
        st.markdown("""
        <div class="agri-card" style="text-align: center; height: 100%;">
            <div style="font-size: 28px; margin-bottom: 8px;">🧪</div>
            <h4 style="margin: 0 0 6px 0; font-size: 16px;">2. Targeted Remediation</h4>
            <p style="color: #556B5B; font-size: 13px; line-height: 1.45;">
                Formulates exact chemical dosages (agricultural lime, gypsum) and physical interventions (swales, biochar) based on soil science laws.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_w3:
        st.markdown("""
        <div class="agri-card" style="text-align: center; height: 100%;">
            <div style="font-size: 28px; margin-bottom: 8px;">🌾</div>
            <h4 style="margin: 0 0 6px 0; font-size: 16px;">3. Two-Tier Crop Plan</h4>
            <p style="color: #556B5B; font-size: 13px; line-height: 1.45;">
                Pairs rapid edible foliage for fast emergency nourishment with resilient, high-carbohydrate staple roots for long-term food security.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    st.info("💡 **Ready to begin?** Select a benchmark preset above or enter field observations in the console, then click **'Analyze Soil & Generate Plan'**.")
