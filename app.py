import streamlit as st
import streamlit.components.v1 as components

# 1. إعدادات الصفحة
st.set_page_config(page_title="Royal Neon Racer", layout="wide", initial_sidebar_state="collapsed")

# 2. تهيئة الذاكرة (النقاط، الفلوس، السيارة المختارة)
if 'score' not in st.session_state: st.session_state.score = 0
if 'money' not in st.session_state: st.session_state.money = 25577
if 'car_color' not in st.session_state: st.session_state.car_color = "#00fbff" # نيون سايان
if 'page' not in st.session_state: st.session_state.page = 'home'

# 3. تصميم الـ UI (خلفية مظلمة + إضاءة نيون)
st.markdown(f"""
    <style>
    .stApp {{
        background: #050505;
        color: white;
        font-family: 'Orbitron', sans-serif;
    }}
    /* تأثير التوهج للوحات */
    .neon-card {{
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid {st.session_state.car_color};
        box-shadow: 0 0 20px {st.session_state.car_color}44;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
    }}
    .stButton>button {{
        background: transparent;
        color: {st.session_state.car_color} !important;
        border: 2px solid {st.session_state.car_color} !important;
        border-radius: 10px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.3s;
        box-shadow: inset 0 0 10px {st.session_state.car_color}44;
    }}
    .stButton>button:hover {{
        background: {st.session_state.car_color};
        color: black !important;
        box-shadow: 0 0 30px {st.session_state.car_color};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- الصفحة الرئيسية (القائمة مع النيون) ---
if st.session_state.page == 'home':
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:{st.session_state.car_color}; text-shadow: 0 0 15px {st.session_state.car_color};'>NEON RACER PRO</h1>", unsafe_allow_html=True)
    st.write(f"💰 BALANCE: ${st.session_state.money} | 🏆 BEST: {st.session_state.score}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ START"): st.session_state.page = 'play'; st.rerun()
    with col2:
        if st.button("🎨 CUSTOMIZE"): st.session_state.page = 'garage'; st.rerun()
    with col3:
        if st.button("🚗 CARS"): st.info("More cars coming soon!"); pass
    st.markdown('</div>', unsafe_allow_html=True)

# --- الكراج المميز (تدور ببطء + Glow) ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.header("🎨 NEON GARAGE")
    
    # مكون السيارة الدوارة (HTML/CSS Animation)
    garage_html = f"""
    <div style="height: 300px; display: flex; justify-content: center; align-items: center; perspective: 1000px;">
        <div id="car-preview" style="
            width: 200px; height: 100px; 
            background: {st.session_state.car_color}; 
            border-radius: 15px;
            box-shadow: 0 0 50px {st.session_state.car_color};
            animation: rotateCar 5s linear infinite;
            position: relative;
        ">
            <div style="position: absolute; top: 20px; left: 20px; width: 160px; height: 40px; background: rgba(0,0,0,0.5); border-radius: 5px;"></div>
            <div style="position: absolute; bottom: -5px; left: 20px; width: 30px; height: 10px; background: #333; border-radius: 2px;"></div>
            <div style="position: absolute; bottom: -5px; right: 20px; width: 30px; height: 10px; background: #333; border-radius: 2px;"></div>
        </div>
    </div>
    <style>
        @keyframes rotateCar {{
            0% {{ transform: rotateY(0deg) scale(1); }}
            50% {{ transform: rotateY(180deg) scale(1.1); }}
            100% {{ transform: rotateY(360deg) scale(1); }}
        }}
    </style>
    """
    st.components.v1.html(garage_html, height=320)
    
    st.session_state.car_color = st.color_picker("PICK NEON COLOR", st.session_state.car_color)
    
    if st.button("💾 SAVE & EXIT"): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- السباق المطور (خلفية Blur + طريق مضيء) ---
elif st.session_state.page == 'play':
    game_js = f"""
    <div style="display:flex; justify-content:space-between; color:{st.session_state.car_color}; font-weight:bold; margin-bottom:10px;">
        <span style="background:rgba(0,0,0,0.5); padding:5px 15px; border-radius:10px; border:1px solid">POINTS: <span id="s">0</span></span>
    </div>
    <canvas id="race" width="340" height="500" style="border:2px solid {st.session_state.car_color}; border-radius:20px; background:#000; box-shadow: 0 0 20px {st.session_state.car_color}66;"></canvas>
    
    <script>
        const c=document.getElementById("race"), ctx=c.getContext("2d");
        let px=145, py=400, score=0, enemies=[], speed=8, offset=0;

        function draw() {{
            // 1. خلفية متحركة مع Blur خفيف
            ctx.fillStyle="#050505"; ctx.fillRect(0,0,340,500);
            
            // 2. الطريق المضيء (Glow Borders)
            ctx.strokeStyle="{st.session_state.car_color}"; ctx.lineWidth=4;
            ctx.shadowBlur=15; ctx.shadowColor="{st.session_state.car_color}";
            ctx.beginPath(); ctx.moveTo(20,0); ctx.lineTo(20,500); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(320,0); ctx.lineTo(320,500); ctx.stroke();

            // 3. خطوط الطريق المتحركة
            ctx.setLineDash([30, 30]); ctx.lineDashOffset = -offset;
            ctx.strokeStyle="rgba(255,255,255,0.1)"; ctx.beginPath();
            ctx.moveTo(170,0); ctx.lineTo(170,500); ctx.stroke();
            offset += speed;

            // 4. رسم السيارة بتوهج (Glow)
            ctx.shadowBlur=20; ctx.fillStyle="{st.session_state.car_color}";
            ctx.beginPath(); ctx.roundRect(px, py, 50, 85, 10); ctx.fill();
            ctx.fillStyle="#000"; ctx.fillRect(px+5, py+15, 40, 25); // الزجاج

            // 5. الأعداء
            if(Math.random()<0.02) enemies.push({{x:Math.random()*250 + 30, y:-100}});
            enemies.forEach((en, i)=>{{
                en.y += speed;
                ctx.shadowBlur=0; ctx.fillStyle="#444";
                ctx.beginPath(); ctx.roundRect(en.x, en.y, 50, 85, 5); ctx.fill();
                
                // تصادم (تصفير فوري وبدون رسالة)
                if(en.y+70 > py && en.y < py+70 && en.x+40 > px && en.x < px+40) {{
                    score=0; speed=8; enemies=[];
                }}
                if(en.y > 500) {{ enemies.splice(i,1); score += 10; speed += 0.1; }}
            }});

            document.getElementById("s").innerText = score;
            requestAnimationFrame(draw);
        }}

        // التحكم باللمس (سحب ناعم)
        c.ontouchmove = (e) => {{
            let touchX = e.touches[0].clientX - c.getBoundingClientRect().left;
            px = Math.max(30, Math.min(260, touchX - 25));
            e.preventDefault();
        }};
        draw();
    </script>
    """
    components.html(game_js, height=600)
    if st.button("🔙 EXIT TO GARAGE"): st.session_state.page = 'home'; st.rerun()
    
