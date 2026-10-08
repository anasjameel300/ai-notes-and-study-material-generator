"""
Quiz & Assessment Parser for parsing and rendering interactive MCQs and theory questions.
"""

import re
from typing import List, Dict, Any

def parse_mcqs(text: str) -> List[Dict[str, Any]]:
    """
    Extracts structured MCQs, options, correct answers, explanations, and Bloom's levels
    from generated assignment markdown.
    """
    mcqs = []
    
    # Match patterns like "### MCQ 1", "**Question 1**", or "Question 1:"
    chunks = re.split(r"(?:###\s*MCQ\s*\d+|\*\*Question\s*\d+[:\.]?\*\*|Question\s*\d+[:\.])", text)
    
    for idx, block in enumerate(chunks[1:], start=1):
        if not block.strip():
            continue
            
        stem_match = re.search(r"(?:\*\*Question\*\*[:\s]*|Question[:\s]*|^)(.*?)(?=(?:-?\s*A\)|A\.|-?\s*A\.))", block, re.DOTALL | re.IGNORECASE)
        stem = stem_match.group(1).strip() if stem_match else ""
        stem = re.sub(r"^\*+|\*+$", "", stem).strip()
        stem = re.sub(r"^:\s*", "", stem).strip()
        
        opt_a = re.search(r"(?:-?\s*A\)|A\.|A\))\s*(.*?)(?=(?:-?\s*B\)|B\.|B\)|\Z))", block, re.DOTALL)
        opt_b = re.search(r"(?:-?\s*B\)|B\.|B\))\s*(.*?)(?=(?:-?\s*C\)|C\.|C\)|\Z))", block, re.DOTALL)
        opt_c = re.search(r"(?:-?\s*C\)|C\.|C\))\s*(.*?)(?=(?:-?\s*D\)|D\.|D\)|\Z))", block, re.DOTALL)
        opt_d = re.search(r"(?:-?\s*D\)|D\.|D\))\s*(.*?)(?=(?:\*\*Correct Answer|\bCorrect Answer|\Z))", block, re.DOTALL)
        
        ans_match = re.search(r"(?:\*\*Correct Answer\*\*|Correct Answer)[:\s]*([A-D])", block, re.IGNORECASE)
        correct_ans = ans_match.group(1).upper() if ans_match else ""
        
        exp_match = re.search(r"(?:\*\*Explanation\*\*|Explanation)[:\s]*(.*?)(?=(?:\*\*Bloom|\bBloom|\n\n|\Z))", block, re.DOTALL | re.IGNORECASE)
        explanation = exp_match.group(1).strip() if exp_match else ""
        
        bloom_match = re.search(r"(?:\*\*Bloom's Level\*\*|Bloom's Level)[:\s]*([A-Za-z]+)", block, re.IGNORECASE)
        bloom_level = bloom_match.group(1).strip() if bloom_match else "Understand"
        
        if stem and opt_a and opt_b and opt_c and opt_d:
            mcqs.append({
                "number": idx,
                "stem": stem,
                "options": {
                    "A": opt_a.group(1).strip(),
                    "B": opt_b.group(1).strip(),
                    "C": opt_c.group(1).strip(),
                    "D": opt_d.group(1).strip()
                },
                "correct_answer": correct_ans,
                "explanation": explanation,
                "bloom_level": bloom_level
            })
            
    return mcqs


def parse_short_questions(text: str) -> List[Dict[str, Any]]:
    """
    Parses Section B Short-Answer Questions with on-demand model answers.
    """
    questions = []
    if "## SECTION B:" not in text:
        return questions
        
    sec_b = text.split("## SECTION B:")[1]
    if "## SECTION C:" in sec_b:
        sec_b = sec_b.split("## SECTION C:")[0]
        
    # Split by ### Question or 1.
    blocks = re.split(r"(?:###\s*Question\s*\d+|(?:\n|^)\s*\d+\.\s*\*\*)", sec_b)
    for idx, b in enumerate(blocks[1:], start=1):
        if not b.strip():
            continue
            
        marks_match = re.search(r"\[(\d+)\s*Marks?\]", b, re.IGNORECASE)
        marks = marks_match.group(1) if marks_match else "3"
        
        # Split prompt and model answer
        parts = re.split(r"(?:-\s*\*\*Model Answer Outline|Model Answer Outline)", b, flags=re.IGNORECASE)
        prompt_text = parts[0].strip()
        # Clean marks from prompt if needed
        prompt_clean = re.sub(r"\[\d+\s*Marks?\]", "", prompt_text).strip()
        prompt_clean = re.sub(r"^\*+|\*+$", "", prompt_clean).strip()
        
        answer_text = ""
        if len(parts) > 1:
            answer_text = re.sub(r"^[:\s\*]+", "", parts[1]).strip()
            
        if prompt_clean:
            questions.append({
                "number": idx,
                "marks": marks,
                "question": prompt_clean,
                "answer": answer_text
            })
            
    return questions


def parse_long_questions(text: str) -> List[Dict[str, Any]]:
    """
    Parses Section C Long-Answer Questions with on-demand rubrics.
    """
    questions = []
    if "## SECTION C:" not in text:
        return questions
        
    sec_c = text.split("## SECTION C:")[1]
    blocks = re.split(r"(?:###\s*Question\s*\d+|(?:\n|^)\s*\d+\.\s*\*\*)", sec_c)
    for idx, b in enumerate(blocks[1:], start=1):
        if not b.strip():
            continue
            
        marks_match = re.search(r"\[(\d+)\s*Marks?\]", b, re.IGNORECASE)
        marks = marks_match.group(1) if marks_match else "10"
        
        parts = re.split(r"(?:-\s*\*\*Detailed Solution Blueprint|Solution Blueprint|Evaluation Rubric)", b, flags=re.IGNORECASE)
        prompt_text = parts[0].strip()
        prompt_clean = re.sub(r"\[\d+\s*Marks?\]", "", prompt_text).strip()
        prompt_clean = re.sub(r"^\*+|\*+$", "", prompt_clean).strip()
        
        rubric_text = ""
        if len(parts) > 1:
            rubric_text = re.sub(r"^[:\s\*]+", "", parts[1]).strip()
            
        if prompt_clean:
            questions.append({
                "number": idx,
                "marks": marks,
                "question": prompt_clean,
                "rubric": rubric_text
            })
            
    return questions
