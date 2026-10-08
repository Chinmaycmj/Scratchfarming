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
    page_title="TERRAFORM // Planetary Survival OS",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Sci-Fi Survival CSS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, .hud-title {
        font-family: 'JetBrains Mono', monospace !important;
        letter-spacing: -0.5px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        margin-right: 8px;
    }
    .badge-green { background: #064E3B; color: #34D399; border: 1px solid #059669; }
    .badge-amber { background: #78350F; color: #FBBF24; border: 1px solid #D97706; }
    .badge-blue { background: #1E3A8A; color: #60A5FA; border: 1px solid #2563EB; }
    
    .card-container {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        color: #FFFFFF;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🛰️ MISSION CONTROLS")
    st.markdown("---")
    
    api_key_input = st.text_input(
        "Gemini API Key (Optional)",
        type="password",
        help="Paste your Google Gemini API key for live multimodal vision reasoning. If left empty, the local First-Principles Agronomic Engine executes automatically."
    )
    
    st.markdown("---")
    st.markdown("### 📂 QUICK SCENARIO PRESETS")
    preset_choice = st.selectbox(
        "Load Preset Archetype (For Testing):",
        [
            "Select or use custom input below...",
            "1. Arid Hyper-Sandy Desert (pH 8.4, 0% Retention)",
            "2. Coastal Saline Shoreline (EC 7.8 dS/m, Sodic Clay)",
            "3. Acidic Tropical Clay / Laterite (pH 4.5, Toxic Al3+)",
            "4. Degraded Rocky Mountain Slope (<10cm Topsoil)",
            "5. Waterlogged Wetland Peat Marsh (Anaerobic Anoxia)"
        ]
    )

    preset_texts = {
        "1. Arid Hyper-Sandy Desert (pH 8.4, 0% Retention)": (
            "Hyper-arid sand dunes with intense solar radiation (>45°C). Soil has over 90% coarse sand with zero organic matter. "
            "Poured water drains straight through in seconds. Highly alkaline with trace boron contamination. Survivor needs emergency calories."
        ),
        "2. Coastal Saline Shoreline (EC 7.8 dS/m, Sodic Clay)": (
            "Low-lying coastal marshland subjected to saltwater intrusion. Electrical conductivity reaches 7.8 dS/m. "
            "Soil exhibits heavy sodium dispersion and surface white salt crusting. Normal seeds fail to germinate due to osmotic drought."
        ),
        "3. Acidic Tropical Clay / Laterite (pH 4.5, Toxic Al3+)": (
            "Deep reddish heavy clay terrain in an abandoned tropical clear-cut. Soil test reveals severe acidity at pH 4.5. "
            "High soluble aluminum (Al3+) causing immediate root stunting. Phosphorus is chemically locked into insoluble clay matrices."
        ),
        "4. Degraded Rocky Mountain Slope (<10cm Topsoil)": (
            "Steep mountainous slope subject to harsh winds, high altitude UV, and cold nights. Topsoil horizon is skeletal and under 10cm. "
            "Torrential rains cause immediate topsoil sheet erosion. Severe nitrogen and carbon depletion."
        ),
        "5. Waterlogged Wetland Peat Marsh (Anaerobic Anoxia)": (
            "Saturated silt wetland basin with high water table right at surface. Complete lack of oxygen (rhizosphere anoxia) causing sulfur smells. "
            "Fungal root rot is prevalent. Soil temperature is cold and organic matter decomposition is severely retarded."
        )
    }

    st.markdown("---")
    st.markdown("### 🏆 JUDGE DEMO CHEATSHEET")
    st.caption("1. Upload Judge's scenario photo (Rule 19).\n2. Paste Judge's unseen narrative.\n3. Click 'TERRAFORM'.\n4. Show radar chart & chemical dosages.\n5. Invite Judge to test the Curveball Terminal!")

# Main Header Banner
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="color: #10B981; margin: 0; font-size: 28px;">🌱 TERRAFORM // SURVIVAL OS</h1>
            <p style="color: #94A3B8; margin: 4px 0 0 0; font-size: 13px;">PLANETARY SOIL DIAGNOSTICS & AUTONOMOUS HARVEST REASONING CORE</p>
        </div>
        <div>
            <span class="status-badge badge-green">CORE: ONLINE</span>
            <span class="status-badge badge-blue">REASONING: MULTIMODAL</span>
            <span class="status-badge badge-amber">RULE 19: ARMED</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input Panel Layout (2 Columns)
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown("#### 📸 STEP 1: OFFICIAL SCENARIO IMAGE (RULE 19)")
    uploaded_image = st.file_uploader(
        "Upload Official Land / Soil Photograph provided by Judges:",
        type=["jpg", "jpeg", "png"],
        help="In compliance with Rule 19, upload the official image accompanying the unseen scenario."
    )
    
    image_bytes = None
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Analyzed Terrain Surface Feed", use_container_width=True)
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="JPEG")
        image_bytes = img_buffer.getvalue()

with col_right:
    st.markdown("#### 📝 STEP 2: UNSEEN LAND SCENARIO NARRATIVE")
    default_text = preset_texts.get(preset_choice, "")
    scenario_input = st.text_area(
        "Paste Judge's Scenario Narrative or Field Observations:",
        value=default_text,
        height=180,
        placeholder="e.g. Red lateritic soil with deep fissures, stunted shrub foliage, high aluminum runoff from nearby rocks, survivor starving with zero seed stock..."
    )
    
    analyze_btn = st.button("🚀 INITIATE PLANETARY TERRAFORMING")

# Session state persistence for results
if "result_data" not in st.session_state:
    st.session_state.result_data = None

if analyze_btn:
    if not scenario_input.strip() and not image_bytes:
        st.warning("⚠️ Please provide a scenario description or upload a terrain image to begin.")
    else:
        with st.spinner("🛰️ Deep agronomic reasoning in progress... Extracting soil physics, computing amendments, and evaluating crop viability..."):
            result = call_gemini_multimodal(
                scenario_text=scenario_input,
                image_bytes=image_bytes,
                api_key=api_key_input
            )
            st.session_state.result_data = result

# Display Results if Available
if st.session_state.result_data:
    data = st.session_state.result_data
    sc_analysis = data.get("scenario_analysis", {})
    metrics = sc_analysis.get("soil_metrics", {})
    remediation = data.get("remediation_protocol", [])
    crops = data.get("recommended_crops", [])
    roadmap = data.get("survival_harvest_roadmap", [])

    st.markdown("---")
    st.markdown(f"### 🎯 DIAGNOSTIC MATRIX: {sc_analysis.get('identified_archetype', 'Uncharted Ground').upper()}")
    
    if sc_analysis.get("visual_findings"):
        st.info(f"👁️ **Multimodal Visual Intelligence (Rule 19):** {sc_analysis.get('visual_findings')}")

    # Row 1: KPI Telemetry Cards
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric(
            label="Soil Reaction (pH)",
            value=f"{metrics.get('ph', 7.0):.1f}",
            delta=f"Target: {metrics.get('target_ph', 6.5):.1f}"
        )
    with kpi2:
        st.metric(
            label="Salinity (EC)",
            value=f"{metrics.get('salinity_ec_ds_m', 0.5):.1f} dS/m",
            delta="Optimal: <1.5"
        )
    with kpi3:
        st.metric(
            label="Moisture Retention",
            value=f"{metrics.get('moisture_pct', 50):.0f}%",
            delta="Field Cap: 60%"
        )
    with kpi4:
        st.metric(
            label="Organic Carbon",
            value=f"{metrics.get('organic_matter_pct', 1.0):.1f}%",
            delta="Healthy: >3.0%"
        )
    with kpi5:
        st.metric(
            label="Survival Fertility Index",
            value=f"{metrics.get('fertility_index', 50)}/100",
            delta="Calculated Biocapacity"
        )

    # Row 2: Radar Chart + Remediation Protocol
    st.markdown("<br/>", unsafe_allow_html=True)
    col_chart, col_remedy = st.columns([1, 1], gap="medium")

    with col_chart:
        st.markdown("#### 📊 SOIL HEALTH TELEMETRY (RAW VS POST-TREATMENT)")
        
        categories = ['pH Balance', 'Low Salinity', 'Water Retention', 'Organic Matter', 'Biological Activity']
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
                line_color='#EF4444'
            ))
            fig.add_trace(go.Scatterpolar(
                r=[92, 95, 85, 88, 90],
                theta=categories,
                fill='toself',
                name='Post-Terraform Target',
                line_color='#10B981'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], color="#94A3B8"),
                    bgcolor="#0F172A"
                ),
                paper_bgcolor="#0B0F19",
                font=dict(color="#E2E8F0"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                margin=dict(l=40, r=40, t=20, b=40),
                height=340
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart({
                "Metric": categories,
                "Raw Baseline": [raw_ph_score, raw_sal_score, raw_moist_score, raw_om_score, raw_bio_score],
                "Post-Terraform": [92, 95, 85, 88, 90]
            }, x="Metric")
            st.caption("💡 Tip: Install plotly for 360° radar chart: `python -m pip install plotly`")

    with col_remedy:
        st.markdown("#### 🧪 FIRST-PRINCIPLES REMEDIATION PROTOCOL")
        for step in remediation:
            st.markdown(f"""
            <div class="card-container" style="border-left: 4px solid #10B981;">
                <span class="status-badge badge-green">{step.get('phase', 'Action')}</span>
                <strong style="color: #F8FAFC; font-size: 14px;">{step.get('amendment', 'Treatment')}</strong><br/>
                <div style="color: #FBBF24; font-family: 'JetBrains Mono', monospace; font-size: 12px; margin: 4px 0;">
                    ⚖️ DOSAGE: {step.get('dosage', 'Calculated by soil volume')}
                </div>
                <p style="color: #94A3B8; font-size: 12px; margin: 4px 0 0 0;">
                    🔬 <em>{step.get('scientific_rationale', 'Neutralizes limiting factor.')}</em>
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Row 3: Two-Tier Crop Matchmaker
    st.markdown("---")
    st.markdown("#### 🌾 SURVIVAL CROP MATCHMAKER (TWO-TIER CALORIC DEPLOYMENT)")
    
    crop_cols = st.columns(len(crops)) if crops else [st.container()]
    for idx, (col, crop) in enumerate(zip(crop_cols, crops)):
        with col:
            st.markdown(f"""
            <div class="card-container" style="border-top: 4px solid #2563EB;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="color: #38BDF8; margin: 0; font-size: 18px;">{crop.get('crop_name')}</h3>
                    <span class="status-badge badge-blue">{crop.get('viability_score', 85)}% VIABILITY</span>
                </div>
                <div style="color: #F59E0B; font-size: 11px; font-weight: 600; margin: 6px 0;">
                    🏷️ {crop.get('tier', 'Survival Crop')}
                </div>
                <div style="color: #CBD5E1; font-size: 12px; margin-bottom: 8px;">
                    ⏱️ <b>Harvest:</b> {crop.get('days_to_harvest')} days | 🥗 <b>Emergency:</b> {crop.get('emergency_days', 20)} days<br/>
                    ⚡ <b>Caloric Density:</b> {crop.get('calories', '150 kcal/100g')}
                </div>
                <p style="color: #94A3B8; font-size: 11.5px; margin-bottom: 6px;">
                    <b>Why Viable:</b> {crop.get('why_viable')}
                </p>
                <div style="background: #1E293B; border-radius: 6px; padding: 6px 10px; font-size: 11px; color: #E2E8F0;">
                    🛡️ <b>Risk Mitigation:</b> {crop.get('failure_mitigation')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(crop.get('viability_score', 85) / 100)

    # Row 4: Step-by-Step Survival Roadmap
    st.markdown("---")
    st.markdown("#### 🗺️ DAY-BY-DAY SURVIVAL ROADMAP (BARE SOIL TO FULL HARVEST)")
    for r in roadmap:
        with st.expander(f"📍 {r.get('stage')}", expanded=True):
            for act in r.get("actions", []):
                st.markdown(f"- ✅ **{act}**")

    # Row 5: Interactive Judge Curveball Terminal
    st.markdown("---")
    st.markdown("### ⚡ LIVE JUDGE STRESS-TEST & CURVEBALL TERMINAL")
    st.caption("Ask any sudden crisis (e.g. 'Flash flood on Day 15', 'Locust infestation', 'Unseasonal drought') to witness live adaptive reasoning:")
    
    curve_col1, curve_col2 = st.columns([4, 1])
    with curve_col1:
        judge_question = st.text_input(
            "Judge Challenge Query:",
            placeholder="e.g. A torrential flash flood hits on Day 20 washing away top mulching. What does the system adjust?",
            label_visibility="collapsed"
        )
    with curve_col2:
        ask_btn = st.button("STRESS-TEST AI")

    if ask_btn and judge_question.strip():
        with st.spinner("Analyzing crisis dynamics against active soil biology..."):
            ans = answer_curveball_query(
                question=judge_question,
                context=data,
                api_key=api_key_input
            )
            st.markdown(f"""
            <div class="card-container" style="border-left: 4px solid #F59E0B; background: #1E293B;">
                <h4 style="color: #FBBF24; margin-top: 0;">🛰️ TACTICAL ADAPTATION PROTOCOL:</h4>
                <div style="color: #E2E8F0; font-size: 13px; line-height: 1.6;">
                    {ans.replace(chr(10), '<br/>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
