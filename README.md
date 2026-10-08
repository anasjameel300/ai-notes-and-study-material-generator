# 🎓 AI Assignment & Study Material Generator

A production-ready academic curriculum and assignment suite designed for educators, professors, and students. The system generates syllabus-standard study modules, unified assignment sheets with on-demand solutions, interactive flashcards, visual mind trees, and timed exam-mode practice quizzes.

---

## 📌 Core Modules

### 1. 📖 Comprehensive Study Material
- **Course Learning Outcomes (CLOs)**: Mapped to Bloom's Revised Taxonomy verbs.
- **Formal Definitions & Technical Glossary**: Exam-standard definitions with mathematical notations.
- **In-Depth Conceptual Breakdown**: Architectural walkthroughs, state models, queue diagrams.
- **Real-World Intuitive Analogies**: Concrete mappings connecting abstract concepts to intuitive everyday systems (e.g., Michelin Head Chef kitchen for CPU scheduling).
- **Practical Implementation**: Production-grade POSIX C and real-world system calls (`fork()`, `exec()`, `wait()`).
- **Exam Revision Cheat-Sheet**: High-yield takeaways and common semester exam traps.

### 2. 🌳 Mind Tree (Hierarchical Concept Map)
- Visual top-down concept tree using **Mermaid diagram syntax**.
- Breaks down the unit into Core Concepts, State Transitions, Kernel PCB Architecture, CPU Scheduling, and POSIX Implementation.

### 3. 🗂️ Interactive Study Flashcards
- High-yield flashcard deck extracted automatically from definitions, analogies, and system calls.
- Interactive **"Flip Card"** animation with progress tracker (`Card X of Y`).

### 4. 📝 Unified Assignment Sheet (Questions & Answers)
- **Section A**: Multiple Choice Questions (with on-demand `💡 Show Answer & Explanation` expander).
- **Section B**: Short-Answer Conceptual Questions (with on-demand `💡 Show Model Answer Outline` expander).
- **Section C**: University Long-Answer & Design Questions (with on-demand `💡 Show Solution Blueprint & Marking Rubric` expander).
- **Export Options**: Download clean unsolved question paper or full solutions master key in Markdown (`.md`).

### 5. 🎯 Practice Quiz (30-Minute Timed Exam Mode)
- **Exam Simulator**: Real-time JavaScript countdown timer (configurable to 15, 30, 45, or 60 minutes).
- **Blind Submission**: Answers and explanations remain hidden while taking the exam.
- **Automated Grading**: Instant score calculation, accuracy percentage, and question-by-question review with explanations upon clicking **"Submit Answers"**.

### 6. 🔬 Background Prompt Engineering (Evaluation Mode)
- Built on persona prompting, audience calibration, and cognitive scaffolding.
- Optional toggle: **"Include Naive Prompt Comparison"** compares the output with a naive baseline prompt (`"Explain Operating System"`).

---

## 🛠️ Multi-Provider API Setup

Provide any **ONE** of the following in your `.env` file or directly in the sidebar:
```env
# 1. Google Gemini API (Recommended free tier)
GEMINI_API_KEY=your_gemini_api_key_here

# 2. OpenRouter API (Claude, Llama 3, DeepSeek, GPT-4o)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# 3. OpenAI API (GPT-4o, GPT-4o-mini)
OPENAI_API_KEY=your_openai_api_key_here
```

*(Note: If no API key is provided, the application runs seamlessly in **High-Fidelity Offline Engine** mode).*

---

## 🚀 Running the Project
```powershell
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.
