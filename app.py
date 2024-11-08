import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input):
    model=genai.GenerativeModel("gemini-pro")
    response =model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in reader(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

input_prompt = """
Hey, act like a skilled and experienced ATS (Applicant Tracking System) with a deep understanding of the tech field, software engineering, data science, data analytics, and big data engineering. Your task is to evaluate the resume based on the given job description.

Consider that the job market is very competitive, so you should provide the best assistance for improving the resumes. Assign a percentage match based on the job description and identify any missing keywords with high accuracy.

resume: {text}
description: {jd}

I want the response in one single string, structured as follows:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

st.title("Smart ATS")
st.text("Immprove Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploaded("Upload Your Resume",type="pdf",help="Please upload the pdf")

submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)