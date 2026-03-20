import streamlit as st
import streamlit.components.v1 as components

# إعدادات أساسية لضمان عدم حدوث خطأ NameError
st.set_page_config(page_title="Royal Racer Pro", layout="wide")

if 'score' not in st.session_state: st.session_state.score = 0
if 'money' not in st.session_state: st.session_state.money = 1000
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'color' not in st.session_state: st.session_state.color = "#FFD700"

# تصميم الواجهة الملكية (CSS)
st.markdown(f"""
    <style>
    .stApp {{ background: #0e1117; color: white; }}
    .royal-box {{
        background: rgba(255, 215, 0, 0.1);
        border: 2px solid {st.session_state.color};
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 20px {st.session_state.color}55;
    }}
    .stButton>button {{
        background: {st.session_state.color};
        color: black !important;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="royal-box">', unsafe_allow_html=True)
    st.title("🔱 ROYAL RACER PRO 🔱")
    st.subheader(f"💰 المحفظة: {st.session_state.money} | 🏆 القمة: {st.session_state.score}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏁 دخول الميدان"):
            st.session_state.page = 'play'
            st.rerun()
    with col2:
        if st.button("🛠️ كراج النخبة"):
            st.session_state.page = 'garage'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الكراج (تغيير اللون) ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="royal-box">', unsafe_allow_html=True)
    st.header("🛠️ كراج التعديلات")
    st.session_state.color = st.color_picker("اختر لون سيارتك الملكي", st.session_state.color)
    st.write("تم تفعيل النيترو والمحرك الذهبي!")
    if st.button("🔙 حفظ والعودة"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- ميدان السباق (اللعبة المطورة) ---
elif st.session_state.page == 'play':
    # كود JS متطور للرسم الحقيقي
    game_js = f"""
    <div style="display:flex; justify-content:space-around; color:{st.session_state.color}; font-size:22px; font-weight:bold; margin-bottom:10px;">
        <span>🏆 SCORE: <span id="s">0</span></span>
        <span id="n_ui" style="color:white;">⚡ NITRO: READY</span>
    </div>
    <canvas id="rc" width="320" height="500" style="border:4px solid {st.session_state.color}; border-radius:15px; background:#1a1a1a;"></canvas>
    
    <script>
        const c=document.getElementById("rc"), ctx=c.getContext("2d");
        let px=135, py=400, score=0, enemies=[], nitro=false, speed=7;

        function drawCar(x, y, color, isPlayer) {{
            ctx.fillStyle = color;
            ctx.beginPath(); ctx.roundRect(x, y, 50, 85, 10); ctx.fill(); // جسم السيارة
            ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.fillRect(x+5, y+15, 40, 20); // زجاج
            if(isPlayer && nitro) {{ // لهب النيترو
                ctx.fillStyle="orange"; ctx.fillRect(x+10, y+85, 10, 15); ctx.fillRect(x+30, y+85, 10, 15);
            }}
        }}

        function update() {{
            ctx.fillStyle="#1a1a1a"; ctx.fillRect(0,0,320,500); // خلفية الطريق
            // رسم خطوط الطريق المتحركة
            ctx.strokeStyle="#333"; ctx.setLineDash([20, 20]);
            ctx.beginPath(); ctx.moveTo(160,0); ctx.lineTo(160,500); ctx.stroke();

            drawCar(px, py, "{st.session_state.color}", true);

            if(Math.random()<0.02) enemies.push({{x:Math.random()*260, y:-100, c:"#fff"}});
            
            enemies.forEach((en, i)=>{{
                en.y += nitro ? 15 : speed;
                drawCar(en.x, en.y, en.c, false);
                
                if(en.y+80 > py && en.y < py+80 && en.x+45 > px && en.x < px+45) {{
                    alert("نهاية السباق! السكور: " + score); location.reload();
                }}
                if(en.y > 500) {{ enemies.splice(i,1); score += 10; }}
            }});
            document.getElementById("s").innerText = score;
            requestAnimationFrame(update);
        }}

        c.ontouchstart = (e) => {{
            let tx = e.touches[0].clientX - c.offsetLeft;
            if(e.touches.length > 1) {{ // لمستين لتفعيل النيترو
                nitro = true; document.getElementById("n_ui").style.color="orange";
                setTimeout(()=>{{nitro=false; document.getElementById("n_ui").style.color="white";}}, 2000);
            }} else {{
                px = (tx < 160) ? Math.max(10, px-60) : Math.min(260, px+60);
            }}
        }};
        update();
    </script>
    """
    components.html(game_js, height=600)
    if st.button("❌ إنهاء والعودة للكراج"):
        st.session_state.page = 'home'
        st.rerun()
    
