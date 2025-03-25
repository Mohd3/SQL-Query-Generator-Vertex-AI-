import streamlit as st
from langchain_app import process_question

st.set_page_config(page_title="SQL Query Generator with Gemini", page_icon="🦾")
st.title("🦾 SQL Query Generator & Answering (Google Vertex AI)")

user_question = st.text_input("Ask Your Question About The T-shirt Shop Database:")

if st.button("Run"):
    if not user_question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Processing..."):
            try:
                query, result, answer = process_question(user_question)
                st.subheader("🧠 Generated SQL Query")
                st.code(query, language="sql")

                st.subheader("📊 SQL Result")
                st.write(result)

                st.subheader("✅ Final Answer")
                st.success(answer)

            except Exception as e:
                st.error(f"An error occurred: {e}")
