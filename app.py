import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Neon Traffic Racer", layout="centered")

# تصميم الواجهة الخارجية (Neon Style)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #fff; }
    .hud-container {
        display: flex; justify-content: space-between;
        padding: 10px; border: 2px solid #bc13fe;
        border-radius: 15px; box-shadow: 0 0 15px #bc13fe;
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
    }
    .neon-text { color: #0ff; text-shadow: 0 0 10px #0ff; font-weight: bold; }
    </style>
    <div class="hud-container">
        <span class="neon-text">SPEED: <span id="ui-speed">0</span> KM/H</span>
        <span style="color: #f0f;">SCORE: <span id="ui-score">0</span></span>
        <span style="color: #ff0055;">LIFE: ❤️❤️❤️</span>
    </div>
    """, unsafe_allow_html=True)

# كود اللعبة المتقدم (JavaScript)
game_js = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; display: flex; flex-direction: column; align-items: center; background: #000; font-family: sans-serif; }
        canvas { border: 3px solid #bc13fe; box-shadow: 0 0 20px #bc13fe; border-radius: 10px; touch-action: none; }
        .controls { display: flex; gap: 40px; margin-top: 20px; }
        .btn { 
            width: 80px; height: 80px; border-radius: 50%; border: 2px solid #0ff;
            background: rgba(0, 255, 255, 0.1); color: #0ff; font-size: 30px;
            display: flex; align-items: center; justify-content: center;
            user-select: none; backdrop-filter: blur(5px); transition: 0.1s;
        }
        .btn:active { transform: scale(1.2); background: rgba(0, 255, 255, 0.4); }
    </style>
</head>
<body>
    <canvas id="road" width="350" height="500"></canvas>
    
    <div class="controls">
        <div class="btn" id="leftBtn">◀</div>
        <div class="btn" id="nitroBtn" style="border-color:#f0f; color:#f0f;">🔥</div>
        <div class="btn" id="rightBtn">▶</div>
    </div>

    <script>
        const canvas = document.getElementById("road");
        const ctx = canvas.getContext("2d");

        // المتغيرات الأساسية
        let carX = 150, speed = 0, score = 0, lives = 3;
        let roadOffset = 0, gameActive = true, nitro = false;
        let obstacles = [];

        // نظام العوائق (المرور)
        function spawnObstacle() {
            if (Math.random() < 0.03) {
                obstacles.push({ x: Math.random() * 270 + 20, y: -100, speed: Math.random() * 3 + 2 });
            }
        }

        function update() {
            if (!gameActive) return;

            // 1. نظام السرعة
            if (speed < 120) speed += 0.2;
            if (nitro) speed = 220;
            
            roadOffset += speed / 10;
            score += Math.floor(speed / 50);

            // 2. حركة العوائق وتصادمها
            obstacles.forEach((obs, index) => {
                obs.y += (speed/20) + obs.speed;
                // تصادم
                if (obs.y + 60 > 420 && obs.x < carX + 40 && obs.x + 40 > carX) {
                    lives--;
                    obstacles.splice(index, 1);
                    if (lives <= 0) gameActive = false;
                }
                if (obs.y > 600) obstacles.splice(index, 1);
            });

            spawnObstacle();
            draw();
            requestAnimationFrame(update);
        }

        function draw() {
            ctx.fillStyle = "#111"; // أرضية الطريق
            ctx.fillRect(0, 0, 350, 500);

            // رسم الطريق اللانهائي (خطوط النيون)
            ctx.strokeStyle = "#bc13fe";
            ctx.setLineDash([30, 30]);
            ctx.lineDashOffset = -roadOffset;
            ctx.lineWidth = 5;
            ctx.beginPath(); ctx.moveTo(175, 0); ctx.lineTo(175, 500); ctx.stroke();

            // رسم سيارة اللاعب (نيون أزرق)
            ctx.shadowBlur = 15; ctx.shadowColor = "#0ff";
            ctx.fillStyle = "#0ff";
            ctx.fillRect(carX, 420, 40, 70);
            
            // رسم سيارات المرور (نيون بنفسجي)
            ctx.shadowColor = "#f0f"; ctx.fillStyle = "#f0f";
            obstacles.forEach(obs => ctx.fillRect(obs.x, obs.y, 40, 60));
            ctx.shadowBlur = 0;
        }

        // أزرار الموبايل واللمس
        document.getElementById("leftBtn").ontouchstart = () => { if(carX > 20) carX -= 40; };
        document.getElementById("rightBtn").ontouchstart = () => { if(carX < 290) carX += 40; };
        document.getElementById("nitroBtn").ontouchstart = () => { nitro = true; setTimeout(()=>nitro=false, 2000); };

        update();
    </script>
</body>
</html>
"""

components.html(game_js, height=700)

st.sidebar.markdown("### 🛠 إعدادات المطور")
color = st.sidebar.color_picker("اختر لون سيارتك", "#00ffff")
st.sidebar.write("سيتم ربط اللون برمجياً في التحديث القادم!")
