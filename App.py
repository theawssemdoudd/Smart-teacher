import streamlit as st
from transformers import pipeline

# 1) تحميل نموذج جاهز من Hugging Face (يمكن تغييره لاحقاً لنموذج أقوى أو خاص)
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

# 2) واجهة المستخدم
st.set_page_config(page_title="المعلم الذكي", page_icon="📘", layout="centered")

st.title("📘 المعلم الذكي بالذكاء الصناعي")
st.write("اسأل أي سؤال في الرياضيات، الفيزياء أو أي مادة، وسأجيبك كمعلم خصوصي.")

# إدخال سؤال الطالب
question = st.text_area("✍️ اكتب سؤالك هنا:")

if st.button("إجابة"):
    if question.strip():
        with st.spinner("⏳ جاري التفكير..."):
            # 3) توليد الإجابة
            response = qa_pipeline(question, max_length=200, num_return_sequences=1)
            answer = response[0]['generated_text']

            # 4) عرض الإجابة
            st.subheader("✅ الإجابة:")
            st.write(answer)

            # 5) اقتراح تمرين إضافي
            st.subheader("📝 تمرين إضافي لك:")
            st.write(f"جرّب حل سؤال مشابه: {question} لكن بأرقام أو معطيات مختلفة.")
    else:
        st.warning("من فضلك اكتب سؤالاً أولاً.")
