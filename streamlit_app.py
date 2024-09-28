import streamlit as st
from googlesearch import search
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
if "user_interests" not in st.session_state:
    st.session_state.user_interests = []

# แสดงข้อความแชทที่เกิดขึ้นก่อนหน้า
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# อินพุตผู้ใช้สำหรับถามคำถามหรือค้นหาร้านอาหาร
if user_input := st.chat_input("คุณต้องการหาข้อมูลอะไร?"):
    # บันทึกข้อความของผู้ใช้ลงในประวัติการสนทนา
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # เก็บข้อมูลที่ผู้ใช้สนใจ
    if user_input.strip():
        st.session_state.user_interests.append(user_input)

        try:
            # สร้าง prompt โดยรวมประวัติการสนทนา
            history = "\n".join([f"{role}: {message}" for role, message in st.session_state.chat_history[-5:]])  # เก็บคำถาม-คำตอบ 5 ตัวล่าสุด
            prompt = f"นี่คือประวัติการสนทนาที่ผ่านมา:\n{history}\n\nคำถามใหม่: {user_input}"

            # ค้นหาข้อมูลจาก Google
            search_results = search(user_input, num_results=3)  # จำนวนผลลัพธ์ที่ต้องการ
            results = "\n".join(search_results)

            # บันทึกการตอบกลับจากการค้นหา
            if results:
                bot_response = f"นี่คือผลลัพธ์จากการค้นหา:\n{results}"
            else:
                bot_response = "ไม่พบข้อมูลที่เกี่ยวข้อง"

            # บันทึกการตอบกลับจากระบบ AI ลงในประวัติการสนทนา
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.error("กรุณาใส่ข้อความที่ถูกต้อง.")

# แสดงความสนใจของผู้ใช้
if st.session_state.user_interests:
    st.sidebar.subheader("ความสนใจของคุณ:")
    for interest in st.session_state.user_interests:
        st.sidebar.markdown(f"- {interest}")
