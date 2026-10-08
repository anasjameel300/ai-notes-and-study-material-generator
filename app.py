"""
AI Assignment & Study Material Generator
A production-grade academic curriculum and assignment suite powered by Prompt Engineering.
Supports:
- Google Gemini (Gemini 2.5 Flash, 2.5 Pro, 2.0 Flash, 1.5 Flash) via official google-genai SDK
- OpenRouter (DeepSeek, Llama 3.3, Claude, GPT-4o)
- OpenAI (GPT-4o, GPT-4o-mini)
- Clean error reporting (no silent fallbacks when an API key is used)
"""

import os
import time
import streamlit as st
from prompts import (
    build_study_material_prompt,
    build_assignment_prompt,
    get_naive_generic_prompt,
    get_prompt_engineering_breakdown
)
from llm_service import LLMService
from quiz_engine import (
    parse_mcqs,
    parse_short_questions,
    parse_long_questions
)
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
if "quiz_start_time" not in st.session_state:
    st.session_state.quiz_start_time = None
if "quiz_duration_mins" not in st.session_state:
    st.session_state.quiz_duration_mins = 30

# Preset Data Map
PRESET_DATA = {
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
        "unit": "Binary Search Trees",
        "level": "B.Tech",
        "focus": "BST Invariant, In-order Traversal, Deletion cases, AVL Rotations"
    }
}

# Sidebar: Multi-Provider LLM Configuration
with st.sidebar:
    st.markdown("### ⚙️ Multi-Provider LLM Engine")
    
    provider_choice = st.selectbox(
        "AI Provider:",
        ["Google Gemini", "OpenRouter", "OpenAI", "Offline Academic Engine"],
        index=0
    )

    env_gemini = os.getenv("GEMINI_API_KEY", "")
    env_openrouter = os.getenv("OPENROUTER_API_KEY", "")
    env_openai = os.getenv("OPENAI_API_KEY", "")

    if provider_choice == "Google Gemini":
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            value=env_gemini,
            placeholder="AIzaSy...",
            help="Get your key at https://aistudio.google.com/app/apikey"
        )
        gemini_model_choice = st.selectbox(
            "Gemini Model Tier",
            [
                "gemini-2.5-flash",
                "gemini-2.5-pro",
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "Custom Model Name..."
            ],
            index=0
        )
        if gemini_model_choice == "Custom Model Name...":
            selected_model = st.text_input("Enter Gemini Model Identifier", value="gemini-2.5-flash")
        else:
            selected_model = gemini_model_choice

    elif provider_choice == "OpenRouter":
        api_key_input = st.text_input(
            "OpenRouter API Key",
            type="password",
            value=env_openrouter,
            placeholder="sk-or-...",
            help="Get your key at https://openrouter.ai/keys"
        )
        openrouter_model_choice = st.selectbox(
            "OpenRouter Model",
            [
                "openai/gpt-4o-mini",
                "deepseek/deepseek-chat",
                "meta-llama/llama-3.3-70b-instruct",
                "anthropic/claude-3.5-sonnet",
                "Custom Model..."
            ],
            index=0
        )
        if openrouter_model_choice == "Custom Model...":
            selected_model = st.text_input("Enter Model ID", value="openai/gpt-4o-mini")
        else:
            selected_model = openrouter_model_choice

    elif provider_choice == "OpenAI":
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            value=env_openai,
            placeholder="sk-...",
            help="Get your key at https://platform.openai.com/api-keys"
        )
        selected_model = st.selectbox("OpenAI Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)

    else:
        api_key_input = ""
        selected_model = "Offline Academic Engine"

    # Status Indicator
    if api_key_input and len(api_key_input.strip()) > 8:
        st.success(f"Connected: {provider_choice} ({selected_model})")
    else:
        st.info("Offline Academic Engine (Local Mode)")

    st.markdown("---")
    st.markdown("### Server Launch Command")
    st.code("streamlit run app.py", language="bash")
    st.caption("Run this in your terminal to start the portal.")

# Main Application Banner
st.markdown("""
<div class="app-header">
    <div class="tagline">Curriculum & Courseware Portal</div>
    <h1>Study Material & Assignment Generator</h1>
    <p>A syllabus-aligned academic platform for lecture modules, assignment sheets, flashcards, and examination test banks.</p>
</div>
""", unsafe_allow_html=True)

# Preset Loader
with st.expander("Syllabus Templates (Click to Pre-fill)", expanded=False):
    preset_choice = st.selectbox("Select a course template:", list(PRESET_DATA.keys()))
    if st.button("Apply Template"):
        p_val = PRESET_DATA[preset_choice]
        st.session_state["f_topic"] = p_val["topic"]
        st.session_state["f_unit"] = p_val["unit"]
        st.session_state["f_focus"] = p_val["focus"]
        st.success(f"Applied template: {preset_choice}")
        st.rerun()

# 1. Input Parameters
st.markdown("### 📋 1. Course & Curriculum Specifications")
col1, col2, col3 = st.columns([1.5, 1, 1.5])

with col1:
    course_topic = st.text_input(
        "Course / Subject Title",
        value=st.session_state.get("f_topic", "AI and ML"),
        key="input_course_topic",
        placeholder="e.g. AI and ML, Operating Systems, Database Management"
    )
with col2:
    academic_level = st.selectbox(
        "Academic Level",
        ["B.Tech (Undergraduate)", "M.Tech / Postgraduate", "BCA / BSc Computer Science", "Diploma in Engineering", "High School"],
        index=0
    )
with col3:
    unit_name = st.text_input(
        "Unit / Module Title",
        value=st.session_state.get("f_unit", "Deep Learning & Foundation Models"),
        key="input_unit_name",
        placeholder="e.g. Deep Learning Architectures, Neural Networks, Process Management"
    )

focus_areas = st.text_input(
    "Key Subtopics & Core Focus Areas (Mandatory for custom topics)",
    value=st.session_state.get("f_focus", "LLM, LVM, CNN, RNN and ML"),
    key="input_focus_areas",
    placeholder="e.g. LLM, LVM, CNN, RNN, Transformers, Loss Functions"
)

col_gen1, col_gen2 = st.columns([2, 1])
with col_gen1:
    gen_mode = st.radio(
        "Output Generation Mode:",
        [
            "📦 Complete Course Pack (Study Material + Assignment & Exam + Helpers)",
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
    st.session_state.quiz_submitted = False
    st.session_state.quiz_answers = {}
    st.session_state.flashcard_idx = 0
    st.session_state.flashcard_flipped = False
    st.session_state.quiz_start_time = time.time()

    # Smart guard: If user changed topic to AI/ML or another topic, but left unit as Process Management, adapt it!
    effective_unit = unit_name.strip()
    if not effective_unit or ("process management" in effective_unit.lower() and "operat" not in course_topic.lower() and "os" not in course_topic.lower()):
        effective_unit = "Deep Learning & Foundation Models" if ("ai" in course_topic.lower() or "ml" in course_topic.lower()) else (focus_areas.split(",")[0].strip() or "Core Foundations")

    llm = LLMService(
        provider=provider_choice,
        api_key=api_key_input,
        model=selected_model
    )

    st.session_state.active_topic = course_topic
    st.session_state.active_unit = effective_unit
    st.session_state.active_level = academic_level

    generation_failed = False

    with st.spinner(f"Querying {provider_choice} ({selected_model}) for '{course_topic}: {effective_unit}' (Focus: {focus_areas})..."):
        if "Complete Course Pack" in gen_mode:
            study_prompt = build_study_material_prompt(course_topic, academic_level, effective_unit, focus_areas)
            assign_prompt = build_assignment_prompt(course_topic, academic_level, effective_unit, focus_areas)
            
            study_res = llm.generate(study_prompt)
            if not study_res["success"]:
                st.error(f"❌ {study_res['error']}")
                generation_failed = True
            else:
                st.session_state.study_content = study_res["content"]
                
                assign_res = llm.generate(assign_prompt)
                if not assign_res["success"]:
                    st.error(f"❌ {assign_res['error']}")
                    generation_failed = True
                else:
                    st.session_state.assignment_content = assign_res["content"]
            
        elif "Study Material Only" in gen_mode:
            study_prompt = build_study_material_prompt(course_topic, academic_level, effective_unit, focus_areas)
            study_res = llm.generate(study_prompt)
            if not study_res["success"]:
                st.error(f"❌ {study_res['error']}")
                generation_failed = True
            else:
                st.session_state.study_content = study_res["content"]
                st.session_state.assignment_content = None
            
        else:
            assign_prompt = build_assignment_prompt(course_topic, academic_level, effective_unit, focus_areas)
            assign_res = llm.generate(assign_prompt)
            if not assign_res["success"]:
                st.error(f"❌ {assign_res['error']}")
                generation_failed = True
            else:
                st.session_state.assignment_content = assign_res["content"]
                st.session_state.study_content = None

        if compare_naive and not generation_failed:
            naive_prompt = get_naive_generic_prompt(course_topic, effective_unit, academic_level, focus_areas)
            naive_res = llm.generate(naive_prompt)
            if naive_res["success"]:
                st.session_state.naive_content = naive_res["content"]
        else:
            st.session_state.naive_content = None

    if not generation_failed:
        st.success(f"Curriculum generated successfully using {provider_choice} ({selected_model})!")

# 2. Display Academic Hub
if st.session_state.study_content or st.session_state.assignment_content:
    st.markdown("---")
    st.markdown(f"### 📂 Academic Study Pack: {st.session_state.active_unit} ({st.session_state.active_level})")

    tabs_to_show = []
    if st.session_state.study_content:
        tabs_to_show.append("Lecture Notes")
        tabs_to_show.append("Concept Mind Map")
        tabs_to_show.append("Study Flashcards")
    if st.session_state.assignment_content:
        tabs_to_show.append("Assignment & Question Bank")
        tabs_to_show.append("Timed Examination (30 Min)")
    if st.session_state.naive_content:
        tabs_to_show.append("Prompt Engineering Comparison")

    rendered_tabs = st.tabs(tabs_to_show)
    tab_index = 0

    # TAB: Study Material
    if st.session_state.study_content and "Lecture Notes" in tabs_to_show:
        with rendered_tabs[tab_index]:
            c_head1, c_head2 = st.columns([3, 1])
            with c_head1:
                st.markdown(f"#### 📖 Lecture Notes & Core Theory: {st.session_state.active_unit}")
                st.caption(f"Course: {st.session_state.active_topic} | Level: {st.session_state.active_level}")
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
    if st.session_state.study_content and "Concept Mind Map" in tabs_to_show:
        with rendered_tabs[tab_index]:
            st.markdown(f"#### Concept Mind Map: {st.session_state.active_unit}")
            st.caption(f"Hierarchical concept map for {st.session_state.active_topic}.")
            
            mermaid_diagram = generate_mind_tree_mermaid(
                st.session_state.active_topic,
                st.session_state.active_unit
            )

            st.markdown(f"```mermaid\n{mermaid_diagram}\n```")
            
            with st.expander("View Diagram Code", expanded=False):
                st.code(mermaid_diagram, language="mermaid")
        tab_index += 1

    # TAB: Interactive Flashcards
    if st.session_state.study_content and "Study Flashcards" in tabs_to_show:
        with rendered_tabs[tab_index]:
            st.markdown(f"#### Study Flashcards: {st.session_state.active_unit}")
            st.caption("Review definitions and key mechanisms.")

            cards = extract_flashcards_from_study_material(
                st.session_state.study_content,
                st.session_state.active_unit
            )

            total_cards = len(cards)
            current_card_idx = st.session_state.flashcard_idx % total_cards
            active_card = cards[current_card_idx]

            st.markdown(f"**Card {current_card_idx + 1} of {total_cards}**")
            st.progress((current_card_idx + 1) / total_cards)

            card_html = f"""
            <div class="flashcard-box">
                <div class="flashcard-badge">{active_card.get('category', 'Concept')}</div>
                <div class="flashcard-content">{active_card['front']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            fc_col1, fc_col2, fc_col3 = st.columns([1, 1, 1])
            with fc_col1:
                if st.button("Previous Card", use_container_width=True):
                    st.session_state.flashcard_idx = (st.session_state.flashcard_idx - 1) % total_cards
                    st.session_state.flashcard_flipped = False
                    st.rerun()

            with fc_col2:
                flip_label = "Hide Answer" if st.session_state.flashcard_flipped else "Show Answer"
                if st.button(flip_label, type="primary", use_container_width=True):
                    st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
                    st.rerun()

            with fc_col3:
                if st.button("Next Card", use_container_width=True):
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

    # TAB: Assignment Sheet (With On-Demand Show Answer)
    if st.session_state.assignment_content and "Assignment & Question Bank" in tabs_to_show:
        with rendered_tabs[tab_index]:
            c_as1, c_as2, c_as3 = st.columns([2, 1, 1])
            with c_as1:
                st.markdown(f"#### Assignment Paper: {st.session_state.active_unit}")
                st.caption("Click 'Show Answer' under any question to inspect solutions and rubrics.")
            with c_as2:
                import re
                clean_student_sheet = re.sub(r"\*\*Correct Answer\*\*:[^\n]*\n", "", st.session_state.assignment_content)
                clean_student_sheet = re.sub(r"\*\*Explanation\*\*:[^\n]*\n", "", clean_student_sheet)
                clean_student_sheet = re.sub(r"-\s*\*\*Model Answer Outline[^\n]*\n(?:[ \t]*-[^\n]*\n)*", "", clean_student_sheet)
                clean_student_sheet = re.sub(r"-\s*\*\*Detailed Solution Blueprint[^\n]*\n(?:[ \t]*-[^\n]*\n)*", "", clean_student_sheet)
                st.download_button(
                    label="Download Questions (.md)",
                    data=clean_student_sheet,
                    file_name=f"{st.session_state.active_topic}_{st.session_state.active_unit}_Questions.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with c_as3:
                st.download_button(
                    label="Download Solutions (.md)",
                    data=st.session_state.assignment_content,
                    file_name=f"{st.session_state.active_topic}_{st.session_state.active_unit}_Full_Solutions.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            st.markdown("---")

            # SECTION A: MCQs with Show Answer
            parsed_mcqs = parse_mcqs(st.session_state.assignment_content)
            st.markdown("### SECTION A: Multiple Choice Questions")
            for mcq in parsed_mcqs:
                q_num = mcq["number"]
                st.markdown(f"""
                <div class="question-container">
                    <strong>Q{q_num}. {mcq['stem']}</strong><br><br>
                    A) {mcq['options']['A']}<br>
                    B) {mcq['options']['B']}<br>
                    C) {mcq['options']['C']}<br>
                    D) {mcq['options']['D']}
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"Show Answer & Explanation (Q{q_num})", expanded=False):
                    st.markdown(f"**Correct Answer:** Option **{mcq['correct_answer']}**")
                    if mcq["explanation"]:
                        st.markdown(f"**Explanation:** {mcq['explanation']}")
                    st.caption(f"Cognitive Level: {mcq.get('bloom_level', 'Understand')}")

            st.markdown("---")

            # SECTION B: Short-Answer with Show Answer
            short_qs = parse_short_questions(st.session_state.assignment_content)
            st.markdown("### SECTION B: Short-Answer Conceptual Questions (3-5 Marks Each)")
            if short_qs:
                for sq in short_qs:
                    s_num = sq["number"]
                    st.markdown(f"**Question {s_num}** <span class='marks-badge'>[{sq['marks']} Marks]</span>", unsafe_allow_html=True)
                    st.markdown(f"> {sq['question']}")
                    
                    with st.expander(f"Show Model Answer (Question {s_num})", expanded=False):
                        if sq["answer"]:
                            st.markdown(sq["answer"])
                        else:
                            st.info("Model answer outline is available in the downloadable full solutions sheet.")
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("Section B questions available in the downloadable full solutions sheet.")

            st.markdown("---")

            # SECTION C: Long-Answer with Show Rubric
            long_qs = parse_long_questions(st.session_state.assignment_content)
            st.markdown("### SECTION C: University Long-Answer & Design Questions (10-15 Marks Each)")
            if long_qs:
                for lq in long_qs:
                    l_num = lq["number"]
                    st.markdown(f"**Question {l_num}** <span class='marks-badge'>[{lq['marks']} Marks]</span>", unsafe_allow_html=True)
                    st.markdown(f"> {lq['question']}")
                    
                    with st.expander(f"Show Evaluation Rubric (Question {l_num})", expanded=False):
                        if lq["rubric"]:
                            st.markdown(lq["rubric"])
                        else:
                            st.info("Evaluation rubric is available in the downloadable full solutions sheet.")
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("Section C long-answer questions available in the downloadable full solutions sheet.")
        tab_index += 1

    # TAB: Practice Quiz (Exam Mode with 30-Minute Timer)
    if st.session_state.assignment_content and "Timed Examination (30 Min)" in tabs_to_show:
        with rendered_tabs[tab_index]:
            st.markdown(f"#### Timed Examination: {st.session_state.active_unit}")
            st.caption("Answers are hidden during the test and will be evaluated upon submission.")

            parsed_mcqs = parse_mcqs(st.session_state.assignment_content)
            if not parsed_mcqs:
                st.info("No parsed MCQs available in this question bank.")
            else:
                total_mcqs = len(parsed_mcqs)

                t_col1, t_col2 = st.columns([1, 2])
                with t_col1:
                    timer_mins = st.selectbox(
                        "Set Exam Duration:",
                        [15, 30, 45, 60],
                        index=1,
                        help="Default is 30 minutes. You can adjust before starting."
                    )
                    st.session_state.quiz_duration_mins = timer_mins

                with t_col2:
                    if st.session_state.quiz_start_time is None:
                        st.session_state.quiz_start_time = time.time()

                    duration_seconds = st.session_state.quiz_duration_mins * 60
                    elapsed_seconds = int(time.time() - st.session_state.quiz_start_time)
                    remaining_seconds = max(0, duration_seconds - elapsed_seconds)

                    rem_mins = remaining_seconds // 60
                    rem_secs = remaining_seconds % 60

                    timer_html = f"""
                    <div class="timer-banner">
                        <div>
                            <strong>⏱️ Exam Timer Active</strong> ({timer_mins} Minutes Total)
                        </div>
                        <div class="timer-digits" id="countdown_clock">
                            {rem_mins:02d}:{rem_secs:02d}
                        </div>
                    </div>
                    <script>
                        var secondsLeft = {remaining_seconds};
                        var clock = document.getElementById('countdown_clock');
                        if (clock && secondsLeft > 0) {{
                            var interval = setInterval(function() {{
                                secondsLeft--;
                                if (secondsLeft <= 0) {{
                                    clearInterval(interval);
                                    clock.innerHTML = "00:00 (Time Up!)";
                                    clock.style.color = "#f87171";
                                }} else {{
                                    var m = Math.floor(secondsLeft / 60);
                                    var s = secondsLeft % 60;
                                    clock.innerHTML = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
                                }}
                            }}, 1000);
                        }}
                    </script>
                    """
                    st.components.v1.html(timer_html, height=75)

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

                if st.session_state.quiz_submitted:
                    score = 0
                    for mcq in parsed_mcqs:
                        q_num = mcq["number"]
                        ans = st.session_state.quiz_answers.get(q_num)
                        picked_letter = ans[0] if ans else None
                        if picked_letter == mcq["correct_answer"]:
                            score += 1

                    pct = int((score / total_mcqs) * 100)
                    st.markdown("### 📊 Exam Results & Performance Analysis")
                    c_sc1, c_sc2 = st.columns([1, 2])
                    with c_sc1:
                        st.metric("Final Score", f"{score} / {total_mcqs}", delta=f"{pct}% Score")
                    with c_sc2:
                        if pct >= 80:
                            st.success("🌟 Outstanding Performance! Excellent conceptual mastery.")
                        elif pct >= 60:
                            st.warning("👍 Good Attempt! Review the detailed explanations below to strengthen weak areas.")
                        else:
                            st.error("⚠️ Needs Revision. Review the Study Material tab before re-attempting.")

                    st.markdown("---")
                    st.markdown("#### 🔍 Question-by-Question Detailed Review")

                    for mcq in parsed_mcqs:
                        q_num = mcq["number"]
                        ans = st.session_state.quiz_answers.get(q_num)
                        picked_letter = ans[0] if ans else "Unanswered"
                        is_correct = (picked_letter == mcq["correct_answer"])

                        status_pill = (
                            f'<span class="quiz-pill-correct">✅ Correct (You picked: {picked_letter})</span>' 
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

                    if st.button("🔄 Retake Exam / Reset Timer", use_container_width=True):
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_start_time = time.time()
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
