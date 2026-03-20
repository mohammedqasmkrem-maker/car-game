import streamlit as st
import streamlit.components.v1 as components

# 1. الإعدادات الفنية (الأساس)
st.set_page_config(page_title="Royal Racer PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. نظام الحالة (المحفظة، النقاط، السيارة)
if 'money' not in st.session_state: st.session_state.money = 25577 # القيمة الظاهرة في صورتك
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'active_car' not in st.session_state: st.session_state.active_car = 'BMW-Blue'

# قاعدة بيانات السيارات الاحترافية
CARS = {
    'BMW-Blue': {'color': '#0066ff', 'speed': 9, 'price': 0, 'desc': 'Standard Sport'},
    'Neon-Green': {'color': '#39ff14', 'speed': 12, 'price': 5000, 'desc': 'Hyper Fast'},
    'Gold-Edition': {'color': '#ffd700', 'speed': 15, 'price': 15000, 'desc': 'Royal Status'}
}

# 3. محرك التصميم (CSS Modern UI)
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;700&display=swap');
    
    .stApp {{
        background: radial-gradient(circle at top, #1a1a1a, #050505);
        color: white;
        font-family: 'Inter', sans-serif;
    }}
    
    /* كارت التصميم */
    .glass-panel {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 40px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        text-align: center;
    }}
    
    /* الأزرار */
    .stButton>button {{
        background: linear-gradient(135deg, {CARS[st.session_state.active_car]['color']}, #000);
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        height: 60px;
        font-weight: bold;
        transition: 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stButton>button:hover {{
        transform: scale(1.03);
        box-shadow: 0 0 30px {CARS[st.session_state.active_car]['color']}88;
    }}
</style>
""", unsafe_allow_html=True)

# --- [ الواجهة 1: الشاشة الرئيسية ] ---
if st.session_state.page == 'home':
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family:Syncopate; font-size:50px; margin-bottom:0;'>ROYAL RACER</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:gray;'>PREMIUM RACING EXPERIENCE</p>", unsafe_allow_html=True)
    
    # عرض العدادات
    c1, c2 = st.columns(2)
    c1.metric("BANK BALANCE", f"${st.session_state.money:,.0f}")
    c2.metric("HIGHEST SCORE", st.session_state.score)
    
    st.divider()
    
    col_play, col_garage = st.columns(2)
    with col_play:
        if st.button("🏁 START RACE", use_container_width=True):
            st.session_state.page = 'play'
            st.rerun()
    with col_garage:
        if st.button("🚗 SHOWROOM", use_container_width=True):
            st.session_state.page = 'garage'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الواجهة 2: الكراج الاحترافي ] ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.title("LUXURY SHOWROOM")
    
    cols = st.columns(3)
    for i, (name, data) in enumerate(CARS.items()):
        with cols[i]:
            st.markdown(f"""
                <div style="border: 1px solid {data['color']}; border-radius:15px; padding:15px;">
                    <div style="font-size:40px;">🏎️</div>
                    <h3 style="color:{data['color']}">{name}</h3>
                    <p>{data['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"SELECT {name}", key=name):
                st.session_state.active_car = name
                st.rerun()
                
    if st.button("🔙 RETURN HOME"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الواجهة 3: محرك السباق (Extreme Engine) ] ---
elif st.session_state.page == 'play':
    car_config = CARS[st.session_state.active_car]
    
    game_html = f"""
    <div style="display:flex; justify-content:space-around; font-weight:bold; color:{car_config['color']}; font-size:20px; margin-bottom:10px;">
        <span>SCORE: <span id="scr">0</span></span>
        <span>CASH: $<span id="mny">0</span></span>
    </div>
    <canvas id="raceCanvas" width="350" height="550" style="border:5px solid {car_config['color']}; border-radius:25px; background:#0a0a0a; display:block; margin:auto; touch-action:none;"></canvas>
    
    <script>
        const canvas = document.getElementById("raceCanvas");
        const ctx = canvas.getContext("2d");
        let px=150, py=450, score=0, cash=0, entities=[], speed={car_config['speed']}, frame=0;

        function drawPlayer() {{
            ctx.shadowBlur = 20; ctx.shadowColor = "{car_config['color']}";
            ctx.fillStyle = "{car_config['color']}";
            ctx.beginPath(); ctx.roundRect(px, py, 50, 90, 15); ctx.fill();
            ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(px+5, py+20, 40, 25);
        }}

        function update() {{
            ctx.clearRect(0,0,350,550);
            
            // رسم الشارع المضيء
            ctx.strokeStyle = "#222"; ctx.setLineDash([30, 20]);
            ctx.beginPath(); ctx.moveTo(175, 0); ctx.lineTo(175, 550); ctx.stroke();

            drawPlayer();

            if(frame % 60 == 0) {{
                let type = Math.random() > 0.3 ? 'enemy' : 'coin';
                entities.push({{t: type, x: Math.random()*280+10, y: -100}});
            }}

            entities.forEach((ent, i) => {{
                ent.y += speed;
                if(ent.t == 'enemy') {{
                    ctx.shadowBlur = 0; ctx.fillStyle = "#ff4444";
                    ctx.beginPath(); ctx.roundRect(ent.x, ent.y, 50, 85, 10); ctx.fill();
                    // تصادم
                    if(ent.y+80 > py && ent.y < py+80 && ent.x+45 > px && ent.x < px+45) {{
                        alert("WASTED! FINAL SCORE: " + score);
                        location.reload();
                    }}
                }} else {{
                    ctx.shadowBlur = 15; ctx.shadowColor = "gold"; ctx.fillStyle = "gold";
                    ctx.beginPath(); ctx.arc(ent.x+20, ent.y+20, 15, 0, Math.PI*2); ctx.fill();
                    // جمع عملة
                    if(ent.y+30 > py && ent.y < py+80 && ent.x+30 > px && ent.x < px+40) {{
                        entities.splice(i, 1); cash += 100;
                    }}
                }}

                if(ent.y > 600) {{
                    entities.splice(i, 1);
                    if(ent.t == 'enemy') score += 10;
                }}
            }});

            document.getElementById("scr").innerText = score;
            document.getElementById("mny").innerText = cash;
            frame++;
            requestAnimationFrame(update);
        }}

        canvas.addEventListener("touchmove", (e) => {{
            let rect = canvas.getBoundingClientRect();
            let touchX = e.touches[0].clientX - rect.left;
            px = Math.max(10, Math.min(290, touchX - 25));
            e.preventDefault();
        }}, {{passive: false}});

        update();
    </script>
    """
    components.html(game_html, height=650)
    
    if st.button("❌ TERMINATE MISSION"):
        st.session_state.page = 'home'
        st.rerun()
    
