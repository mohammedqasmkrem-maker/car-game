import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="ASTRA REAL RACER", layout="wide", initial_sidebar_state="collapsed")

# تصميم UI احترافي مع خلفية نجمية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #1a1a2e 0%, #0a0a0a 100%);
        color: #e0e0e0;
    }
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 50px;
        letter-spacing: 5px;
        margin-bottom: 0px;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    
    .control-btn {
        background: rgba(0, 242, 254, 0.1);
        border: 1px solid #00f2fe;
        color: #00f2fe;
        border-radius: 50%;
        width: 70px; height: 70px;
        font-size: 24px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
    }
    </style>
    <h1 class="main-header">ASTRA</h1>
    """, unsafe_allow_html=True)

# الجزء الخاص باللعبة (محرك محسّن بصرياً)
# **ملاحظة:** تحتاج إلى صور سيارات شفافة (PNG) ترفعها على الإنترنت
# وتبدل الروابط هنا
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; display: flex; flex-direction: column; align-items: center; background: transparent; }
        canvas { 
            border-radius: 25px; 
            box-shadow: 0 0 50px rgba(79, 172, 254, 0.2);
            background: #0f172a;
        }
        .ui-overlay {
            position: absolute; top: 20px; width: 300px;
            display: flex; justify-content: space-between;
            font-family: 'monospace'; color: #00f2fe; text-shadow: 0 0 5px #00f2fe;
            z-index: 10;
        }
    </style>
</head>
<body>
    <div class="ui-overlay">
        <div id="score">SCORE: 000</div>
        <div id="lives">❤️❤️❤️</div>
    </div>
    <canvas id="gameCanvas" width="340" height="550"></canvas>
    
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        
        let carPos = 150, score = 0, speed = 5, frame = 0, lives = 3;
        let traffic = [];

        // تحميل صور السيارات (يجب أن تكون شفافة PNG)
        // **هنا لازم تحط روابط لصور سياراتك**
        const playerCarImg = new Image();
        playerCarImg.src = "https://i.ibb.co/L5p0Gv0/player-car.png"; // رابط لسيارتك
        
        const enemyCarImg = new Image();
        enemyCarImg.src = "https://i.ibb.co/3Wf4Gz7/enemy-car.png"; // رابط لسيارة العدو

        function drawPlayer() {
            ctx.shadowBlur = 15; ctx.shadowColor = "#00f2fe";
            ctx.drawImage(playerCarImg, carPos, 450, 40, 70);
            ctx.shadowBlur = 0;
        }

        function gameLoop() {
            if (!lives) { // إذا خلصت الأرواح
                ctx.fillStyle = "white";
                ctx.font = "30px Orbitron";
                ctx.fillText("GAME OVER", canvas.width / 2 - 80, canvas.height / 2);
                return;
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // رسم الطريق (خطوط بيضاء تتحرك)
            ctx.setLineDash([40, 20]);
            ctx.strokeStyle = "rgba(255,255,255,0.1)"; // لون خطوط الطريق
            ctx.lineWidth = 4;
            ctx.lineDashOffset = -frame * speed;
            ctx.beginPath(); 
            ctx.moveTo(100, 0); ctx.lineTo(100, 550); ctx.stroke(); // خط يسار
            ctx.moveTo(240, 0); ctx.lineTo(240, 550); ctx.stroke(); // خط يمين
            
            drawPlayer();
            
            // توليد وحركة المرور
            if(frame % 100 == 0) traffic.push({x: Math.random()*240 + 50, y: -100}); // نطاق توليد أوسع
            traffic.forEach((car, i) => {
                car.y += speed;
                ctx.drawImage(enemyCarImg, car.x, car.y, 40, 70);
                
                // اصطدام
                if(car.y > 400 && car.y < 520 && car.x > carPos - 35 && car.x < carPos + 35) {
                   lives--;
                   document.getElementById("lives").innerText = "❤️".repeat(lives);
                   traffic.splice(i, 1); // حذف السيارة بعد الاصطدام
                }
                if(car.y > 550) traffic.splice(i, 1); // حذف السيارات اللي تطلع برا الشاشة
            });

            score++;
            document.getElementById("score").innerText = "SCORE: " + score;
            frame++;
            requestAnimationFrame(gameLoop);
        }

        window.addEventListener("keydown", e => {
            if(e.key == "ArrowLeft" && carPos > 20) carPos -= 30;
            if(e.key == "ArrowRight" && carPos < 280) carPos += 30;
        });

        gameLoop();
    </script>
</body>
</html>
"""

# عرض اللعبة في كرت زجاجي
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        components.html(game_html, height=600)

# أزرار تحكم الموبايل (تصميم نيون دائري)
st.markdown("""
    <div style="display: flex; justify-content: center; gap: 50px; margin-top: -50px;">
        <button class="control-btn" onclick="window.parent.postMessage('left', '*')">L</button>
        <button class="control-btn" style="border-color: #ff0055; color: #ff0055;">🔥</button>
        <button class="control-btn" onclick="window.parent.postMessage('right', '*')">R</button>
    </div>
    """, unsafe_allow_html=True)

st.write(" ")
st.caption("<center>ASTRA ENGINE v1.0 - Premium Driving Experience</center>", unsafe_allow_html=True)
