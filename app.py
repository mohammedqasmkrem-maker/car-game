import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="Car Hub Pro", layout="centered")

# --- القائمة الجانبية (الغرف) ---
st.sidebar.title("🎮 القائمة الرئيسية")
page = st.sidebar.radio("اختر الوجهة:", ["🏠 الرئيسية", "🏎️ صالة اللعب"])

# --- الغرفة الأولى: الرئيسية (خفيفة جداً) ---
if page == "🏠 الرئيسية":
    st.markdown("<h1 style='text-align: center;'>مرحباً بك في Car Hub Pro</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80", caption="مستقبل السيارات بين يديك")
    st.write("استخدم القائمة الجانبية للدخول إلى صالة اللعب واختبار مهاراتك!")

# --- الغرفة الثانية: صالة اللعب (معزولة) ---
elif page == "🏎️ صالة اللعب":
    st.markdown("<h2 style='text-align: center; color: yellow;'>ميدان السباق</h2>", unsafe_allow_html=True)
    
    # كود اللعبة (محسن لتقليل الضغط)
    game_js = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { margin: 0; background: #111; display: flex; flex-direction: column; align-items: center; }
            canvas { border: 2px solid yellow; border-radius: 10px; background: #222; }
            .ui { color: white; font-family: sans-serif; margin: 10px; font-size: 18px; }
        </style>
    </head>
    <body>
        <div class="ui">SCORE: <span id="s">0</span> | ❤️: <span id="l">3</span></div>
        <canvas id="canvas" width="320" height="480"></canvas>
        <script>
            const canvas = document.getElementById("canvas");
            const ctx = canvas.getContext("2d");
            
            // استخدام روابط ثابتة وسريعة لتقليل وقت التحميل
            const carImg = new Image(); carImg.src = "https://raw.githubusercontent.com/Subrata-S/Car-Racing-Game-JavaScript/master/img/car.png";
            const enemyImg = new Image(); enemyImg.src = "https://raw.githubusercontent.com/Subrata-S/Car-Racing-Game-JavaScript/master/img/enemy.png";
            
            let x = 135, y = 380, score = 0, lives = 3, enemies = [];
            
            function update() {
                ctx.clearRect(0, 0, 320, 480);
                
                // رسم سيارة اللاعب
                ctx.drawImage(carImg, x, y, 50, 80);
                
                // حركة الأعداء
                if(Math.random() < 0.02) enemies.push({x: Math.random()*270, y: -100});
                enemies.forEach((en, i) => {
                    en.y += 5;
                    ctx.drawImage(enemyImg, en.x, en.y, 50, 80);
                    
                    // تصادم
                    if(en.y > 330 && en.y < 430 && en.x > x-40 && en.x < x+40) {
                        lives--; enemies.splice(i, 1);
                        if(lives <= 0) location.reload();
                    }
                    if(en.y > 480) { enemies.splice(i, 1); score += 10; }
                });
                
                document.getElementById("s").innerText = score;
                document.getElementById("l").innerText = lives;
                requestAnimationFrame(update);
            }

            canvas.addEventListener("touchstart", (e) => {
                let t = e.touches[0].clientX - canvas.offsetLeft;
                x = (t < 160) ? Math.max(0, x-60) : Math.min(270, x+60);
            });
            
            carImg.onload = update;
        </script>
    </body>
    </html>
    """
    components.html(game_js, height=550)
    st.warning("⚠️ إذا لم تظهر اللعبة فوراً، انتظر ثوانٍ لتحميل الصور.")
    
