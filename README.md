# 🌱 TERRAFORM: Single-Handed VS Code Playbook

> **Event Date:** October 15  
> **Mission:** Transform unknown bare soil into a full harvest survival roadmap using AI First-Principles Agronomy.

---

## 1. Opening & Running in Visual Studio Code (VSC)

### Step 1: Open Folder in VS Code
1. Open **Visual Studio Code**.
2. Click **File > Open Folder...** (or press `Ctrl + K`, `Ctrl + O`).
3. Select this folder:
   ```text
   C:\Users\Chinmay\.gemini\antigravity\scratch\terraform
   ```

### Step 2: Select Python Interpreter
1. Press `Ctrl + Shift + P` to open the Command Palette.
2. Type `Python: Select Interpreter` and hit Enter.
3. Choose your active Python installation (Python 3.12+ or 3.14).

### Step 3: Run the Application
You can run it in **two ways**:
- **Option A (One-Click F5 Debugger):** Press `F5` on your keyboard. VS Code will automatically launch Streamlit using the pre-configured `.vscode/launch.json`.
- **Option B (Terminal Command):** Press `Ctrl + ~` to open the integrated terminal in VS Code and run:
  ```powershell
  streamlit run app.py
  ```
Your default browser will immediately open to: `http://localhost:8501`.

---

## 2. The Solo / Single-Handed Workflow Layout in VS Code

Building single-handedly is an immense competitive advantage because there is zero communication overhead and zero git conflicts. In VS Code, organize your workspace like a command center:

```
┌─────────────────────────────────┬─────────────────────────────────┐
│  EDITOR LEFT:                   │  EDITOR RIGHT:                  │
│  core/reasoner.py               │  app.py                         │
│  (Multimodal AI logic & domain  │  (Streamlit visual telemetry &  │
│   soil chemistry rules)         │   judge controls)               │
├─────────────────────────────────┴─────────────────────────────────┤
│  SPLIT TERMINAL (BOTTOM):                                         │
│  [Terminal 1: streamlit run app.py]  |  [Terminal 2: python tests]│
└───────────────────────────────────────────────────────────────────┘
```

1. **Split Editor:** Right-click `app.py` in the explorer and click **Open to the Side** (`Ctrl + \`).
2. **Auto-Reload:** Every time you press `Ctrl + S` in `app.py` or `reasoner.py`, Streamlit detects the change and prompts you to **Rerun** in the browser.

---

## 3. How the Offline & Online Modes Work

- **Online Mode (Gemini 2.5 Flash Multimodal):**
  - Enter your API Key in the left sidebar or set environment variable `GEMINI_API_KEY`.
  - Ingests the judge's uploaded photo (Rule 19) + text description directly into Gemini Flash.
- **Fail-Safe Offline Mode:**
  - If venue Wi-Fi drops or API rate limits hit, the system **automatically and invisibly switches** to our deterministic First-Principles Agronomy engine in `core/reasoner.py`.
  - Zero crashes, zero blank screens, 100% reliable during live judge tests.

---

## 4. Live Judge Demo in 3 Minutes

1. **Rule 19 Live Image:** Ask the judge for their scenario photo and upload it into **STEP 1: OFFICIAL SCENARIO IMAGE**.
2. **Scenario Text:** Paste their unseen scenario narrative in **STEP 2**.
3. **Click "Initiate Planetary Terraforming":**
   - Show the **Soil Health Radar Chart** comparing baseline toxic soil with post-treatment target.
   - Point out the **Calculated Chemical Dosages** (e.g. 350g/m² Agricultural Lime for Al3+ neutralization).
   - Show the **Two-Tier Crop Plan**: Emergency protein greens in 22 days (Cowpea) + Sustained starch tubers in 180 days (Cassava).
4. **The Curveball Finale:** Expand the **Live Judge Stress-Test Terminal** at the bottom and ask the judge to throw any natural disaster at your land!
