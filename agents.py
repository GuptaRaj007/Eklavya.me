from typing import Dict, List


class GeneratorAgent:
    """
    Responsibility:
    Generate grade-appropriate educational content
    for a given grade and topic.
    """

    def generate(self, input_data: Dict, feedback: List[str] = None) -> Dict:
        grade = input_data["grade"]
        raw_topic = input_data["topic"].strip()

        if not raw_topic:
            return {
                "explanation": "Please provide a valid topic to generate content.",
                "mcqs": []
            }

        topic = raw_topic.lower()

        # -------------------------------
        # TOPIC: TYPES OF ANGLES
        # -------------------------------
        if "angle" in topic:
            if grade <= 3:
                explanation = (
                    "An angle is made when two lines meet. "
                    "A right angle looks like the corner of a book. "
                    "Some angles are smaller and some are bigger."
                )
            else:
                explanation = (
                    "An angle is formed when two lines meet at a point. "
                    "There are different types of angles based on how wide they open. "
                    "A right angle looks like the corner of a square. "
                    "An acute angle is smaller than a right angle. "
                    "An obtuse angle is bigger than a right angle."
                )

            # Refinement
            if feedback:
                explanation = (
                    "An angle is made when two lines meet. "
                    "A right angle looks like the corner of a book. "
                    "An acute angle is smaller than a right angle. "
                    "An obtuse angle is larger than a right angle."
                )

            mcqs = [
                {
                    "question": "Which angle looks like the corner of a book?",
                    "options": ["Acute angle", "Right angle", "Obtuse angle", "Straight angle"],
                    "answer": "Right angle"
                },
                {
                    "question": "Which angle is smaller than a right angle?",
                    "options": ["Obtuse angle", "Straight angle", "Acute angle", "Reflex angle"],
                    "answer": "Acute angle"
                },
                {
                    "question": "Which angle is bigger than a right angle?",
                    "options": ["Acute angle", "Right angle", "Obtuse angle", "Zero angle"],
                    "answer": "Obtuse angle"
                }
            ]

        # -------------------------------
        # TOPIC: SHAPES
        # -------------------------------
        elif "shape" in topic:
            explanation = (
                "Shapes have different forms. "
                "A circle is round. "
                "A square has four equal sides. "
                "A triangle has three sides. "
                "A rectangle has four sides with opposite sides equal."
            )

            if feedback:
                explanation = (
                    "Shapes are objects with different forms. "
                    "A circle is round. "
                    "A square has four sides. "
                    "A triangle has three sides."
                )

            mcqs = [
                {
                    "question": "Which shape is round?",
                    "options": ["Square", "Triangle", "Circle", "Rectangle"],
                    "answer": "Circle"
                },
                {
                    "question": "How many sides does a triangle have?",
                    "options": ["2", "3", "4", "5"],
                    "answer": "3"
                },
                {
                    "question": "Which shape has four equal sides?",
                    "options": ["Rectangle", "Triangle", "Circle", "Square"],
                    "answer": "Square"
                }
            ]

        # -------------------------------
        # TOPIC: FRACTIONS
        # -------------------------------
        elif "fraction" in topic:
            explanation = (
                "A fraction shows a part of a whole. "
                "It has a top number and a bottom number. "
                "The top number shows parts taken, "
                "and the bottom number shows total equal parts."
            )

            mcqs = [
                {
                    "question": "What does a fraction show?",
                    "options": ["A whole number", "A part of a whole", "A shape", "An angle"],
                    "answer": "A part of a whole"
                },
                {
                    "question": "In the fraction 1/2, what does 2 mean?",
                    "options": ["Parts taken", "Total parts", "Answer", "Shape"],
                    "answer": "Total parts"
                },
                {
                    "question": "Which fraction means one part out of four?",
                    "options": ["1/2", "1/3", "1/4", "2/4"],
                    "answer": "1/4"
                }
            ]

        # -------------------------------
        # TOPIC: PERIMETER
        # -------------------------------
        elif "perimeter" in topic:
            explanation = (
                "Perimeter is the distance around a shape. "
                "It is found by adding the lengths of all sides."
            )

            mcqs = [
                {
                    "question": "What does perimeter mean?",
                    "options": [
                        "Space inside a shape",
                        "Distance around a shape",
                        "Number of sides",
                        "Type of angle"
                    ],
                    "answer": "Distance around a shape"
                },
                {
                    "question": "How do we find the perimeter?",
                    "options": [
                        "Multiply sides",
                        "Subtract sides",
                        "Add all sides",
                        "Divide sides"
                    ],
                    "answer": "Add all sides"
                },
                {
                    "question": "Which shape has a perimeter?",
                    "options": ["Only circles", "Only squares", "All shapes", "Only triangles"],
                    "answer": "All shapes"
                }
            ]

        # -------------------------------
        # UNSUPPORTED TOPIC
        # -------------------------------
        else:
            explanation = (
                f"The topic '{raw_topic}' is not supported yet. "
                "Please try another basic math topic."
            )
            mcqs = []

        return {
            "explanation": explanation,
            "mcqs": mcqs
        }


class ReviewerAgent:
    """
    Responsibility:
    Review generated content for:
    - Topic alignment
    - Grade appropriateness
    - Conceptual correctness
    - Structural validity
    """

    def review(self, content: Dict, grade: int, topic: str) -> Dict:
        feedback = []

        explanation = content["explanation"].lower()
        topic = topic.strip().lower()

        # 1️⃣ Empty topic check
        if not topic:
            feedback.append("Topic is empty and cannot be validated.")

        # 2️⃣ Unsupported topic check
        elif "not supported" in explanation:
            feedback.append(f"Topic '{topic}' is not supported yet.")

        # 3️⃣ Topic alignment (multi-word safe)
        else:
            topic_keywords = topic.split()
            if content["mcqs"] and not any(keyword in explanation for keyword in topic_keywords):
                feedback.append(
                    f"Generated content does not clearly align with the topic '{topic}'."
                )

        # 4️⃣ Grade sensitivity
        if grade <= 3 and any(word in explanation for word in ["obtuse", "perimeter"]):
            feedback.append("Some concepts may be too advanced for Grade 3.")

        # 5️⃣ MCQ structure validation
        if content["mcqs"] and len(content["mcqs"]) != 3:
            feedback.append("Each topic must have exactly 3 MCQs.")

        for idx, mcq in enumerate(content["mcqs"], start=1):
            if mcq["answer"] not in mcq["options"]:
                feedback.append(f"MCQ {idx} has an invalid correct answer.")

        status = "fail" if feedback else "pass"

        return {
            "status": status,
            "feedback": feedback
        }
