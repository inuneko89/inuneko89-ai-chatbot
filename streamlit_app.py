import streamlit as st
import google.generativeai as genai

# ตั้งค่าการออกแบบ
st.set_page_config(page_title="🌟 My Food Hunter", page_icon="🍽️", layout="wide")

# แสดงส่วนเนื้อหาหลักที่อยู่ด้านบนสุด
st.title("🌟 My Food Hunter")
st.subheader("ค้นหาร้านอาหารที่ดีที่สุดในเมือง")

# แถบด้านข้าง
st.sidebar.header("ค้นหาร้านอาหาร")
gemini_api_key = "AIzaSyCCQumrGPGSzDgY7_YFSSI5kFzYb-WXFB4"

# ปุ่มประเภทอาหาร
cuisine_types = ["อาหารไทย", "อาหารอิตาเลียน", "อาหารจีน", "อาหารญี่ปุ่น", "อาหารฝรั่งเศส"]
selected_cuisine = st.sidebar.selectbox("เลือกประเภทอาหาร:", cuisine_types)

# อินพุตเพื่อค้นหาร้านอาหารเพิ่มเติม
user_input = st.sidebar.text_input("คุณต้องการข้อมูลเพิ่มเติมเกี่ยวกับ:", "")

# ปุ่มค้นหา
if st.sidebar.button("ค้นหา"):
    if user_input.strip():
        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel("gemini-pro")
            prompt = (
                f"แนะนำร้านอาหารที่ดีและคุ้มค่าในประเภท '{selected_cuisine}' "
                f"ตามคำขอ: {user_input}. รวมถึงรีวิวที่น่าสนใจและน่าดึงดูด."
            )
            response = model.generate_content(prompt)
            bot_response = response.text
            
            # แสดงการตอบกลับในหน้าแอป
            st.success("คำแนะนำจากระบบ:")
            st.markdown(bot_response)
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.error("กรุณาใส่ข้อความที่ถูกต้อง.")

# การจัดระเบียบการแสดงผล
st.markdown("---")  # เส้นแบ่ง

# แสดงประวัติการสนทนา
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)
