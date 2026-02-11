import streamlit as st
import secrets
import string
import time
import random

# 1. --- CONFIGURATION ---
st.set_page_config(page_title="AVISVIR PassGen", page_icon="🔐", layout="centered")

# 2. --- THE TRANSPARENCY BLUEPRINT (CSS) ---
# This forces the Streamlit "sandwich" to be transparent so the rain shows through
st.markdown("""
    <style>
        /* Target every possible Streamlit background layer */
        .stApp, .stAppViewMain, .stMain, [data-testid="stAppViewMain"], .main {
            background: transparent !important;
        }
        /* Hide UI clutter */
        header, footer, .stDeployButton { visibility: hidden !important; display: none !important; }
        
        /* Typography */
        h1 { 
            color: #00FF41 !important; 
            text-align: center; 
            font-size: 1.5rem !important;
            font-family: 'Courier New', monospace;
            text-shadow: 0 0 10px #003300;
        }
        .stCode { background: rgba(0,0,0,0.7) !important; border: 1px solid #004d13 !important; }
        p, label { color: #00FF41 !important; font-family: 'Courier New', monospace; }
        
        /* Input & Buttons */
        .stTextInput input {
            background: rgba(0, 20, 0, 0.9) !important;
            color: #00FF41 !important;
            border: 1px solid #00FF41 !important;
        }
        .stButton button {
            background: black !important;
            color: #00FF41 !important;
            border: 1px solid #00FF41 !important;
            width: 100%;
        }
        .stButton button:hover { background: #00FF41 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# 3. --- THE ANIMATION ENGINE (HTML/JS) ---
# This runs the rain on a fixed canvas behind the app
matrix_bg = """
<div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; background: black;">
    <canvas id="m"></canvas>
</div>
<script>
    const c = document.getElementById("m");
    const q = c.getContext("2d");
    const s = window.screen;
    const w = c.width = s.width;
    const h = c.height = s.height;
    const p = Array(Math.floor(w/20)).fill(1);
    const m = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*";

    setInterval(() => {
        q.fillStyle = "rgba(0,0,0,0.05)";
        q.fillRect(0,0,w,h);
        
        // Background Rain
        q.fillStyle = "#003300";
        q.font = "15px monospace";
        p.forEach((y, i) => {
            if (i > 3) { // Offset for the parallax strip
                q.fillText(m[Math.floor(Math.random()*m.length)], i*20, y);
                p[i] = (y > h + Math.random()*1e4) ? 0 : y + 20;
            }
        });

        // Parallax Binary Strip (Left Side)
        q.fillStyle = "#00FF41";
        for(let j=0; j<4; j++) {
            q.fillText(Math.random() > 0.5 ? "1" : "0", j*20+5, (Date.now()*0.2 + (j*100)) % h);
        }
    }, 33);
</script>
"""
st.components.v1.html(matrix_bg, height=0)

# 4. --- LOGIC ---
ANIMALS = ["Wolf", "Bear", "Hawk", "Horse", "Tiger", "Shark", "Eagle", "Snake", "Lion", "Raven", "Panda", "Fox", "Crow", "Deer", "Lynx"]

def to_l33t(t):
    d = {'a':'4','e':'3','i':'1','o':'0','s':'5','t':'7','b':'8','g':'9','z':'2'}
    return "".join(d.get(c.lower(), c) for c in t)

def generate_strong_password(seed=None):
    base = to_l33t(seed.replace(" ","")) if seed else to_l33t(secrets.choice(ANIMALS))
    while len(base) < 10: base += to_l33t(secrets.choice(ANIMALS))
    
    # Complexity: 2 Upper, 2 Lower, 2 Nums, 1 Special
    res = list(base)
    for i, char_set in enumerate([string.ascii_uppercase, string.ascii_lowercase, string.digits, "!@#$%&*"]):
        needed = 2 if i < 3 else 1
        for _ in range(needed):
            res[secrets.randbelow(len(res))] = secrets.choice(char_set)
    
    # Final cleanup & chance for '!'
    pwd = "".join(res)
    if len(pwd) < 15 and secrets.choice([True, False]): pwd += "!"
    return pwd[:15] if len(pwd) > 15 else (pwd if len(pwd) >= 12 else pwd.ljust(12, '1'))

# 5. --- UI ---
if 'pass_list' not in st.session_state: st.session_state.pass_list = []
if 'last_act' not in st.session_state: st.session_state.last_act = time.time()

# 5-Min Hard Wipe
if time.time() - st.session_state.last_act > 300:
    st.session_state.pass_list = []
    st.session_state.last_act = time.time()

st.markdown("<h1>AVISVIR PassGen</h1>", unsafe_allow_html=True)

seed = st.text_input("LABEL", placeholder="ENTER CURRENT PASSWORD OR GENERATE PASSWORD", label_visibility="collapsed", key="seed_input")

def run():
    st.session_state.last_act = time.time()
    s = st.session_state.seed_input
    st.session_state.pass_list = [generate_strong_password(s if s.strip() else None) for _ in range(8)]

# Enter Key behavior: If seed exists, treat as "Enhance"
if seed and not st.session_state.pass_list: run()

c1, c2 = st.columns(2)
if c1.button("GENERATE PASSWORD"): run()
if seed.strip() and c2.button("ENHANCE CURRENT PASSWORD"): run()

if st.session_state.pass_list:
    st.write("---")
    for i, p in enumerate(st.session_state.pass_list):
        col1, col2 = st.columns([4, 1])
        col1.code(p, language=None)
        if col2.button("ENHANCE", key=f"e_{i}"):
            st.session_state.last_act = time.time()
            st.session_state.pass_list[i] = generate_strong_password(p[:6])
            st.rerun()
