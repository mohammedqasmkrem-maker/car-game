import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون واسعة وفخمة
st.set_page_config(page_title="Pro Traffic Racer", layout="wide")

# تصميم الواجهة (CSS) لتشبه ألعاب الموبايل
st.markdown("""
    <style>
    .stApp { background-color: #000; }
    .game-box {
        border: 5px solid #99ff33;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 0 30px #99ff33;
    }
    .title {
        color: #99ff33;
        text-align: center;
        font-family: 'Arial Black';
        font-size: 40px;
        margin-bottom: 20px;
    }
    </style>
    <p class="title">TRAFFIC RACER PRO 3D</p>
    """, unsafe_allow_html=True)

# عرض اللعبة (سحب لعبة 3D حقيقية من سيرفر ألعاب)
# ملاحظة: هذا الرابط هو للعبة سيارات 3D حقيقية
game_url = "https://www.cutetherapy.com/games/road-racer/index.html" 

with st.container():
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.markdown('<div class="game-box">', unsafe_allow_html=True)
        components.iframe(game_url, height=600, scrolling=False)
        st.markdown('</div>', unsafe_allow_html=True)

# أزرار تحت اللعبة
st.write(" ")
c1, c2, c3 = st.columns(3)
c1.button("🏆 المتصدرين")
c2.button("🚗 كراج السيارات")
c3.button("⚙️ الإعدادات")
