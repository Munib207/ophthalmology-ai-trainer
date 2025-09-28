import streamlit as st
import random

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0

# Simple question database
questions = [
    {
        "question": "A patient presents with sudden painless vision loss and cherry red spot. What is the diagnosis?",
        "options": ["CRAO", "CRVO", "Retinal detachment", "Macular degeneration"],
        "correct": "CRAO",
        "explanation": "Cherry red spot is pathognomonic for Central Retinal Artery Occlusion (CRAO)"
    },
    {
        "question": "Which condition presents with floaters, flashes, and curtain over vision?",
        "options": ["Cataract", "Retinal detachment", "Glaucoma", "Uveitis"],
        "correct": "Retinal detachment", 
        "explanation": "Floaters, flashes, and curtain vision are classic for retinal detachment"
    },
    {
        "question": "Acute angle closure glaucoma presents with:",
        "options": ["Painless vision loss", "Eye pain with halos", "Gradual blurring", "Itching"],
        "correct": "Eye pain with halos",
        "explanation": "Angle closure presents with pain, headache, nausea, and halos around lights"
    }
]

def generate_question():
    return random.choice(questions)

# App layout
st.title("👁️ Ophthalmology Quiz")
st.write("Test your ophthalmology knowledge!")

# Sidebar
with st.sidebar:
    st.header("Your Stats")
    st.write(f"Score: {st.session_state.score}/{st.session_state.total}")
    if st.session_state.total > 0:
        accuracy = (st.session_state.score / st.session_state.total) * 100
        st.write(f"Accuracy: {accuracy:.1f}%")

# Main content
if st.button("🎯 New Question"):
    st.session_state.current_question = generate_question()
    st.rerun()

if st.session_state.current_question:
    q = st.session_state.current_question
    
    st.subheader("Question:")
    st.info(q["question"])
    
    selected = st.radio("Choose your answer:", q["options"])
    
    if st.button("Submit Answer"):
        st.session_state.total += 1
        
        if selected == q["correct"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect. The correct answer is: {q['correct']}")
        
        st.write(f"**Explanation:** {q['explanation']}")
        
        # Show next question button
        if st.button("Next Question"):
            st.session_state.current_question = generate_question()
            st.rerun()
else:
    st.info("Click 'New Question' to start!")

# Features section
st.markdown("---")
st.subheader("🎯 Features")
st.write("• Simple multiple-choice questions")
st.write("• Instant feedback with explanations")  
st.write("• Score tracking")
st.write("• Ophthalmology-focused content")
