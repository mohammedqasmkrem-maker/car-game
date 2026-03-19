import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Real Traffic Racer", layout="centered")

# واجهة التطبيق الخارجية
st.markdown("""
    <style>
    .stApp { background-color: #2d5a27; } /* خلفية عشبية خارج اللعبة */
    .title { color: white; text-align: center; font-family: 'Arial Black'; font-size: 35px; text-shadow: 2px 2px #000; }
    </style>
    <p class="title">TRAFFIC RACER MOBILE</p>
    """, unsafe_allow_html=True)

# كود اللعبة (الأسفلت والسيارات الحقيقية)
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; display: flex; flex-direction: column; align-items: center; background: transparent; }
        canvas { border: 4px solid #333; border-radius: 10px; background: #444; touch-action: none; }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="350" height="550"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // صور اللعبة
        const roadImg = new Image(); roadImg.src = "https://i.ibb.co/vY6YfTr/road-texture.jpg"; // صورة أسفلت حقيقي
        const playerImg = new Image(); playerImg.src = "https://i.ibb.co/mS79vS6/blue-pickup.png"; // سيارة بيك آب زرقاء
        const enemyImg = new Image(); enemyImg.src = "https://i.ibb.co/fNdf8v8/white-car.png"; // سيارات مرور

        let carX = 150, roadY = 0, score = 0, speed = 7, lives = 3;
        let traffic = [];

        function update() {
            if (lives <= 0) {
                ctx.fillStyle = "rgba(0,0,0,0.7)"; ctx.fillRect(0,0,350,550);
                ctx.fillStyle = "red"; ctx.font = "40px Bold"; ctx.fillText("خسرت!", 110, 280);
                return;
            }

            roadY += speed; if (roadY >= 550) roadY = 0;
            if (Math.random() < 0.02) traffic.push({x: Math.random()*250+50, y: -100});

            traffic.forEach((obs, i) => {
                obs.y += speed - 2;
                if (obs.y > 400 && obs.y < 520 && obs.x > carX-35 && obs.x < carX+35) {
                    lives--; traffic.splice(i, 1);
                }
                if (obs.y > 600) traffic.splice(i, 1);
            });
            score++;
            draw();
            requestAnimationFrame(update);
        }

        function draw() {
            // 1. رسم الطريق الواقعي
            ctx.drawImage(roadImg, 0, roadY, 350, 550);
            ctx.drawImage(roadImg, 0, roadY - 550, 350, 550);

            // 2. رسم سيارة اللاعب (البيك آب)
            ctx.drawImage(playerImg, carX, 450, 50, 90);

            // 3. رسم سيارات المرور
            traffic.forEach(obs => ctx.drawImage(enemyImg, obs.x, obs.y, 45, 85));

            // 4. عرض النقاط والحياة
            ctx.fillStyle = "yellow"; ctx.font = "20px Arial";
            ctx.fillText("Score: " + score, 20, 30);
            ctx.fillText("❤️".repeat(lives), 260, 30);
        }

        // تحكم لمس للموبايل
        canvas.addEventListener("touchstart", (e) => {
            let touchX = e.touches[0].clientX - canvas.offsetLeft;
            if (touchX < 175) carX = Math.max(50, carX - 60);
            else carX = Math.min(250, carX + 60);
        });

        update();
    </script>
</body>
</html>
"""

components.html(game_html, height=600)

# أزرار تحكم إضافية بالأسفل
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("إعادة اللعب 🔄"):
        st.rerun()

st.caption("<center>تصميم واقعي لمحاكاة Traffic Racer</center>", unsafe_allow_html=True)
