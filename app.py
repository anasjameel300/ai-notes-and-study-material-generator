"""
AI Assignment & Study Material Generator
A production-grade academic curriculum and assignment suite powered by Prompt Engineering.
Supports Google Gemini, OpenRouter, and OpenAI APIs, plus Interactive Flashcards,
Mermaid Mind Trees, and exam-mode Practice Quizzes.
"""

import os
import streamlit as st
from prompts import (
    build_study_material_prompt,
    build_assignment_prompt,
    get_naive_generic_prompt,
    get_prompt_engineering_breakdown
)
from llm_service import LLMService
from quiz_engine import parse_mcqs
from study_helpers import (
    extract_flashcards_from_study_material,
    generate_mind_tree_mermaid
)

# Page Configuration
st.set_page_config(
    page_title="AI Assignment & Study Material Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_file = os.path.join(os.path.dirname(__file__), "static", "style.css")
if os.path.exists(css_file):
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State Initialization
if "study_content" not in st.session_state:
    st.session_state.study_content = None
if "assignment_content" not in st.session_state:
    st.session_state.assignment_content = None
if "naive_content" not in st.session_state:
    st.session_state.naive_content = None
if "active_topic" not in st.session_state:
    st.session_state.active_topic = "Operating System"
if "active_unit" not in st.session_state:
    st.session_state.active_unit = "Process Management"
if "active_level" not in st.session_state:
    st.session_state.active_level = "B.Tech"
if "flashcard_idx" not in st.session_state:
    st.session_state.flashcard_idx = 0
if "flashcard_flipped" not in st.session_state:
    st.session_state.flashcard_flipped = False
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# Sidebar: Multi-Provider LLM Configuration
with st.sidebar:
    st.markdown("### ⚙️ Multi-Provider LLM Engine")
    
    provider_choice = st.selectbox(
        "AI Provider:",
        ["Auto-Detect / Offline Engine", "Google Gemini", "OpenRouter", "OpenAI"],
        index=0
    )

    # Provider defaults & key loading
    env_gemini = os.getenv("GEMINI_API_KEY", "")
    env_openrouter = os.getenv("OPENROUTER_API_KEY", "")
    env_openai = os.getenv("OPENAI_API_KEY", "")

    if provider_choice == "Google Gemini":
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            value=env_gemini,
            help="Get from https://aistudio.google.com/app/apikey"
        )
        model_options = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]
        selected_model = st.selectbox("Gemini Model", model_options, index=0)

    elif provider_choice == "OpenRouter":
        api_key_input = st.text_input(
            "OpenRouter API Key",
            type="password",
            value=env_openrouter,
            help="Get from https://openrouter.ai/keys"
        )
        model_options = [
            "openai/gpt-4o-mini",
            "deepseek/deepseek-chat",
            "meta-llama/llama-3.3-70b-instruct",
            "anthropic/claude-3.5-sonnet"
        ]
        selected_model = st.selectbox("OpenRouter Model", model_options, index=0)

    elif provider_choice == "OpenAI":
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            value=env_openai,
            help="Get from https://platform.openai.com/api-keys"
        )
        model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
        selected_model = st.selectbox("OpenAI Model", model_options, index=0)

    else:
        # Auto Detect
        api_key_input = ""
        selected_model = "Academic Engine"

    # Status indicator
    if api_key_input and len(api_key_input.strip()) > 8:
        st.success(f"🟢 Active: {provider_choice} ({selected_model})")
    else:
        st.info("💡 High-Fidelity Academic Engine (Offline / Demo Ready)")

    st.markdown("---")
    st.markdown("### 📚 Quick Course Presets")
    selected_preset = st.selectbox(
        "Load Syllabus Template:",
        [
            "Operating Systems (Process Management)",
            "Database Management (Normalization & SQL)",
            "Computer Networks (Transport Layer & TCP)",
            "Data Structures (Binary Search Trees)"
        ]
    )

    preset_details = {
        "Operating Systems (Process Management)": {
            "topic": "Operating System",
            "unit": "Process Management",
            "level": "B.Tech",
            "focus": "Process States, Process Control Block (PCB), Context Switching, fork()/exec()"
        },
        "Database Management (Normalization & SQL)": {
            "topic": "Database Management Systems",
            "unit": "Relational Normalization",
            "level": "B.Tech",
            "focus": "Functional Dependencies, 1NF, 2NF, 3NF, BCNF, Lossless Joins"
        },
        "Computer Networks (Transport Layer & TCP)": {
            "topic": "Computer Networks",
            "unit": "Transport Layer Protocols",
            "level": "B.Tech",
            "focus": "TCP 3-Way Handshake, Flow Control (Sliding Window), Congestion Control, UDP"
        },
        "Data Structures (Binary Search Trees)": {
            "topic": "Data Structures & Algorithms",
            "unit": "Binary Search Trees & Self-Balancing Trees",
            "level": "B.Tech",
            "focus": "BST Invariant, In-order Traversal, Deletion cases, AVL Rotations"
        }
    }
    
    preset_data = preset_details[selected_preset]

# Main Application Banner
st.markdown("""
<div class="app-header">
    <div class="tagline">University Curriculum, Flashcards & Assessment Suite</div>
    <h1>AI Assignment & Study Material Generator</h1>
    <p>Generate comprehensive academic lecture modules, student assignments, interactive flashcards, and concept mind trees.</p>
</div>
""", unsafe_allow_html=True)

# 1. Input Parameters
st.markdown("### 📋 1. Course & Curriculum Specifications")
col1, col2, col3 = st.columns([1.5, 1, 1.5])

with col1:
    course_topic = st.text_input("Course / Subject Title", value=preset_data["topic"])
with col2:
    academic_level = st.selectbox(
        "Academic Level",
        ["B.Tech (Undergraduate)", "M.Tech / Postgraduate", "BCA / BSc Computer Science", "Diploma in Engineering", "High School"],
        index=0
    )
with col3:
    unit_name = st.text_input("Unit / Module Title", value=preset_data["unit"])

focus_areas = st.text_input(
    "Key Subtopics & Core Focus Areas (Optional)",
    value=preset_data["focus"],
    help="Add key concepts you want explicitly covered in the study material and questions."
)

col_gen1, col_gen2 = st.columns([2, 1])
with col_gen1:
    gen_mode = st.radio(
        "Output Generation Mode:",
        [
            "📦 Complete Course Pack (Study Material + Full Assignment + Helpers)",
            "📖 Comprehensive Study Material Only",
            "📝 Assignment & Question Bank Only"
        ],
        horizontal=True
    )
with col_gen2:
    compare_naive = st.checkbox(
        "🔬 Include Naive Prompt Comparison (Demonstrate Prompt Engineering)",
        value=False,
        help="Generates an un-engineered baseline to showcase how prompt engineering elevates academic output."
    )

# Generation Action
generate_button = st.button("🚀 Generate Academic Material & Study Pack", type="primary", use_container_width=True)

if generate_button:
    # Reset quiz state
    st.session_state.quiz_submitted = False
    st.session_state.quiz_answers = {}
    st.session_state.flashcard_idx = 0
    st.session_state.flashcard_flipped = False

    llm = LLMService(
        provider=provider_choice if provider_choice != "Auto-Detect / Offline Engine" else "auto",
        api_key=api_key_input,
        model=selected_model if provider_choice != "Auto-Detect / Offline Engine" else None
    )

    st.session_state.active_topic = course_topic
    st.session_state.active_unit = unit_name
    st.session_state.active_level = academic_level

    with st.spinner(f"Generating university-grade curriculum for '{unit_name}' in {course_topic}..."):
        if "Complete Course Pack" in gen_mode:
            study_prompt = build_study_material_prompt(course_topic, academic_level, unit_name)
            assign_prompt = build_assignment_prompt(course_topic, academic_level, unit_name)
            
            study_res = llm.generate(study_prompt)
            assign_res = llm.generate(assign_prompt)
            
            st.session_state.study_content = study_res["content"]
            st.session_state.assignment_content = assign_res["content"]
            
        elif "Study Material Only" in gen_mode:
            study_prompt = build_study_material_prompt(course_topic, academic_level, unit_name)
            study_res = llm.generate(study_prompt)
            st.session_state.study_content = study_res["content"]
            st.session_state.assignment_content = None
            
        else:
            assign_prompt = build_assignment_prompt(course_topic, academic_level, unit_name)
            assign_res = llm.generate(assign_prompt)
            st.session_state.assignment_content = assign_res["content"]
            st.session_state.study_content = None

        if compare_naive:
            naive_prompt = get_naive_generic_prompt(course_topic, unit_name, academic_level)
            naive_res = llm.generate(naive_prompt)
            st.session_state.naive_content = naive_res["content"]
        else:
            st.session_state.naive_content = None

    st.success("Curriculum & Study Pack generated successfully!")

# 2. Display Academic Hub
if st.session_state.study_content or st.session_state.assignment_content:
    st.markdown("---")
    st.markdown(f"### 📂 Academic Study Pack: {st.session_state.active_unit} ({st.session_state.active_level})")

    tabs_to_show = []
    if st.session_state.study_content:
        tabs_to_show.append("📖 Study Material")
        tabs_to_show.append("🌳 Mind Tree (Concept Map)")
        tabs_to_show.append("🗂️ Interactive Flashcards")
    if st.session_state.assignment_content:
        tabs_to_show.append("📝 Student Assignment Sheet")
        tabs_to_show.append("🧑‍🏫 Solutions & Grading Rubric")
        tabs_to_show.append("🎯 Practice Quiz (Exam Mode)")
    if st.session_state.naive_content:
        tabs_to_show.append("🔬 Prompt Engineering Comparison")

    rendered_tabs = st.tabs(tabs_to_show)
    tab_index = 0

    # TAB: Study Material
    if st.session_state.study_content and "📖 Study Material" in tabs_to_show:
        with rendered_tabs[tab_index]:
            c_head1, c_head2 = st.columns([3, 1])
            with c_head1:
                st.markdown(f"#### 📖 Lecture Notes & Core Theory: {st.session_state.active_unit}")
                st.caption(f"Structured syllabus module for {st.session_state.active_level} students.")
            with c_head2:
                st.download_button(
                    label="📥 Download Study Notes (.md)",
                    data=st.session_state.study_content,
                    file_name=f"{st.session_state.active_topic}_{st.session_state.active_unit}_StudyNotes.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            st.markdown(st.session_state.study_content)
        tab_index += 1

    # TAB: Mind Tree (Concept Map)
    if st.session_state.study_content and "🌳 Mind Tree (Concept Map)" in tabs_to_show:
        with rendered_tabs[tab_index]:
            st.markdown("#### 🌳 Visual Mind Tree & Hierarchical Concept Map")
            st.caption("A top-down architectural decomposition of this unit's key topics, states, and mechanisms.")
            
            mermaid_diagram = generate_mind_tree_mermaid(
                st.session_state.active_topic,
                st.session_state.active_unit
            )

            st.markdown(f"```mermaid\n{mermaid_diagram}\n```")
            
            with st.expander("📋 View Mermaid Code / Raw Architecture", expanded=False):
                st.code(mermaid_diagram, language="mermaid")
        tab_index += 1

    # TAB: Interactive Flashcards
    if st.session_state.study_content and "🗂️ Interactive Flashcards" in tabs_to_show:
        with rendered_tabs[tab_index]:
            st.markdown("#### 🗂️ Interactive Flashcard Deck")
            st.caption("Test your quick recall on core terminology, system calls, and real-world analogies.")

            cards = extract_flashcards_from_study_material(
                st.session_state.study_content,
                st.session_state.active_unit
            )

            total_cards = len(cards)
            current_card_idx = st.session_state.flashcard_idx % total_cards
            active_card = cards[current_card_idx]

            st.markdown(f"**Card {current_card_idx + 1} of {total_cards}**")
            st.progress((current_card_idx + 1) / total_cards)

            # Flashcard Display Box
            card_html = f"""
            <div class="flashcard-box">
                <div class="flashcard-badge">{active_card.get('category', 'Concept')}</div>
                <div class="flashcard-content">{active_card['front']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            # Flip / Show Answer
            fc_col1, fc_col2, fc_col3 = st.columns([1, 1, 1])
            with fc_col1:
                if st.button("⬅️ Previous Card", use_container_width=True):
                    st.session_state.flashcard_idx = (st.session_state.flashcard_idx - 1) % total_cards
                    st.session_state.flashcard_flipped = False
                    st.rerun()

            with fc_col2:
                flip_label = "🙈 Hide Answer" if st.session_state.flashcard_flipped else "💡 Flip Card (Show Answer)"
                if st.button(flip_label, type="primary", use_container_width=True):
                    st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
                    st.rerun()

            with fc_col3:
                if st.button("➡️ Next Card", use_container_width=True):
                    st.session_state.flashcard_idx = (st.session_state.flashcard_idx + 1) % total_cards
                    st.session_state.flashcard_flipped = False
                    st.rerun()

            if st.session_state.flashcard_flipped:
                st.markdown(f"""
                <div class="flashcard-answer">
                    <strong>Answer / Key Concept:</strong><br>
                    {active_card['back']}
                </div>
                """, unsafe_allow_html=True)
        tab_index += 1

    # TAB: Student Assignment Sheet
    if st.session_state.assignment_content and "📝 Student Assignment Sheet" in tabs_to_show:
        with rendered_tabs[tab_index]:
            c_as1, c_as2 = st.columns([3, 1])
            with c_as1:
                st.markdown(f"#### 📝 Assignment Paper: {st.session_state.active_unit}")
                st.caption("Clean printable format for distribution to students (answers hidden).")
            with c_as2:
                import re
                clean_student_sheet = re.sub(r"\*\*Correct Answer\*\*:[^\n]*\n", "", st.session_state.assignment_content)
                clean_student_sheet = re.sub(r"\*\*Explanation\*\*:[^\n]*\n", "", clean_student_sheet)
                clean_student_sheet = re.sub(r"-\s*\*\*Model Answer Outline[^\n]*\n(?:[ \t]*-[^\n]*\n)*", "", clean_student_sheet)
                clean_student_sheet = re.sub(r"-\s*\*\*Detailed Solution Blueprint[^\n]*\n(?:[ \t]*-[^\n]*\n)*", "", clean_student_sheet)

                st.download_button(
                    label="📥 Download Student Assignment (.md)",
                    data=clean_student_sheet,
                    file_name=f"{st.session_state.active_topic}_{st.session_state.active_unit}_Assignment_Paper.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            parsed_mcqs = parse_mcqs(st.session_state.assignment_content)
            
            st.markdown("### SECTION A: Multiple Choice Questions")
            for mcq in parsed_mcqs:
                st.markdown(f"""
                <div class="question-container">
                    <strong>Q{mcq['number']}. {mcq['stem']}</strong><br><br>
                    A) {mcq['options']['A']}<br>
                    B) {mcq['options']['B']}<br>
                    C) {mcq['options']['C']}<br>
                    D) {mcq['options']['D']}
                </div>
                """, unsafe_allow_html=True)

            raw_text = st.session_state.assignment_content
            if "## SECTION B:" in raw_text:
                sec_b_part = raw_text.split("## SECTION B:")[1]
                if "## SECTION C:" in sec_b_part:
                    sec_b_clean, sec_c_clean = sec_b_part.split("## SECTION C:")
                else:
                    sec_b_clean = sec_b_part
                    sec_c_clean = ""
                
                st.markdown("### SECTION B: Short-Answer Conceptual Questions (3-5 Marks Each)")
                sec_b_display = re.sub(r"-\s*\*\*Model Answer Outline.*?(?=(?:### Question|\Z))", "", sec_b_clean, flags=re.DOTALL)
                st.markdown(sec_b_display)

                if sec_c_clean:
                    st.markdown("### SECTION C: University Long-Answer & Design Questions (10-15 Marks Each)")
                    sec_c_display = re.sub(r"-\s*\*\*Solution Blueprint.*?(?=(?:### Question|\Z))", "", sec_c_clean, flags=re.DOTALL)
                    st.markdown(sec_c_display)
        tab_index += 1

    # TAB: Teacher's Guide & Solutions
    if st.session_state.assignment_content and "🧑‍🏫 Solutions & Grading Rubric" in tabs_to_show:
        with rendered_tabs[tab_index]:
            c_sol1, c_sol2 = st.columns([3, 1])
            with c_sol1:
                st.markdown("#### 🧑‍🏫 Master Solution Key & Evaluation Rubrics")
                st.caption("Confidential marking guidelines, MCQ explanations, and long-answer mark breakdowns.")
            with c_sol2:
                st.download_button(
                    label="📥 Download Teacher Solutions (.md)",
                    data=st.session_state.assignment_content,
                    file_name=f"{st.session_state.active_topic}_{st.session_state.active_unit}_Teacher_Solutions.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            st.markdown(st.session_state.assignment_content)
        tab_index += 1

    # TAB: Practice Quiz (Exam Mode - Answers ONLY revealed after filling and submitting)
    if st.session_state.assignment_content and "🎯 Practice Quiz (Exam Mode)" in tabs_to_show:
        with rendered_tabs[tab_index]:
            st.markdown("#### 🎯 Interactive Practice Quiz (Exam Mode)")
            st.caption("Fill in your answers below. Explanations and correct answers will ONLY be revealed after you submit!")

            parsed_mcqs = parse_mcqs(st.session_state.assignment_content)
            if not parsed_mcqs:
                st.info("No parsed MCQs available in this question bank.")
            else:
                total_mcqs = len(parsed_mcqs)

                # Form for taking the test
                with st.form("exam_quiz_form"):
                    user_selections = {}
                    for mcq in parsed_mcqs:
                        q_num = mcq["number"]
                        st.markdown(f"**Question {q_num}: {mcq['stem']}**")
                        
                        options = [
                            f"A) {mcq['options']['A']}",
                            f"B) {mcq['options']['B']}",
                            f"C) {mcq['options']['C']}",
                            f"D) {mcq['options']['D']}"
                        ]
                        
                        selected = st.radio(
                            f"Select answer for Q{q_num}:",
                            options=options,
                            index=None,
                            key=f"exam_q_{q_num}",
                            disabled=st.session_state.quiz_submitted
                        )
                        user_selections[q_num] = selected
                        st.markdown("---")

                    submit_quiz = st.form_submit_button(
                        "📝 Submit Answers & Check Score" if not st.session_state.quiz_submitted else "Already Submitted",
                        type="primary",
                        disabled=st.session_state.quiz_submitted
                    )

                if submit_quiz:
                    st.session_state.quiz_submitted = True
                    st.session_state.quiz_answers = user_selections
                    st.rerun()

                # Results Display (ONLY shown after quiz is submitted)
                if st.session_state.quiz_submitted:
                    score = 0
                    for mcq in parsed_mcqs:
                        q_num = mcq["number"]
                        ans = st.session_state.quiz_answers.get(q_num)
                        picked_letter = ans[0] if ans else None
                        if picked_letter == mcq["correct_answer"]:
                            score += 1

                    # Score Summary
                    pct = int((score / total_mcqs) * 100)
                    st.markdown("### 📊 Quiz Results & Performance Analysis")
                    c_sc1, c_sc2 = st.columns([1, 2])
                    with c_sc1:
                        st.metric("Final Score", f"{score} / {total_mcqs}", delta=f"{pct}% Score")
                    with c_sc2:
                        if pct >= 80:
                            st.success("🌟 Outstanding Mastery! Excellent conceptual understanding.")
                        elif pct >= 60:
                            st.warning("👍 Good Attempt! Review the detailed explanations below to polish weak spots.")
                        else:
                            st.error("⚠️ Needs Review. Study the concepts in the Study Material tab before re-attempting.")

                    st.markdown("---")
                    st.markdown("#### 🔍 Question-by-Question Detailed Review")

                    for mcq in parsed_mcqs:
                        q_num = mcq["number"]
                        ans = st.session_state.quiz_answers.get(q_num)
                        picked_letter = ans[0] if ans else "Unanswered"
                        is_correct = (picked_letter == mcq["correct_answer"])

                        status_pill = (
                            f'<span class="quiz-pill-correct">✅ Correct (You picked {picked_letter})</span>' 
                            if is_correct 
                            else f'<span class="quiz-pill-incorrect">❌ Incorrect (You picked: {picked_letter} | Correct: {mcq["correct_answer"]})</span>'
                        )

                        st.markdown(f"**Q{q_num}. {mcq['stem']}** &nbsp; {status_pill}", unsafe_allow_html=True)
                        st.markdown(f"- A) {mcq['options']['A']}")
                        st.markdown(f"- B) {mcq['options']['B']}")
                        st.markdown(f"- C) {mcq['options']['C']}")
                        st.markdown(f"- D) {mcq['options']['D']}")

                        if mcq["explanation"]:
                            st.info(f"💡 **Explanation & Learning Key**: {mcq['explanation']}")
                        st.markdown("---")

                    if st.button("🔄 Retake Quiz", use_container_width=True):
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        st.rerun()
        tab_index += 1

    # TAB: Prompt Engineering Comparison
    if st.session_state.naive_content and "🔬 Prompt Engineering Comparison" in tabs_to_show:
        with rendered_tabs[tab_index]:
            st.markdown("#### 🔬 Prompt Engineering Comparative Evaluation")
            st.markdown(
                "This evaluation analyzes the difference between a **Naive / Generic Prompt** "
                "and the **Engineered Prompt** powering this generator."
            )

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown("##### ⚠️ Baseline: Naive Generic Prompt")
                st.caption(f"Prompt Sent: `{get_naive_generic_prompt(st.session_state.active_topic, st.session_state.active_unit, st.session_state.active_level)}`")
                st.markdown(st.session_state.naive_content)
                
            with col_p2:
                st.markdown("##### ✨ Production: Engineered Prompt Result")
                st.caption("Prompt Applied: Persona + Bloom's Taxonomy + Strict Modular Schema")
                summary_preview = (st.session_state.study_content or st.session_state.assignment_content)[:1200]
                st.markdown(summary_preview + "\n\n*(Full content available in dedicated tabs)*")

            st.markdown("---")
            st.markdown("##### 🔍 Why the Engineered Prompt Produces Superior Results:")
            breakdown = get_prompt_engineering_breakdown()
            for b in breakdown:
                with st.expander(f"**{b['technique']}**", expanded=False):
                    st.markdown(f"**How it is applied:** {b['implementation']}")
                    st.markdown(f"**Why it matters in curriculum design:** {b['why_it_matters']}")
        tab_index += 1
