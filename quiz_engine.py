"""
Quiz & Assessment Parser for parsing and rendering interactive MCQs from generated assignments.
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
    
    # We skip chunk 0 because it's text before the first question
    for idx, block in enumerate(chunks[1:], start=1):
        if not block.strip():
            continue
            
        # Extract Question Stem
        # Stem is typically after "**Question**:" or directly up until the first option
        stem_match = re.search(r"(?:\*\*Question\*\*[:\s]*|Question[:\s]*|^)(.*?)(?=(?:-?\s*A\)|A\.|-?\s*A\.))", block, re.DOTALL | re.IGNORECASE)
        stem = stem_match.group(1).strip() if stem_match else ""
        stem = re.sub(r"^\*+|\*+$", "", stem).strip()
        stem = re.sub(r"^:\s*", "", stem).strip()
        
        # Extract Options A, B, C, D
        opt_a = re.search(r"(?:-?\s*A\)|A\.|A\))\s*(.*?)(?=(?:-?\s*B\)|B\.|B\)|\Z))", block, re.DOTALL)
        opt_b = re.search(r"(?:-?\s*B\)|B\.|B\))\s*(.*?)(?=(?:-?\s*C\)|C\.|C\)|\Z))", block, re.DOTALL)
        opt_c = re.search(r"(?:-?\s*C\)|C\.|C\))\s*(.*?)(?=(?:-?\s*D\)|D\.|D\)|\Z))", block, re.DOTALL)
        opt_d = re.search(r"(?:-?\s*D\)|D\.|D\))\s*(.*?)(?=(?:\*\*Correct Answer|\bCorrect Answer|\Z))", block, re.DOTALL)
        
        # Extract Correct Answer
        ans_match = re.search(r"(?:\*\*Correct Answer\*\*|Correct Answer)[:\s]*([A-D])", block, re.IGNORECASE)
        correct_ans = ans_match.group(1).upper() if ans_match else ""
        
        # Extract Explanation
        exp_match = re.search(r"(?:\*\*Explanation\*\*|Explanation)[:\s]*(.*?)(?=(?:\*\*Bloom|\bBloom|\n\n|\Z))", block, re.DOTALL | re.IGNORECASE)
        explanation = exp_match.group(1).strip() if exp_match else ""
        
        # Extract Bloom's Level
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
