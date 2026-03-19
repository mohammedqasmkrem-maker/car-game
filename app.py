import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة الأساسية - ضرورية جداً
st.set_page_config(page_title="Pro Racer", layout="centered")

# منع الهوامش البيضاء اللي تخرب التصميم
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    iframe { border-radius: 15px; box-shadow: 0 0 20px #0ff; }
    </style>
    """, unsafe_allow_html=True)

# نظام الغرف (التنقل)
if 'page' not in st.session_state:
    st.session_state.page = 'main'

def go(p):
    st.session_state.page = p

# --- الغرفة 1: الرئيسية ---
if st.session_state.page == 'main':
    st.markdown("<h1 style='text-align:center; color:#0ff;'>🏎️ TRAFFIC RACER PRO</h1>", unsafe_allow_html=True)
    st.write("---")
    if st.button("🏁 ابدأ السباق الآن", use_container_width=True):
        go('play')
    if st.button("🛠️ دخول الكراج", use_container_width=True):
        go('garage')
    st.image("https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=500", caption="جاهز للتحدي؟")

# --- الغرفة 2: الكراج ---
elif st.session_state.page == 'garage':
    st.header("🛠️ كراج التعديلات")
    st.color_picker("اختر لون السيارة النيون", "#00f2fe")
    st.select_slider("تطوير المحرك", ["V6", "V8", "V10", "V12"])
    if st.button("⬅️ العودة للرئيسية"):
        go('main')

# --- الغرفة 3: اللعب (الكود اللي مستحيل يطلع فارغ) ---
elif st.session_state.page == 'play':
    # كود HTML/JS معزول تماماً ومبني داخل الصفحة
    game_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { margin: 0; background: #111; font-family: sans-serif; overflow: hidden; display: flex; flex-direction: column; align-items: center; }
            #c { border: 2px solid #0ff; background: #222; touch-action: none; cursor: crosshair; }
            .ui { color: #0ff; font-size: 20px; margin: 10px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="ui">SCORE: <span id="s">0</span> | ❤️: <span id="l">3</span></div>
        <canvas id="c" width="320" height="480"></canvas>
        <script>
            const canvas = document.getElementById("c");
            const ctx = canvas.getContext("2d");
            
            let player = { x: 135, y: 380, w: 50, h: 80 };
            let score = 0, lives = 3, enemies = [], speed = 5;

            function draw() {
                ctx.fillStyle = "#222"; ctx.fillRect(0,0,320,480);
                
                // خطوط الطريق
                ctx.strokeStyle = "#444"; ctx.setLineDash([20, 20]);
                ctx.beginPath(); ctx.moveTo(160,0); ctx.lineTo(160,480); ctx.stroke();

                // رسم اللاعب (سيارة بيك آب زرقاء بالرسم)
                ctx.fillStyle = "#00f2fe";
                ctx.fillRect(player.x, player.y, 50, 80); 
                ctx.fillStyle = "#000"; ctx.fillRect(player.x+5, player.y+10, 40, 20); // الزجاج

                // الأعداء
                if(Math.random() < 0.02) enemies.push({ x: Math.random()*270, y: -100 });
                enemies.forEach((en, i) => {
                    en.y += speed;
                    ctx.fillStyle = "#ff0055"; ctx.fillRect(en.x, en.y, 50, 80); // سيارة العدو
                    
                    // تصادم
                    if(en.y+80 > player.y && en.y < player.y+80 && en.x+50 > player.x && en.x < player.x+50) {
                        lives--; enemies.splice(i, 1);
                        if(lives <= 0) { alert("Game Over! Score: " + score); location.reload(); }
                    }
                    if(en.y > 480) { enemies.splice(i, 1); score += 10; speed += 0.1; }
                });

                document.getElementById("s").innerText = score;
                document.getElementById("l").innerText = lives;
                requestAnimationFrame(draw);
            }

            // تحكم لمس بسيط ومضمون
            canvas.addEventListener("touchstart", (e) => {
                let tx = e.touches[0].clientX - canvas.offsetLeft;
                player.x = (tx < 160) ? Math.max(0, player.x-60) : Math.min(270, player.x+60);
            });

            draw();
        </script>
    </body>
    </html>
    """
    components.html(game_html, height=580)
    if st.button("❌ إنهاء اللعب"):
        go('main')
    
