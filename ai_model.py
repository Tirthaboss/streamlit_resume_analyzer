import openai
from app import *
openai.api_key = api

def analyze_resume(text, job_description):
    prompt = f"Compare this resume:\n{text}\nwith the job description:\n{job_description}\nGive improvement tips and score it out of 100."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content
