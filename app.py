import streamlit as st
import streamlit.components.v1 as components

# 1. الإعدادات الأساسية
st.set_page_config(page_title="Royal Neon Max", layout="wide", initial_sidebar_state="collapsed")

# 2. نظام الذاكرة المستمر
if 'money' not in st.session_state: st.session_state.money = 25577
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'my_cars' not in st.session_state: st.session_state.my_cars = ['Neon']
if 'active_car' not in st.session_state: st.session_state.active_car = 'Neon'

# بيانات السيارات (السعر، اللون، السرعة)
CARS_DB = {
    'Neon': {'price': 0, 'color': '#00fbff', 'speed': 8, 'img': '🏎️'},
    'BMW-M': {'price': 5000, 'color': '#ff0055', 'speed': 11, 'img': '🚙'},
    'GT-Turbo': {'price': 15000, 'color': '#00ff44', 'speed': 14, 'img': '🏎️'},
    'Royal-G': {'price': 50000, 'color': '#ffd700', 'speed': 18, 'img': '👑'}
}

active_color = CARS_DB[st.session_state.active_car]['color']

# 3. واجهة المستخدم (التصميم النيوني الفخم)
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
    .stApp {{ background: #020202; color: white; font-family: 'Orbitron', sans-serif; }}
    .neon-border {{
        border: 2px solid {active_color};
        box-shadow: 0 0 20px {active_color}55, inset 0 0 10px {active_color}22;
        border-radius: 25px; padding: 25px; background: rgba(0,0,0,0.85); text-align: center;
    }}
    .btn-main button {{
        background: transparent !important; color: {active_color} !important;
        border: 2px solid {active_color} !important; border-radius: 15px !important;
        height: 55px; font-weight: 900; transition: 0.4s;
    }}
    .btn-main button:hover {{ background: {active_color} !important; color: black !important; box-shadow: 0 0 30px {active_color}; }}
</style>
""", unsafe_allow_html=True)

# --- [ الصفحة الرئيسية ] ---
if st.session_state.page == 'home':
    st.markdown(f'<div class="neon-border">', unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:{active_color}; text-shadow: 0 0 20px {active_color}; font-size:45px;'>ROYAL RACER MAX</h1>", unsafe_allow_html=True)
    st.write(f"### 💰 المحفظة: ${st.session_state.money} | 🏆 أفضل سكور: {st.session_state.score}")
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🏁 انطلاق", key="start", use_container_width=True): st.session_state.page='play'; st.rerun()
    with c2:
        if st.button("🏢 المعرض", key="shop", use_container_width=True): st.session_state.page='store'; st.rerun()
    with c3:
        if st.button("⚙️ الكراج", key="garage", use_container_width=True): st.session_state.page='garage'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ متجر السيارات ] ---
elif st.session_state.page == 'store':
    st.markdown('<div class="neon-border">', unsafe_allow_html=True)
    st.header("🏢 معرض السيارات الفاخرة")
    cols = st.columns(4)
    for i, (name, d) in enumerate(CARS_DB.items()):
        with cols[i]:
            st.markdown(f"<div style='font-size:40px;'>{d['img']}</div><b style='color:{d['color']}'>{name}</b>", unsafe_allow_html=True)
            if name in st.session_state.my_cars:
                if st.button(f"اختيار", key=name): st.session_state.active_car=name; st.rerun()
            else:
                if st.button(f"شراء ${d['price']}", key=name):
                    if st.session_state.money >= d['price']:
                        st.session_state.money -= d['price']
                        st.session_state.my_cars.append(name)
                        st.rerun()
                    else: st.error("الفلوس ما تكفي!")
    if st.button("🔙 رجوع"): st.session_state.page='home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الكراج الدوار ] ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="neon-border">', unsafe_allow_html=True)
    st.header("⚙️ تخصيص المركبة")
    garage_ui = f"""
    <div style="height:250px; display:flex; justify-content:center; align-items:center;">
        <div id="car" style="width:150px; height:80px; background:{active_color}; border-radius:15px; box-shadow:0 0 50px {active_color}; animation:spin 4s linear infinite;"></div>
    </div>
    <style> @keyframes spin {{ from {{transform:rotateY(0deg);}} to {{transform:rotateY(360deg);}} }} </style>
    """
    components.html(garage_ui, height=260)
    st.write(f"السيارة الحالية: **{st.session_state.active_car}**")
    if st.button("🔙 حفظ وخروج"): st.session_state.page='home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ اللعبة الاحترافية ] ---
elif st.session_state.page == 'play':
    car_v = CARS_DB[st.session_state.active_car]
    game_logic = f"""
    <div style="display:flex; justify-content:space-between; color:{active_color}; font-family:sans-serif; font-weight:900; padding:10px;">
        <span>CASH: $<span id="m">0</span></span>
        <span>SCORE: <span id="s">0</span></span>
    </div>
    <canvas id="g" width="340" height="500" style="border:3px solid {active_color}; border-radius:20px; background:#000; box-shadow:0 0 30px {active_color}44; touch-action:none;"></canvas>
    
    <audio id="cSound" src="https://www.soundjay.com/misc/sounds/coin-spade-7.mp3"></audio>

    <script>
        const canvas=document.getElementById("g"), ctx=canvas.getContext("2d");
        const snd=document.getElementById("cSound");
        let px=145, py=400, score=0, cash=0, items=[], speed={car_v['speed']}, active=true;

        function draw() {{
            if(!active) return;
            ctx.fillStyle="#050505"; ctx.fillRect(0,0,340,500);
            
            // رسم الشارع
            ctx.strokeStyle="#222"; ctx.setLineDash([20,20]); ctx.beginPath(); ctx.moveTo(170,0); ctx.lineTo(170,500); ctx.stroke();

            // سيارة اللاعب
            ctx.shadowBlur=20; ctx.shadowColor="{active_color}"; ctx.fillStyle="{active_color}";
            ctx.beginPath(); ctx.roundRect(px, py, 45, 80, 10); ctx.fill();

            if(Math.random()<0.02) items.push({{t:'e', x:Math.random()*260+20, y:-100}});
            if(Math.random()<0.01) items.push({{t:'c', x:Math.random()*260+20, y:-100}});

            items.forEach((it, i)=>{{
                it.y += speed;
                if(it.t=='e') {{
                    ctx.shadowBlur=0; ctx.fillStyle="#444";
                    ctx.beginPath(); ctx.roundRect(it.x, it.y, 45, 80, 5); ctx.fill();
                    if(it.y+70>py && it.y<py+70 && it.x+40>px && it.x<px+40) {{ active=false; alert("Game Over!"); location.reload(); }}
                }} else {{
                    ctx.shadowBlur=15; ctx.shadowColor="gold"; ctx.fillStyle="gold";
                    ctx.beginPath(); ctx.arc(it.x+20, it.y+20, 15, 0, 7); ctx.fill();
                    if(it.y+30>py && it.y<py+80 && it.x+30>px && it.x<px+40) {{ items.splice(i,1); cash+=100; snd.play(); }}
                }}
                if(it.y>550) {{ items.splice(i,1); if(it.t=='e') score+=10; }}
            }});

            document.getElementById("s").innerText = score;
            document.getElementById("m").innerText = cash;
            requestAnimationFrame(draw);
        }}

        canvas.addEventListener("touchmove", (e)=>{{
            let rect = canvas.getBoundingClientRect();
            px = Math.max(20, Math.min(275, e.touches[0].clientX - rect.left - 22));
            e.preventDefault();
        }}, {{passive:false}});

        draw();
    </script>
    """
    components.html(game_logic, height=650)
    if st.button("🔙 إنهاء"): st.session_state.page='home'; st.rerun()
