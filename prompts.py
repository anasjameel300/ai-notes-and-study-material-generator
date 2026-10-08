"""
Prompt Engineering Core for AI Assignment & Study Material Generator.
Guarantees that user's custom Course Topic, Unit/Module, AND specific Focus Areas
are strictly injected and emphasized in the generation.
"""

from typing import Dict, Any, List

def build_study_material_prompt(topic: str, level: str, unit: str, focus_areas: str = "", depth: str = "High-Yield", **kwargs) -> str:
    """
    Engineered prompt specifically crafted for in-depth, syllabus-standard study material.
    Strictly incorporates topic, unit, and user's specific focus concepts.
    """
    focus_directive = ""
    if focus_areas and focus_areas.strip():
        focus_directive = f"""
PRIMARY FOCUS & MANDATORY TOPICS:
The student/instructor has requested that you EXPLICITLY and THOROUGHLY cover the following concepts, architectures, and models:
👉 {focus_areas.strip()}
Make sure every single one of these concepts is explained with technical depth, architectural diagrams, formulas, and real-world examples!
"""

    pacing_directive = (
        "Pacing & Length: Produce a high-yield, punchy, and rigorous module (approximately 1,500 to 2,000 words total). "
        "Maximize technical density, mathematical clarity, and code quality while avoiding redundant rambling."
        if depth == "High-Yield" else
        "Pacing & Length: Exhaustive, comprehensive university lecture manual (~3,000+ words). Cover every sub-mechanism in granular academic depth."
    )

    return f"""Act as a distinguished Senior Professor and Curriculum Director in {topic}.

Your task is to write a master-class, publication-grade academic Study Material module on:
- Subject / Discipline: {topic}
- Academic Level: {level}
- Unit / Module Title: {unit}
{focus_directive}
{pacing_directive}

Format your output in clean, professional Markdown with the following exact structure:

# {topic}: {unit}
*Academic Level: {level} | Curriculum Study Material*

## 1. Introduction & Learning Objectives
- Provide a rigorous 2-3 paragraph academic overview of {unit} in the context of {topic}.
- Clearly enumerate 4-5 measurable Course Learning Outcomes (CLOs) using Bloom's Taxonomy verbs (Define, Analyze, Evaluate, Implement).

## 2. Core Definitions & Technical Glossary
- Provide precise, exam-standard definitions for every critical term, concept, and metric in this unit.
- If focus areas ({focus_areas or unit}) are specified, define each one with mathematical / formal clarity.

## 3. In-Depth Technical Concepts & Architectural Walkthrough
- Provide a structured conceptual explanation tailored to {level} students.
- Break down the core mechanisms, internal structures, state transitions, mathematical equations, or neural architectures.
- Include structured ASCII or Markdown comparison tables, component diagrams, and workflow summaries.
- Address edge cases, training bottlenecks, optimization trade-offs, or scaling laws.

## 4. Real-World Intuitive Analogy
- Provide a memorable, high-clarity real-world analogy that makes abstract theoretical concepts intuitive.
- Provide a clean mapping table connecting each component of the analogy to its technical counterpart.

## 5. Practical Implementation & Real-World Code / Case Study
- Provide realistic, clean code snippets (e.g. PyTorch, Python, POSIX C, or pseudocode) demonstrating real-world usage.
- Walk through the implementation logic step-by-step.
- Highlight key libraries, APIs, or design patterns used in production.

## 6. Key Takeaways & Quick Revision Summary
- Bullet-point high-yield facts, formula cheat-sheets, and common exam pitfalls to avoid.
"""


def build_assignment_prompt(topic: str, level: str, unit: str, focus_areas: str = "", num_mcqs: int = 5, depth: str = "High-Yield", **kwargs) -> str:
    """
    Engineered prompt specifically crafted for multi-tiered assignments and question banks.
    Strictly assesses the user's specific topic and focus concepts.
    """
    focus_directive = ""
    if focus_areas and focus_areas.strip():
        focus_directive = f"""
PRIMARY FOCUS & MANDATORY TOPICS:
Ensure your questions directly test and evaluate the following concepts:
👉 {focus_areas.strip()}
"""

    num_short = 3 if depth == "High-Yield" else 5
    num_long = 2 if depth == "High-Yield" else 5

    return f"""Act as an Examination Board Chief Moderator for {level} in {topic}.

Create a rigorous, university-standard Assignment & Examination Question Bank for:
- Subject: {topic}
- Academic Level: {level}
- Unit / Module: {unit}
{focus_directive}
Ensure the questions assess varying cognitive levels (Recall, Comprehension, Application, Synthesis).
Format your output in clean Markdown following this exact structure:

# Assignment & Examination Question Bank: {unit}
*Subject: {topic} | Target: {level}*

---

## SECTION A: Multiple Choice Questions ({num_mcqs} Questions)
Generate exactly {num_mcqs} high-caliber, non-trivial MCQs testing conceptual understanding and analytical ability.
For each question, strictly follow this format:

### MCQ [Number]
**Question**: [Question stem]
- A) [Option A]
- B) [Option B]
- C) [Option C]
- D) [Option D]
**Correct Answer**: [Option Letter]
**Explanation**: [Crisp 2-sentence explanation of why the correct option is right and common misconception for wrong options]
**Bloom's Level**: [Remember / Understand / Apply / Analyze]

---

## SECTION B: Short-Answer Conceptual Questions ({num_short} Questions, 3-5 Marks Each)
Provide {num_short} focused analytical questions suitable for university mid-term exams.
For each question:
1. State the question clearly.
2. Specify the recommended marks (e.g., [3 Marks] or [5 Marks]).
3. Provide a **Model Answer Outline / Key Grading Criteria** that examiners look for.

---

## SECTION C: Long-Answer & Design Questions ({num_long} Questions, 10-15 Marks Each)
Provide {num_long} comprehensive essay, numerical, or architectural design questions typical of university semester end examinations.
For each question:
1. State the full question prompt with any relevant specifications or constraints.
2. Specify marks (e.g., [10 Marks] or [15 Marks]).
3. Provide a **Detailed Solution Blueprint & Evaluation Rubric**:
   - Key diagrams required
   - Expected derivation or algorithmic steps
   - Step-by-step mark distribution breakdown
"""


def get_naive_generic_prompt(topic: str, unit: str, level: str, focus_areas: str = "") -> str:
    """
    Baseline naive prompt used for comparison demonstration.
    """
    focus_str = f" including {focus_areas}" if focus_areas else ""
    return f"Explain {topic} - {unit}{focus_str} for {level} and give some questions."


def get_prompt_engineering_breakdown() -> List[Dict[str, str]]:
    """
    Returns educational insights explaining how prompt engineering powers the generator.
    """
    return [
        {
            "technique": "Role & Persona Prompting",
            "implementation": "Specifies 'Senior Professor and Curriculum Director' / 'Examination Board Chief Moderator'.",
            "why_it_matters": "Activates high-depth domain knowledge, academic vocabulary, and pedagogical rigor instead of colloquial chat responses."
        },
        {
            "technique": "Audience & Scope Calibration",
            "implementation": "Explicitly targets university grade (e.g., B.Tech) and unit boundaries.",
            "why_it_matters": "Prevents oversimplification or irrelevant advanced trivia; matches university syllabus standards."
        },
        {
            "technique": "Strict Injection of Focus Concepts",
            "implementation": "Forces explicit coverage of user-specified topics (e.g. CNNs, Transformers, LLMs).",
            "why_it_matters": "Eliminates generic boilerplate and guarantees that student-requested subtopics are taught and tested."
        },
        {
            "technique": "Structural & Format Constraints",
            "implementation": "Enforces numbered sections, markdown tables, exact MCQ syntax, and rubric blocks.",
            "why_it_matters": "Enables deterministic parsing into interactive quizzes, printable sheets, and structured tabs without model hallucination or omission."
        },
        {
            "technique": "Cognitive Scaffolding (Bloom's Taxonomy)",
            "implementation": "Orchestrates progression from Recall (Definitions) → Comprehension (Analogies) → Application (Code) → Evaluation (University Long Questions).",
            "why_it_matters": "Transforms simple information retrieval into a holistic learning and testing environment."
        }
    ]
