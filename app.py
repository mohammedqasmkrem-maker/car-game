import streamlit as st
import streamlit.components.v1 as components
import random

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="Royal Racer Pro", layout="wide", initial_sidebar_state="collapsed")

# 2. نظام الذاكرة (Session State) لحفظ النقاط والتعديلات
if 'score' not in st.session_state: st.session_state.score = 0
if 'money' not in st.session_state: st.session_state.money = 1000
if 'selected_car_id' not in st.session_state: st.session_state.selected_car_id = 'car_1' # السيارة الافتراضية
if 'owned_cars' not in st.session_state: st.session_state.owned_cars = ['car_1'] # يمتلك السيارة الأولى افتراضيا
if 'page' not in st.session_state: st.session_state.page = 'home'

# تعريف السيارات المتوفرة (صور واقعية)
cars = {
    'car_1': {'name': "السيارة العادية", 'price': 0, 'image': "https://i.ibb.co/mS79vS6/blue-pickup.png", 'color': "#0000FF"}, # بيك آب
    'car_2': {'name': "السيارة الرياضية", 'price': 1500, 'image': "https://i.ibb.co/r7h4X90/sport-car.png", 'color': "#FF0000"}, # رياضية حمراء
    'car_3': {'name': "سيارة النخبة", 'price': 3000, 'image': "https://i.ibb.co/S68Jt5D/luxury-car.png", 'color': "#D4AF37"}, # فخمة ذهبية
}

# 3. تصميم الواجهة الملكية (CSS)
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1200");
        background-size: cover;
        color: white;
    }}
    .royal-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 2px solid {cars[st.session_state.selected_car_id]['color']};
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 30px {cars[st.session_state.selected_car_id]['color']}44;
    }}
    .stButton>button {{
        background: linear-gradient(45deg, {cars[st.session_state.selected_car_id]['color']}, #fff);
        color: black !important;
        border-radius: 50px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- الغرفة 1: الواجهة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.title("🔱 ROYAL TRAFFIC RACER 🔱")
    st.subheader(f"💰 الرصيد: {st.session_state.money} | 🏆 أعلى نتيجة: {st.session_state.score}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏁 ابدأ السباق"): st.session_state.page = 'play'; st.rerun()
    with col2:
        if st.button("🛠️ الكراج الملكي"): st.session_state.page = 'garage'; st.rerun()
    with col3:
        if st.button("🏆 المتصدرين"): st.session_state.page = 'leaderboard'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 2: الكراج المتطور (اختيار وشراء السيارات) ---
elif st.session_state.page == 'garage':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header("🛠️ اختر سيارتك الفخمة")
    
    cols = st.columns(len(cars))
    for i, (car_id, car_info) in enumerate(cars.items()):
        with cols[i]:
            st.image(car_info['image'], caption=car_info['name'], width=150)
            if car_id == st.session_state.selected_car_id:
                st.success("✅ هذه هي سيارتك الحالية")
            elif car_id in st.session_state.owned_cars:
                if st.button(f"اختر {car_info['name']}", key=f"select_{car_id}"):
                    st.session_state.selected_car_id = car_id
                    st.rerun()
            else:
                if st.button(f"شراء بـ {car_info['price']} 💰", key=f"buy_{car_id}"):
                    if st.session_state.money >= car_info['price']:
                        st.session_state.money -= car_info['price']
                        st.session_state.owned_cars.append(car_id)
                        st.session_state.selected_car_id = car_id
                        st.success(f"مبروك! اشتريت {car_info['name']}")
                        st.rerun()
                    else:
                        st.error("الرصيد غير كافٍ!")
    
    st.write(f"رصيدك الحالي: {st.session_state.money} 💰")
    if st.button("⬅️ العودة للرئيسية"): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الغرفة 3: ميدان السباق (اللعبة الاحترافية بصور سيارات حقيقية) ---
elif st.session_state.page == 'play':
    # جلب معلومات السيارة المختارة
    current_car_info = cars[st.session_state.selected_car_id]
    
    game_js = f"""
    <div style="display:flex; justify-content:space-between; color:{current_car_info['color']}; font-weight:bold; font-size:20px; padding:10px;">
        <span>POINTS: <span id="s">0</span></span>
        <span>NITRO: <span id="n">READY</span></span>
    </div>
    <canvas id="race" width="320" height="500" style="border:3px solid {current_car_info['color']}; border-radius:20px; background:#222;"></canvas>
    
    <script>
        const c=document.getElementById("race"), ctx=c.getContext("2d");
        let px=135, score=0, enemies=[], nitro=false, speed=7;
        let playerCarImg = new Image(); playerCarImg.src = "{current_car_info['image']}";
        
        let enemyCarImgs = [
            "https://raw.githubusercontent.com/Subrata-S/Car-Racing-Game-JavaScript/master/img/enemy.png", // سيارة حمراء
            "https://i.ibb.co/fNdf8v8/white-car.png", // سيارة بيضاء
            "https://i.ibb.co/hR4yFhX/green-car.png"  // سيارة خضراء
        ];
        
        function update() {{
            ctx.fillStyle="#1a1a1a"; ctx.fillRect(0,0,320,500); // الشارع
            
            // خطوط الطريق
            ctx.strokeStyle="#444"; ctx.setLineDash([20, 20]);
            ctx.beginPath(); ctx.moveTo(160, 0); ctx.lineTo(160, 500); ctx.stroke();

            ctx.drawImage(playerCarImg, px, 400, 50, 90); // رسم سيارة اللاعب
            if(nitro) {{ /* تأثير النيترو هنا */ }} // يمكنك إضافة تأثير اهتزاز أو ضوء

            if(Math.random()<0.02) {{
                let randomEnemyImg = new Image();
                randomEnemyImg.src = enemyCarImgs[Math.floor(Math.random() * enemyCarImgs.length)];
                enemies.push({{x:Math.random()*260, y:-100, img: randomEnemyImg}});
            }}
            
            enemies.forEach((en, i)=>{{
                en.y += nitro ? speed*2 : speed;
                ctx.drawImage(en.img, en.x, en.y, 50, 90); // رسم سيارات العدو
                
                // تصادم
                if(en.y+80 > 400 && en.y < 490 && en.x+40 > px && en.x < px+40) {{
                    alert("GAME OVER! Score: " + score); 
                    const currentScore = {st.session_state.score};
                    if (score > currentScore) {{
                        // تحديث أعلى سكور ورصيد العملات
                        window.parent.postMessage({{ type: 'streamlit:setSessionState', key: 'score', value: score }}, '*');
                        window.parent.postMessage({{ type: 'streamlit:setSessionState', key: 'money', value: {st.session_state.money} + score / 10 }}, '*'); // ربح عملات
                    }}
                    location.reload();
                }}
                if(en.y > 500) {{ enemies.splice(i,1); score += 10; }}
            }});

            document.getElementById("s").innerText = score;
            requestAnimationFrame(update);
        }}

        // التحكم
        c.ontouchstart = (e) => {{
            let tx = e.touches[0].clientX - c.offsetLeft;
            if(e.touches.length > 1) {{ // لمستين للنيترو
                nitro = true;
                document.getElementById("n").innerText = "ACTIVE!";
                setTimeout(()=>{{nitro=false; document.getElementById("n").innerText = "READY";}}, 2000); 
            }}
            else {{ px = (tx < 160) ? Math.max(10, px-60) : Math.min(260, px+60); }}
        }};
        
        playerCarImg.onload = update; // البدء بعد تحميل صورة اللاعب
    </script>
    """
    components.html(game_js, height=600)

    if st.button("🏁 إنهاء السباق"):
        # تحديث أعلى سكور ورصيد العملات عند إنهاء السباق
        if score > st.session_state.score:
            st.session_state.score = score
        st.session_state.money += score // 10 # كسب عملات من النقاط
        st.session_state.page = 'home'
        st.rerun()

# --- الغرفة 4: المتصدرين ---
elif st.session_state.page == 'leaderboard':
    st.markdown('<div class="royal-card">', unsafe_allow_html=True)
    st.header("🏆 قائمة أساطير الطريق")
    st.table({"المركز": [1,2,3], "اللاعب": ["أنت", "VIP_Racer", "King_Speed"], "النقاط": [st.session_state.score, 15000, 12000]})
    if st.button("🔙 عودة"): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

