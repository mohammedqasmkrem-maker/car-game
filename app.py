import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="Royal Racer Hub", layout="centered")

# --- تصميم الواجهة الملكية (CSS) ---
st.markdown("""
    <style>
    /* إضافة خلفية ملكية للصورة */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* جعل الحاويات شفافة وزجاجية */
    .main-box {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* تصميم الأزرار الملكية */
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: black !important;
        border-radius: 50px;
        border: none;
        font-weight: bold;
        font-size: 20px;
        height: 3em;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# نظام التنقل بين الغرف
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate(p):
    st.session_state.page = p

# --- الغرفة 1: الواجهة الملكية (Home) ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.markdown("<h1 style='color: #FFD700; text-shadow: 2px 2px 5px #000;'>ROYAL TRAFFIC RACER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: white;'>مرحباً بك في عالم الفخامة والسرعة</p>", unsafe_allow_html=True)
    
    if st.button("🏁 دخول الميدان الملكي"):
        navigate('game')
    if st.button("🛠️ كراج النخبة"):
        navigate('garage')
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 2: الكراج (التعديل) ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.header("🛠️ كراج التعديلات")
    st.write("خصص سيارتك لتناسب ذوقك الملكي")
    
    color = st.color_picker("اختر لون السيارة", "#FFD700")
    engine = st.selectbox("المحرك", ["V8 Bi-Turbo", "V12 Gold Edition"])
    
    if st.button("✅ حفظ التعديلات والعودة"):
        navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 3: اللعبة (بدون مشاكل برمجية) ---
elif st.session_state.page == 'game':
    st.markdown('<div class="main-box" style="padding: 10px;">', unsafe_allow_html=True)
    
    # اللعبة داخل إطار زجاجي
    game_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { margin: 0; background: transparent; display: flex; flex-direction: column; align-items: center; }
            canvas { border: 3px solid #FFD700; border-radius: 15px; background: #222; }
            .info { color: #FFD700; font-family: sans-serif; font-size: 22px; margin-bottom: 10px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="info">POINTS: <span id="s">0</span></div>
        <canvas id="g" width="320" height="480"></canvas>
        <script>
            const canvas = document.getElementById("g");
            const ctx = canvas.getContext("2d");
            let x = 135, score = 0, enemies = [];
            
            function draw() {
                ctx.fillStyle = "#111"; ctx.fillRect(0,0,320,480);
                // رسم سيارة ذهبية مبسطة
                ctx.fillStyle = "#FFD700"; ctx.fillRect(x, 380, 50, 80);
                
                if(Math.random() < 0.02) enemies.push({x: Math.random()*270, y: -100});
                enemies.forEach((en, i) => {
                    en.y += 6;
                    ctx.fillStyle = "#fff"; ctx.fillRect(en.x, en.y, 45, 80);
                    if(en.y > 330 && en.y < 430 && en.x > x-40 && en.x < x+40) { location.reload(); }
                    if(en.y > 480) { enemies.splice(i,1); score += 50; }
                });
                document.getElementById("s").innerText = score;
                requestAnimationFrame(draw);
            }
            canvas.ontouchstart = (e) => {
                let tx = e.touches[0].clientX - canvas.offsetLeft;
                x = (tx < 160) ? Math.max(0, x-60) : Math.min(270, x+60);
            };
            draw();
        </script>
    </body>
    </html>
    """
    components.html(game_html, height=550)
    
    if st.button("❌ خروج"):
        navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)
    
