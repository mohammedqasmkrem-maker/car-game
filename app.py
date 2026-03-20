import streamlit as st
import streamlit.components.v1 as components

# 1. الإعدادات الأساسية
st.set_page_config(page_title="Space Racer Elite", layout="wide", initial_sidebar_state="collapsed")

# 2. نظام حفظ البيانات (الفلوس ثابتة 25,577)
if 'money' not in st.session_state: st.session_state.money = 25577
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'control' not in st.session_state: st.session_state.control = 'touch'
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'car_color' not in st.session_state: st.session_state.car_color = '#00fbff'

# النصوص
UI = {
    'ar': {'play': 'انطلاق', 'store': 'المتجر', 'settings': 'الإعدادات', 'back': 'رجوع', 'money': 'الرصيد'},
    'en': {'play': 'START', 'store': 'SHOP', 'settings': 'SETTINGS', 'back': 'BACK', 'money': 'BALANCE'}
}
txt = UI[st.session_state.lang]

# 3. تصميم واجهة الفضاء (CSS)
st.markdown(f"""
<style>
    .stApp {{
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        color: white;
    }}
    .space-card {{
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid {st.session_state.car_color};
        box-shadow: 0 0 20px {st.session_state.car_color}55;
        border-radius: 20px; padding: 30px; text-align: center;
    }}
    .stButton>button {{
        background: transparent !important; color: white !important;
        border: 1px solid {st.session_state.car_color} !important;
        border-radius: 10px; height: 50px; width: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# --- [ الصفحة الرئيسية ] ---
if st.session_state.page == 'home':
    st.markdown('<div class="space-card">', unsafe_allow_html=True)
    st.title("🚀 SPACE RACER PRO")
    st.write(f"### {txt['money']}: ${st.session_state.money}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(txt['play']): st.session_state.page = 'play'; st.rerun()
        if st.button(txt['store']): st.session_state.page = 'shop'; st.rerun()
    with col2:
        if st.button("🎨 GARAGE"): st.session_state.page = 'garage'; st.rerun()
        if st.button(txt['settings']): st.session_state.page = 'settings'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ المتجر - Shop ] ---
elif st.session_state.page == 'shop':
    st.markdown('<div class="space-card">', unsafe_allow_html=True)
    st.header(txt['store'])
    st.write("🌌 يتوفر قريباً: مركبة 'الصقر' و مركبة 'التنين'")
    if st.button(txt['back']): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الإعدادات - Settings ] ---
elif st.session_state.page == 'settings':
    st.markdown('<div class="space-card">', unsafe_allow_html=True)
    st.header(txt['settings'])
    if st.button("Change Language (عربي/EN)"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
    
    st.write("---")
    st.write("Control Method / طريقة التحكم")
    c1, c2 = st.columns(2)
    if c1.button("📱 Touch / لمس"): st.session_state.control = 'touch'; st.rerun()
    if c2.button("🎡 Wheel / ستيرن"): st.session_state.control = 'wheel'; st.rerun()
    
    if st.button(txt['back']): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ محرك اللعب المطور مع خلفية نجوم ] ---
elif st.session_state.page == 'play':
    game_js = f"""
    <div style="display:flex; justify-content:space-between; color:{st.session_state.car_color}; font-weight:bold; padding:10px;">
        <span>CASH: ${st.session_state.money}</span>
        <span id="sc">SCORE: 0</span>
    </div>
    <canvas id="race" width="340" height="500" style="border:2px solid {st.session_state.car_color}; border-radius:20px; background:#000; display:block; margin:auto;"></canvas>
    
    <script>
        const c=document.getElementById("race"), ctx=c.getContext("2d");
        let px=145, py=400, score=0, items=[], stars=[], active=true;

        // إنشاء نجوم الفضاء
        for(let i=0; i<50; i++) stars.push({{x:Math.random()*340, y:Math.random()*500, s:Math.random()*2}});

        function draw() {{
            if(!active) return;
            ctx.fillStyle="#000"; ctx.fillRect(0,0,340,500);
            
            // رسم وتحريك النجوم
            ctx.fillStyle="white";
            stars.forEach(s => {{
                ctx.beginPath(); ctx.arc(s.x, s.y, s.s, 0, 7); ctx.fill();
                s.y += 2; if(s.y > 500) s.y = 0;
            }});

            // سيارة اللاعب نيون
            ctx.shadowBlur=20; ctx.shadowColor="{st.session_state.car_color}"; ctx.fillStyle="{st.session_state.car_color}";
            ctx.beginPath(); ctx.roundRect(px, py, 45, 80, 10); ctx.fill();

            if(Math.random()<0.02) items.push({{t:'e', x:Math.random()*280+10, y:-100}});
            if(Math.random()<0.01) items.push({{t:'c', x:Math.random()*280+10, y:-100}});

            items.forEach((it, i)=>{{
                it.y += 7;
                if(it.t=='e') {{
                    ctx.shadowBlur=0; ctx.fillStyle="#ff4444";
                    ctx.beginPath(); ctx.roundRect(it.x, it.y, 45, 80, 5); ctx.fill();
                    if(it.y+70>py && it.y<py+70 && it.x+40>px && it.x<px+40) {{ active=false; alert("Game Over!"); location.reload(); }}
                }} else {{
                    ctx.shadowBlur=15; ctx.shadowColor="gold"; ctx.fillStyle="gold";
                    ctx.beginPath(); ctx.arc(it.x+15, it.y+15, 12, 0, 7); ctx.fill();
                    if(it.y+30>py && it.y<py+80 && it.x+30>px && it.x<px+40) {{ items.splice(i,1); }}
                }}
                if(it.y>550) {{ items.splice(i,1); if(it.t=='e') score+=10; }}
            }});
            document.getElementById("sc").innerText = "SCORE: " + score;
            requestAnimationFrame(draw);
        }}

        c.addEventListener("touchmove", (e) => {{
            let r = c.getBoundingClientRect();
            px = Math.max(10, Math.min(285, e.touches[0].clientX - r.left - 22));
            e.preventDefault();
        }}, {{passive:false}});
        
        draw();
    </script>
    """
    components.html(game_js, height=600)
    if st.button(txt['back']): st.session_state.page = 'home'; st.rerun()
        
