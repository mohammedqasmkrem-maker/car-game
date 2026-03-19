import streamlit as st
import streamlit.components.v1 as components
import random

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="Royal Racer Pro", layout="wide", initial_sidebar_state="collapsed")

# 2. نظام الذاكرة (Session State) لحفظ النقاط والتعديلات
if 'score' not in st.session_state: st.session_state.score = 0
if 'money' not in st.session_state: st.session_state.money = 1000
if 'car_color' not in st.session_state: st.session_state.car_color = "#D4AF37"
if 'engine_level' not in st.session_state: st.session_state.engine_level = "V8"
if 'page' not in st.session_state: st.session_state.page = 'home'

# 3. تصميم الواجهة الملكية (CSS)
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1200");
        background-size: cover;
        color: white;
    }}
    .royal-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 2px solid {st.session_state.car_color};
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 30px {st.session_state.car_color}44;
    }}
    .stButton>button {{
        background: linear-gradient(45deg, {st.session_state.car_color}, #fff);
        color: black !important;
        border-radius: 50px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- الغرفة 1: الواجهة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.title("🔱 ROYAL TRAFFIC RACER 🔱")
    st.subheader(f"💰 الرصيد: {st.session_state.money} | 🏆 أعلى نتيجة: {st.session_state.score}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏁 ابدأ السباق"): st.session_state.page = 'play'; st.rerun()
    with col2:
        if st.button("🛠️ الكراج الملكي"): st.session_state.page = 'garage'; st.rerun()
    with col3:
        if st.button("🏆 المتصدرين"): st.session_state.page = 'leaderboard'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 2: الكراج المتطور ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header("🛠️ تخصيص مركبة النخبة")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.session_state.car_color = st.color_picker("لون الهيكل (النيون)", st.session_state.car_color)
        st.session_state.engine_level = st.select_slider("تطوير المحرك", options=["V8", "V10", "V12", "W16 Hyper"])
    with col_b:
        st.write("🔧 حالة المركبة: ممتازة")
        st.write(f"💸 تكلفة التطوير: 500 عملة")
        if st.button("شراء تطوير التوربو"):
            if st.session_state.money >= 500:
                st.session_state.money -= 500
                st.success("تم التطوير!")
            else: st.error("الرصيد غير كافٍ!")

    if st.button("⬅️ العودة للرئيسية"): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 3: ميدان السباق (اللعبة الاحترافية) ---
elif st.session_state.page == 'play':
    # كود اللعبة المطور مع نيترو، تصادم، وحركة واقعية
    game_js = f"""
    <div style="display:flex; justify-content:space-between; color:{st.session_state.car_color}; font-weight:bold; font-size:20px; padding:10px;">
        <span>POINTS: <span id="s">0</span></span>
        <span>NITRO: <span id="n">READY</span></span>
    </div>
    <canvas id="race" width="320" height="500" style="border:3px solid {st.session_state.car_color}; border-radius:20px; background:#222;"></canvas>
    
    <script>
        const c=document.getElementById("race"), ctx=c.getContext("2d");
        let px=135, py=400, score=0, enemies=[], nitro=false, speed=7;

        function drawPlayer(x, y, isNitro) {{
            ctx.fillStyle = isNitro ? "#fff" : "{st.session_state.car_color}";
            ctx.beginPath(); ctx.roundRect(x, y, 50, 85, 10); ctx.fill();
            // تفاصيل السيارة
            ctx.fillStyle = "#111"; ctx.fillRect(x+5, y+15, 40, 20); // زجاج
            if(isNitro) {{ // لهب النيترو
                ctx.fillStyle = "orange"; ctx.fillRect(x+10, y+85, 10, 20); ctx.fillRect(x+30, y+85, 10, 20);
            }}
        }}

        function update() {{
            ctx.fillStyle="#1a1a1a"; ctx.fillRect(0,0,320,500); // الشارع
            
            // خطوط الطريق
            ctx.strokeStyle="#444"; ctx.setLineDash([20, 20]);
            ctx.beginPath(); ctx.moveTo(160, 0); ctx.lineTo(160, 500); ctx.stroke();

            drawPlayer(px, py, nitro);

            if(Math.random()<0.02) enemies.push({{x:Math.random()*260, y:-100, color: '#'+Math.floor(Math.random()*16777215).toString(16)}});
            
            enemies.forEach((en, i)=>{{
                en.y += nitro ? speed*2 : speed;
                ctx.fillStyle = en.color; ctx.beginPath(); ctx.roundRect(en.x, en.y, 45, 80, 5); ctx.fill();
                
                // تصادم
                if(en.y+70 > py && en.y < py+70 && en.x+40 > px && en.x < px+40) {{
                    alert("GAME OVER! Score: " + score); location.reload();
                }}
                if(en.y > 500) {{ enemies.splice(i,1); score += 10; }}
            }});

            document.getElementById("s").innerText = score;
            requestAnimationFrame(update);
        }}

        // التحكم
        c.ontouchstart = (e) => {{
            let tx = e.touches[0].clientX - c.offsetLeft;
            if(e.touches.length > 1) {{ nitro = true; setTimeout(()=>nitro=false, 2000); }} // لمستين للنيترو
            else {{ px = (tx < 160) ? Math.max(10, px-60) : Math.min(260, px+60); }}
        }};
        
        update();
    </script>
    """
    components.html(game_js, height=600)
    if st.button("🏁 إنهاء السباق"):
        st.session_state.page = 'home'
        st.rerun()

# --- الغرفة 4: المتصدرين ---
elif st.session_state.page == 'leaderboard':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header("🏆 قائمة أساطير الطريق")
    st.table({"المركز": [1,2,3], "اللاعب": ["أنت", "VIP_Racer", "King_Speed"], "النقاط": [st.session_state.score, 15000, 12000]})
    if st.button("🔙 عودة"): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
        
