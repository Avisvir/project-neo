import streamlit as st
import secrets
import string
import time
import random

# 1. --- CONFIGURATION ---
st.set_page_config(page_title="AVISVIR PassGen", page_icon="🔐", layout="centered")

# 2. --- THE MATRIX VISUAL ENGINE ---
# We inject the Canvas and CSS directly into the main DOM to ensure it sits behind the app
matrix_code = """
<style>
    /* 1. FORCE TRANSPARENCY ON ALL STREAMLIT LAYERS */
    .stApp {
        background: transparent !important;
    }
    header, footer {
        visibility: hidden !important;
    }
    .stDeployButton {
        display: none !important;
    }
    
    /* 2. THE CANVAS (BACKGROUND) */
    #matrix_canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1; /* Puts it behind everything */
        background: black;
    }

    /* 3. UI ELEMENT STYLING */
    h1 {
        color: #00FF41 !important;
        text-shadow: 0px 0px 10px #003300;
        font-family: 'Courier New', monospace;
    }
    
    /* Green Border & Text for Inputs */
    .stTextInput>div>div>input {
        color: #00FF41 !important;
        background-color: rgba(0, 20, 0, 0.8) !important;
        border: 1px solid #00FF41 !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Green Buttons */
    .stButton>button {
        color: #00FF41 !important;
        background-color: black !important;
        border: 1px solid #00FF41 !important;
        font-family: 'Courier New', monospace;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00FF41 !important;
        color: black !important;
        box-shadow: 0px 0px 15px #00FF41;
    }
    
    /* Code Blocks (Passwords) */
    .stCode {
        background-color: rgba(0, 0, 0, 0.9) !important;
        border-left: 5px solid #00FF41 !important;
    }
</style>

<canvas id="matrix_canvas"></canvas>

<script>
    const cvs = document.getElementById("matrix_canvas");
    const ctx = cvs.getContext("2d");

    // Force Fullscreen
    function resize() {
        cvs.width = window.innerWidth;
        cvs.height = window.innerHeight;
    }
    window.addEventListener("resize", resize);
    resize();

    // Configuration
    const cols = Math.floor(cvs.width / 20);
    const drops = Array(cols).fill(1);
    const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%^&*";
    
    // Parallax Strip Configuration (Left Side)
    const strip_cols = 4; // Width of the binary strip
    const strip_drops = Array(strip_cols).fill(1);

    function draw() {
        // Semi-transparent black rect to create trail effect
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, cvs.width, cvs.height);

        // 1. DRAW BACKGROUND RAIN (Dim Green)
        ctx.fillStyle = "#003300"; 
        ctx.font = "15px monospace";
        
        for (let i = strip_cols; i < drops.length; i++) {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * 20, drops[i] * 20);

            // Reset drop randomly after it crosses screen
            if (drops[i] * 20 > cvs.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }

        // 2. DRAW PARALLAX STRIP (Bright Neon Green, Different Speed)
        ctx.fillStyle = "#00FF41";
        ctx.font = "bold 16px monospace";
        
        for (let j = 0; j < strip_cols; j++) {
            const bin = Math.random() > 0.5 ? "1" : "0";
            const x = j * 20 + 5;
            
            // Draw at current drop position
            ctx.fillText(bin, x, strip_drops[j] * 20);
            
            if (strip_drops[j] * 20 > cvs.height && Math.random() > 0.95) {
                strip_drops[j] = 0;
            }
            // Fall speed is slightly faster (1.5x) for parallax effect
            strip_drops[j] += 1.25; 
        }
    }
    
    // Run animation loop
    setInterval(draw, 33);
</script>
"""
st.markdown(matrix_code, unsafe_allow_html=True)

# 3. --- ADVANCED LOGIC ENGINE ---

ANIMALS = ["Wolf", "Bear", "Hawk", "Horse", "Tiger", "Shark", "Eagle", "Snake", "Lion", "Raven", "Panda", "Fox", "Crow", "Deer", "Lynx"]

def to_l33t(text):
    # Heavy L33t mapping
    mapping = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7', 'b': '8', 'g': '9', 'z': '2'}
    return "".join(mapping.get(c.lower(), c) for c in text)

def ensure_complexity(text):
    """
    Forces the string to have:
    - At least 2 Uppercase
    - At least 2 Lowercase
    - At least 2 Digits
    - At least 1 Special Char
    """
    # Convert string to list for mutation
    chars = list(text)
    
    # Define sets
    upper = list(string.ascii_uppercase)
    lower = list(string.ascii_lowercase)
    digits = list(string.digits)
    special = list("!@#$%&*")
    
    # Check counts
    u_count = sum(1 for c in chars if c.isupper())
    l_count = sum(1 for c in chars if c.islower())
    d_count = sum(1 for c in chars if c.isdigit())
    s_count = sum(1 for c in chars if c in "!@#$%&*")
    
    # Inject missing types (replacing random characters)
    while u_count < 2:
        idx = secrets.randbelow(len(chars))
        chars[idx] = secrets.choice(upper)
        u_count += 1
        
    while l_count < 2:
        idx = secrets.randbelow(len(chars))
        chars[idx] = secrets.choice(lower)
        l_count += 1
        
    while d_count < 2:
        idx = secrets.randbelow(len(chars))
        chars[idx] = secrets.choice(digits)
        d_count += 1
        
    while s_count < 1:
        idx = secrets.randbelow(len(chars))
        chars[idx] = secrets.choice(special)
        s_count += 1
        
    return "".join(chars)

def generate_strong_password(seed=None):
    # 1. Base Generation
    if seed:
        clean = seed.replace(" ", "").replace("_", "")
        base = to_l33t(clean)
    else:
        base = to_l33t(secrets.choice(ANIMALS))
    
    # 2. Length padding (add animals if too short)
    while len(base) < 10:
        base += to_l33t(secrets.choice(ANIMALS))
        
    # 3. Apply Complexity Rules (2 Upper, 2 Lower, 2 Digits, 1 Special)
    complex_pass = ensure_complexity(base)
    
    # 4. Final Polish
    # 50% chance to append '!' if length permits
    if len(complex_pass) < 15 and secrets.choice([True, False]):
        complex_pass += "!"
        
    # Trim to max 15
    if len(complex_pass) > 15:
        complex_pass = complex_pass[:15]
        
    # Pad to min 12
    if len(complex_pass) < 12:
        padding = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12 - len(complex_pass)))
        complex_pass += padding
        
    return complex_pass

# 4. --- SESSION STATE & TIMERS ---

if 'pass_list' not in st.session_state:
    st.session_state.pass_list = []
if 'last_action' not in st.session_state:
    st.session_state.last_action = time.time()

# 5-Minute Hard Wipe
if time.time() - st.session_state.last_action > 300:
    st.session_state.pass_list = []
    st.session_state.last_action = time.time()

def update_timer():
    st.session_state.last_action = time.time()

def run_gen():
    update_timer()
    seed = st.session_state.seed_input
    # Generate 8 variations
    st.session_state.pass_list = [
        generate_strong_password(seed if seed.strip() else None) 
        for _ in range(8)
    ]

# 5. --- UI LAYOUT ---

st.markdown("<h1>AVISVIR PassGen</h1>", unsafe_allow_html=True)

# Main Input
st.text_input(
    "LABEL_HIDDEN", 
    placeholder="ENTER CURRENT PASSWORD OR GENERATE PASSWORD", 
    label_visibility="collapsed",
    key="seed_input",
    on_change=run_gen
)

c1, c2 = st.columns(2)

if c1.button("GENERATE PASSWORD"):
    run_gen()

current_val = st.session_state.get("seed_input", "")
if current_val.strip() != "":
    if c2.button("ENHANCE CURRENT PASSWORD"):
        run_gen()

# 6. --- RESULTS ---

if st.session_state.pass_list:
    st.write("---")
    for i, pwd in enumerate(st.session_state.pass_list):
        col_code, col_btn = st.columns([4, 1])
        col_code.code(pwd, language=None)
        
        if col_btn.button("ENHANCE", key=f"btn_{i}"):
            update_timer()
            # Regenerate using the current result as the seed
            st.session_state.pass_list[i] = generate_strong_password(pwd[:6])
            st.rerun()

# 7. --- BACKGROUND REFRESH ---
# Keeps the connection alive to check the 5-minute timer
st.components.v1.html(
    f"""<script>
    setTimeout(function(){{ window.parent.location.reload(); }}, 305000);
    </script>""",
    height=0
)
