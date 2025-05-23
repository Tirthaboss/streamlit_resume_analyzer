import streamlit as st
from db import create_user, authenticate_user
from resume_parser import extract_text_from_pdf, extract_text_from_docx
import os
import openai

st.set_page_config(page_title="AI Resume Auth App", layout="centered")

api = st.text_input(label="OpenAI API Key", placeholder="ENTER YOUR OPENAI API", max_chars=48)

openai_api = openai.api_key = api

def analyze_resume(text, job_description,openai_api):
    prompt = f"Compare this resume:\n{text}\nwith the job description:\n{job_description}\nGive improvement tips and score it out of 100."
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content
if "user" not in st.session_state:
    st.title("AI Resume Analyzer - Login System")
    choice = st.selectbox("Login or Signup", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            success = create_user(email, password)
            if success:
                st.success("Account created!")
            else:
                st.error("User already exists.")
    elif choice == "Login":
        if st.button("Login"):
            user = authenticate_user(email, password)
            if user:
                st.session_state["user"] = email
                st.success("Logged in as " + email)
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    st.markdown("---")
    st.markdown("### Or Login with OAuth")
    st.markdown("""
    <!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body>
<!-- GitHub Button -->
<a href="#" class="flex items-center px-5 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition">
  <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" class="w-5 h-5 mr-3" alt="GitHub logo">
  Sign in with GitHub
</a>

<!-- Google Button -->
<a href="#" class="flex items-center px-5 py-2 bg-neutral-900 text-white rounded-full border border-gray-300 hover:bg-neutral-800 transition">
  <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" class="w-5 h-5 mr-3" alt="Google logo">
  Sign in with Google
</a>
	
</body>
</html>

				      

    """, unsafe_allow_html=True)
    st.markdown("[Login with GitHub](https://streamlit.io)", unsafe_allow_html=True)
    st.caption("OAuth login placeholders (Streamlit Cloud doesn’t support popups or Flask server)")

else:
    # LOGGED-IN VIEW
    st.sidebar.success(f"Logged in as: {st.session_state['user']}")
    if st.sidebar.button("Logout"):
        del st.session_state["user"]
        st.rerun()

    st.title("AI-Powered Resume Analyzer")
    
    resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Paste Job Description")

    if resume_file and job_description:
        if resume_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_docx(resume_file)

        st.write("Analyzing...")
        analysis = analyze_resume(resume_text, job_description)
        st.success("Analysis Complete")
        st.write(analysis)
	
