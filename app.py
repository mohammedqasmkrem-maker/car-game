import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة وتصميم النيون الفخم
st.set_page_config(page_title="Traffic Racer Pro", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
    .stApp { background-color: #0a0a0a; color: white; font-family: 'Orbitron', sans-serif; }
    .stButton>button { width: 100%; border-radius: 10px; background: linear-gradient(45deg, #00f2fe, #4facfe); color: black; font-weight: bold; border: none; }
    .sidebar .sidebar-content { background-image: linear-gradient(#1a1a2e, #16213e); }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (نظام الغرف) ---
with st.sidebar:
    st.image("https://i.ibb.co/mS79vS6/blue-pickup.png", width=100)
    st.title("القائمة الرئيسية")
    choice = st.radio("انتقل إلى:", ["🏠 الشاشة الرئيسية", "🚗 الكراج (تعديل)", "🏁 سباق الآن", "🏆 المتصدرين"])
    st.info("النقاط الحالية: 1250 💰")

# --- الغرفة 1: الشاشة الرئيسية ---
if choice == "🏠 الشاشة الرئيسية":
    st.markdown("<h1 style='text-align:center;'>TRAFFIC RACER PRO</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=800&q=80")
    st.success("✅ التطبيق جاهز. اذهب للكراج لتجهيز سيارتك!")

# --- الغرفة 2: الكراج (التعديل) ---
elif choice == "🚗 الكراج (تعديل)":
    st.header("🛠️ كراج التعديلات")
    col1, col2 = st.columns(2)
    with col1:
        st.color_picker("اختر لون السيارة النيون", "#00f2fe")
        st.selectbox("نوع الجنوط", ["رياضي سبورت", "كلاسيك", "نيون مضيء"])
    with col2:
        st.slider("مستوى تطوير المحرك (Speed)", 0, 100, 50)
        st.button("حفظ التعديلات ✅")
    st.image("https://i.ibb.co/mS79vS6/blue-pickup.png", caption="سيارتك الحالية")

# --- الغرفة 3: سباق الآن (اللعبة الفعلية) ---
elif choice == "🏁 سباق الآن":
    st.markdown("<h3 style='text-align:center;'>ميدان التحدي</h3>", unsafe_allow_html=True)
    
    # كود اللعبة المطور (جافا سكريبت)
    game_js = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { margin: 0; background: #000; display: flex; flex-direction: column; align-items: center; }
            canvas { border: 3px solid #00f2fe; border-radius: 15px; box-shadow: 0 0 20px #00f2fe; }
            .hud { color: #00f2fe; font-family: 'Courier New'; font-size: 18px; margin: 10px; width: 320px; display: flex; justify-content: space-between; }
        </style>
    </head>
    <body>
        <div class="hud">
            <div>KM/H: <span id="sp">0</span></div>
            <div>❤️: <span id="li">3</span></div>
        </div>
        <canvas id="race" width="320" height="480"></canvas>
        <script>
            const canvas = document.getElementById("race");
            const ctx = canvas.getContext("2d");
            
            const carImg = new Image(); carImg.src = "https://raw.githubusercontent.com/Subrata-S/Car-Racing-Game-JavaScript/master/img/car.png";
            const enemyImg = new Image(); enemyImg.src = "https://raw.githubusercontent.com/Subrata-S/Car-Racing-Game-JavaScript/master/img/enemy.png";
            
            let x = 135, speed = 0, score = 0, lives = 3, enemies = [];
            
            function loop() {
                ctx.fillStyle = "#222"; ctx.fillRect(0,0,320,480);
                
                // رسم خطوط الطريق المتحركة
                ctx.strokeStyle = "white"; ctx.setLineDash([20, 20]); ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(160, 0); ctx.lineTo(160, 480); ctx.stroke();

                if(speed < 180) speed += 0.5; // زيادة السرعة تدريجياً
                
                ctx.drawImage(carImg, x, 380, 50, 80);
                
                if(Math.random() < 0.02) enemies.push({x: Math.random()*270, y: -100});
                
                enemies.forEach((en, i) => {
                    en.y += (speed/20) + 2;
                    ctx.drawImage(enemyImg, en.x, en.y, 50, 80);
                    
                    // تصادم
                    if(en.y > 330 && en.y < 430 && en.x > x-40 && en.x < x+40) {
                        lives--; enemies.splice(i, 1);
                        if(lives <= 0) { alert("GAME OVER! Score: " + score); location.reload(); }
                    }
                });
                
                score++;
                document.getElementById("sp").innerText = Math.floor(speed);
                document.getElementById("li").innerText = "❤️".repeat(lives);
                requestAnimationFrame(loop);
            }

            canvas.addEventListener("touchstart", (e) => {
                let t = e.touches[0].clientX - canvas.offsetLeft;
                x = (t < 160) ? Math.max(10, x-60) : Math.min(260, x+60);
            });
            
            carImg.onload = loop;
        </script>
    </body>
    </html>
    """
    components.html(game_js, height=600)

# --- الغرفة 4: المتصدرين ---
elif choice == "🏆 المتصدرين":
    st.header("🏆 قائمة الأساطير")
    st.table({
        "المركز": [1, 2, 3],
        "اللاعب": ["محمد القاسم", "أحمد علي", "عاشق السيارات"],
        "النقاط": [15400, 12300, 9800]
    })
    
