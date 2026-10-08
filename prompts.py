"""
Prompt Engineering Core for AI Assignment & Study Material Generator.

This module houses the carefully engineered prompt architectures that produce
university-grade Study Materials, Assignment Sheets, and Examination Question Banks,
while preserving the ability to compare with naive/generic prompts for academic evaluation.
"""

from typing import Dict, Any, List

def build_study_material_prompt(topic: str, level: str, unit: str, depth: str = "Comprehensive") -> str:
    """
    Engineered prompt specifically crafted for in-depth, syllabus-standard study material.
    """
    return f"""Act as a distinguished Senior Professor and Curriculum Director in {topic}.

Your task is to write a master-class, publication-grade academic Study Material module on:
- Subject: {topic}
- Academic Level: {level}
- Unit / Module: {unit}
- Coverage Depth: {depth}

Format your output in clean, professional Markdown with the following exact structure:

# {topic}: {unit}
*Academic Level: {level} | Curriculum Study Material*

## 1. Introduction & Learning Objectives
- Provide a rigorous 2-3 paragraph academic overview of {unit} in the context of {topic}.
- Clearly enumerate 4-5 measurable Course Learning Outcomes (CLOs) using Bloom's Taxonomy verbs (Define, Analyze, Evaluate, Implement).

## 2. Core Definitions & Technical Glossary
- Provide precise, exam-standard definitions for every critical term, concept, and metric in this unit.
- Format with bold terms followed by technical explanations and mathematical/symbolic representations where applicable.

## 3. In-Depth Technical Concepts & Architectural Walkthrough
- Provide an exhaustive, step-by-step conceptual explanation tailored to {level} students.
- Break down the core mechanisms, internal structures, state transitions, algorithms, or protocols.
- Include structured ASCII or Markdown comparison tables, state diagrams, and workflow summaries.
- Address edge cases, race conditions, performance bottlenecks, or trade-offs.

## 4. Real-World Intuitive Analogy
- Provide a memorable, high-clarity real-world analogy that makes abstract theoretical concepts intuitive.
- Provide a clean mapping table connecting each component of the analogy to its technical counterpart.

## 5. Practical Implementation & Real-World Case Study
- Provide realistic code snippets, pseudocode, or industrial architecture examples (e.g., Linux kernel, POSIX, production systems).
- Walk through the implementation logic line-by-line.
- Highlight key system calls, APIs, or design patterns used in production.

## 6. Key Takeaways & Quick Revision Summary
- Bullet-point high-yield facts, formula cheat-sheets, and common exam pitfalls to avoid.
"""


def build_assignment_prompt(topic: str, level: str, unit: str, num_mcqs: int = 5) -> str:
    """
    Engineered prompt specifically crafted for multi-tiered assignments and question banks.
    """
    return f"""Act as an Examination Board Chief Moderator for {level} in {topic}.

Create a rigorous, university-standard Assignment & Examination Question Bank for:
- Subject: {topic}
- Academic Level: {level}
- Unit: {unit}

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

## SECTION B: Short-Answer Conceptual Questions (5 Questions, 3-5 Marks Each)
Provide 5 focused analytical questions suitable for university mid-term exams.
For each question:
1. State the question clearly.
2. Specify the recommended marks (e.g., [3 Marks] or [5 Marks]).
3. Provide a **Model Answer Outline / Key Grading Criteria** that examiners look for.

---

## SECTION C: Long-Answer & Design Questions (5 Questions, 10-15 Marks Each)
Provide 5 comprehensive essay, numerical, or architectural design questions typical of university semester end examinations.
For each question:
1. State the full question prompt with any relevant specifications or constraints.
2. Specify marks (e.g., [10 Marks] or [15 Marks]).
3. Provide a **Detailed Solution Blueprint & Evaluation Rubric**:
   - Key diagrams required
   - Expected derivation or algorithmic steps
   - Step-by-step mark distribution breakdown
"""


def build_complete_coursepack_prompt(topic: str, level: str, unit: str) -> str:
    """
    Combines both study material and assignment into a single unified course pack.
    """
    return f"""Act as a distinguished Senior Professor and Curriculum Architect in {topic}.

Create a complete, end-to-end Course Module Pack (Comprehensive Study Material + Full Assignment & Question Bank) for:
- Subject: {topic}
- Academic Level: {level}
- Unit / Module: {unit}

You must strictly include:
PART I: COMPREHENSIVE STUDY MATERIAL
1. Executive Introduction & Learning Outcomes
2. Formal Definitions & Core Technical Glossary
3. Exhaustive Conceptual Deep Dive (Mechanisms, Architectures, Comparison Tables)
4. Intuitive Real-Life Analogy with Technical Mapping
5. Practical Implementation (POSIX / Real-world Code & Architecture)
6. Summary & High-Yield Exam Revision Notes

PART II: ASSIGNMENT & EXAMINATION QUESTION BANK
7. Section A: 5 High-Quality MCQs (with Options, Correct Answer, Explanation, and Bloom's Level)
8. Section B: 5 Short-Answer Conceptual Questions (3-5 Marks Each, with Model Answer Outlines)
9. Section C: 5 University Long-Answer Exam Questions (10-15 Marks Each, with Marking Rubrics and Diagrams Expected)

Use rigorous academic tone, precise terminology, and clean Markdown formatting throughout.
"""


def get_naive_generic_prompt(topic: str, unit: str, level: str) -> str:
    """
    Baseline naive prompt used for comparison demonstration.
    """
    return f"Explain {topic} - {unit} for {level} and give some questions."


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
            "technique": "Structural & Format Constraints",
            "implementation": "Enforces numbered sections, markdown tables, exact MCQ syntax, and rubric blocks.",
            "why_it_matters": "Enables deterministic parsing into interactive quizzes, printable sheets, and structured tabs without model hallucination or omission."
        },
        {
            "technique": "Cognitive Scaffolding (Bloom's Taxonomy)",
            "implementation": "Orchestrates progression from Recall (Definitions) → Comprehension (Analogies) → Application (Code) → Evaluation (University Long Questions).",
            "why_it_matters": "Transforms simple information retrieval into a holistic learning and testing environment."
        },
        {
            "technique": "Dual-Key Rubric Engineering",
            "implementation": "Demands model answer outlines, distractor explanations, and mark distribution schemas.",
            "why_it_matters": "Provides immediate value to educators for grading and to students for self-assessment."
        }
    ]
