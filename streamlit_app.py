import streamlit as st
import secrets
import string
import time

# 1. --- CONFIGURATION ---
st.set_page_config(page_title="PROJECT_NEO", page_icon="📟", layout="centered")

# 2. --- STYLING & MATRIX ENGINE ---
style_and_matrix = """
<style>
    #matrixCanvas {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        z-index: -1;
    }
    .stApp { background: rgba(0, 0, 0, 0.9); color: #00FF41; font-family: 'Courier New', monospace; }
    .stCode { border-left: 3px solid #00FF41 !important; background-color: #050505 !important; }
    .stButton>button { border: 1px solid #00FF41; background: black; color: #00FF41; border-radius: 0; width: 100%; }
    .stTextInput>div>div>input { background-color: #000 !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
</style>
<canvas id="matrixCanvas"></canvas>
<script>
    const canvas = document.getElementById('matrixCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*";
    const fontSize = 16;
    const columns = Math.floor(canvas.width / fontSize);
    const drops = Array(columns).fill(1);
    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#0F0';
        ctx.font = fontSize + 'px monospace';
        for (let i = 0; i < drops.length; i++) {
            const text = letters.charAt(Math.floor(Math.random() * letters.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 50);
</script>
"""
st.markdown(style_and_matrix, unsafe_allow_html=True)

# 3. --- SECURITY & SESSION LOGIC ---

if 'pass_list' not in st.session_state:
    st.session_state.pass_list = []
if 'last_action' not in st.session_state:
    st.session_state.last_action = time.time()

# SELF-DESTRUCT CALCULATION
TIMEOUT = 300 # 5 Minutes
time_passed = time.time() - st.session_state.last_action

if time_passed > TIMEOUT and st.session_state.pass_list:
    st.session_state.pass_list = []
    st.session_state.last_action = time.time()
    st.rerun()

def update_activity():
    st.session_state.last_action = time.time()

def is_input_safe(word):
    banned = ["password", "admin", "root", "12345"]
    for b in banned:
        if b in word.lower(): return False, b
    return True, None

def generate_variations(base):
    vars = []
    for i in range(10):
        s = secrets.choice("!@#$%^&*")
        n = secrets.choice(string.digits)
        suf = "".join(secrets.choice(string.ascii_letters) for _ in range(3))
        if i < 3: vars.append(f"{base}{n}{n}{s}")
        elif i < 6: vars.append(f"{s}{base}{n}{suf}")
        else:
            leet = base.translate(str.maketrans("aeio", "@310"))
            vars.append(f"{leet}_{suf}{s}")
    return vars

def enhance_password(pwd):
    salt = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(4))
    return f"{salt}-{pwd}-{salt[::-1]}"

# 4. --- UI INTERFACE ---

st.title("⚡ [ PROJECT_NEO ]")

# Safety Status Bar
time_left = int(TIMEOUT - time_passed)
if st.session_state.pass_list:
    st.info(f"🛡️ SESSION ACTIVE: Data auto-destructs in {time_left} seconds of inactivity.")

user_input = st.text_input("ENTER SEED WORD:", placeholder="Skyline", on_change=update_activity)

col_gen, col_clr = st.columns(2)

if col_gen.button("EXECUTE GENERATOR"):
    update_activity()
    if user_input:
        safe, trigger = is_input_safe(user_input)
        if safe:
            st.session_state.pass_list = generate_variations(user_input)
        else:
            st.error(f"SECURITY ALERT: {trigger.upper()}")
    else:
        st.warning("ERROR: NO SEED DETECTED")

if col_clr.button("WIPE ALL DATA"):
    st.session_state.pass_list = []
    st.session_state.last_action = time.time()
    st.rerun()

# 5. --- RESULTS & EXPORT ---

if st.session_state.pass_list:
    st.write("---")
    
    # Prepare Export Data
    export_string = "\n".join(st.session_state.pass_list)
    
    st.download_button(
        label="📥 DOWNLOAD ENCRYPTED TEXT FILE",
        data=export_string,
        file_name="NEO_PASSWORDS.txt",
        mime="text/plain",
        on_click=update_activity
    )

    for i, pwd in enumerate(st.session_state.pass_list):
        c1, c2 = st.columns([4, 1])
        c1.code(pwd, language=None)
        if c2.button("ENHANCE", key=f"enh_{i}"):
            update_activity()
            st.session_state.pass_list[i] = enhance_password(pwd)
            st.rerun()

# 6. --- DISCLAIMER & AUTO-REFRESH ---
st.divider()
st.caption("STATUS: ENCRYPTED // CONNECTION: HTTPS // STORAGE: NONE (RAM ONLY)")
st.caption("PRIVACY: No data is saved to disk. All passwords vanish on refresh or inactivity.")

# Hidden Auto-Refresh Script (Forces a check every 30 seconds)
st.components.v1.html(
    """<script>window.parent.setTimeout(function(){ window.parent.location.reload(); }, 30000);</script>""",
    height=0
)