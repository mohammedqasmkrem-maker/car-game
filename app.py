elif st.session_state.page == 'play':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    
    # كود اللعبة بتصميم واقعي (سيارات وطريق)
    game_html = """
    <div style="color:#D4AF37; font-size:24px; font-weight:bold; margin-bottom:10px; font-family:Arial;">
        🏆 SCORE: <span id="sc">0</span>
    </div>
    <canvas id="rc" width="320" height="500" style="border:4px solid #D4AF37; border-radius:20px; background:#333; box-shadow: 0 0 20px rgba(212,175,55,0.5);"></canvas>
    
    <script>
        const c=document.getElementById("rc"), ctx=c.getContext("2d");
        let px=135, py=400, score=0, roadY=0, enemies=[];

        function drawPlayer(x, y) {
            // رسم جسم السيارة الملكية (ذهبي وأسود)
            ctx.fillStyle = "#D4AF37";
            ctx.beginPath();
            ctx.roundRect(x, y, 50, 85, 10);
            ctx.fill();
            // الزجاج الأمامي
            ctx.fillStyle = "#111";
            ctx.fillRect(x+5, y+15, 40, 20);
            // الإطارات
            ctx.fillStyle = "#000";
            ctx.fillRect(x-5, y+10, 5, 20); ctx.fillRect(x+50, y+10, 5, 20);
            ctx.fillRect(x-5, y+55, 5, 20); ctx.fillRect(x+50, y+55, 5, 20);
        }

        function drawEnemy(x, y) {
            // رسم سيارات المرور (أبيض وفضي)
            ctx.fillStyle = "#C0C0C0";
            ctx.beginPath();
            ctx.roundRect(x, y, 48, 80, 8);
            ctx.fill();
            ctx.fillStyle = "#333";
            ctx.fillRect(x+8, y+55, 32, 15); // الزجاج الخلفي
        }

        function draw() {
            // رسم الطريق المتحرك
            ctx.fillStyle="#222"; ctx.fillRect(0,0,320,500);
            ctx.strokeStyle="#D4AF37"; ctx.setLineDash([30, 30]); ctx.lineWidth=4;
            roadY += 10; if(roadY > 60) roadY = 0;
            ctx.beginPath(); ctx.moveTo(160, -60 + roadY); ctx.lineTo(160, 560 + roadY); ctx.stroke();

            // رسم اللاعب
            drawPlayer(px, py);

            // حركة المرور
            if(Math.random()<0.025) enemies.push({x:Math.random()*250 + 10, y:-100});
            
            enemies.forEach((en, i)=>{
                en.y += 7; // سرعة السيارات الأخرى
                drawEnemy(en.x, en.y);

                // كشف التصادم (حقيقي)
                if(en.y+70 > py && en.y < py+70 && en.x+40 > px && en.x < px+40) {
                    alert("تحطمت السيارة! نقاطك: " + score);
                    location.reload();
                }

                if(en.y > 500) { enemies.splice(i,1); score += 100; }
            });

            document.getElementById("sc").innerText = score;
            requestAnimationFrame(draw);
        }

        // تحكم لمس ناعم
        c.ontouchstart=(e)=>{
            let t=e.touches[0].clientX - c.offsetLeft;
            px = (t < 160) ? Math.max(15, px-65) : Math.min(255, px+65);
        };

        draw();
    </script>
    """
    components.html(game_html, height=600)
    
    if st.button("🏁 إنهاء السباق والعودة للكراج"):
        st.session_state.page = 'main'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
