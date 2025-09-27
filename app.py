import streamlit as st
import random
from datetime import datetime
import numpy as np

# ===== INITIALIZE SESSION STATE =====
if "resident_tracking" not in st.session_state:
    st.session_state.resident_tracking = {}
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Adaptive Learning"
if "current_patient_case" not in st.session_state:
    st.session_state.current_patient_case = None
if "user_type" not in st.session_state:
    st.session_state.user_type = "Resident"
if "resident_id" not in st.session_state:
    st.session_state.resident_id = None
if "program_id" not in st.session_state:
    st.session_state.program_id = None
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False

# ===== COMPREHENSIVE OPHTHALMOLOGY DATABASE =====
diagnoses = {
    "CRAO (Central Retinal Artery Occlusion)": {
        "symptoms": ["sudden painless vision loss", "complete blackness"],
        "key_finding": "APD, cherry red spot", 
        "urgency": "EMERGENT",
        "category": "Retina",
        "teaching": ["Time is vision! 4-6 hour window", "Always check for APD", "Look for cherry red spot"]
    },
    "Retinal Detachment": {
        "symptoms": ["floaters", "flashes", "curtain over vision"],
        "key_finding": "visual field defect, retinal tear",
        "urgency": "URGENT", 
        "category": "Retina",
        "teaching": ["Ask about floaters and flashes", "Check visual fields", "Ultra-sound if no view"]
    },
    "Angle Closure Glaucoma": {
        "symptoms": ["eye pain", "headache", "nausea", "halos"],
        "key_finding": "elevated IOP, corneal edema",
        "urgency": "EMERGENT",
        "category": "Glaucoma",
        "teaching": ["Check IOP immediately", "Laser iridotomy definitive treatment"]
    },
    "Corneal Ulcer": {
        "symptoms": ["severe pain", "purulent discharge", "photophobia"],
        "key_finding": "corneal infiltrate, epithelial defect", 
        "urgency": "URGENT",
        "category": "Cornea",
        "teaching": ["Contact lens major risk factor", "Never patch infected ulcer"]
    },
    "Optic Neuritis": {
        "symptoms": ["pain with eye movement", "color desaturation", "vision loss"],
        "key_finding": "APD, optic disc edema",
        "urgency": "URGENT", 
        "category": "Neuro-Ophthalmology",
        "teaching": ["Often associated with MS", "Pain with movement classic"]
    },
    "Amblyopia": {
        "symptoms": ["reduced vision one eye", "asymptomatic in children"],
        "key_finding": "vision loss without structural abnormality",
        "urgency": "URGENT",
        "category": "Pediatrics",
        "teaching": ["Treatment effective before age 7-10", "Patching mainstay of therapy"]
    }
}

# ===== VIRTUAL PATIENT SIMULATIONS =====
virtual_patients = {
    "case_001": {
        "title": "Diabetic Retinopathy Progression",
        "patient": "58yo male with Type 2 Diabetes",
        "history": "15-year history of diabetes, HbA1c 9.2%, hypertension",
        "presentation": "Gradual vision blurring over 6 months",
        "symptoms": ["gradual vision loss", "floaters", "metamorphopsia"],
        "correct_diagnosis": "Diabetic Macular Edema",
        "questions": [
            {
                "question": "What is the most appropriate initial management?",
                "options": [
                    "Pan-retinal photocoagulation",
                    "Anti-VEGF injections", 
                    "Observation with 6-month follow-up",
                    "Focal laser treatment"
                ],
                "correct_answer": "Anti-VEGF injections",
                "explanation": "Anti-VEGF is first-line for center-involving DME with vision loss"
            }
        ],
        "teaching_points": [
            "Tight glycemic control slows progression",
            "Anti-VEGF first-line for center-involving DME"
        ],
        "category": "Retina"
    },
    "case_002": {
        "title": "Acute Angle Closure Crisis",
        "patient": "62yo female with hyperopia",
        "history": "No significant medical history, family history of glaucoma",
        "presentation": "Sudden eye pain, headache, nausea, and halos around lights",
        "symptoms": ["severe eye pain", "headache", "nausea", "halos", "vision loss"],
        "correct_diagnosis": "Acute Angle Closure Glaucoma",
        "questions": [
            {
                "question": "What is the first-line treatment?",
                "options": [
                    "Oral acetazolamide",
                    "Laser iridotomy", 
                    "Topical beta-blockers",
                    "Observation"
                ],
                "correct_answer": "Laser iridotomy",
                "explanation": "Laser iridotomy is definitive treatment for angle closure"
            }
        ],
        "category": "Glaucoma"
    }
}

# ===== BOARD EXAM QUESTION BANK =====
board_questions = {
    "q_001": {
        "stem": "A 65-year-old woman presents with sudden, painless loss of vision in her right eye. Examination reveals a relative afferent pupillary defect and a cherry-red spot. The most likely diagnosis is:",
        "options": [
            "Central retinal vein occlusion",
            "Branch retinal artery occlusion", 
            "Central retinal artery occlusion",
            "Ischemic optic neuropathy"
        ],
        "correct_answer": "Central retinal artery occlusion",
        "explanation": "Cherry-red spot is pathognomonic for CRAO. Sudden, painless vision loss with APD suggests retinal artery occlusion.",
        "category": "Retina"
    },
    "q_002": {
        "stem": "A patient presents with eye pain, headache, nausea, and halos around lights. The anterior chamber is shallow. The most urgent action is:",
        "options": [
            "Check intraocular pressure",
            "Order a CT scan",
            "Prescribe oral analgesics",
            "Schedule follow-up in 1 week"
        ],
        "correct_answer": "Check intraocular pressure",
        "explanation": "These symptoms suggest acute angle closure glaucoma. IOP measurement is critical for diagnosis and management.",
        "category": "Glaucoma"
    }
}

# ===== RESIDENCY PROGRAM MANAGEMENT =====
residency_programs = {
    "UCSF_Ophthalmology": {
        "name": "UCSF Department of Ophthalmology",
        "residents": ["smith_j", "johnson_m"],
        "current_rotation": "Retina"
    },
    "Hopkins_Eye": {
        "name": "Wilmer Eye Institute", 
        "residents": ["davis_r", "martinez_j"],
        "current_rotation": "Glaucoma"
    }
}

# ===== QUESTION TEMPLATES =====
question_templates = [
    {"type": "symptoms_to_diagnosis", "template": "A patient presents with **{symptoms}**. The most likely diagnosis is:", "data_field": "symptoms"},
    {"type": "finding_to_diagnosis", "template": "Which condition is characterized by **{key_finding}**?", "data_field": "key_finding"},
    {"type": "urgency_recognition", "template": "A patient with **{symptoms}** requires what level of urgency?", "data_field": "symptoms"}
]

# ===== AI ADAPTIVE LEARNING ENGINE =====
def initialize_resident_diagnosis_tracking(resident_id):
    """Initialize detailed tracking for each diagnosis"""
    categories = list(set([info["category"] for info in diagnoses.values()]))
    
    if resident_id not in st.session_state.resident_tracking:
        st.session_state.resident_tracking[resident_id] = {
            "question_count": 0,
            "correct_count": 0,
            "category_performance": {category: {"correct": 0, "total": 0} for category in categories},
            "first_login": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

def get_adaptive_question():
    """Intelligent question selection"""
    if not st.session_state.resident_id:
        return random.choice(list(diagnoses.keys()))
    
    resident_data = st.session_state.resident_tracking.get(st.session_state.resident_id, {})
    
    if not resident_data or resident_data["question_count"] == 0:
        return random.choice(list(diagnoses.keys()))
    
    # Find weakest category
    weak_categories = []
    for category, perf in resident_data["category_performance"].items():
        if perf["total"] > 0 and (perf["correct"] / perf["total"]) < 0.6:
            weak_categories.append(category)
    
    if weak_categories:
        selected_category = random.choice(weak_categories)
    else:
        selected_category = random.choice(list(set([info["category"] for info in diagnoses.values()])))
    
    # Get diagnoses from selected category
    category_diagnoses = [dx for dx, info in diagnoses.items() if info["category"] == selected_category]
    return random.choice(category_diagnoses)

def generate_adaptive_question():
    """Generate a new adaptive learning question"""
    correct_dx = get_adaptive_question()
    dx_info = diagnoses[correct_dx]
    
    question_template = random.choice(question_templates)
    
    if question_template["type"] == "urgency_recognition":
        symptoms = random.sample(dx_info["symptoms"], min(2, len(dx_info["symptoms"])))
        question = question_template["template"].format(symptoms=", ".join(symptoms))
        options = ["EMERGENT", "URGENT", "ROUTINE", "ELECTIVE"]
        correct_answer = dx_info["urgency"]
    else:
        data_to_show = dx_info[question_template["data_field"]]
        if isinstance(data_to_show, list):
            data_to_show = random.sample(data_to_show, min(2, len(data_to_show)))
            data_to_show = ", ".join(data_to_show)
        
        question = question_template["template"].format(**{question_template["data_field"]: data_to_show})
        
        distractors = [dx for dx in diagnoses.keys() if dx != correct_dx]
        options = [correct_dx] + random.sample(distractors, 3)
        correct_answer = correct_dx
    
    random.shuffle(options)
    
    return {
        "question": question,
        "options": options,
        "correct_answer": correct_answer,
        "diagnosis": correct_dx,
        "explanation": f"**Category:** {dx_info['category']}\n\n**Key Finding:** {dx_info['key_finding']}\n\n**Urgency:** {dx_info['urgency']}",
        "teaching_points": dx_info["teaching"],
        "mode": "adaptive"
    }

# ===== STREAMLIT APP CONFIGURATION =====
st.set_page_config(
    page_title="Ophthalmology AI Trainer",
    page_icon="👁️",
    layout="wide"
)

# Calculate statistics
categories = list(set([info["category"] for info in diagnoses.values()]))
category_counts = {}
for dx_info in diagnoses.values():
    cat = dx_info["category"]
    category_counts[cat] = category_counts.get(cat, 0) + 1
total_diagnoses = len(diagnoses)

# ===== HEADER =====
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1A237E, #1565C0);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
">
    <h1 style="color: white; margin: 0;">👁️ Ophthalmology AI Trainer</h1>
    <p style="margin: 0.5rem 0 0 0;">{total_diagnoses} Diagnoses • {len(categories)} Specialties • AI-Powered Learning</p>
</div>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 👨‍⚕️ Platform Access")
    
    user_type = st.radio("Login as:", ["Resident", "Program Director"])
    st.session_state.user_type = user_type
    
    if user_type == "Resident":
        resident_id = st.text_input("Enter Resident ID:", placeholder="e.g., smith_j")
        
        if resident_id and resident_id.strip():
            resident_id = resident_id.strip()
            st.session_state.resident_id = resident_id
            initialize_resident_diagnosis_tracking(resident_id)
            st.session_state.resident_tracking[resident_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            st.success(f"✅ **Resident:** {resident_id}")
            
            training_mode = st.selectbox(
                "Training Mode:",
                ["Adaptive Learning", "Virtual Patients", "Board Exam Prep"]
            )
            st.session_state.current_mode = training_mode
            
            # Resident analytics
            resident_data = st.session_state.resident_tracking[resident_id]
            accuracy = (resident_data["correct_count"] / resident_data["question_count"] * 100) if resident_data["question_count"] > 0 else 0
            
            st.markdown("### 📊 Your Performance")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Questions", resident_data["question_count"])
            with col2:
                st.metric("Accuracy", f"{accuracy:.1f}%")
            
            # Progress by category
            st.markdown("#### 📈 Category Performance")
            for category, perf in resident_data["category_performance"].items():
                if perf["total"] > 0:
                    accuracy_pct = (perf["correct"] / perf["total"] * 100)
                    st.write(f"**{category}:** {perf['correct']}/{perf['total']} ({accuracy_pct:.0f}%)")
                    st.progress(perf["correct"] / perf["total"])
    
    elif user_type == "Program Director":
        program_id = st.selectbox("Select Program:", list(residency_programs.keys()))
        if program_id:
            st.session_state.program_id = program_id
            st.success(f"👨‍🏫 **Program:** {residency_programs[program_id]['name']}")

# ===== TRAINING MODULES =====
def show_adaptive_learning():
    """Adaptive learning interface"""
    st.markdown("### 🧠 Adaptive Learning")
    
    if st.session_state.user_type == "Resident" and st.session_state.resident_id:
        if st.button("🎯 Generate New Question", type="primary", use_container_width=True):
            st.session_state.current_question = generate_adaptive_question()
            st.session_state.answer_submitted = False
            st.rerun()

def show_virtual_patients():
    """Virtual patients interface"""
    st.markdown("### 🏥 Virtual Patient Cases")
    
    if st.session_state.current_patient_case is None:
        case_id = random.choice(list(virtual_patients.keys()))
        st.session_state.current_patient_case = virtual_patients[case_id]
    
    case = st.session_state.current_patient_case
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"#### 📋 {case['title']}")
        st.write(f"**Patient:** {case['patient']}")
        st.write(f"**History:** {case['history']}")
        st.write(f"**Presentation:** {case['presentation']}")
        
        with st.expander("📊 Clinical Details"):
            st.write("**Symptoms:**")
            for symptom in case['symptoms']:
                st.write(f"- {symptom}")
    
    with col2:
        st.markdown("#### 🔍 Differential Diagnosis")
        st.write(f"Consider: **{case['correct_diagnosis']}**")
    
    # Case question
    if case.get('questions') and st.session_state.current_question is None:
        q_data = case['questions'][0]
        st.session_state.current_question = {
            "question": q_data["question"],
            "options": q_data["options"],
            "correct_answer": q_data["correct_answer"],
            "explanation": q_data["explanation"],
            "teaching_points": case.get('teaching_points', []),
            "mode": "virtual_patient"
        }
        st.session_state.answer_submitted = False

def show_board_prep():
    """Board exam preparation"""
    st.markdown("### 📚 Board Exam Prep")
    
    if st.button("📝 Generate Board Question", type="primary", use_container_width=True):
        question_data = random.choice(list(board_questions.values()))
        st.session_state.current_question = {
            "question": question_data["stem"],
            "options": question_data["options"],
            "correct_answer": question_data["correct_answer"],
            "explanation": question_data["explanation"],
            "mode": "board_prep"
        }
        st.session_state.answer_submitted = False
        st.rerun()

def show_program_dashboard():
    """Program director dashboard"""
    if not st.session_state.program_id:
        st.info("Please select a program from the sidebar")
        return
    
    program_id = st.session_state.program_id
    program = residency_programs[program_id]
    
    st.markdown(f"### 👨‍🏫 Program Dashboard - {program['name']}")
    st.info("Program director features coming soon...")

# ===== QUESTION DISPLAY AND HANDLING =====
def display_question():
    """Display current question and handle answers"""
    if not st.session_state.current_question:
        return
    
    q = st.session_state.current_question
    
    st.markdown("---")
    st.markdown("#### 📋 Question")
    st.info(q["question"])
    
    # Create a unique key for the radio button based on question content
    radio_key = f"answer_{hash(q['question'])}"
    
    selected = st.radio("Select your answer:", q["options"], key=radio_key)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Submit Answer", type="secondary", use_container_width=True):
            handle_answer_submission(selected, q)
    
    with col2:
        if st.button("🔄 New Question", type="primary", use_container_width=True):
            st.session_state.current_question = None
            st.session_state.answer_submitted = False
            if st.session_state.current_mode == "Virtual Patients":
                st.session_state.current_patient_case = None
            st.rerun()
    
    # Show explanation if answer was submitted
    if st.session_state.answer_submitted:
        st.markdown("#### 📖 Explanation")
        st.write(q["explanation"])
        
        if "teaching_points" in q and q["teaching_points"]:
            st.markdown("#### 🎓 Key Points")
            for point in q["teaching_points"]:
                st.write(f"• {point}")

def handle_answer_submission(selected, q):
    """Handle answer submission and update tracking"""
    if st.session_state.user_type == "Resident" and st.session_state.resident_id:
        resident_id = st.session_state.resident_id
        resident_data = st.session_state.resident_tracking[resident_id]
        
        resident_data["question_count"] += 1
        
        # Update category performance
        if 'diagnosis' in q and q['diagnosis'] in diagnoses:
            dx_info = diagnoses[q['diagnosis']]
            category = dx_info["category"]
            resident_data["category_performance"][category]["total"] += 1
            
            if selected == q["correct_answer"]:
                resident_data["correct_count"] += 1
                resident_data["category_performance"][category]["correct"] += 1
                st.success("### ✅ Correct!")
            else:
                st.error(f"### ❌ Incorrect. Correct answer: {q['correct_answer']}")
        else:
            # For board questions without specific diagnosis
            if selected == q["correct_answer"]:
                resident_data["correct_count"] += 1
                st.success("### ✅ Correct!")
            else:
                st.error(f"### ❌ Incorrect. Correct answer: {q['correct_answer']}")
        
        resident_data["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    st.session_state.answer_submitted = True
    st.rerun()

# ===== MAIN APP LAYOUT =====
col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.user_type == "Program Director":
        show_program_dashboard()
    else:
        # Show current training mode
        if st.session_state.current_mode == "Adaptive Learning":
            show_adaptive_learning()
        elif st.session_state.current_mode == "Virtual Patients":
            show_virtual_patients()
        elif st.session_state.current_mode == "Board Exam Prep":
            show_board_prep()
        
        # Display current question
        if st.session_state.current_question:
            display_question()
        else:
            st.info("👆 Click 'Generate Question' to start training!")

with col2:
    st.markdown("### 🎯 Training Features")
    
    features = [
        "🤖 AI-Powered Adaptive Learning",
        "🏥 Virtual Patient Simulations", 
        "📚 Board Exam Preparation",
        "📊 Real-time Analytics",
        "👥 Multi-program Support"
    ]
    
    for feature in features:
        st.write(f"• {feature}")
    
    st.markdown("### 📈 Specialties Covered")
    for category, count in category_counts.items():
        st.write(f"• **{category}:** {count} diagnoses")
    
    if st.session_state.user_type == "Resident" and st.session_state.resident_id:
        resident_data = st.session_state.resident_tracking.get(st.session_state.resident_id, {})
        if resident_data and resident_data["question_count"] > 0:
            accuracy = (resident_data["correct_count"] / resident_data["question_count"] * 100)
            st.metric("Your Accuracy", f"{accuracy:.1f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>Ophthalmology AI Trainer</strong> • Medical Education Platform</p>
</div>
""", unsafe_allow_html=True)
