import streamlit as st
import streamlit.components.v1 as components

# 1. إعدادات الصفحة
st.set_page_config(page_title="Royal Racer BMW", layout="wide", initial_sidebar_state="collapsed")

# 2. تهيئة الذاكرة
if 'score' not in st.session_state: st.session_state.score = 0
if 'money' not in st.session_state: st.session_state.money = 25577
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'car_color' not in st.session_state: st.session_state.car_color = "#3498db" # اللون الأزرق مثل الصورة
if 'lang' not in st.session_state: st.session_state.lang = 'ar'

# 3. نصوص اللغة
texts = {
    'ar': {'start': 'ابدأ السباق', 'garage': 'الكراج', 'settings': 'الإعدادات', 'bank': 'المحفظة', 'points': 'النقاط', 'back': 'رجوع'},
    'en': {'start': 'START RACE', 'garage': 'GARAGE', 'settings': 'SETTINGS', 'bank': 'BANK', 'points': 'POINTS', 'back': 'BACK'}
}
T = texts[st.session_state.lang]

# 4. التصميم الملكي مع خلفية BMW
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("https://images.unsplash.com/photo-1555215695-3004980ad54e?w=1200");
        background-size: cover;
        color: white;
    }}
    .main-card {{
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border: 2px solid #D4AF37;
        border-radius: 25px;
        padding: 30px;
        text-align: center;
    }}
    .stButton>button {{
        background: #D4AF37; color: black !important; font-weight: bold; border-radius: 15px; width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🔱 BMW ROYAL RACER 🔱")
    st.subheader(f"💰 {T['bank']}: ${st.session_state.money} | 🏆 {T['points']}: {st.session_state.score}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"🏁 {T['start']}"): st.session_state.page = 'play'; st.rerun()
    with col2:
        if st.button(f"🛠️ {T['garage']}"): st.session_state.page = 'garage'; st.rerun()
    
    # اختيار اللغة
    lang_toggle = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)
    st.session_state.lang = 'ar' if lang_toggle == "العربية" else 'en'
    st.markdown('</div>', unsafe_allow_html=True)

# --- الكراج (مثل تصميم الصورة) ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header(T['garage'])
    st.image("https://i.ibb.co/mS79vS6/blue-pickup.png", width=300) # صورة تقريبية للبيك اب الأزرق
    st.session_state.car_color = st.color_picker("اختر لون السيارة", st.session_state.car_color)
    
    st.write("📊 السرعة: 25 | المناورة: 15 | الفرملة: 15")
    if st.button(T['back']): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- اللعبة (تحكم ستيرن + بدون Alert مزعج) ---
elif st.session_state.page == 'play':
    game_js = f"""
    <div style="text-align:center; color:#D4AF37; font-weight:bold; font-size:22px; margin-bottom:10px;">
        {T['points']}: <span id="sc">0</span>
    </div>
    <div style="position:relative; width:340px; margin:auto;">
        <canvas id="race" width="340" height="500" style="border:3px solid #D4AF37; border-radius:20px; background:#111;"></canvas>
        
        <div id="steering" style="width:100px; height:100px; background:rgba(212,175,55,0.3); border:4px solid #D4AF37; border-radius:50%; margin:20px auto; position:relative; touch-action:none;">
            <div style="width:10px; height:40px; background:#D4AF37; position:absolute; left:45px; top:0;"></div>
        </div>
    </div>

    <script>
        const c=document.getElementById("race"), ctx=c.getContext("2d"), st=document.getElementById("steering");
        let px=145, py=400, score=0, enemies=[], angle=0, active=false;

        function update() {{
            ctx.fillStyle="#1a1a1a"; ctx.fillRect(0,0,340,500);
            ctx.setLineDash([20, 20]); ctx.strokeStyle="#444";
            ctx.beginPath(); ctx.moveTo(170,0); ctx.lineTo(170,500); ctx.stroke();

            // رسم سيارتك (BMW Style)
            ctx.fillStyle="{st.session_state.car_color}";
            ctx.beginPath(); ctx.roundRect(px, py, 50, 85, 10); ctx.fill();
            ctx.fillStyle="#000"; ctx.fillRect(px+5, py+15, 40, 25); // زجاج

            if(Math.random()<0.02) enemies.push({{x:Math.random()*280, y:-100}});
            
            enemies.forEach((en, i)=>{{
                en.y += 7;
                ctx.fillStyle="#fff"; ctx.beginPath(); ctx.roundRect(en.x, en.y, 50, 85, 5); ctx.fill();
                
                // تصادم (بدون alert، تصفير مباشر)
                if(en.y+70 > py && en.y < py+70 && en.x+40 > px && en.x < px+40) {{
                    score = 0; enemies = []; // تصفير النقاط بدل الرسالة المزعجة
                }}
                if(en.y > 500) {{ enemies.splice(i,1); score += 10; }}
            }});
            
            document.getElementById("sc").innerText = score;
            requestAnimationFrame(update);
        }}

        // تحكم الستيرن
        st.addEventListener("touchstart", () => active = true);
        st.addEventListener("touchmove", (e) => {{
            if(!active) return;
            let touch = e.touches[0];
            let rect = st.getBoundingClientRect();
            let centerX = rect.left + rect.width/2;
            angle = (touch.clientX - centerX) * 0.5;
            st.style.transform = `rotate(${{angle}}deg)`;
            px = Math.max(10, Math.min(280, px + angle/10));
        }});
        st.addEventListener("touchend", () => {{ active = false; st.style.transform = "rotate(0deg)"; }});

        update();
    </script>
    """
    components.html(game_js, height=750)
    if st.button(T['back']): st.session_state.page = 'home'; st.rerun()
    
