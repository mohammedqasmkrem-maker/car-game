import streamlit as st
import streamlit.components.v1 as components

# 1. إعدادات الصفحة والذاكرة
st.set_page_config(page_title="Royal Neon Pro", layout="wide", initial_sidebar_state="collapsed")

if 'score' not in st.session_state: st.session_state.score = 0
if 'money' not in st.session_state: st.session_state.money = 25577
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'owned_cars' not in st.session_state: st.session_state.owned_cars = ['Neon Basic']
if 'current_car' not in st.session_state: st.session_state.current_car = 'Neon Basic'

# قائمة السيارات المميزة
CARS = {
    'Neon Basic': {'price': 0, 'color': '#00fbff', 'speed': 8},
    'BMW M4 Style': {'price': 5000, 'color': '#ff0055', 'speed': 10},
    'Porsche Elite': {'price': 15000, 'color': '#00ff44', 'speed': 12},
    'Royal Gold': {'price': 50000, 'color': '#ffd700', 'speed': 15}
}

# 2. تصميم الـ UI الملكي
st.markdown(f"""
    <style>
    .stApp {{ background: #050505; color: white; font-family: 'Orbitron', sans-serif; }}
    .neon-card {{
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid {CARS[st.session_state.current_car]['color']};
        box-shadow: 0 0 25px {CARS[st.session_state.current_car]['color']}44;
        border-radius: 20px; padding: 25px; text-align: center;
    }}
    .stButton>button {{
        background: transparent; color: {CARS[st.session_state.current_car]['color']} !important;
        border: 2px solid {CARS[st.session_state.current_car]['color']} !important;
        border-radius: 10px; width: 100%; transition: 0.3s;
    }}
    .stButton>button:hover {{ background: {CARS[st.session_state.current_car]['color']}; color: black !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.title("⚡ NEON RACER ELITE ⚡")
    st.subheader(f"💰 BALANCE: ${st.session_state.money} | 🚗 CAR: {st.session_state.current_car}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ START RACE"): st.session_state.page = 'play'; st.rerun()
    with col2:
        if st.button("🛒 SHOWROOM"): st.session_state.page = 'store'; st.rerun()
    with col3:
        if st.button("🎨 GARAGE"): st.session_state.page = 'garage'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- متجر السيارات (شراء بالفلوس) ---
elif st.session_state.page == 'store':
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.header("🏢 LUXURY SHOWROOM")
    cols = st.columns(len(CARS))
    for i, (name, specs) in enumerate(CARS.items()):
        with cols[i]:
            st.markdown(f"<div style='color:{specs['color']}'>{name}</div>", unsafe_allow_html=True)
            if name in st.session_state.owned_cars:
                if st.button(f"SELECT", key=name): 
                    st.session_state.current_car = name; st.rerun()
            else:
                if st.button(f"BUY ${specs['price']}", key=name):
                    if st.session_state.money >= specs['price']:
                        st.session_state.money -= specs['price']
                        st.session_state.owned_cars.append(name)
                        st.success("PURCHASED!")
                        st.rerun()
                    else: st.error("LACK OF CASH!")
    if st.button("🔙 BACK"): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- اللعبة (صوت + عملات حقيقية + سيارات مميزة) ---
elif st.session_state.page == 'play':
    car_cfg = CARS[st.session_state.current_car]
    game_js = f"""
    <div id="ui" style="display:flex; justify-content:space-between; color:{car_cfg['color']}; font-weight:bold; margin-bottom:10px;">
        <span>CASH: $<span id="m">{st.session_state.money}</span></span>
        <span>POINTS: <span id="s">0</span></span>
    </div>
    <canvas id="race" width="340" height="520" style="border:2px solid {car_cfg['color']}; border-radius:20px; background:#000;"></canvas>
    
    <audio id="engine" loop src="https://www.soundjay.com/transportation/sounds/car-accelerating-01.mp3"></audio>
    <audio id="coinSound" src="https://www.soundjay.com/misc/sounds/coin-spade-7.mp3"></audio>

    <script>
        const c=document.getElementById("race"), ctx=c.getContext("2d");
        const eng=document.getElementById("engine"), cSnd=document.getElementById("coinSound");
        let px=145, py=420, score=0, cash=0, items=[], speed={car_cfg['speed']}, active=false;

        function draw() {{
            if(!active) {{ // تفعيل الصوت مع أول لمسة
                ctx.fillStyle="white"; ctx.fillText("TOUCH TO START ENGINE", 100, 250);
                return;
            }}
            ctx.clearRect(0,0,340,520);
            
            // رسم السيارة (Glow)
            ctx.shadowBlur=20; ctx.shadowColor="{car_cfg['color']}";
            ctx.fillStyle="{car_cfg['color']}";
            ctx.beginPath(); ctx.roundRect(px, py, 45, 80, 10); ctx.fill();

            // توليد أعداء وعملات
            if(Math.random()<0.02) items.push({{type:'car', x:Math.random()*250+30, y:-100}});
            if(Math.random()<0.01) items.push({{type:'coin', x:Math.random()*250+30, y:-100}});

            items.forEach((it, i)=>{{
                it.y += speed;
                if(it.type=='car') {{
                    ctx.shadowBlur=0; ctx.fillStyle="#444";
                    ctx.beginPath(); ctx.roundRect(it.x, it.y, 45, 80, 5); ctx.fill();
                    if(it.y+70 > py && it.y < py+70 && it.x+40 > px && it.x < px+40) {{
                        score=0; items=[]; // خسارة وتصفير
                    }}
                }} else {{
                    ctx.shadowBlur=15; ctx.shadowColor="yellow"; ctx.fillStyle="gold";
                    ctx.beginPath(); ctx.arc(it.x+20, it.y+20, 15, 0, Math.PI*2); ctx.fill();
                    if(it.y+30 > py && it.y < py+80 && it.x+30 > px && it.x < px+40) {{
                        items.splice(i,1); cash += 100; cSnd.play(); // جمع فلوس
                    }}
                }}
                if(it.y > 550) {{ items.splice(i,1); if(it.type=='car') score+=10; }}
            }});
            document.getElementById("s").innerText = score;
            document.getElementById("m").innerText = {st.session_state.money} + cash;
            requestAnimationFrame(draw);
        }}

        c.ontouchstart = () => {{ active=true; eng.play(); draw(); }};
        c.ontouchmove = (e) => {{
            let tx = e.touches[0].clientX - c.getBoundingClientRect().left;
            px = Math.max(30, Math.min(265, tx - 22));
            e.preventDefault();
        }};
    </script>
    """
    components.html(game_js, height=650)
    if st.button("🔙 STOP & SAVE"): st.session_state.page = 'home'; st.rerun()
