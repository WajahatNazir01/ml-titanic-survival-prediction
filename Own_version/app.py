from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Titanic boarding check", page_icon="🚢", layout="centered")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;500;700&family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&display=swap');
html, body, .stApp, [class*="css"] { font-family: 'Libre Franklin', system-ui, sans-serif; }
.stApp { background: #E9EEF1; color: #10243B; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 900px; padding-top: 1.5rem; }
.stApp label p, .stApp [data-testid="stWidgetLabel"] p { color: #10243B !important; font-weight: 500; }
.stApp div[data-baseweb="select"] > div { background: #fff; color: #10243B; }

.hero { background: #10243B; border-radius: 6px; padding: 26px 30px 0; margin-bottom: 26px; overflow: hidden; }
.hero h1 { font-family: 'Old Standard TT', Georgia, serif; font-weight: 700; font-size: 2.3rem;
           line-height: 1.15; color: #F3EFE4; margin: 0 0 8px; }
.hero p { color: #A9BBCB; margin: 0; max-width: 52ch; line-height: 1.55; }
.hero svg { display: block; width: 100%; height: 84px; margin-top: 14px; }

.pass { background: #FBFAF6; border-radius: 8px; box-shadow: 0 1px 0 #C9D3DA, 0 10px 24px -14px #10243B66;
        position: relative; overflow: hidden; }
.pass-head { background: #1D4E69; color: #F3EFE4; padding: 14px 22px; display: flex;
             justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap; }
.pass-head .ship { font-family: 'Old Standard TT', Georgia, serif; font-size: 1.25rem; font-weight: 700; }
.pass-head .route { font-size: .85rem; color: #C5D5E0; }
.fields { display: grid; grid-template-columns: 1fr 1fr; gap: 14px 18px; padding: 20px 22px 18px; }
.fields small { display: block; color: #6A7B8A; font-size: .78rem; margin-bottom: 2px; }
.fields b { font-size: 1.05rem; font-weight: 600; }
.perf { border-top: 2px dashed #B9C5CE; margin: 0 14px; position: relative; }
.perf::before, .perf::after { content: ""; position: absolute; top: -11px; width: 20px; height: 20px;
                              border-radius: 50%; background: #E9EEF1; }
.perf::before { left: -24px; } .perf::after { right: -24px; }
.verdict { padding: 22px 22px 24px; text-align: center; }
.stamp { display: inline-block; font-family: 'Old Standard TT', Georgia, serif; font-weight: 700;
         font-size: 1.9rem; padding: 6px 22px; border: 4px double currentColor; border-radius: 6px;
         transform: rotate(-5deg); animation: thud .35s ease-out; }
.stamp.yes { color: #1F7A5A; } .stamp.no { color: #A8232B; }
@keyframes thud { from { transform: rotate(-14deg) scale(1.7); opacity: 0; } to { transform: rotate(-5deg) scale(1); opacity: 1; } }
.bar { height: 10px; background: #D5DDE2; border-radius: 5px; margin: 22px auto 8px; max-width: 360px; overflow: hidden; }
.bar span { display: block; height: 100%; border-radius: 5px; }
.bar .yes { background: #1F7A5A; } .bar .no { background: #A8232B; }
.odds { margin: 0; color: #4A5D70; font-size: .95rem; }
.note { font-size: .82rem; color: #6A7B8A; margin-top: 22px; line-height: 1.5; }
@media (prefers-reduced-motion: reduce) { .stamp { animation: none; } }
</style>
"""

HERO = """
<div class="hero">
  <h1>Would this passenger have survived?</h1>
  <p>Choose a passenger’s details and the model checks the odds, based on 889 real passengers from the 1912 voyage.</p>
  <svg viewBox="0 0 600 84" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
    <rect x="0" y="70" width="600" height="14" fill="#1D4E69"/>
    <path d="M70 70 L90 54 H520 L548 70 Z" fill="#0A1626"/>
    <rect x="130" y="42" width="330" height="12" fill="#E8E4D8"/>
    <g fill="#D9A441"><rect x="170" y="14" width="22" height="28"/><rect x="226" y="14" width="22" height="28"/>
       <rect x="282" y="14" width="22" height="28"/><rect x="338" y="14" width="22" height="28"/></g>
    <g fill="#0A1626"><rect x="170" y="14" width="22" height="6"/><rect x="226" y="14" width="22" height="6"/>
       <rect x="282" y="14" width="22" height="6"/><rect x="338" y="14" width="22" height="6"/></g>
  </svg>
</div>
"""

st.markdown(CSS + HERO, unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return joblib.load(Path(__file__).parent / "titanic_model.pkl")


model = load_model()

left, right = st.columns([5, 6], gap="large")

with left:
    pclass = st.radio("Ticket class", ["First", "Second", "Third"], index=2, horizontal=True)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    sibling = st.select_slider("Siblings or spouses aboard", ["Zero", "One", "Two", "Three or more"])
    embarked = st.selectbox("Port of embarkation", ["Southampton", "Cherbourg", "Queenstown"])

X = pd.DataFrame([{"PClass": pclass, "Gender": gender, "Sibling": sibling, "Embarked": embarked}])
survived = int(model.predict(X)[0]) == 1
prob = float(model.predict_proba(X)[0][1]) * 100
cls, word = ("yes", "Survived") if survived else ("no", "Did not survive")

with right:
    st.markdown(f"""
    <div class="pass">
      <div class="pass-head"><span class="ship">RMS Titanic</span>
        <span class="route">Southampton to New York, April 1912</span></div>
      <div class="fields">
        <div><small>Class</small><b>{pclass}</b></div>
        <div><small>Gender</small><b>{gender}</b></div>
        <div><small>Siblings or spouses</small><b>{sibling}</b></div>
        <div><small>Boarded at</small><b>{embarked}</b></div>
      </div>
      <div class="perf"></div>
      <div class="verdict">
        <div class="stamp {cls}" key="{cls}">{word}</div>
        <div class="bar"><span class="{cls}" style="width:{prob:.0f}%"></span></div>
        <p class="odds">{prob:.0f}% chance of survival</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<p class="note">Built for a university machine learning assignment using the full Titanic '
            'dataset (889 passengers after cleaning). Predictions reflect patterns in that data only.</p>',
            unsafe_allow_html=True)