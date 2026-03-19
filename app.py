import streamlit as st
import streamlit.components.v1 as components

# 1. إعدادات الصفحة والذاكرة
st.set_page_config(page_title="Royal Racer Ultimate", layout="wide")

if 'score' not in st.session_state: st.session_state.score = 0
if 'money' not in st.session_state: st.session_state.money = 0
if 'page' not in st.session_state: st.session_state.page = 'home'

# 2. تصميم الواجهة (الخلفية والأزرار)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1200");
        background-size: cover;
    }
    .royal-panel {
        background: rgba(255, 215, 0, 0.1);
        backdrop-filter: blur(15px);
        border: 2px solid #D4AF37;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 50px rgba(212, 175, 55, 0.3);
    }
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37, #F9EDAD);
        color: black !important;
        font-weight: bold;
        font-size: 24px;
        border-radius: 15px;
        height: 60px;
        width: 100%;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الغرفة 1: القائمة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="royal-panel">', unsafe_allow_html=True)
    st.markdown("<h1 style='color:#D4AF37; font-size:50px;'>🔱 ROYAL RACER PRO 🔱</h1>", unsafe_allow_html=True)
    st.write(f"### 🏆 سكورك العالي: {st.session_state.score} | 💰 محفظتك: {st.session_state.money}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏁 انطلاق للسباق"):
            st.session_state.page = 'play'
            st.rerun()
    with col2:
        if st.button("🛠️ كراج التعديلات"):
            st.session_state.page = 'garage'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 2: الكراج ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="royal-panel">', unsafe_allow_html=True)
    st.header("🛠️ كراج النخبة")
    st.write("هنا يمكنك تطوير سيارتك (قريباً)")
    if st.button("🔙 العودة للقائمة"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 3: ميدان السباق (هنا الشغل الثقيل) ---
elif st.session_state.page == 'play':
    game_html = """
    <div style="display:flex; justify-content:space-around; color:#D4AF37; font-family:Arial; font-weight:bold; font-size:25px; margin-bottom:10px;">
        <span>🏁 SCORE: <span id="sc">0</span></span>
        <span id="nitro-ui" style="color:white;">⚡ NITRO: READY</span>
    </div>
    <canvas id="gameCanvas" width="350" height="550" style="border:5px solid #D4AF37; border-radius:20px; background:#111; box-shadow: 0 0 30px #D4AF37;"></canvas>
    
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        let px = 150, py = 430, score = 0, enemies = [], speed = 6, nitro = false;

        function drawCar(x, y, color, isPlayer) {
            // جسم السيارة
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.roundRect(x, y, 50, 90, 12);
            ctx.fill();
            
            // الزجاج
            ctx.fillStyle = "rgba(0,0,0,0.7)";
            ctx.fillRect(x+5, y+20, 40, 25);
            
            // الأنوار
            ctx.fillStyle = isPlayer ? "#0ff" : "#f00";
            ctx.fillRect(x+5, y, 10, 5); ctx.fillRect(x+35, y, 10, 5);
            
            if(isPlayer && nitro) {
                ctx.fillStyle = "orange";
                ctx.fillRect(x+10, y+90, 10, 30); ctx.fillRect(x+30, y+90, 10, 30);
            }
        }

        function update() {
            ctx.fillStyle = "#222"; ctx.fillRect(0,0,350,550);
            // خطوط الطريق
            ctx.strokeStyle = "#444"; ctx.setLineDash([30, 30]); ctx.lineWidth = 5;
            ctx.beginPath(); ctx.moveTo(175, 0); ctx.lineTo(175, 550); ctx.stroke();

            drawCar(px, py, "#D4AF37", true); // سيارتك

            if(Math.random() < 0.02) {
                enemies.push({x: Math.random()*290, y: -100, c: "#fff"});
            }

            enemies.forEach((en, i) => {
                en.y += nitro ? speed * 2.5 : speed;
                drawCar(en.x, en.y, en.c, false);

                // تصادم
                if(en.y+80 > py && en.y < py+80 && en.x+45 > px && en.x < px+45) {
                    alert("Game Over! Score: " + score);
                    location.reload();
                }
                if(en.y > 550) { enemies.splice(i, 1); score += 10; }
            });

            document.getElementById("sc").innerText = score;
            requestAnimationFrame(update);
        }

        // تحكم لمس ناعم جداً
        canvas.addEventListener("touchstart", (e) => {
            let t = e.touches[0].clientX - canvas.offsetLeft;
            if(e.touches.length > 1) { 
                nitro = true; speed = 12; 
                document.getElementById("nitro-ui").style.color = "orange";
                setTimeout(()=>{ nitro=false; speed=6; document.getElementById("nitro-ui").style.color="white"; }, 2000);
            }
            px = (t < 175) ? Math.max(10, px-70) : Math.min(290, px+70);
        });

        update();
    </script>
    """
    components.html(game_html, height=650)
    if st.button("❌ إنهاء السباق"):
        st.session_state.page = 'home'
        st.rerun()
    
