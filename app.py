import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة وتثبيت الذاكرة
st.set_page_config(page_title="Royal Racer Elite", layout="wide", initial_sidebar_state="collapsed")

if 'score' not in st.session_state: st.session_state.score = 0
if 'money' not in st.session_state: st.session_state.money = 2500
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'car_type' not in st.session_state: st.session_state.car_type = 'sport'

# تصميم الواجهة الاحترافي (Dark Luxury)
st.markdown("""
    <style>
    .stApp { background: #050505; color: #D4AF37; font-family: 'Segoe UI', sans-serif; }
    .glass-card {
        background: rgba(255, 215, 0, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 30px;
        padding: 50px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .stButton>button {
        background: linear-gradient(145deg, #D4AF37, #AA8939);
        color: #000 !important;
        border: none;
        border-radius: 50px;
        padding: 20px;
        font-weight: 900;
        letter-spacing: 2px;
        transition: 0.5s;
        box-shadow: 0 10px 20px rgba(212, 175, 55, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 30px rgba(212, 175, 55, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 60px; text-shadow: 0 0 20px #D4AF37;'>ROYAL RACER</h1>", unsafe_allow_html=True)
    st.markdown(f"### 💳 ROYAL BANK: ${st.session_state.money} | 🏆 HIGH SCORE: {st.session_state.score}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏁 START RACE"): st.session_state.page = 'play'; st.rerun()
    with col2:
        if st.button("🛠️ LUXURY GARAGE"): st.session_state.page = 'garage'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الكراج الفخم ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🛠️ SELECT YOUR SUPERCAR")
    choice = st.radio("Choose Model:", ["Sport V8", "Hyper V12", "Royal Gold Custom"])
    st.session_state.car_type = choice
    if st.button("✅ APPLY & RETURN"): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- محرك اللعبة الاحترافي (Canvas API) ---
elif st.session_state.page == 'play':
    game_js = f"""
    <div style="text-align:center;">
        <div style="color:#D4AF37; font-size:25px; margin-bottom:15px; font-weight:bold;">
            SCORE: <span id="s">0</span> | NITRO: <span id="n" style="color:#fff;">READY [DOUBLE TAP]</span>
        </div>
        <canvas id="game" width="360" height="600" style="border:2px solid #D4AF37; border-radius:30px; box-shadow: 0 0 50px #D4AF3733; background:#000;"></canvas>
    </div>
    
    <script>
        const c=document.getElementById("game"), ctx=c.getContext("2d");
        let px=155, py=480, score=0, enemies=[], speed=8, nitro=false;

        function drawPlayer(x, y) {{
            // رسم سيارة احترافية بظلال وإضاءة
            ctx.shadowBlur = 15; ctx.shadowColor = nitro ? "#00ffff" : "#D4AF37";
            ctx.fillStyle = nitro ? "#fff" : "#D4AF37";
            ctx.beginPath(); ctx.roundRect(x, y, 50, 95, 12); ctx.fill(); // الهيكل
            ctx.fillStyle = "#111"; ctx.fillRect(x+5, y+20, 40, 30); // الزجاج
            ctx.fillStyle = "#f00"; ctx.fillRect(x+5, y+85, 10, 5); ctx.fillRect(x+35, y+85, 10, 5); // اسطبات
        }}

        function drawEnemy(x, y) {{
            ctx.shadowBlur = 0;
            ctx.fillStyle = "#444";
            ctx.beginPath(); ctx.roundRect(x, y, 50, 90, 8); ctx.fill();
            ctx.fillStyle = "#fff"; ctx.fillRect(x+10, y+5, 30, 15); // زجاج العدو
        }}

        function update() {{
            ctx.clearRect(0,0,360,600);
            // رسم الأسفلت
            ctx.fillStyle="#080808"; ctx.fillRect(0,0,360,600);
            ctx.strokeStyle="#333"; ctx.lineWidth=2; ctx.setLineDash([40, 20]);
            ctx.beginPath(); ctx.moveTo(180,0); ctx.lineTo(180,600); ctx.stroke();

            drawPlayer(px, py);

            if(Math.random()<0.03) enemies.push({{x: Math.random()*300, y:-100}});
            
            enemies.forEach((en, i)=>{{
                en.y += nitro ? 20 : speed;
                drawEnemy(en.x, en.y);
                
                // تصادم دقيق
                if(en.y+80 > py && en.y < py+90 && en.x+45 > px && en.x < px+45) {{
                    alert("WASTED! Score: " + score); location.reload();
                }}
                if(en.y > 600) {{ enemies.splice(i,1); score+=10; }}
            }});
            document.getElementById("s").innerText = score;
            requestAnimationFrame(update);
        }}

        c.ontouchstart = (e) => {{
            let t = e.touches[0].clientX - c.offsetLeft;
            if(e.touches.length > 1) {{ 
                nitro=true; speed=15; 
                setTimeout(()=>{{nitro=false; speed=8;}}, 2000); 
            }}
            px = (t < 180) ? Math.max(10, px-70) : Math.min(300, px+70);
        }};
        update();
    </script>
    """
    components.html(game_js, height=700)
    if st.button("🏁 QUIT RACE"): st.session_state.page = 'home'; st.rerun()
    
