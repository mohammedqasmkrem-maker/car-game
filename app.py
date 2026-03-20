import streamlit as st
import streamlit.components.v1 as components

# 1. إعداد الصفحة - لمرة واحدة فقط لمنع الأخطاء
st.set_page_config(page_title="Royal Racer", layout="wide", initial_sidebar_state="collapsed")

# 2. نظام الذاكرة المستقر (بناء الهيكل)
if 'money' not in st.session_state: st.session_state.money = 25577
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'car_color' not in st.session_state: st.session_state.car_color = '#00fbff'

# 3. التصميم العام (Black & Neon)
st.markdown(f"""
<style>
    .stApp {{ background-color: #050505; color: white; font-family: sans-serif; }}
    .main-box {{
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid {st.session_state.car_color};
        border-radius: 20px; padding: 20px; text-align: center;
        box-shadow: 0 0 15px {st.session_state.car_color}44;
    }}
    .stButton>button {{
        background: transparent !important; color: {st.session_state.car_color} !important;
        border: 2px solid {st.session_state.car_color} !important; border-radius: 10px !important;
        width: 100%; font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# --- [ الصفحة الرئيسية ] ---
if st.session_state.page == 'home':
    st.markdown(f'<div class="main-box">', unsafe_allow_html=True)
    st.title("🏎️ NEON RACER PRO")
    st.write(f"💰 المحفظة: ${st.session_state.money} | 🏆 السكور: {st.session_state.score}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏁 ابدأ السباق"): 
            st.session_state.page = 'play'
            st.rerun()
    with col2:
        if st.button("⚙️ الكراج الملكي"): 
            st.session_state.page = 'garage'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الكراج الدوار ] ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.header("⚙️ كراج التعديل")
    
    # محاكاة السيارة الدوارة بصرياً
    garage_visual = f"""
    <div style="height:200px; display:flex; justify-content:center; align-items:center;">
        <div style="width:140px; height:70px; background:{st.session_state.car_color}; border-radius:10px; 
        box-shadow:0 0 40px {st.session_state.car_color}; animation: rotate 3s linear infinite;"></div>
    </div>
    <style> @keyframes rotate {{ from{{transform:rotateY(0deg);}} to{{transform:rotateY(360deg);}} }} </style>
    """
    components.html(garage_visual, height=220)
    
    st.session_state.car_color = st.color_picker("اختر لون سيارتك", st.session_state.car_color)
    
    if st.button("🔙 حفظ ورجوع"): 
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ محرك السباق ] ---
elif st.session_state.page == 'play':
    game_code = f"""
    <div style="display:flex; justify-content:space-between; color:{st.session_state.car_color}; font-weight:bold; margin-bottom:5px;">
        <span>POINTS: <span id="s">0</span></span>
        <span>CASH: $<span id="m">0</span></span>
    </div>
    <canvas id="rc" width="340" height="500" style="border:2px solid {st.session_state.car_color}; border-radius:15px; background:#000; touch-action:none;"></canvas>
    
    <script>
        const c=document.getElementById("rc"), ctx=c.getContext("2d");
        let px=145, py=400, score=0, cash=0, items=[], active=true;

        function update() {{
            if(!active) return;
            ctx.fillStyle="#000"; ctx.fillRect(0,0,340,500);
            
            // سيارة اللاعب
            ctx.shadowBlur=15; ctx.shadowColor="{st.session_state.car_color}"; ctx.fillStyle="{st.session_state.car_color}";
            ctx.beginPath(); ctx.roundRect(px, py, 45, 80, 8); ctx.fill();

            if(Math.random()<0.02) items.push({{t:'e', x:Math.random()*260+20, y:-100}});
            if(Math.random()<0.01) items.push({{t:'c', x:Math.random()*260+20, y:-100}});

            items.forEach((it, i)=>{{
                it.y += 7;
                if(it.t=='e') {{
                    ctx.shadowBlur=0; ctx.fillStyle="#555";
                    ctx.beginPath(); ctx.roundRect(it.x, it.y, 45, 80, 5); ctx.fill();
                    if(it.y+70>py && it.y<py+70 && it.x+40>px && it.x<px+40) {{ active=false; alert("Game Over!"); location.reload(); }}
                }} else {{
                    ctx.shadowBlur=10; ctx.shadowColor="gold"; ctx.fillStyle="gold";
                    ctx.beginPath(); ctx.arc(it.x+15, it.y+15, 12, 0, 7); ctx.fill();
                    if(it.y+30>py && it.y<py+80 && it.x+30>px && it.x<px+40) {{ items.splice(i,1); cash+=100; }}
                }}
                if(it.y>550) {{ items.splice(i,1); if(it.t=='e') score+=10; }}
            }});
            document.getElementById("s").innerText = score;
            document.getElementById("m").innerText = cash;
            requestAnimationFrame(update);
        }}

        c.ontouchmove = (e) => {{
            let r = c.getBoundingClientRect();
            px = Math.max(20, Math.min(275, e.touches[0].clientX - r.left - 22));
            e.preventDefault();
        }};
        update();
    </script>
    """
    components.html(game_code, height=600)
    if st.button("🔙 إنهاء السباق"): 
        st.session_state.page = 'home'
        st.rerun()
