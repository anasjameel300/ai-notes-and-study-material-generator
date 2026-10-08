"""
Multi-Provider LLM Service Module for AI Assignment & Study Material Generator.
Supports:
1. Google Gemini (via official google-genai SDK or OpenAI-compatible endpoint)
2. OpenRouter (OpenAI-compatible client with base_url="https://openrouter.ai/api/v1")
3. OpenAI (Official OpenAI API)
4. Offline Academic Engine (ONLY when no API key is provided)
"""

import os
import time
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(
        self,
        provider: str = "auto",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.provider = provider
        self.api_key = (api_key or "").strip()
        self.model = (model or "").strip()

        self._resolve_credentials()

    def _resolve_credentials(self):
        gemini_env = os.getenv("GEMINI_API_KEY", "").strip()
        openrouter_env = os.getenv("OPENROUTER_API_KEY", "").strip()
        openai_env = os.getenv("OPENAI_API_KEY", "").strip()

        if self.provider == "Google Gemini":
            self.api_key = self.api_key or gemini_env
            self.model = self.model or "gemini-2.5-flash"
        elif self.provider == "OpenRouter":
            self.api_key = self.api_key or openrouter_env
            self.model = self.model or "openai/gpt-4o-mini"
        elif self.provider == "OpenAI":
            self.api_key = self.api_key or openai_env
            self.model = self.model or "gpt-4o-mini"
        else:
            # Auto-detect from key or environment
            if self.api_key:
                if self.api_key.startswith("sk-or-"):
                    self.provider = "OpenRouter"
                    self.model = self.model or "openai/gpt-4o-mini"
                elif self.api_key.startswith("AIza"):
                    self.provider = "Google Gemini"
                    self.model = self.model or "gemini-2.5-flash"
                elif self.api_key.startswith("sk-"):
                    self.provider = "OpenAI"
                    self.model = self.model or "gpt-4o-mini"
                else:
                    # Default key to Gemini if starts with AIza or generic
                    self.provider = "Google Gemini"
                    self.model = self.model or "gemini-2.5-flash"
            elif gemini_env:
                self.provider = "Google Gemini"
                self.api_key = gemini_env
                self.model = self.model or "gemini-2.5-flash"
            elif openrouter_env:
                self.provider = "OpenRouter"
                self.api_key = openrouter_env
                self.model = self.model or "openai/gpt-4o-mini"
            elif openai_env:
                self.provider = "OpenAI"
                self.api_key = openai_env
                self.model = self.model or "gpt-4o-mini"
            else:
                self.provider = "Offline Academic Engine"
                self.model = "Offline Engine"

    def has_live_credentials(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 8)

    def generate(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        """
        Executes query on selected provider.
        CRITICAL: If live credentials are provided, ANY error is captured and returned
        explicitly so the user knows what happened, rather than silently falling back to a hardcoded topic.
        """
        start_time = time.time()

        # 1. Google Gemini
        if self.provider == "Google Gemini" and self.has_live_credentials():
            # Try official google.genai SDK
            try:
                from google import genai
                client = genai.Client(api_key=self.api_key)
                
                # Model normalization (support gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-flash, etc.)
                target_model = self.model or "gemini-2.5-flash"
                
                full_content = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                response = client.models.generate_content(
                    model=target_model,
                    contents=full_content
                )
                
                content = response.text or ""
                duration = time.time() - start_time
                return {
                    "success": True,
                    "content": content,
                    "provider": "Google Gemini",
                    "model_used": target_model,
                    "duration_sec": round(duration, 2),
                    "word_count": len(content.split()),
                    "is_live_api": True,
                    "error": None
                }
            except Exception as e1:
                # Secondary attempt: Google OpenAI-compatible endpoint
                try:
                    from openai import OpenAI
                    client = OpenAI(
                        api_key=self.api_key,
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                    )
                    messages = []
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    messages.append({"role": "user", "content": prompt})

                    target_model = self.model or "gemini-2.5-flash"
                    resp = client.chat.completions.create(
                        model=target_model,
                        messages=messages,
                        temperature=0.6,
                    )
                    content = resp.choices[0].message.content or ""
                    duration = time.time() - start_time
                    return {
                        "success": True,
                        "content": content,
                        "provider": "Google Gemini (Endpoint)",
                        "model_used": target_model,
                        "duration_sec": round(duration, 2),
                        "word_count": len(content.split()),
                        "is_live_api": True,
                        "error": None
                    }
                except Exception as e2:
                    # Return the exact error so the user sees it in the UI!
                    return {
                        "success": False,
                        "content": None,
                        "provider": "Google Gemini",
                        "model_used": self.model,
                        "duration_sec": round(time.time() - start_time, 2),
                        "word_count": 0,
                        "is_live_api": True,
                        "error": f"Gemini API Error: {str(e1)} (Fallback attempt: {str(e2)})"
                    }

        # 2. OpenRouter
        if self.provider == "OpenRouter" and self.has_live_credentials():
            try:
                from openai import OpenAI
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=self.api_key
                )
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                target_model = self.model or "openai/gpt-4o-mini"
                response = client.chat.completions.create(
                    model=target_model,
                    messages=messages,
                    temperature=0.6,
                )
                content = response.choices[0].message.content or ""
                duration = time.time() - start_time
                return {
                    "success": True,
                    "content": content,
                    "provider": "OpenRouter",
                    "model_used": target_model,
                    "duration_sec": round(duration, 2),
                    "word_count": len(content.split()),
                    "is_live_api": True,
                    "error": None
                }
            except Exception as e:
                return {
                    "success": False,
                    "content": None,
                    "provider": "OpenRouter",
                    "model_used": self.model,
                    "duration_sec": round(time.time() - start_time, 2),
                    "word_count": 0,
                    "is_live_api": True,
                    "error": f"OpenRouter API Error: {str(e)}"
                }

        # 3. OpenAI
        if self.provider == "OpenAI" and self.has_live_credentials():
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                target_model = self.model or "gpt-4o-mini"
                response = client.chat.completions.create(
                    model=target_model,
                    messages=messages,
                    temperature=0.6,
                )
                content = response.choices[0].message.content or ""
                duration = time.time() - start_time
                return {
                    "success": True,
                    "content": content,
                    "provider": "OpenAI",
                    "model_used": target_model,
                    "duration_sec": round(duration, 2),
                    "word_count": len(content.split()),
                    "is_live_api": True,
                    "error": None
                }
            except Exception as e:
                return {
                    "success": False,
                    "content": None,
                    "provider": "OpenAI",
                    "model_used": self.model,
                    "duration_sec": round(time.time() - start_time, 2),
                    "word_count": 0,
                    "is_live_api": True,
                    "error": f"OpenAI API Error: {str(e)}"
                }

        # 4. Offline Academic Engine (ONLY when no credentials provided)
        return self._knowledge_engine_fallback(prompt)

    def _knowledge_engine_fallback(self, prompt: str) -> Dict[str, Any]:
        """
        Fallback only when user operates in offline demo mode without an API key.
        Dynamically extracts topic from prompt if not OS.
        """
        import re
        topic_match = re.search(r"Subject:\s*([^\n]+)", prompt)
        unit_match = re.search(r"Unit(?:\s*\/\s*Module)?:\s*([^\n]+)", prompt)
        level_match = re.search(r"Level:\s*([^\n]+)", prompt)

        topic = topic_match.group(1).strip() if topic_match else "Computer Science"
        unit = unit_match.group(1).strip() if unit_match else "Core Principles"
        level = level_match.group(1).strip() if level_match else "B.Tech"

        is_naive = "Explain " in prompt and len(prompt) < 120 and "Act as" not in prompt
        is_assignment_only = "Assignment & Examination Question Bank" in prompt or "SECTION A: Multiple Choice" in prompt
        is_study_only = "Study Material module" in prompt

        if is_naive:
            content = f"""# {topic}: {unit} (Overview)
{topic} is an essential subject in computing. {unit} is a key module covering foundational mechanisms, architecture, and operational lifecycle.

Key Concepts:
1. Core definition of {unit}.
2. Operational principles and architecture.
3. System components and workflows.

Questions:
1. Define {unit} in {topic}.
2. Explain the fundamental components of {unit}.
"""
        elif is_assignment_only:
            content = f"""# Assignment & Examination Question Bank: {unit}
*Subject: {topic} | Target: {level}*

---

## SECTION A: Multiple Choice Questions (5 Questions)

### MCQ 1
**Question**: What is the primary operational objective of {unit} in {topic}?
- A) Hardware clock synchronization
- B) System resource management and execution isolation
- C) Peripheral bus deallocation
- D) Secondary cache invalidation
**Correct Answer**: B
**Explanation**: In {topic}, {unit} is primarily responsible for coordinating system resources and ensuring robust task isolation.
**Bloom's Level**: Understand

### MCQ 2
**Question**: Which data structure or mechanism is fundamentally required to maintain state in {unit}?
- A) Translation Lookaside Buffer
- B) Control Block / State Table
- C) Circular FIFO Buffer
- D) Hash Index Map
**Correct Answer**: B
**Explanation**: A control block or state record stores critical operational metadata required for state transitions.
**Bloom's Level**: Understand

### MCQ 3
**Question**: How does {unit} handle resource contention under high concurrency?
- A) It forcibly aborts all competing threads
- B) It employs scheduling queues and mutual exclusion primitives
- C) It bypasses memory protection registers
- D) It drops non-priority interrupts
**Correct Answer**: B
**Explanation**: Concurrency is managed via prioritized scheduling queues and synchronization primitives to prevent race conditions.
**Bloom's Level**: Analyze

### MCQ 4
**Question**: In modern implementations of {unit}, what is the primary source of operational latency?
- A) Context switching and state saving overhead
- B) Static binary compilation
- C) Read-only data caching
- D) Symbolic link resolution
**Correct Answer**: A
**Explanation**: Preserving execution contexts and reloading architectural registers introduces unavoidable system overhead.
**Bloom's Level**: Analyze

### MCQ 5
**Question**: What is the consequence if state cleanup is neglected upon task completion in {unit}?
- A) Instant operating system panic
- B) Memory leaks and dangling state entries in the kernel table
- C) Hardware register degradation
- D) Automatic privilege escalation
**Correct Answer**: B
**Explanation**: Failing to reclaim allocated resources results in lingering metadata entries and resource leaks.
**Bloom's Level**: Apply

---

## SECTION B: Short-Answer Conceptual Questions (5 Questions, 3-5 Marks Each)

### Question 1 [3 Marks]
**Define the scope and core responsibilities of {unit} in modern computing environments.**
- **Model Answer Outline**:
  - Clear definition of {unit} within {topic}.
  - Key responsibilities: Allocation, execution coordination, and state monitoring.
  - Significance for system reliability and throughput.

### Question 2 [3 Marks]
**Explain the architectural role of state management tables in {unit}.**
- **Model Answer Outline**:
  - Preservation of active runtime parameters and memory pointers.
  - Coordination between hardware registers and operating system routines.

### Question 3 [3 Marks]
**Distinguish between static resource reservation and dynamic on-demand allocation in {unit}.**
- **Model Answer Outline**:
  - Static: Predictable but inefficient utilization.
  - Dynamic: Highly adaptable, minimizes fragmentation, requires active runtime tracking.

### Question 4 [3 Marks]
**Identify two critical edge cases or failure modes in {unit} and how modern systems prevent them.**
- **Model Answer Outline**:
  - Deadlock / starvation: Resolved using priority inheritance and timeout protocols.
  - Memory boundary violation: Enforced via hardware protection registers.

### Question 5 [3 Marks]
**Why is modular decomposition essential when designing systems for {unit}?**
- **Model Answer Outline**:
  - Isolation of faults, ease of verification, and maintainability across diverse architectures.

---

## SECTION C: Long-Answer & Design Questions (5 Questions, 10-15 Marks Each)

### Question 1 [10 Marks]
**Provide an end-to-end architectural walkthrough of {unit}. Illustrate the lifecycle of an entity within this module from creation to reclamation, detailing state transitions and queue management.**
- **Solution Blueprint & Evaluation Rubric**:
  - Labeled architectural diagram (3 Marks)
  - Lifecycle state explanations and triggers (4 Marks)
  - Queue coordination and synchronization strategies (3 Marks)

### Question 2 [12 Marks]
**Critically analyze the performance bottlenecks associated with {unit}. Propose two software or architectural optimizations and derive their mathematical impact on system throughput.**
- **Solution Blueprint & Evaluation Rubric**:
  - Identification of overhead sources (cache misses, context switches) (4 Marks)
  - Detailed design of Optimization 1 & 2 (5 Marks)
  - Throughput / latency derivation (3 Marks)

### Question 3 [10 Marks]
**Design an algorithm or system routine for {unit} that guarantees fair resource allocation without causing starvation. Write syntactically correct pseudocode and analyze its computational complexity.**
- **Solution Blueprint & Evaluation Rubric**:
  - Algorithmic specification and fairness criteria (3 Marks)
  - Complete pseudocode with error handling (4 Marks)
  - Time and space complexity analysis (3 Marks)
"""
        else:
            content = f"""# {topic}: {unit}
*Academic Level: {level} | Curriculum Study Material*

---

## 1. Introduction & Learning Objectives
{topic} is a core discipline in computing and engineering. The module **{unit}** addresses the core architectural concepts, protocols, and mechanisms necessary for building robust and scalable systems.

### Course Learning Outcomes (CLOs)
By the end of this study module, {level} students will be able to:
1. **Define and Contrast** foundational terminology and paradigms in {unit}.
2. **Model and Analyze** internal state lifecycles and architectural interactions.
3. **Evaluate** system performance trade-offs, overhead sources, and resource contention.
4. **Implement** robust algorithms and system routines adhering to industry standards.

---

## 2. Core Definitions & Technical Glossary
- **{unit}**: The formal discipline and implementation subsystem responsible for managing operations, scheduling, and resources in {topic}.
- **Execution Context**: The complete set of registers, memory pointers, and metadata representing the active state of an executing unit.
- **State Transition Model**: The discrete lifecycle through which entities transition (e.g., Initialization, Active, Waiting, Terminated).
- **Control Metadata Structure**: The kernel or runtime data record maintaining identification, scheduling priority, and allocated permissions.
- **Throughput & Latency**: Key performance metrics measuring completed operations per unit time versus turnaround delay.

---

## 3. In-Depth Technical Concepts & Architectural Walkthrough
### 3.1 Core Mechanism & Lifecycle Flow
In {topic}, {unit} relies on structured state machines:
```
[ Initialization ] ---> [ Ready / Queued ] <---> [ Active Execution ] ---> [ Completion ]
                              ^                         |
                              |                         | Resource Wait
                              +--- [ Blocked / Pending ] +
```
- **Initialization**: Allocation of control structures and verification of memory bounds.
- **Queued**: Placement into priority scheduling structures awaiting processor or bus assignment.
- **Active Execution**: Direct execution on system hardware with active instruction fetching.
- **Blocked**: Descheduled during asynchronous I/O or lock contention.

### 3.2 State Management & Control Tables
Every execution unit maintains a dedicated record holding:
| Component | Functionality |
| :--- | :--- |
| **Identifier (ID)** | Unique system-wide identifier. |
| **Current State** | Flag indicating operational status (Ready, Running, Blocked). |
| **Registers / Pointers** | Saved execution counter and stack frame pointers. |
| **Resource Limits** | Quotas for memory, open handles, and execution priority. |

---

## 4. Real-World Intuitive Analogy
**The Air Traffic Control Tower at an International Airport:**
- **The Runway**: The limited computing hardware (CPU / Data Bus) that can only handle one flight at a time.
- **The Aircraft**: Independent tasks or processes awaiting landing and takeoff.
- **The Controller**: The scheduler in {unit} coordinating approach queues, holding patterns, and emergency priority slots.
- **Holding Pattern**: The Waiting state while ground support or runway clearing (I/O) completes.

---

## 5. Practical Implementation & Architectural Pattern
```c
// Conceptual Architectural Pattern for {unit}
#include <stdio.h>
#include <stdlib.h>

typedef struct {{
    int id;
    int state; // 0: Init, 1: Ready, 2: Active, 3: Done
    void (*execute_handler)(void*);
}} UnitTask;

void run_task(UnitTask* task) {{
    if (task && task->state == 1) {{
        task->state = 2; // Transition to Active
        printf("[Task %d] Executing operational logic...\\n", task->id);
        // ... perform system work ...
        task->state = 3; // Terminated
    }}
}}
```

---

## 6. Key Takeaways & Exam Revision Summary
- Understand the trade-offs between static allocation and dynamic queuing.
- Context switches incur overhead: minimize cache thrashing and state-saving penalties.
- Always implement clean termination to prevent dangling descriptors and memory leaks.
"""

        return {
            "success": True,
            "content": content,
            "provider": "Offline Academic Engine",
            "model_used": "Dynamic Syllabus Generator",
            "duration_sec": 0.5,
            "word_count": len(content.split()),
            "is_live_api": False,
            "error": None
        }
