import streamlit as st
import google.generativeai as genai

# ตั้งค่าการออกแบบ
st.set_page_config(page_title="🌟 My Food Hunter", page_icon="🍽️", layout="wide")

# แสดงส่วนเนื้อหาหลักที่อยู่ด้านบนสุด
st.title("🌟 My Food Hunter")
st.subheader("ค้นหาร้านอาหารที่ดีที่สุดในเมือง")

# แถบด้านข้างสำหรับใส่ข้อมูลเพิ่มเติม
st.sidebar.header("ค้นหาร้านอาหาร")
gemini_api_key = "AIzaSyCCQumrGPGSzDgY7_YFSSI5kFzYb-WXFB4"

# ประวัติการสนทนา (chat history)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# แสดงข้อความแชทที่เกิดขึ้นก่อนหน้า
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# ตัวเลือกโมเดล
model_option = st.sidebar.selectbox(
    "เลือกโมเดลที่ต้องการใช้:",
    ["หาร้านและรีวิว", "แนะนำ จัดอันดับร้านน่ากิน", "คุยเรื่องอื่นๆ"]
)

# อินพุตผู้ใช้สำหรับถามคำถามหรือค้นหาร้านอาหาร
if user_input := st.chat_input("คุณกำลังมองหาร้านอาหารประเภทใด?"):
    # บันทึกข้อความของผู้ใช้ลงในประวัติการสนทนา
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # ตรวจสอบข้อความอินพุตจากผู้ใช้
    if user_input.strip():
        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel("gemini-pro")

            # เช็คว่าผู้ใช้ถามหาร้านอาหารหรือไม่ และเลือกโมเดลที่เหมาะสม
            if model_option == "หาร้านและรีวิว":
                prompt = (
                    f"ช่วยแนะนำร้านอาหารที่ดีและคุ้มค่าในบริเวณนี้ ตามที่คุณกล่าวถึง: {user_input}. "
                    "ตอบแบบปกติและไม่ต้องรีวิวทุกคำแนะนำ"
                )
            elif model_option == "แนะนำ จัดอันดับร้านน่ากิน":
                prompt = (
                    f"ช่วยจัดอันดับร้านอาหารที่น่ากินในบริเวณนี้ ตามที่คุณกล่าวถึง: {user_input}. "
                    "โปรดจัดอันดับให้เรียบร้อย"
                )
            else:  # คุยเรื่องอื่นๆ
                prompt = f"ตอบโต้กลับข้อความนี้เหมือนเพื่อนทั่วไป: {user_input}"

            response = model.generate_content(prompt)
            bot_response = response.text

            # บันทึกการตอบกลับจากระบบ AI ลงในประวัติการสนทนา
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.error("กรุณาใส่ข้อความที่ถูกต้อง.")
