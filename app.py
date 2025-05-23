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
    <style>
    /* From Uiverse.io by mRcOol7 */ 
button {
  max-width: 320px;
  display: flex;
  overflow: hidden;
  position: relative;
  padding: 0.875rem 72px 0.875rem 1.75rem;
  background-color: #4285f4;
  color: #ffffff;
  font-size: 15px;
  line-height: 1.25rem;
  font-weight: 700;
  text-align: center;
  text-transform: uppercase;
  vertical-align: middle;
  align-items: center;
  border-radius: 0.5rem;
  gap: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: none;
  transition: all 0.6s ease;
  filter: brightness(1.2);
}

button .google-icon {
  background-color: #fff;
  display: grid;
  position: absolute;
  right: 0;
  place-items: center;
  width: 3rem;
  height: 100%;
  border-radius: 0.5rem 0 0 0.5rem;
  filter: brightness(1.2);
}

button span svg {
  width: 1.5rem;
  height: 1.5rem;
  filter: drop-shadow(0 0 5px rgba(66, 133, 244, 0.8));
}

button:hover {
  box-shadow: 0 4px 30px rgba(66, 133, 244, 0.1),
    0 2px 30px rgba(52, 168, 83, 0.06);
  filter: brightness(1);
}

button:hover .google-icon {
  filter: brightness(1);
	}
 
    </style>
    <!-- From Uiverse.io by mRcOol7 --> 
<button>
  Sign in with Google
  <span class="google-icon">
    <svg viewBox="0 0 48 48">
      <title>Google Logo</title>
      <clipPath id="g">
        <path
          d="M44.5 20H24v8.5h11.8C34.7 33.9 30.1 37 24 37c-7.2 0-13-5.8-13-13s5.8-13 13-13c3.1 0 5.9 1.1 8.1 2.9l6.4-6.4C34.6 4.1 29.6 2 24 2 11.8 2 2 11.8 2 24s9.8 22 22 22c11 0 21-8 21-22 0-1.3-.2-2.7-.5-4z"
        ></path>
      </clipPath>
      <g clip-path="url(#g)" class="colors">
        <path d="M0 37V11l17 13z" fill="#FBBC05"></path>
        <path d="M0 11l17 13 7-6.1L48 14V0H0z" fill="#EA4335"></path>
        <path d="M0 37l30-23 7.9 1L48 0v48H0z" fill="#34A853"></path>
        <path d="M48 48L17 24l-4-3 35-10z" fill="#4285F4"></path>
      </g>
    </svg>
  </span>
</button>

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
	
