import streamlit as st
import secrets
import string
import time
import random

# 1. --- CONFIGURATION ---
st.set_page_config(page_title="AVISVIR PassGen", page_icon="🔐", layout="centered")

# 2. --- STYLING & MATRIX ENGINE (With Parallax) ---
style_and_engine = """
<style>
    /* DE-BRANDING: Hides Streamlit UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* BACKGROUND */
    #matrixCanvas {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        z-index: -1;
        background-color: black;
    }
    
    /* UI STYLING */
    .stApp { background: transparent; color: #00FF41; font-family: 'Courier New', monospace; }
    
    /* INPUT BOX STYLING */
    .stTextInput>div>div>input { 
        background-color: rgba(0,0,0,0.8) !important; 
        color: #00FF41 !important; 
        border: 1px solid #00FF41 !important; 
        border-radius: 0px;
    }
    
    /* BUTTON STYLING */
    .stButton>button { 
        border: 1px solid #00FF41; 
        background: black; 
        color: #00FF41; 
        border-radius: 0; 
        width: 100%; 
        transition: 0.3s;
        text-transform: uppercase;
        font-weight: bold;
    }
    .stButton>button:hover { 
        background: #00FF41; 
        color: black; 
        border-color: #00FF41;
    }
    
    /* TEXT STYLING */
    h1 { 
        font-size: 1.5rem !important; 
        text-align: center; 
        color: #00FF41; 
        margin-bottom: 2rem;
        text-shadow: 0 0 10px #00FF41;
    }
    .stCode { border: 1px solid #004d13 !important; background-color: #050505 !important; }
</style>

<canvas id="matrixCanvas"></canvas>

<script>
    const canvas = document.getElementById('matrixCanvas');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const matrixChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*";
    const binaryChars = "01";
    const fontSize = 14;
    const columns = Math.floor(canvas.width / fontSize);
    
    // Matrix Rain Drops
    const drops = Array(columns).fill(1);
    
    // Parallax Strip Drops (Left side only)
    const stripCols = 5; // Width of the binary strip
    const stripDrops = Array(stripCols).fill(1);

    function draw() {
        // Fade effect for trails
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 1. DRAW SUBTLE MATRIX RAIN (Background)
        ctx.fillStyle = '#003300'; // Very dim green
        ctx.font = fontSize + 'px monospace';
        
        for (let i = stripCols; i < drops.length; i++) {
            const text = matrixChars.charAt(Math.floor(Math.random() * matrixChars.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }

        // 2. DRAW PARALLAX BINARY STRIP (Left Foreground)
        ctx.fillStyle = '#00FF41'; // Bright Neon Green
        for (let j = 0; j < stripCols; j++) {
            const bin = binaryChars.charAt(Math.floor(Math.random() * 2));
            
            // Draw slightly faster/different speed for parallax feel
            ctx.fillText(bin, j * fontSize, stripDrops[j] * fontSize);
            
            if (stripDrops[j] * fontSize > canvas.height && Math.random() > 0.95) {
                stripDrops[j] = 0;
            }
            stripDrops[j] += 1.5; // Faster fall speed
        }
    }
    setInterval(draw, 50);
</script>
"""
st.markdown(style_and_engine, unsafe_allow_html=True)

# 3. --- SECURITY ALGORITHMS ---

ANIMALS = ["Wolf", "Bear", "Hawk", "Horse", "Tiger", "Shark", "Eagle", "Snake", "Lion", "Raven", "Panda", "Fox", "Crow", "Deer", "Lynx"]

def to_l33t(text):
    # Heavy L33t mapping
    mapping = {
        'a': '4', 'e': '3', 'i': '1', 'o': '0', 
        's': '5', 't': '7', 'b': '8', 'g': '9', 'z': '2'
    }
    return "".join(mapping.get(c.lower(), c) for c in text)

def generate_strong_password(base_seed=None):
    # 1. Determine Base
    if base_seed:
        # Clean input: remove spaces/underscores
        clean_seed = base_seed.replace(" ", "").replace("_", "")
        base = to_l33t(clean_seed)
    else:
        base = to_l33t(secrets.choice(ANIMALS))

    # 2. Ensure Length (12-15 chars)
    # If too short, add another l33t animal
    while len(base) < 10:
        base += to_l33t(secrets.choice(ANIMALS))
    
    # 3. Inject Complexity (If missing)
    # We build a suffix to ensure requirements are met
    suffix = ""
    
    # Needs at least 2 numbers
    num_count = sum(c.isdigit() for c in base)
    if num_count < 2:
        suffix += "".join(secrets.choice(string.digits) for _ in range(2 - num_count))
        
    # Needs 1 Special Char
    special_chars = "!@#$%^&*"
    if not any(c in special_chars for c in base):
        suffix += secrets.choice(special_chars)
        
    # Needs 1 Upper Case
    if not any(c.isupper() for c in base):
        # Randomly capitalize a letter in base, or add one
        suffix += secrets.choice(string.ascii_uppercase)

    full_pass = base + suffix
    
    # 4. Final Length Trim/Pad
    if len(full_pass) > 15:
        full_pass = full_pass[:15]
    elif len(full_pass) < 12:
        padding = "".join(secrets.choice(string.digits + special_chars) for _ in range(12 - len(full_pass)))
        full_pass += padding
        
    return full_pass

# 4. --- SESSION & TIMER LOGIC ---

if 'pass_list' not in st.session_state:
    st.session_state.pass_list = []
if 'last_action' not in st.session_state:
    st.session_state.last_action = time.time()

# 5-Minute Hard Wipe
TIMEOUT = 300
if time.time() - st.session_state.last_action > TIMEOUT:
    st.session_state.pass_list = []
    st.session_state.last_action = time.time()

def update_timer():
    st.session_state.last_action = time.time()

def run_generation():
    update_timer()
    seed = st.session_state.seed_input
    
    if not seed:
        # Empty box: Generate 8 random new passwords
        st.session_state.pass_list = [generate_strong_password(None) for _ in range(8)]
    else:
        # Text in box: Generate 8 variations of that text
        st.session_state.pass_list = [generate_strong_password(seed) for _ in range(8)]

# 5. --- UI LAYOUT ---

st.markdown("<h1>AVISVIR PassGen</h1>", unsafe_allow_html=True)

# Input Box (Enter key triggers 'on_change')
st.text_input(
    "LABEL_HIDDEN", 
    placeholder="ENTER CURRENT PASSWORD OR GENERATE RANDOM PASSWORD", 
    label_visibility="collapsed",
    key="seed_input",
    on_change=run_generation
)

col1, col2 = st.columns(2)

# Button 1: Execute (Always visible)
if col1.button("EXECUTE GENERATOR"):
    run_generation()

# Button 2: Enhance (Only visible if text exists)
# Note: We check the session state key because the variable might not update instantly
current_input = st.session_state.get("seed_input", "")
if current_input.strip() != "":
    if col2.button("ENHANCE CURRENT PASSWORD"):
        run_generation()

# 6. --- RESULTS DISPLAY ---

if st.session_state.pass_list:
    st.write("---")
    
    for i, pwd in enumerate(st.session_state.pass_list):
        c1, c2 = st.columns([3, 1])
        
        c1.code(pwd, language=None)
        
        # Unique key for each button to track state
        if c2.button("ENHANCE", key=f"btn_{i}"):
            update_timer()
            # Regenerate this specific password using itself as the seed base
            # We take the first few chars to keep the 'theme' but randomize the rest
            base_seed = pwd[:6] 
            st.session_state.pass_list[i] = generate_strong_password(base_seed)
            st.rerun()

# 7. --- INACTIVITY MONITOR ---
# Hidden script to refresh page if user is idle for > 5 mins (client side check)
st.components.v1.html(
    f"""<script>
    setTimeout(function(){{ window.parent.location.reload(); }}, 305000);
    </script>""",
    height=0
)
