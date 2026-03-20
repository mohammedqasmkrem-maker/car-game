import streamlit as st
import streamlit.components.v1 as components

# 1. نظام الذاكرة المستمر (الفلوس 25,577 ثابتة)
if 'money' not in st.session_state: st.session_state.money = 25577
if 'score' not in st.session_state: st.session_state.score = 0
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'control' not in st.session_state: st.session_state.control = 'touch'
if 'owned_cars' not in st.session_state: st.session_state.owned_cars = ['BMW M4']
if 'current_car' not in st.session_state: st.session_state.current_car = 'BMW M4'

# قاعدة بيانات السيارات (المتجر الشغال)
CARS_SHOP = {
    'BMW M4': {'price': 0, 'color': '#00fbff', 'speed': 8, 'img': '🏎️'},
    'Ferrari F8': {'price': 5000, 'color': '#ff0000', 'speed': 12, 'img': '🏎️'},
    'Porsche 911': {'price': 15000, 'color': '#00ff44', 'speed': 15, 'img': '🏎️'}
}

# 2. التصميم (فضاء نيون)
st.markdown(f"""
<style>
    .stApp {{ background: #050505; color: white; }}
    .glass {{
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid {CARS_SHOP[st.session_state.current_car]['color']};
        border-radius: 20px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px {CARS_SHOP[st.session_state.current_car]['color']}44;
    }}
    .stButton>button {{
        background: transparent !important; color: white !important;
        border: 1px solid {CARS_SHOP[st.session_state.current_car]['color']} !important;
        border-radius: 10px; width: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# --- [ الصفحة الرئيسية ] ---
if st.session_state.page == 'home':
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.title("🚀 SPACE RACER PRO")
    st.write(f"💰 المحفظة: ${st.session_state.money} | 🚗 السيارة: {st.session_state.current_car}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏁 انطلاق"): st.session_state.page = 'play'; st.rerun()
        if st.button("🏢 المتجر"): st.session_state.page = 'shop'; st.rerun()
    with col2:
        if st.button("⚙️ الإعدادات"): st.session_state.page = 'settings'; st.rerun()
        if st.button("🌐 Language"): 
            st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ المتجر الحقيقي الشغال ] ---
elif st.session_state.page == 'shop':
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.header("🛒 معرض السيارات")
    cols = st.columns(3)
    for i, (name, d) in enumerate(CARS_SHOP.items()):
        with cols[i]:
            st.markdown(f"### {name}\n{d['img']}")
            if name in st.session_state.owned_cars:
                if st.button(f"اختيار", key=name): 
                    st.session_state.current_car = name; st.rerun()
            else:
                if st.button(f"شراء ${d['price']}", key=name):
                    if st.session_state.money >= d['price']:
                        st.session_state.money -= d['price']
                        st.session_state.owned_cars.append(name)
                        st.success("تم الشراء!")
                        st.rerun()
                    else: st.error("ما عندك فلوس!")
    if st.button("🔙 رجوع"): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ الإعدادات (تحكم حقيقي) ] ---
elif st.session_state.page == 'settings':
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.header("⚙️ إعدادات التحكم")
    c1, c2 = st.columns(2)
    if c1.button("📱 لمس (Touch)"): st.session_state.control = 'touch'; st.rerun()
    if c2.button("🎡 ستيرن (Wheel)"): st.session_state.control = 'wheel'; st.rerun()
    st.write(f"التحكم الحالي: **{st.session_state.control}**")
    if st.button("🔙 رجوع"): st.session_state.page = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [ اللعبة (عدادات شغالة + تحكم مختار + فضاء) ] ---
elif st.session_state.page == 'play':
    car = CARS_SHOP[st.session_state.current_car]
    game_js = f"""
    <div style="display:flex; justify-content:space-around; color:white; font-family:sans-serif; font-weight:bold; margin-bottom:10px;">
        <div style="text-align:center; border:1px solid {car['color']}; padding:5px; border-radius:10px;">
            SPEED<br><span id="spd" style="color:{car['color']}; font-size:20px;">0</span> KM/H
        </div>
        <div style="text-align:center; border:1px solid gold; padding:5px; border-radius:10px;">
            CASH<br><span style="color:gold;">${st.session_state.money}</span>
        </div>
    </div>
    
    <canvas id="gc" width="340" height="480" style="border:2px solid {car['color']}; border-radius:20px; background:#000; display:block; margin:auto; touch-action:none;"></canvas>
    
    <div id="wheelCont" style="display:{'block' if st.session_state.control == 'wheel' else 'none'}; text-align:center; margin-top:10px;">
        <div id="wheel" style="width:100px; height:100px; border:8px solid #444; border-radius:50%; margin:auto; position:relative;">
            <div style="width:8px; height:50px; background:{car['color']}; position:absolute; left:46px; top:0;"></div>
        </div>
    </div>

    <script>
        const c=document.getElementById("gc"), ctx=c.getContext("2d");
        let px=145, py=380, score=0, items=[], stars=[], active=true, speed={car['speed']};

        for(let i=0; i<40; i++) stars.push({{x:Math.random()*340, y:Math.random()*480, s:Math.random()*2}});

        function draw() {{
            if(!active) return;
            ctx.fillStyle="#000"; ctx.fillRect(0,0,340,480);
            
            // نجوم الفضاء
            ctx.fillStyle="white";
            stars.forEach(s => {{
                ctx.beginPath(); ctx.arc(s.x, s.y, s.s, 0, 7); ctx.fill();
                s.y += speed/2; if(s.y > 480) s.y = 0;
            }});

            // سيارة اللاعب (نيون)
            ctx.shadowBlur=20; ctx.shadowColor="{car['color']}"; ctx.fillStyle="{car['color']}";
            ctx.beginPath(); ctx.roundRect(px, py, 45, 80, 10); ctx.fill();

            // عوائق (نيازك) وعملات
            if(Math.random()<0.02) items.push({{t:'e', x:Math.random()*280+10, y:-100}});
            if(Math.random()<0.01) items.push({{t:'c', x:Math.random()*280+10, y:-100}});

            items.forEach((it, i)=>{{
                it.y += speed;
                if(it.t=='e') {{
                    ctx.shadowBlur=0; ctx.fillStyle="#555";
                    ctx.beginPath(); ctx.roundRect(it.x, it.y, 45, 80, 5); ctx.fill();
                    if(it.y+70>py && it.y<py+70 && it.x+40>px && it.x<px+40) {{ active=false; alert("💥 تحطمت المركبة!"); location.reload(); }}
                }} else {{
                    ctx.shadowBlur=15; ctx.shadowColor="gold"; ctx.fillStyle="gold";
                    ctx.beginPath(); ctx.arc(it.x+15, it.y+15, 12, 0, 7); ctx.fill();
                    if(it.y+30>py && it.y<py+80 && it.x+30>px && it.x<px+40) {{ items.splice(i,1); }}
                }}
                if(it.y>550) items.splice(i,1);
            }});

            document.getElementById("spd").innerText = Math.floor(speed * 20);
            requestAnimationFrame(draw);
        }}

        // نظام التحكم المختار
        if("{st.session_state.control}" == "touch") {{
            c.addEventListener("touchmove", (e) => {{
                let r = c.getBoundingClientRect();
                px = Math.max(10, Math.min(285, e.touches[0].clientX - r.left - 22));
                e.preventDefault();
            }}, {{passive:false}});
        }} else {{
            // تحكم الستيرن (عن طريق السحب على الستيرن السفلي)
            let w = document.getElementById("wheel");
            w.addEventListener("touchmove", (e) => {{
                let rect = w.getBoundingClientRect();
                let center = rect.left + 50;
                let move = (e.touches[0].clientX - center) * 0.5;
                px = Math.max(10, Math.min(285, px + move));
                w.style.transform = `rotate(${{move*5}}deg)`;
                e.preventDefault();
            }}, {{passive:false}});
        }}
        
        draw();
    </script>
    """
    components.html(game_js, height=650)
    if st.button("🔙 إنهاء"): st.session_state.page = 'home'; st.rerun()
                
