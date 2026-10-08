"""
Study Helper Tools: Interactive Flashcards & Mind Tree (Concept Map) Generator.
"""

import re
from typing import List, Dict, Any

def extract_flashcards_from_study_material(text: str, unit: str = "Process Management") -> List[Dict[str, str]]:
    """
    Extracts high-yield flashcards from definitions, analogies, and concepts.
    Returns a list of dicts with 'front' and 'back' content.
    """
    cards = []
    
    # 1. Look for bold terms in Section 2 (Definitions)
    # Format: "- **Term**: Definition" or "**Term**: Definition"
    def_matches = re.findall(r"(?:^|\n)[-\*\s]*\*\*([A-Za-z0-9\s\/\-\(\)]+?)\*\*:\s*([^\n]+)", text)
    for term, definition in def_matches:
        term_clean = term.strip()
        def_clean = definition.strip()
        # Filter out headers or metadata
        if len(term_clean) > 2 and len(def_clean) > 20 and not term_clean.startswith("Question") and not term_clean.startswith("Correct"):
            cards.append({
                "front": f"What is **{term_clean}**?",
                "back": def_clean,
                "category": "Core Definition"
            })

    # 2. Extract Analogy Card if present
    analogy_match = re.search(r"## 4\. Real-World Intuitive Analogy\s*(.*?)(?=(?:## 5|\Z))", text, re.DOTALL)
    if analogy_match:
        analogy_text = analogy_match.group(1).strip()
        # First 2 sentences
        sentences = [s.strip() for s in analogy_text.split("\n\n") if s.strip()]
        if sentences:
            cards.append({
                "front": f"Real-World Analogy for {unit}",
                "back": sentences[0],
                "category": "Intuitive Analogy"
            })

    # 3. Extract Implementation / System Call Card
    if "fork()" in text or "POSIX" in text:
        cards.append({
            "front": "How do `fork()`, `exec()`, and `wait()` work together in POSIX?",
            "back": "`fork()` clones the parent process to create a child. `exec()` replaces the child's address space with a new executable. `wait()` halts the parent until the child exits to avoid zombie processes.",
            "category": "System Implementation"
        })

    # Default fallback deck if extraction yielded fewer than 3
    if len(cards) < 3:
        cards = [
            {
                "front": "What is the difference between a Program and a Process?",
                "back": "A Program is a passive binary entity stored statically on secondary storage (disk). A Process is an active executing instance loaded into RAM with allocated CPU registers, stack, heap, and a PID.",
                "category": "Core Concept"
            },
            {
                "front": "What is a Process Control Block (PCB)?",
                "back": "A kernel data structure containing an execution context: PID, Process State, Program Counter, CPU registers, memory management tables, scheduling priority, and open I/O descriptors.",
                "category": "Kernel Structure"
            },
            {
                "front": "What happens during a Context Switch?",
                "back": "The kernel halts the running process, saves its registers and PC into its PCB, swaps memory mapping registers (e.g. CR3) / flushes TLB, and loads the saved registers of the next ready process.",
                "category": "CPU Architecture"
            },
            {
                "front": "What distinguishes a Zombie Process from an Orphan Process?",
                "back": "A Zombie has finished execution but stays in the process table because the parent hasn't read its exit status with `wait()`. An Orphan's parent terminated before it did; it gets adopted by PID 1 (init/systemd).",
                "category": "Lifecycle"
            },
            {
                "front": "Why is Context Switching classified as pure system overhead?",
                "back": "During a context switch, the CPU performs operating system housekeeping (register state saving, memory swapping) rather than advancing user application computations.",
                "category": "Performance"
            }
        ]

    return cards


def generate_mind_tree_mermaid(topic: str, unit: str) -> str:
    """
    Constructs a visual hierarchical Mind Tree (Concept Map) using Mermaid diagram syntax.
    """
    if "Process" in unit or "Operating System" in topic:
        return """graph TD
    Root["🧠 Process Management in OS"] --> C1["1. Process Concepts"]
    Root --> C2["2. State Transitions"]
    Root --> C3["3. Kernel Architecture (PCB)"]
    Root --> C4["4. Scheduling & Dispatch"]
    Root --> C5["5. POSIX System Calls"]

    C1 --> C1a["Program (Passive on Disk)"]
    C1 --> C1b["Process (Active in RAM)"]
    C1 --> C1c["Memory Layout: Text, Data, Heap, Stack"]

    C2 --> C2a["5-State Model"]
    C2a --> C2b["New ➔ Ready ➔ Running"]
    C2a --> C2c["Running ➔ Waiting (I/O Block)"]
    C2a --> C2d["Running ➔ Terminated"]

    C3 --> C3a["PID & Process State"]
    C3 --> C3b["Program Counter (PC)"]
    C3 --> C3c["CPU Hardware Registers"]
    C3 --> C3d["Memory Limits & Open Files"]

    C4 --> C4a["Context Switching Overhead"]
    C4 --> C4b["Ready Queue & Device Queues"]
    C4 --> C4c["Schedulers: Long, Medium, Short-Term"]

    C5 --> C5a["fork() - Process Duplication"]
    C5 --> C5b["exec() - Binary Overlay"]
    C5 --> C5c["wait() - Zombie Elimination"]

    classDef rootStyle fill:#1e1b4b,stroke:#4338ca,stroke-width:2px,color:#fff;
    classDef branchStyle fill:#f1f5f9,stroke:#94a3b8,stroke-width:1.5px,color:#0f172a;
    classDef leafStyle fill:#eff6ff,stroke:#60a5fa,stroke-width:1px,color:#1e3a8a;

    class Root rootStyle;
    class C1,C2,C3,C4,C5 branchStyle;
    class C1a,C1b,C1c,C2a,C2b,C2c,C2d,C3a,C3b,C3c,C3d,C4a,C4b,C4c,C5a,C5b,C5c leafStyle;
"""

    elif "Normal" in unit or "Database" in topic:
        return """graph TD
    Root["🧠 Relational Normalization"] --> C1["Functional Dependencies"]
    Root --> C2["Normal Forms (1NF - BCNF)"]
    Root --> C3["Decomposition Properties"]

    C1 --> C1a["Full vs Partial Dependency"]
    C1 --> C1b["Transitive Dependency"]
    C1 --> C1c["Armstrong's Axioms"]

    C2 --> C2a["1NF: Atomic Attributes"]
    C2 --> C2b["2NF: No Partial Dependencies"]
    C2 --> C2c["3NF: No Transitive Dependencies"]
    C2 --> C2d["BCNF: Determinant is Superkey"]

    C3 --> C3a["Lossless Join Decomposition"]
    C3 --> C3b["Dependency Preservation"]

    classDef rootStyle fill:#1e1b4b,stroke:#4338ca,stroke-width:2px,color:#fff;
    classDef branchStyle fill:#f1f5f9,stroke:#94a3b8,stroke-width:1.5px,color:#0f172a;
    class Root rootStyle;
    class C1,C2,C3 branchStyle;
"""

    else:
        # Dynamic generic tree structure
        t_clean = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
        u_clean = re.sub(r'[^a-zA-Z0-9\s]', '', unit)
        return f"""graph TD
    Root["🧠 {u_clean} in {t_clean}"] --> P1["1. Core Foundations"]
    Root --> P2["2. Theoretical Mechanisms"]
    Root --> P3["3. Architectural Walkthrough"]
    Root --> P4["4. Practical Implementation"]
    Root --> P5["5. Evaluation & Assessment"]

    P1 --> P1a["Formal Definitions"]
    P1 --> P1b["Learning Outcomes"]

    P2 --> P2a["Mathematical / Logical Basis"]
    P2 --> P2b["Real-World Analogy"]

    P3 --> P3a["Internal Components"]
    P3 --> P3b["State & Flow Models"]

    P4 --> P4a["Code / Algorithms"]
    P4 --> P4b["System Calls & APIs"]

    P5 --> P5a["MCQs & Concept Checks"]
    P5 --> P5b["University Exam Questions"]

    classDef rootStyle fill:#1e1b4b,stroke:#4338ca,stroke-width:2px,color:#fff;
    classDef branchStyle fill:#f1f5f9,stroke:#94a3b8,stroke-width:1.5px,color:#0f172a;
    class Root rootStyle;
    class P1,P2,P3,P4,P5 branchStyle;
"""
