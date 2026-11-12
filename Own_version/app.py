from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="RMS Titanic — Boarding Pass & Survival Check",
    page_icon="🚢",
    layout="wide",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
  --primary-navy: #0B192C;
  --ocean-blue: #1E3E62;
  --parchment: #FDFBF7;
  --aged-paper: #F3EFE6;
  --gold-accent: #C5A059;
  --border-sepia: #D8CEBE;
  --text-dark: #1F2421;
  --survived-green: #1b6348;
  --lost-red: #8B2635;
}

html, body, .stApp {
  background: radial-gradient(circle at 50% 0%, #1e293b 0%, #0B192C 100%) !important;
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
  color: #E2E8F0 !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
  max-width: 1080px !important;
  padding: 2.2rem 1.5rem 3rem !important;
}

/* Hero Section */
.hero-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(197, 160, 89, 0.35);
  border-radius: 12px;
  padding: 2.2rem 2.5rem 1.6rem;
  margin-bottom: 2rem;
  box-shadow: 0 16px 36px -12px rgba(0, 0, 0, 0.5);
  text-align: center;
}
.hero-crest {
  font-family: 'Cinzel', serif;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--gold-accent);
  margin-bottom: 6px;
}
.hero-card h1 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #FAF8F5;
  margin: 0 0 10px 0;
  letter-spacing: -0.02em;
}
.hero-card p {
  color: #94A3B8;
  max-width: 58ch;
  margin: 0 auto;
  font-size: 0.98rem;
  line-height: 1.6;
}

/* Control Panel */
.panel-card {
  background: #112238;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 1.6rem 1.8rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.panel-title {
  font-family: 'Cinzel', serif;
  font-size: 1.05rem;
  letter-spacing: 0.08em;
  color: var(--gold-accent);
  border-bottom: 1px solid rgba(197, 160, 89, 0.25);
  padding-bottom: 8px;
  margin-bottom: 1.2rem;
}
.stApp label p, .stApp [data-testid="stWidgetLabel"] p {
  color: #CBD5E1 !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  letter-spacing: 0.02em;
}

/* Boarding Pass */
.pass-ticket {
  background: var(--parchment);
  color: var(--text-dark);
  border-radius: 10px;
  box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(0,0,0,0.05);
  position: relative;
  overflow: hidden;
  border: 2px solid #D6CBB8;
}
.pass-header {
  background: #0E2238;
  border-bottom: 2px solid var(--gold-accent);
  padding: 18px 22px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #FAF8F5;
}
.star-line {
  font-family: 'Cinzel', serif;
  font-size: 0.75rem;
  letter-spacing: 0.18em;
  color: var(--gold-accent);
  text-transform: uppercase;
}
.ship-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.45rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.ticket-num {
  font-family: 'Courier New', monospace;
  font-size: 0.82rem;
  background: rgba(255,255,255,0.1);
  padding: 4px 10px;
  border-radius: 4px;
  letter-spacing: 0.08em;
}

.ticket-body {
  padding: 20px 24px 16px;
  background-image: radial-gradient(#d6cbb8 0.75px, transparent 0.75px);
  background-size: 14px 14px;
}
.ticket-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px 24px;
}
.field-cell small {
  display: block;
  text-transform: uppercase;
  font-size: 0.68rem;
  letter-spacing: 0.09em;
  font-weight: 700;
  color: #7A6B56;
}
.field-cell span {
  font-size: 1.08rem;
  font-weight: 700;
  color: #172121;
}

/* Perforation Tear Line */
.perforated-strip {
  display: flex;
  align-items: center;
  position: relative;
  height: 24px;
  background: transparent;
}
.notch-left, .notch-right {
  width: 24px;
  height: 24px;
  background: #0B192C;
  border-radius: 50%;
  position: absolute;
  top: 0;
}
.notch-left { left: -12px; }
.notch-right { right: -12px; }
.dashed-wire {
  flex-grow: 1;
  border-top: 2px dashed #B8A994;
  margin: 0 16px;
}

/* Verdict & Stamp */
.verdict-box {
  padding: 16px 24px 24px;
  text-align: center;
  background: #FAF6ED;
}
.stamp-wrap {
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 6px;
}
.stamp {
  display: inline-block;
  font-family: 'Cinzel', serif;
  font-weight: 800;
  font-size: 1.7rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 7px 22px;
  border-radius: 6px;
  border: 4px solid currentColor;
  box-shadow: 0 0 0 2px currentColor;
  transform: rotate(-4deg);
  animation: stamp-slam 0.32s cubic-bezier(0.18, 0.89, 0.32, 1.28);
}
.stamp.yes {
  color: var(--survived-green);
  background: rgba(27, 99, 72, 0.07);
}
.stamp.no {
  color: var(--lost-red);
  background: rgba(139, 38, 53, 0.07);
}

@keyframes stamp-slam {
  0% { transform: scale(2.2) rotate(-16deg); opacity: 0; }
  100% { transform: scale(1) rotate(-4deg); opacity: 0.95; }
}

.meter-frame {
  height: 12px;
  background: #E0D7C6;
  border-radius: 999px;
  max-width: 380px;
  margin: 16px auto 8px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.12);
}
.meter-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s ease;
}
.meter-fill.yes { background: linear-gradient(90deg, #2E8B57, #1b6348); }
.meter-fill.no { background: linear-gradient(90deg, #D9534F, #8B2635); }

.stat-caption {
  font-size: 0.9rem;
  color: #555A54;
  margin: 0;
  font-weight: 600;
}
.note-box {
  margin-top: 1.8rem;
  padding: 12px 16px;
  border-radius: 8px;
  background: rgba(255,255,255,0.03);
  border-left: 3px solid var(--gold-accent);
  color: #94A3B8;
  font-size: 0.8rem;
  line-height: 1.5;
}
</style>
"""

HERO = """
<div class="hero-card">
  <div class="hero-crest">White Star Line • Inquiry Division</div>
  <h1>RMS Titanic Boarding & Prognosis</h1>
  <p>Input passenger manifest attributes to estimate survival probability using historical voyage data from 1912.</p>
</div>
"""

st.markdown(CSS + HERO, unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return joblib.load(Path(__file__).parent / "titanic_model.pkl")


model = load_model()

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="panel-card"><div class="panel-title">Passenger Manifest Details</div>', unsafe_allow_html=True)
    
    pclass = st.radio("Ticket Class", ["First", "Second", "Third"], index=2, horizontal=True)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    sibling = st.select_slider("Siblings or Spouses Aboard", ["Zero", "One", "Two", "Three or more"])
    embarked = st.selectbox("Port of Embarkation", ["Southampton", "Cherbourg", "Queenstown"])

    st.markdown("</div>", unsafe_allow_html=True)

X = pd.DataFrame([{"PClass": pclass, "Gender": gender, "Sibling": sibling, "Embarked": embarked}])
survived = int(model.predict(X)[0]) == 1
prob = float(model.predict_proba(X)[0][1]) * 100
cls, word = ("yes", "Survived") if survived else ("no", "Did Not Survive")

with right:
    st.markdown(f"""
    <div class="pass-ticket">
      <div class="pass-header">
        <div>
          <div class="star-line">White Star Line</div>
          <div class="ship-title">RMS Titanic</div>
        </div>
        <div class="ticket-num">№ 1912-WSL</div>
      </div>
      <div class="ticket-body">
        <div class="ticket-grid">
          <div class="field-cell"><small>Class</small><span>{pclass} Class</span></div>
          <div class="field-cell"><small>Gender</small><span>{gender}</span></div>
          <div class="field-cell"><small>Accompanied By</small><span>{sibling} relative(s)</span></div>
          <div class="field-cell"><small>Port of Boarding</small><span>{embarked}</span></div>
        </div>
      </div>
      <div class="perforated-strip">
        <div class="notch-left"></div>
        <div class="dashed-wire"></div>
        <div class="notch-right"></div>
      </div>
      <div class="verdict-box">
        <div class="stamp-wrap">
          <div class="stamp {cls}">{word}</div>
        </div>
        <div class="meter-frame">
          <div class="meter-fill {cls}" style="width: {prob:.1f}%;"></div>
        </div>
        <p class="stat-caption">{prob:.1f}% estimated survival rate</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<div class="note-box">Model inference trained on 889 historical passengers. '
    'Predictions illustrate demographic survival patterns and biases of early 20th-century maritime evacuation protocols.</div>',
    unsafe_allow_html=True
)