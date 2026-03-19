import streamlit as st
import streamlit.components.v1 as components

# 1. إعداد الصفحة
st.set_page_config(page_title="Royal Racer", layout="wide")

# 2. تصميم الواجهة الفخمة
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1000");
        background-size: cover;
        color: #D4AF37;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 2px solid #D4AF37;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
    }
    .stButton>button {
        background: #D4AF37;
        color: black !important;
        border-radius: 12px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. نظام التنقل (الغرف)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- الغرفة 1: الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🔱 مركز رويال ريسر 🔱")
    st.write("استعد لتجربة قيادة ملكية فريدة")
    if st.button("🏁 دخول السباق"):
        st.session_state.page = 'play'
        st.rerun()
    if st.button("🛠️ دخول الكراج"):
        st.session_state.page = 'garage'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 2: الكراج ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("🛠️ كراج النخبة")
    st.color_picker("لون الهيكل الملكي", "#D4AF37")
    if st.button("⬅️ حفظ والعودة"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 3: السباق (تصميم جديد) ---
elif st.session_state.page == 'play':
    st.markdown('<div class="main-card" style="padding:10px;">', unsafe_allow_html=True)
    game_html = """
    <div style="color:#D4AF37; font-size:20px; margin-bottom:10px;">🏆 SCORE: <span id="s">0</span></div>
    <canvas id="race" width="300" height="450" style="border:3px solid #D4AF37; border-radius:15px; background:#222;"></canvas>
    <script>
        const c=document.getElementById("race"), ctx=c.getContext("2d");
        let x=125, score=0, enemies=[];
        function draw() {
            ctx.fillStyle="#222"; ctx.fillRect(0,0,300,450);
            ctx.fillStyle="#D4AF37"; ctx.fillRect(x, 350, 50, 80); // سيارتك
            if(Math.random()<0.02) enemies.push({x:Math.random()*250, y:-100});
            enemies.forEach((en, i)=>{
                en.y+=7; ctx.fillStyle="#fff"; ctx.fillRect(en.x, en.y, 45, 75); // عدو
                if(en.y>320 && en.y<430 && en.x>x-40 && en.x<x+40) location.reload();
                if(en.y>450) { enemies.splice(i,1); score+=100; }
            });
            document.getElementById("s").innerText=score;
            requestAnimationFrame(draw);
        }
        c.ontouchstart=(e)=>{ let t=e.touches[0].clientX-c.offsetLeft; x=(t<150)?Math.max(0,x-60):Math.min(250,x+60); };
        draw();
    </script>
    """
    components.html(game_html, height=520)
    if st.button("🔙 إنهاء"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
