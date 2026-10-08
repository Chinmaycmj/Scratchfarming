# 🧪 TERRAFORM: Test Scenarios & Image Suite

This directory contains **5 realistic agricultural test scenarios** complete with high-resolution terrain photos for practicing the live hackathon judging flow and Rule 19 compliance.

---

## The 5 Test Cases

### 1. Hyper-Arid Red Dune Basin
* **Image:** `scenario_1_arid_desert.jpg`
* **Limiting Factors:** pH 8.4, coarse sand (91%), zero water retention, thermal stress (>48°C).
* **Target Crops:** Pearl Millet, Tepary Beans, Grain Sorghum.
* **Remediation:** Biochar + Bentonite clay, thick straw mulch, subsurface olla pots.

### 2. Brackish Coastal Saline Basin
* **Image:** `scenario_2_coastal_saline.jpg`
* **Limiting Factors:** EC 7.8 dS/m, white crystalline salt crust, osmotic drought, dispersed sodic clay.
* **Target Crops:** Barley, Quinoa, Sugar Beet.
* **Remediation:** Gypsum ($CaSO_4$) to displace $Na^+$, freshwater leaching, raised 35cm drainage ridges.

### 3. Acidic Tropical Laterite Clay Clearcut
* **Image:** `scenario_3_acidic_clay.jpg`
* **Limiting Factors:** pH 4.5, red oxidized clay, Aluminum ($Al^{3+}$) toxicity, phosphorus fixation.
* **Target Crops:** Cassava, Sweet Potato, Cowpea.
* **Remediation:** Agricultural Lime ($CaCO_3$) 350g/m², Rock Phosphate with mycorrhizae, biochar aeration.

### 4. Eroded Alpine Rocky Scree Slope
* **Image:** `scenario_4_rocky_slope.jpg`
* **Limiting Factors:** Topsoil <8cm, 32° slope, loose gravel scree, cold winds, UV radiation.
* **Target Crops:** Grain Amaranth, Buckwheat, Cold-Hardy Potatoes.
* **Remediation:** Contour stone swales, Vetiver grass retaining barriers, compost sheet mulching.

### 5. Waterlogged Silt Wetland Peat Basin
* **Image:** `scenario_5_wetland_peat.jpg`
* **Limiting Factors:** Rhizosphere anoxia (0% $O_2$), toxic $H_2S$, saturated black muck, Pythium root rot.
* **Target Crops:** Swamp Taro (Colocasia), Deep-Water Rice, Water Spinach.
* **Remediation:** Herringbone French drainage ditches, high raised ridge mounds (Chinampa), coarse sand blending.

---

## How to Test in the Streamlit HUD:
1. Open the web app at `http://localhost:8501`.
2. Drag and drop any `.jpg` file from this folder into **STEP 1: OFFICIAL SCENARIO IMAGE**.
3. Copy and paste the corresponding narrative text from `scenarios.json` into **STEP 2: UNSEEN LAND SCENARIO NARRATIVE**.
4. Click **🚀 INITIATE PLANETARY TERRAFORMING**.
5. Test the **Curveball Terminal** using the sample crisis provided in `scenarios.json`!
