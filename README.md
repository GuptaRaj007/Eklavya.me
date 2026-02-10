# AI Agent-Based Educational Content Generator

## Overview

This project implements a lightweight **agent-based AI system** with a **UI-driven pipeline**, built specifically to satisfy the requirements of the AI assessment.

The system consists of two clearly defined agents:

1. **Generator Agent** – Generates grade-appropriate educational content
2. **Reviewer Agent** – Evaluates the generated content for topic alignment, grade appropriateness, and structural validity

A simple **Streamlit UI** orchestrates the flow and makes the agent interactions explicit and easy to understand.

---

## Assignment Objectives (Mapped)

The implementation strictly follows the assignment requirements:

* ✔ Two AI agents with clear responsibilities
* ✔ Structured input and output for each agent
* ✔ Deterministic output structure
* ✔ Feedback-based refinement (single pass only)
* ✔ UI integration to trigger and visualize the agent pipeline
* ✔ Empty or unsupported topics are handled gracefully
* ✔ Multi-word topic alignment validated in Reviewer Agent

---

## System Architecture

```
User (UI)
   ↓
Generator Agent
   ↓
Reviewer Agent
   ↓
(Optional) One-Time Refinement
   ↓
UI Output
```

Each component has a single responsibility, ensuring clarity and maintainability.

---

## Agent Definitions

### 1. Generator Agent

**Responsibility:**
Generate draft educational content for a given grade and topic.

**Input (Structured):**

```json
{ "grade": 4, "topic": "Types of angles" }
```

**Output (Structured):**

```json
{
  "explanation": "...",
  "mcqs": [
    {
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "B"
    }
  ]
}
```

**Key Characteristics:**

* Language matches the selected grade level
* Concepts are mathematically correct
* Output structure is deterministic
* Refines content using Reviewer feedback if needed (single pass)

---

### 2. Reviewer Agent

**Responsibility:**
Evaluate the Generator Agent’s output and determine if refinement is needed.

**Evaluation Criteria:**

* Topic alignment (multi-word safe)
* Grade appropriateness
* Conceptual correctness
* Structural validity of MCQs

**Input:**

* JSON output from the Generator Agent

**Output (Structured):**

```json
{
  "status": "pass | fail",
  "feedback": ["..."]
}
```

**Notable Updates:**

* Empty topics trigger a fail with feedback
* Unsupported topics are flagged automatically
* Multi-word topic alignment ensures content relevance
* Detects advanced concepts for lower grades (≤3)
* Ensures exactly 3 MCQs with valid answers

---

## Refinement Logic

* If the Reviewer Agent returns `fail`, the Generator Agent is re-run **once**
* Reviewer feedback is embedded into the Generator logic to simplify or correct content
* Only **one refinement pass** is allowed to keep the system deterministic and avoid loops

---

## UI Integration (Streamlit)

The Streamlit UI provides:

* Input controls for grade and topic
* Button to trigger the full agent pipeline
* Display of:

  * Generator Agent output
  * Reviewer Agent feedback
  * Refined output (only if applicable)

The UI makes the agent flow explicit and easy to follow.

---

## Project Structure

```
ai_assessment/
│
├── app.py          # Streamlit UI
├── agents.py       # Generator and Reviewer agents
├── requirements.txt
└── README.md
```

---

## Installation & Setup

```bash
git clone https://github.com/GuptaRaj007/Eklavya.me.git
cd Eklavya.me

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

---

## Testing the System

### Test Case 1: Successful Pass

**Input:**

* Grade: 4
* Topic: Types of angles

**Expected Result:**

* Generator produces valid content
* Reviewer returns `pass`
* No refinement triggered

---

### Test Case 2: Fail + Refinement

**Scenario:**

* Grade ≤3 with advanced concepts (e.g., obtuse angles)
* Reviewer detects complexity or mismatch

**Expected Result:**

* Reviewer returns `fail` with feedback
* Generator re-runs once using feedback
* Refined output displayed in UI

---

### Test Case 3: Empty or Unsupported Topic

**Input:**

* Grade: 3
* Topic: "" or unsupported topic

**Expected Result:**

* Generator returns placeholder explanation
* Reviewer returns `fail` with clear feedback
* User prompted to try another topic

---

## Design Decisions

* No heavy agent frameworks used – keeps solution simple and transparent
* Deterministic logic ensures predictable outputs
* Clear separation of responsibilities aligns with real-world agent-based systems
* Multi-word topic alignment and grade-aware content improve robustness

---
---

**Author:** Raj

---

If you want, I can also **write a tiny “Known Limitations & Future Improvements” section** at the end to make it extra professional for submission. This usually gives bonus points in assessments. Do you want me to add that?
