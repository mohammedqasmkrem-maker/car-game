import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Real Traffic Racer", layout="centered")

# كود اللعبة باستخدام جافا سكريبت احترافي وصور واقعية
game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #222; font-family: sans-serif; }
        canvas { display: block; margin: 0 auto; border: 4px solid #555; border-radius: 15px; }
        .stats { position: absolute; top: 10px; left: 20px; color: yellow; font-size: 20px; font-weight: bold; text-shadow: 2px 2px #000; }
    </style>
</head>
<body>
    <div class="stats">SCORE: <span id="score">0</span> | LIVES: <span id="lives">❤️❤️❤️</span></div>
    <canvas id="game" width="350" height="550"></canvas>

    <script>
        const canvas = document.getElementById("game");
        const ctx = canvas.getContext("2d");

        // صور واقعية (سيارات وطريق)
        const roadImg = new Image(); roadImg.src = "https://i.ibb.co/vY6YfTr/road-texture.jpg"; 
        const playerImg = new Image(); playerImg.src = "https://i.ibb.co/mS79vS6/blue-pickup.png";
        const enemyImg = new Image(); enemyImg.src = "https://i.ibb.co/fNdf8v8/white-car.png";

        let carX = 150, score = 0, roadY = 0, speed = 8, lives = 3, gameActive = true;
        let traffic = [];

        function draw() {
            if (!gameActive) return;

            // تحريك الطريق
            roadY += speed; if (roadY >= 550) roadY = 0;
            ctx.drawImage(roadImg, 0, roadY, 350, 550);
            ctx.drawImage(roadImg, 0, roadY - 550, 350, 550);

            // رسم سيارتك (البيك آب)
            ctx.drawImage(playerImg, carX, 430, 50, 90);

            // توليد وحركة المرور
            if (Math.random() < 0.02) traffic.push({x: Math.random() * 260 + 20, y: -100});
            
            traffic.forEach((obs, i) => {
                obs.y += speed - 2;
                ctx.drawImage(enemyImg, obs.x, obs.y, 45, 85);

                // كشف التصادم
                if (obs.y + 70 > 430 && obs.y < 520 && obs.x < carX + 45 && obs.x + 45 > carX) {
                    lives--; traffic.splice(i, 1);
                    if (lives <= 0) {
                        gameActive = false;
                        alert("انتهت اللعبة! مجموع نقاطك: " + score);
                        location.reload();
                    }
                }
                if (obs.y > 600) { traffic.splice(i, 1); score += 10; }
            });

            document.getElementById("score").innerText = score;
            document.getElementById("lives").innerText = "❤️".repeat(lives);
            requestAnimationFrame(draw);
        }

        // تحكم الموبايل (لمس الشاشة)
        canvas.addEventListener("touchstart", (e) => {
            const touchX = e.touches[0].clientX - canvas.offsetLeft;
            carX = (touchX < 175) ? Math.max(20, carX - 60) : Math.min(280, carX + 60);
        });

        draw();
    </script>
</body>
</html>
"""

st.markdown("<h2 style='text-align: center; color: #99ff33;'>TRAFFIC RACER MOBILE</h2>", unsafe_allow_html=True)
components.html(game_code, height=600)
st.info("💡 تحكم من الموبايل: اضغط على يسار أو يمين الشاشة لتحريك السيارة.")
