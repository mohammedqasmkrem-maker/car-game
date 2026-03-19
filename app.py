import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Car Hub Pro", page_icon="🏎️", layout="wide")

# --- تنسيق CSS مخصص لجعل الواجهة تبدو فخمة ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background-color: #ff4b4b; color: white; border-radius: 10px; width: 100%;
    }
    .car-card {
        background-color: #262730; padding: 20px; border-radius: 15px;
        border: 1px solid #464646; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- بيانات وهمية (بيانات السيارات) ---
data = {
    'السيارة': ['Tesla Model 3', 'BMW M4', 'Mercedes G-Wagon', 'Toyota Supra', 'Audi RS7'],
    'السعر ($)': [45000, 78000, 140000, 55000, 120000],
    'النوع': ['كهربائية', 'بنزين', 'بنزين', 'بنزين', 'هجين'],
    'التسارع (0-100)': [3.1, 3.8, 4.5, 3.9, 3.5]
}
df = pd.DataFrame(data)

# --- القائمة الجانبية (Navigation) ---
with st.sidebar:
    selected = option_menu(
        menu_title="Car Hub Pro",
        options=["الرئيسية", "المعرض", "تحليل الأسعار", "المستشار الذكي"],
        icons=["house", "car-front", "graph-up", "robot"],
        menu_icon="cast", default_index=0,
    )

# --- الصفحة الرئيسية ---
if selected == "الرئيسية":
    st.title("🏎️ مرحباً بك في مستقبـل السيارات")
    st.subheader("اكتشف، قارن، واشترِ سيارة أحلامك بضغطة زر.")
    st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80")

# --- صفحة المعرض (Gallery with Filters) ---
elif selected == "المعرض":
    st.title("🖼️ معرض السيارات المميزة")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        type_filter = st.multiselect("نوع المحرك", df['النوع'].unique(), default=df['النوع'].unique())
    with col_f2:
        price_filter = st.slider("نطاق السعر ($)", 30000, 150000, (30000, 150000))

    filtered_df = df[(df['النوع'].isin(type_filter)) & (df['السعر ($)'].between(price_filter[0], price_filter[1]))]

    for index, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="car-card">
                <h3>{row['السيارة']}</h3>
                <p>السعر: <b>${row['السعر ($)']:,.0f}</b> | النوع: {row['النوع']} | التسارع: {row['التسارع (0-100)']} ثانية</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"تفاصيل {row['السيارة']}", key=index):
                st.toast(f"جاري تحميل مواصفات {row['السيارة']}...")

# --- صفحة التحليل (Charts) ---
elif selected == "تحليل الأسعار":
    st.title("📊 مقارنة أداء وسعر السيارات")
    fig = px.scatter(df, x="السعر ($)", y="التسارع (0-100)", size="السعر ($)", color="السيارة",
                     hover_name="السيارة", log_x=True, size_max=60, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- صفحة المستشار الذكي ---
elif selected == "المستشار الذكي":
    st.title("🤖 مساعد الشراء الذكي")
    user_input = st.text_input("صف لي احتياجك (مثلاً: أريد سيارة سريعة وعائلية):")
    if user_input:
        st.success("بناءً على طلبك، نقترح عليك تفقد سيارة **Audi RS7** لأنها تجمع بين الفخامة والأداء العالي.")

# --- Footer ---
st.markdown("---")
st.caption("تم التطوير بواسطة ذكاء اصطناعي لخدمة عشاق السيارات 2026")
