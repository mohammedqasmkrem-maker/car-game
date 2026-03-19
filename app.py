import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Real Traffic Racer", layout="centered")

# واجهة التطبيق
st.markdown("<h1 style='text-align: center; color: white; font-family: sans-serif;'>🏎️ TRAFFIC RACER 🏎️</h1>", unsafe_allow_html=True)

# كود اللعبة المطور
game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; display: flex; flex-direction: column; align-items: center; background: #000; overflow: hidden; }
        canvas { border: 3px solid #555; border-radius: 15px; background: #333; touch-action: none; }
        .info { color: yellow; font-family: Arial; font-size: 18px; margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="info">SCORE: <span id="s">0</span> | ❤️: <span id="l">3</span></div>
    <canvas id="g" width="340" height="500"></canvas>

    <script>
        const canvas = document.getElementById("g");
        const ctx = canvas.getContext("2d");

        // صور واقعية جديدة (روابط مباشرة دائمة)
        const roadImg = new Image(); roadImg.src = "https://raw.githubusercontent.com/Subrata-S/Car-Racing-Game-JavaScript/master/img/road.png";
        const playerImg = new Image(); playerImg.src = "https://raw.githubusercontent.com/Subrata-S/Car-Racing-Game-JavaScript/master/img/car.png";
        const enemyImg = new Image(); enemyImg.src = "https://raw.githubusercontent.com/Subrata-S/Car-Racing-Game-JavaScript/master/img/enemy.png";

        let carX = 145, score = 0, roadY = 0, speed = 8, lives = 3, gameActive = true;
        let traffic = [];

        function update() {
            if (!gameActive) return;

            // تحريك الطريق الأسفلتي
            roadY += speed; if (roadY >= 500) roadY = 0;
            ctx.drawImage(roadImg, 0, roadY, 340, 500);
            ctx.drawImage(roadImg, 0, roadY - 500, 340, 500);

            // رسم سيارتك (الرياضية)
            ctx.drawImage(playerImg, carX, 400, 50, 90);

            // توليد سيارات المرور بشكل عشوائي
            if (Math.random() < 0.02) traffic.push({x: Math.random() * 250 + 20, y: -100});
            
            traffic.forEach((obs, i) => {
                obs.y += speed - 2;
                ctx.drawImage(enemyImg, obs.x, obs.y, 50, 90);

                // كشف التصادم الحقيقي
                if (obs.y + 80 > 400 && obs.y < 490 && obs.x < carX + 45 && obs.x + 45 > carX) {
                    lives--; traffic.splice(i, 1);
                    if (lives <= 0) {
                        gameActive = false;
                        alert("GAVE OVER! Your Score: " + score);
                        location.reload();
                    }
                }
                if (obs.y > 550) { traffic.splice(i, 1); score += 10; }
            });

            document.getElementById("s").innerText = score;
            document.getElementById("l").innerText = lives;
            requestAnimationFrame(update);
        }

        // تحكم لمس احترافي للموبايل
        canvas.addEventListener("touchstart", (e) => {
            const touchX = e.touches[0].clientX - canvas.offsetLeft;
            carX = (touchX < 170) ? Math.max(20, carX - 60) : Math.min(270, carX + 60);
        });

        draw = () => update();
        playerImg.onload = draw;
    </script>
</body>
</html>
"""

components.html(game_code, height=600)
st.button("إعادة تشغيل اللعبة 🔄")
