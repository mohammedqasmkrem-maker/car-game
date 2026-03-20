import streamlit as st
import streamlit.components.v1 as components

# 1. إعدادات النظام والذاكرة
st.set_page_config(page_title="Space Racer Pro", layout="wide", initial_sidebar_state="collapsed")

if 'money' not in st.session_state: st.session_state.money = 25577
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'control' not in st.session_state: st.session_state.control = 'touch' # touch, wheel, tilt
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'active_car_color' not in st.session_state: st.session_state.active_car_color = '#00f2ff'

# نصوص اللغتين
TEXTS = {
    'ar': {'start': 'ابدأ السباق', 'shop': 'المتجر', 'settings': 'الإعدادات', 'garage': 'الكراج', 'lang_btn': 'English', 'control': 'نوع التحكم', 'back': 'رجوع'},
    'en': {'start': 'START RACE', 'shop': 'SHOP', 'settings': 'SETTINGS', 'garage': 'GARAGE', 'lang_btn': 'العربية', 'control': 'Control Type', 'back': 'BACK'}
}
T = TEXTS[st.session_state.lang]

# 2. تصميم الواجهة (خلفية فضاء نيون)
st.markdown(f"""
<style>
    .stApp {{
        background: url("https://wallpaperaccess.com/full/416568.jpg");
        background-size: cover;
        color: white;
    }}
    .glass-morphism {{
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border: 2px solid {st.session_state.active_car_color};
        border-radius: 20px; padding: 25px; text-align: center;
    }}
    .stButton>button {{
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid {st.session_state.active_car_color} !important;
        border-radius: 10px; font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# --- [ الصفحة الرئيسية ] ---
if st.session_state.page == 'home':
    st.markdown('<div class="glass-morphism">', unsafe_allow_html=True)
    st.title("🌌 SPACE NEON RACER")
    st.write(f"💰 ${st.session_state.money} | ⚙️ {st.session_state.control.upper()}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(T['start']): st.session_state.page = 'play'; st.rerun()
        if st.button(T['garage']): st.session_state.page = 'garage'; st.rerun()
    with col2:
        if st.button(T['shop']): st.session_state.page = 'shop'; st.rerun()
        if st.button(T['settings']): st.session_state.page = 'settings'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ صفحة الإعدادات (لغة + تحكم) ] ---
elif st.session_state.page == 'settings':
    st.markdown('<div class="glass-morphism">', unsafe_allow_html=True)
    st.header(T['settings'])
    
    # تغيير اللغة
    if st.button(T['lang_btn']):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
    
    # اختيار التحكم
    st.write(f"### {T['control']}")
    c1, c2, c3 = st.columns(3)
    if c1.button("📱 Touch"): st.session_state.control = 'touch'; st.rerun()
    if c2.button("🎡 Wheel"): st.session_state.control = 'wheel'; st.rerun()
    if c3.button("📳 Tilt"): st.session_state.control = 'tilt'; st.rerun()
    
    if st.button(T['back']): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ المتجر ] ---
elif st.session_state.page == 'shop':
    st.markdown('<div class="glass-morphism">', unsafe_allow_html=True)
    st.header(T['shop'])
    st.write("🚚 سيارات جديدة قادمة قريباً في تحديث المجرة!")
    if st.button(T['back']): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الكراج ] ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="glass-morphism">', unsafe_allow_html=True)
    st.header(T['garage'])
    st.session_state.active_car_color = st.color_picker("Change Neon Color", st.session_state.active_car_color)
    if st.button(T['back']): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ محرك اللعب المتقدم ] ---
elif st.session_state.page == 'play':
    game_js = f"""
    <div style="display:flex; justify-content:space-between; color:white; font-family:sans-serif; padding:10px;">
        <span>CASH: ${st.session_state.money}</span>
        <span id="score">SCORE: 0</span>
    </div>
    <canvas id="game" width="340" height="500" style="border:3px solid {st.session_state.active_car_color}; border-radius:20px; background: url('https://i.imgur.com/8K5MhVn.png');"></canvas>
    
    <script>
        const canvas = document.getElementById("game"), ctx = canvas.getContext("2d");
        let px=145, py=400, score=0, items=[], active=true;
        const controlType = "{st.session_state.control}";

        function draw() {{
            if(!active) return;
            ctx.clearRect(0,0,340,500);

            // اللاعب
            ctx.shadowBlur=20; ctx.shadowColor="{st.session_state.active_car_color}";
            ctx.fillStyle="{st.session_state.active_car_color}";
            ctx.beginPath(); ctx.roundRect(px, py, 45, 85, 12); ctx.fill();

            // الأعداء (كأنها نيازك)
            if(Math.random()<0.02) items.push({{x: Math.random()*280+10, y: -100}});

            items.forEach((it, i)=>{{
                it.y += 8;
                ctx.shadowBlur=0; ctx.fillStyle="#ff4400";
                ctx.beginPath(); ctx.arc(it.x+22, it.y+40, 20, 0, 7); ctx.fill();

                if(it.y+60>py && it.y<py+70 && it.x+40>px && it.x<px+40) {{
                    active=false; alert("Game Over!"); location.reload();
                }}
                if(it.y>550) {{ items.splice(i,1); score+=10; }}
            }});
            document.getElementById("score").innerText = "SCORE: " + score;
            requestAnimationFrame(draw);
        }}

        // نظام التحكم حسب الإعدادات
        if(controlType === 'touch' || controlType === 'wheel') {{
            canvas.addEventListener("touchmove", (e) => {{
                let rect = canvas.getBoundingClientRect();
                px = Math.max(10, Math.min(285, e.touches[0].clientX - rect.left - 22));
                e.preventDefault();
            }}, {{passive:false}});
        }} else if(controlType === 'tilt') {{
            window.addEventListener('deviceorientation', (e) => {{
                px += e.gamma * 0.5; // تحريك حسب ميلان الجهاز
                px = Math.max(10, Math.min(285, px));
            }});
        }}

        draw();
    </script>
    """
    components.html(game_js, height=600)
    if st.button(T['back']): st.session_state.page = 'home'; st.rerun()
    
