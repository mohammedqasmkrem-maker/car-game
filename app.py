import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Traffic Racer Pro", layout="centered")

# تصميم الواجهة بالألوان اللي ردتها
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; }
    .title { color: #99ff33; text-align: center; font-size: 40px; font-weight: bold; font-family: 'Arial Black'; }
    </style>
    <p class="title">TRAFFIC RACER JS</p>
    """, unsafe_allow_html=True)

# كود اللعبة بلغة JavaScript و HTML
game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #333; }
        canvas { display: block; background: #555; margin: 0 auto; border: 5px solid #99ff33; }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="300" height="500"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let carX = 130;
        let enemyY = -100;
        let enemyX = 130;
        let score = 0;
        let gameOver = false;

        function draw() {
            if (gameOver) {
                ctx.fillStyle = "white";
                ctx.font = "30px Arial";
                ctx.fillText("Game Over!", 70, 250);
                ctx.fillText("Score: " + score, 90, 300);
                return;
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // الطريق
            ctx.fillStyle = "gray";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = "white";
            ctx.setLineDash([20, 20]);
            ctx.moveTo(150, 0); ctx.lineTo(150, 500); ctx.stroke();

            // سيارتك (الزرقاء)
            ctx.fillStyle = "blue";
            ctx.fillRect(carX, 400, 40, 70);

            // سيارة العدو (الحمراء)
            ctx.fillStyle = "red";
            ctx.fillRect(enemyX, enemyY, 40, 70);

            enemyY += 5; // سرعة العدو
            if (enemyY > 500) {
                enemyY = -100;
                enemyX = Math.random() > 0.5 ? 60 : 200;
                score++;
            }

            // كشف الاصطدام
            if (enemyY + 70 > 400 && enemyX < carX + 40 && enemyX + 40 > carX) {
                gameOver = true;
            }

            requestAnimationFrame(draw);
        }

        document.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft" && carX > 50) carX -= 70;
            if (e.key === "ArrowRight" && carX < 210) carX += 70;
        });

        draw();
    </script>
</body>
</html>
"""

# عرض اللعبة داخل التطبيق
components.html(game_code, height=520)

# أزرار التحكم (للموبايل)
st.write("استخدم الأزرار للتحرك:")
col1, col2 = st.columns(2)
if col1.button("⬅️ يسار"):
    st.warning("حالياً التحكم فقط بلوحة المفاتيح (الأسهم)، برمجياً نحتاج ربط الأزرار بالـ JS")
if col2.button("يمين ➡️"):
    pass

st.markdown("---")
st.button("🏆 قائمة المتصدرين")
st.button("⚙️ الإعدادات")
