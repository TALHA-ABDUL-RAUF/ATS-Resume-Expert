# 🎯 ATS Resume Expert

<div align="center">

### AI-Powered Resume Analysis using Google Gemini 2.5 Flash

Analyze resumes against job descriptions with AI-generated ATS scores, recruiter feedback, and personalized improvement suggestions.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge\&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge\&logo=streamlit)
![Google Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-4285F4?style=for-the-badge\&logo=google)
![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)

</div>

---

# 📌 Overview

ATS Resume Expert is an AI-powered web application that helps job seekers evaluate how well their resume matches a target job description.

The application leverages **Google Gemini 2.5 Flash** to perform intelligent resume analysis by comparing an uploaded resume with a job description and generating structured recruiter-style feedback.

The system provides:

* 📊 ATS Match Score
* 🔍 Missing Keywords Detection
* 👨‍💼 HR-style Resume Review
* 💡 Personalized Resume Improvement Suggestions

---

# ✨ Features

* 📄 Upload Resume (PDF)
* 📝 Paste Job Description
* 📊 ATS Compatibility Analysis
* 🔍 Missing Keywords Detection
* 💡 Resume Improvement Suggestions
* 👨‍💼 Recruiter-style Resume Review
* ⬇️ Download AI Analysis Report
* 🎨 Modern Streamlit Interface

---

# 🏗 System Architecture

```
                 User

                   │

        Streamlit Web Application

        ┌──────────┴──────────┐

        │                     │

 Job Description         Resume PDF

        │                     │

        └──────────┬──────────┘

                   │

          Input Validation

                   │

         PDF → Image Conversion

                   │

        Google Gemini API

                   │

      AI Resume Intelligence

      ┌────────┼─────────┐

      │        │         │

 ATS Score  Resume Review  Improve Resume

                   │

          Download Report
```

---

# ⚙️ Technology Stack

| Category              | Technology              |
| --------------------- | ----------------------- |
| Programming Language  | Python                  |
| Web Framework         | Streamlit               |
| AI Model              | Google Gemini 2.5 Flash |
| PDF Processing        | pdf2image               |
| Environment Variables | python-dotenv           |
| Styling               | HTML + CSS              |

---

# 📂 Project Structure

```text
ATS-Resume-Expert/

│

├── app.py

├── requirements.txt

├── README.md

├── .env.example

├── .gitignore

│

├── assets/

│   ├── home.png

│   ├── ats_score.png

│   ├── review.png

│   └── improve.png

│

├── sample_data/

│   ├── sample_resume.pdf

│   └── sample_job_description.txt

│

└── docs/

    ├── Project_Documentation.pdf

    └── Model_Documentation.pdf
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/TALHA-ABDUL-RAUF/ATS-Resume-Expert.git
```

Move into the project

```bash
cd ATS-Resume-Expert
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

---

# 📖 Usage

1. Launch the application.
2. Paste the target Job Description.
3. Upload a Resume in PDF format.
4. Select one of the available analyses.
5. View the AI-generated report.
6. Download the report if required.

---

# 📸 Screenshots

## 🏠 Home Page

> Add screenshot

```
assets/home.png
```

---

## 📊 ATS Score

> Add screenshot

```
assets/ats_score.png
```

---

## 👨‍💼 Resume Review

> Add screenshot

```
assets/review.png
```

---

## 💡 Resume Improvement

> Add screenshot

```
assets/improve.png
```

---

# 📈 Future Enhancements

* Multi-page Resume Analysis
* DOCX Resume Support
* Authentication System
* Recruiter Dashboard
* Resume History
* AI Chat Assistant
* PDF Report Export
* Advanced ATS Scoring Algorithm

---

# 🎓 Learning Outcomes

This project demonstrates practical experience with:

* Prompt Engineering
* Google Gemini API
* Streamlit Application Development
* Python Programming
* PDF Processing
* Environment Variable Management
* UI Development
* AI Integration

---

# 👨‍💻 Author

**Talha Abdul Rauf**

Learning Agentic AI Engineer

---

# ⭐ If you found this project useful, consider giving it a Star.
