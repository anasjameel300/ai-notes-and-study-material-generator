# 🎓 AI Assignment & Study Material Generator

A production-ready academic curriculum and assignment suite designed for educators, professors, and students. The system generates syllabus-standard study modules, student assignment papers, teacher solution rubrics, and interactive self-assessment quizzes from any course topic.

---

## 📌 Core Capabilities

### 1. 📖 Comprehensive Study Material Module
- **Introduction & Learning Outcomes**: 4-5 measurable Course Learning Outcomes (CLOs) mapped to Bloom's Revised Taxonomy verbs.
- **Core Definitions & Technical Glossary**: Syllabus-standard technical definitions with mathematical and formal notations.
- **In-Depth Conceptual Breakdown**: Architectural walkthroughs, state models, queue diagrams, and performance trade-offs.
- **Real-World Intuitive Analogies**: Concrete mappings connecting abstract technical concepts to intuitive everyday systems (e.g., Michelin Head Chef kitchen for CPU scheduling).
- **Practical Implementation**: Production-grade POSIX C and real-world system calls (`fork()`, `exec()`, `wait()`).
- **Exam Revision Cheat-Sheet**: High-yield takeaways and common semester exam traps.

### 2. 📝 Student Assignment Sheet
- Clean, classroom-ready format designed for direct student distribution.
- **Section A**: Multiple Choice Questions (with problem stems and choices, without revealing answers).
- **Section B**: Short-Answer Conceptual Questions (with assigned marks).
- **Section C**: University Long-Answer & Design Questions (10-15 marks each).
- **Download**: One-click export to Markdown (`.md`).

### 3. 🧑‍🏫 Teacher Solutions & Grading Rubrics
- Comprehensive evaluation guide for instructors and examiners.
- Detailed rationale for correct MCQ options and common misconceptions for wrong distractors.
- Model answer outlines for conceptual short questions.
- Step-by-step marking schemes and diagram requirements for university long-answer questions.

### 4. 🎯 Interactive Practice Quiz
- Allows students to self-test directly in the web application.
- Instant automated scoring, accuracy percentages, and in-depth conceptual explanations.

### 5. 🔬 Background Prompt Engineering (Evaluation Mode)
- Built with a prompt engineering architecture: Role Prompting, Audience Calibration, Structural Schemas, and Bloom's Cognitive Scaffolding.
- Optional toggle: **"Include Naive Prompt Comparison"** lets students and evaluators contrast the production output against a baseline naive prompt (`"Explain Operating System"`).

---

## 🚀 Getting Started

### 1. Installation
Navigate to the project folder:
```powershell
cd "c:\Users\anasjameel\Desktop\local notebook"
```

Install requirements:
```powershell
pip install -r requirements.txt
```

### 2. Launching the App
Start the Streamlit application:
```powershell
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your web browser.

### 3. API Key Configuration (Optional)
- **Live Mode**: Enter your OpenAI API key in the sidebar to generate custom material on any topic.
- **High-Fidelity Offline Engine**: Works out-of-the-box with comprehensive curriculum presets (Operating Systems, DBMS, Computer Networks, Data Structures) for testing and viva presentation without requiring an API key.

---

## 📂 Project Structure
```
local notebook/
├── app.py                   # Main Streamlit academic application
├── prompts.py               # Prompt engineering templates & curriculum builders
├── llm_service.py           # LLM service with live OpenAI API and offline knowledge engine
├── quiz_engine.py           # MCQ parser and interactive quiz state evaluator
├── static/
│   └── style.css            # Custom CSS for academic cards, badges, and clean layout
├── requirements.txt         # Project dependencies
├── .env.example             # Environment template
└── README.md                # Project documentation
```
