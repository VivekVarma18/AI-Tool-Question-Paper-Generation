import streamlit as st
from PyPDF2 import PdfReader
import openai
import os

# ---------------- API CONFIG ----------------
API_KEY = os.getenv("TOGETHER_API_KEY")
if not API_KEY:
    st.error("❌ TOGETHER_API_KEY not found. Please set it in CMD.")
    st.stop()

openai.api_key = API_KEY
openai.api_base = "https://api.together.xyz/v1"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Question Paper Generator",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: 700;
    text-align: center;
}
.sub-title {
    text-align: center;
    color: #555;
    margin-bottom: 30px;
}
.output-box {
    background-color: #ffffff;
    color: #000000;
    padding: 28px;
    border-radius: 10px;
    border: 1px solid #999;
    font-family: "Times New Roman", serif;
    font-size: 16px;
    line-height: 1.6;
    white-space: pre-wrap;
}
.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>🧠 AI Question Paper Generator</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>Automatic University Question Paper Creation using AI</div>",
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Paper Settings")

    role = st.radio("Select Role", ["Teacher", "Student"])

    subject = st.text_input(
        "📘 Subject Name",
        placeholder="Enter Subject Name"
    )

    difficulty = st.selectbox(
        "🎯 Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )

    paper_set = st.selectbox(
        "📄 Question Paper Set",
        ["Set A", "Set B", "Set C"]
    )

    st.markdown("### 🧮 Marks Distribution (Total = 100)")
    two_mark = st.number_input("2 Mark Questions", 0, 20, 10)
    five_mark = st.number_input("5 Mark Questions", 0, 10, 4)
    ten_mark = st.number_input("10 Mark Questions", 0, 10, 6)

# ---------------- MAIN INPUT AREA ----------------
st.markdown("## 📥 Input Content")

input_type = st.radio(
    "Choose Input Type",
    ["Paste Text", "Upload PDF"],
    horizontal=True
)

content = ""

if input_type == "Paste Text":
    content = st.text_area(
        "Paste syllabus / notes / previous question papers",
        height=260
    )
else:
    pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])
    if pdf_file:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                content += text + "\n"

# ---------------- GENERATE BUTTON ----------------
st.markdown("## 🚀 Generate Question Paper")

if st.button("📝 Generate Question Paper", use_container_width=True):

    if not subject.strip():
        st.warning("⚠️ Please enter the subject name.")
    elif content.strip() == "":
        st.warning("⚠️ Please provide syllabus content.")
    else:
        with st.spinner("Generating professional university question paper..."):

            prompt = f"""
You are a PROFESSIONAL Indian University Question Paper Setter.

Create a STRICTLY FORMATTED Question Paper.

SUBJECT: {subject}
DIFFICULTY: {difficulty}
SET: {paper_set}

TIME: 3 Hours
MAX MARKS: 100

IMPORTANT RULES:
- Follow Indian university exam style
- DO NOT underline anything
- DO NOT mention marks beside each question
- Use academic language
- Clear numbering
- NO answers
- NO explanations
- NO repetition

QUESTION PAPER FORMAT:

------------------------------------
{subject}
Time: 3 Hours
Max Marks: 100
{paper_set}

PART A
Answer ALL questions

(Generate exactly {two_mark} questions – short answer type)

PART B
Answer ALL questions

(Generate exactly {five_mark} questions – brief answer type)

PART C
Answer ALL questions

(Generate exactly {ten_mark} questions – long answer / essay type)

Use the syllabus content below ONLY to create questions.

SYLLABUS CONTENT:
{content}
"""

            response = openai.ChatCompletion.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                messages=[
                    {
                        "role": "system",
                        "content": "You generate Indian university question papers."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=2500
            )

            question_paper = response["choices"][0]["message"]["content"]

        st.success("✅ Question Paper Generated Successfully")

        st.markdown("## 📄 Generated Question Paper")
        st.markdown(
            f"<div class='output-box'>{question_paper}</div>",
            unsafe_allow_html=True
        )

# ---------------- FOOTER ----------------
st.markdown(
    "<div class='footer'>🚀 Built with Streamlit + Together.ai (Mixtral)</div>",
    unsafe_allow_html=True
)
