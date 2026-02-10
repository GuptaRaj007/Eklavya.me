import streamlit as st
from agents import GeneratorAgent, ReviewerAgent

st.set_page_config(page_title="AI Assessment – Agent Pipeline", layout="wide")

st.title("🤖 AI Agent-Based Educational Content Generator")

# Input Section
st.header("📥 Input")
grade = st.selectbox("Select Grade", [1, 2, 3, 4, 5], index=3)
topic = st.text_input("Enter Topic", value="Types of angles")

if st.button("Run Agent Pipeline"):
    input_data = {"grade": grade, "topic": topic}

    generator = GeneratorAgent()
    reviewer = ReviewerAgent()

    # Step 1: Generate
    st.subheader("🧠 Generator Agent Output")
    generated_output = generator.generate(input_data)
    st.json(generated_output)

    # Step 2: Review
    st.subheader("🔍 Reviewer Agent Feedback")
    review_output = reviewer.review(generated_output, grade, topic)
    st.json(review_output)

    # Step 3: Refinement (One pass only)
    if review_output["status"] == "fail":
        st.subheader("🔁 Refined Generator Output")
        refined_output = generator.generate(
            input_data,
            feedback=review_output["feedback"]
        )
        st.json(refined_output)
