import streamlit as st
import streamlit.components.v1 as components
import random

# 1. الإعدادات الأساسية لمنع الـ Syntax Error
st.set_page_config(page_title="BMW Royal Empire", layout="wide", initial_sidebar_state="collapsed")

# 2. تهيئة نظام البيانات (المحفظة، الكراج، الإنجازات)
if 'money' not in st.session_state: st.session_state.money = 25577 # القيمة من صورتك
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = 'main_menu'
if 'car_color' not in st.session_state: st.session_state.car_color = '#3498db'
if 'unlocked_cars' not in st.session_state: st.session_state.unlocked_cars = ['Basic']
if 'selected_car' not in st.session_state: st.session_state.selected_car = 'Basic'

# قاعدة بيانات الغرف والسيارات
ROOMS = {
    'City': {'bg': '#111', 'speed': 7, 'hazard': '🚧'},
    'Desert': {'bg': '#2c1e14', 'speed': 10, 'hazard': '🌵'},
    'Cyber': {'bg': '#000511', 'speed': 14, 'hazard': '⚡'}
}

# 3. محرك التصميم (CSS Modern UI)
st.markdown(f"""
<style>
    .stApp {{ background: #000; color: white; font-family: 'Courier New', Courier, monospace; }}
    .royal-card {{
        background: linear-gradient(145deg, #111, #000);
        border: 2px solid {st.session_state.car_color};
        box-shadow: 0 0 20px {st.session_state.car_color}55;
        border-radius: 20px; padding: 25px; text-align: center; margin-bottom: 20px;
    }}
    .stButton>button {{
        background: transparent !important; color: {st.session_state.car_color} !important;
        border: 2px solid {st.session_state.car_color} !important;
        border-radius: 12px !important; font-weight: bold; height: 50px; transition: 0.3s;
    }}
    .stButton>button:hover {{ background: {st.session_state.car_color} !important; color: black !important; }}
</style>
""", unsafe_allow_html=True)

# --- [ الغرفة 1: القائمة الرئيسية ] ---
if st.session_state.page == 'main_menu':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.title("🔱 BMW ROYAL EMPIRE 🔱")
    st.subheader(f"💰 BANK: ${st.session_state.money:,} | 🏆 BEST: {st.session_state.score}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏁 RACE (الغرف)"): st.session_state.page = 'room_select'; st.rerun()
    with col2:
        if st.button("⚙️ GARAGE (الكراج)"): st.session_state.page = 'garage'; st.rerun()
    with col3:
        if st.button("🛒 SHOP (المتجر)"): st.session_state.page = 'shop'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الغرفة 2: اختيار ساحة المعركة (3 غرف) ] ---
elif st.session_state.page == 'room_select':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header("🗺️ SELECT YOUR ARENA")
    cols = st.columns(3)
    for i, (name, info) in enumerate(ROOMS.items()):
        with cols[i]:
            st.markdown(f"### {name}")
            st.write(f"Speed: {info['speed']}x")
            if st.button(f"ENTER {name}", key=name):
                st.session_state.current_room = name
                st.session_state.page = 'play'
                st.rerun()
    if st.button("🔙 BACK"): st.session_state.page = 'main_menu'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الغرفة 3: الكراج الاحترافي (تعديل سيارات) ] ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header("⚙️ CUSTOM GARAGE")
    # عرض السيارة الدوارة
    visual = f"""
    <div style="height:150px; display:flex; justify-content:center; align-items:center;">
        <div style="width:120px; height:60px; background:{st.session_state.car_color}; border-radius:10px; 
        box-shadow:0 0 30px {st.session_state.car_color}; animation: spin 4s linear infinite;"></div>
    </div>
    <style> @keyframes spin {{ from{{transform:rotateY(0deg);}} to{{transform:rotateY(360deg);}} }} </style>
    """
    components.html(visual, height=160)
    st.session_state.car_color = st.color_picker("REPAINT CAR", st.session_state.car_color)
    st.write("---")
    if st.button("✅ SAVE & EXIT"): st.session_state.page = 'main_menu'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الغرفة 4: ساحة اللعب المتقدمة ] ---
elif st.session_state.page == 'play':
    room = ROOMS[st.session_state.current_room]
    game_js = f"""
    <div style="display:flex; justify-content:space-between; color:{st.session_state.car_color}; font-weight:bold; font-size:20px; padding:10px;">
        <span>PTS: <span id="s">0</span></span>
        <span>ROOM: {st.session_state.current_room}</span>
        <span>CASH: $<span id="m">0</span></span>
    </div>
    <canvas id="race" width="340" height="500" style="border:3px solid {st.session_state.car_color}; border-radius:20px; background:{room['bg']}; display:block; margin:auto; touch-action:none;"></canvas>
    
    <script>
        const c=document.getElementById("race"), ctx=c.getContext("2d");
        let px=145, py=400, score=0, cash=0, items=[], offset=0, active=true;

        function draw() {{
            if(!active) return;
            ctx.clearRect(0,0,340,500);
            
            // رسم الطريق المتحرك
            ctx.strokeStyle="#333"; ctx.setLineDash([20, 20]); ctx.lineDashOffset = -offset;
            ctx.beginPath(); ctx.moveTo(170,0); ctx.lineTo(170,500); ctx.stroke();
            offset += {room['speed']};

            // سيارة اللاعب (BMW Style)
            ctx.shadowBlur=20; ctx.shadowColor="{st.session_state.car_color}"; ctx.fillStyle="{st.session_state.car_color}";
            ctx.beginPath(); ctx.roundRect(px, py, 45, 80, 10); ctx.fill();
            ctx.fillStyle="rgba(0,0,0,0.4)"; ctx.fillRect(px+5, py+15, 35, 20); // الزجاج

            if(Math.random()<0.02) items.push({{t:'e', x:Math.random()*260+20, y:-100}});
            if(Math.random()<0.01) items.push({{t:'c', x:Math.random()*260+20, y:-100}});

            items.forEach((it, i)=>{{
                it.y += {room['speed']};
                if(it.t=='e') {{
                    ctx.shadowBlur=0; ctx.fillStyle="#ff4444";
                    ctx.beginPath(); ctx.roundRect(it.x, it.y, 45, 80, 5); ctx.fill();
                    if(it.y+70>py && it.y<py+70 && it.x+40>px && it.x<px+40) {{
                        active=false; alert("💥 WASTED!"); location.reload();
                    }}
                }} else {{
                    ctx.shadowBlur=15; ctx.shadowColor="gold"; ctx.fillStyle="gold";
                    ctx.beginPath(); ctx.arc(it.x+15, it.y+15, 12, 0, 7); ctx.fill();
                    if(it.y+30>py && it.y<py+80 && it.x+30>px && it.x<px+40) {{
                        items.splice(i,1); cash+=100;
                    }}
                }}
                if(it.y>550) {{ items.splice(i,1); if(it.t=='e') score+=10; }}
            }});
            document.getElementById("s").innerText = score;
            document.getElementById("m").innerText = cash;
            requestAnimationFrame(draw);
        }}

        c.ontouchmove = (e) => {{
            let r = c.getBoundingClientRect();
            px = Math.max(20, Math.min(275, e.touches[0].clientX - r.left - 22));
            e.preventDefault();
        }};
        draw();
    </script>
    """
    components.html(game_js, height=620)
    if st.button("🛑 EXIT RACE"): st.session_state.page = 'main_menu'; st.rerun()
