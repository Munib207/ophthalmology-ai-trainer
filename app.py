import streamlit as st
import random

# ===== COMPREHENSIVE OPHTHALMOLOGY DATABASE (45+ DIAGNOSES) =====
diagnoses = {
    # RETINA (15 diagnoses)
    "CRAO (Central Retinal Artery Occlusion)": {
        "symptoms": ["sudden painless vision loss", "complete blackness"],
        "key_finding": "APD, cherry red spot", 
        "urgency": "EMERGENT - 4-6 hour window",
        "category": "Retina",
        "teaching": ["Time is vision! 4-6 hour window", "Always check for APD", "Look for cherry red spot"]
    },
    "Retinal Detachment": {
        "symptoms": ["floaters", "flashes", "curtain over vision"],
        "key_finding": "visual field defect, retinal tear",
        "urgency": "URGENT - 24-48 hours", 
        "category": "Retina",
        "teaching": ["Ask about floaters and flashes", "Check visual fields", "Ultra-sound if no view"]
    },
    "CRVO (Central Retinal Vein Occlusion)": {
        "symptoms": ["gradual vision loss", "multiple dark spots"],
        "key_finding": "retinal hemorrhages, disc edema",
        "urgency": "URGENT - needs workup",
        "category": "Retina",
        "teaching": ["Workup for hypertension/diabetes", "Monitor for neovascularization"]
    },
    "BRVO (Branch Retinal Vein Occlusion)": {
        "symptoms": ["sudden vision loss", "field defect"],
        "key_finding": "sectoral retinal hemorrhages",
        "urgency": "URGENT - macular edema risk",
        "category": "Retina",
        "teaching": ["Sectoral pattern characteristic", "Treat macular edema if present"]
    },
    "Diabetic Retinopathy (NPDR)": {
        "symptoms": ["asymptomatic", "gradual vision loss"],
        "key_finding": "microaneurysms, dot-blot hemorrhages",
        "urgency": "ROUTINE - annual screening",
        "category": "Retina", 
        "teaching": ["Annual dilated exams for diabetics", "Tight glycemic control slows progression"]
    },
    "Diabetic Retinopathy (PDR)": {
        "symptoms": ["floaters", "vision loss", "asymptomatic"],
        "key_finding": "neovascularization, vitreous hemorrhage",
        "urgency": "URGENT - needs laser",
        "category": "Retina",
        "teaching": ["Pan-retinal photocoagulation indicated", "High risk of vision loss"]
    },
    "Diabetic Macular Edema": {
        "symptoms": ["gradual vision loss", "metamorphopsia"],
        "key_finding": "retinal thickening, hard exudates",
        "urgency": "URGENT - needs treatment",
        "category": "Retina",
        "teaching": ["Anti-VEGF first line treatment", "Laser for non-center involving"]
    },
    "Macular Degeneration (Dry)": {
        "symptoms": ["gradual central vision loss"],
        "key_finding": "drusen, geographic atrophy", 
        "urgency": "ROUTINE - monitoring",
        "category": "Retina",
        "teaching": ["AREDS2 supplements may help", "Low vision rehabilitation"]
    },
    "Macular Degeneration (Wet)": {
        "symptoms": ["rapid central vision loss", "metamorphopsia"],
        "key_finding": "subretinal fluid, hemorrhage, CNV",
        "urgency": "URGENT - anti-VEGF needed",
        "category": "Retina",
        "teaching": ["Anti-VEGF injections mainstay", "Monthly monitoring initially"]
    },
    "Macular Hole": {
        "symptoms": ["central vision loss", "metamorphopsia"],
        "key_finding": "full-thickness retinal defect on OCT",
        "urgency": "URGENT - surgical consideration",
        "category": "Retina", 
        "teaching": ["Vitrectomy often required", "Watch for progression"]
    },
    "Epiretinal Membrane": {
        "symptoms": ["gradual vision loss", "metamorphopsia"],
        "key_finding": "retinal surface wrinkling",
        "urgency": "ELECTIVE - if symptomatic",
        "category": "Retina",
        "teaching": ["Cellophane maculopathy", "Surgery for significant symptoms"]
    },
    "Retinitis Pigmentosa": {
        "symptoms": ["night blindness", "tunnel vision"],
        "key_finding": "bone spicule pigmentation",
        "urgency": "ROUTINE - genetic counseling",
        "category": "Retina",
        "teaching": ["Inherited pattern important", "Low vision services helpful"]
    },
    "Hypertensive Retinopathy": {
        "symptoms": ["asymptomatic", "headaches"],
        "key_finding": "arteriolar narrowing, AV nicking",
        "urgency": "URGENT - BP control",
        "category": "Retina",
        "teaching": ["Grade I-IV severity scale", "Reflects systemic BP control"]
    },
    "Vitreous Hemorrhage": {
        "symptoms": ["sudden floaters", "red haze", "vision loss"],
        "key_finding": "no red reflex, blood in vitreous",
        "urgency": "URGENT - needs ultrasound",
        "category": "Retina",
        "teaching": ["Ultrasound to rule out detachment", "Monitor for clearance"]
    },
    "Retinoblastoma": {
        "symptoms": ["leukocoria", "strabismus", "poor vision"],
        "key_finding": "white retinal mass, calcifications",
        "urgency": "EMERGENT - oncology referral",
        "category": "Retina",
        "teaching": ["Most common pediatric intraocular cancer", "Genetic counseling needed"]
    },

    # GLAUCOMA (8 diagnoses)
    "Angle Closure Glaucoma": {
        "symptoms": ["eye pain", "headache", "nausea", "halos"],
        "key_finding": "elevated IOP, corneal edema",
        "urgency": "EMERGENT - immediate treatment",
        "category": "Glaucoma",
        "teaching": ["Check IOP immediately", "Laser iridotomy definitive treatment"]
    },
    "Open Angle Glaucoma": {
        "symptoms": ["asymptomatic", "peripheral vision loss"],
        "key_finding": "elevated IOP, optic nerve cupping",
        "urgency": "URGENT - needs treatment",
        "category": "Glaucoma",
        "teaching": ["Lifelong medication typically needed", "Monitor progression with fields"]
    },
    "Normal Tension Glaucoma": {
        "symptoms": ["asymptomatic", "field loss"],
        "key_finding": "optic nerve damage with normal IOP",
        "urgency": "URGENT - workup needed",
        "category": "Glaucoma",
        "teaching": ["Treat despite normal pressure", "Consider vascular factors"]
    },
    "Pigmentary Glaucoma": {
        "symptoms": ["young myopic male", "exercise-induced blurring"],
        "key_finding": "Krukenberg spindle, iris transillumination",
        "urgency": "URGENT - needs treatment",
        "category": "Glaucoma",
        "teaching": ["Reverse pupillary block mechanism", "Laser iridotomy may help"]
    },
    "Pseudoexfoliation Glaucoma": {
        "symptoms": ["asymptomatic", "unilateral often"],
        "key_finding": "white material on lens surface",
        "urgency": "URGENT - aggressive course",
        "category": "Glaucoma",
        "teaching": ["Systemic condition", "Poor response to medications"]
    },
    "Neovascular Glaucoma": {
        "symptoms": ["pain", "redness", "vision loss"],
        "key_finding": "iris neovascularization, elevated IOP",
        "urgency": "EMERGENT - pan-retinal photocoagulation",
        "category": "Glaucoma",
        "teaching": ["Always underlying retinal ischemia", "Treat underlying cause"]
    },
    "Uveitic Glaucoma": {
        "symptoms": ["pain", "redness", "photophobia"],
        "key_finding": "inflammation, elevated IOP",
        "urgency": "URGENT - control inflammation first",
        "category": "Glaucoma",
        "teaching": ["Treat inflammation before IOP", "Steroid-induced component"]
    },
    "Congenital Glaucoma": {
        "symptoms": ["infant with tearing", "photophobia", "large eyes"],
        "key_finding": "enlarged cornea, Haab striae",
        "urgency": "EMERGENT - surgical intervention",
        "category": "Glaucoma",
        "teaching": ["Tearing and photophobia classic", "Surgical treatment required"]
    },

    # CORNEA/ANTERIOR SEGMENT (12 diagnoses)
    "Corneal Ulcer": {
        "symptoms": ["severe pain", "purulent discharge", "photophobia"],
        "key_finding": "corneal infiltrate, epithelial defect", 
        "urgency": "URGENT - needs cultures",
        "category": "Cornea",
        "teaching": ["Contact lens major risk factor", "Never patch infected ulcer"]
    },
    "Herpes Simplex Keratitis": {
        "symptoms": ["pain", "redness", "photophobia", "decreased vision"],
        "key_finding": "dendritic ulcer with fluorescein staining",
        "urgency": "EMERGENT - antiviral needed",
        "category": "Cornea",
        "teaching": ["Dendritic pattern pathognomonic", "Avoid steroids initially"]
    },
    "Herpes Zoster Ophthalmicus": {
        "symptoms": ["pain", "vesicular rash in V1 distribution", "redness"],
        "key_finding": "dermatomal rash, keratitis",
        "urgency": "EMERGENT - antiviral treatment",
        "category": "Cornea",
        "teaching": ["V1 distribution characteristic", "Can cause multiple ocular complications"]
    },
    "Cataract": {
        "symptoms": ["gradual vision loss", "glare", "halos", "faded colors"],
        "key_finding": "lens opacity on slit lamp",
        "urgency": "ELECTIVE - when affects QOL",
        "category": "Cataract",
        "teaching": ["Most common reversible blindness", "Surgery when affects ADLs"]
    },
    "Anterior Uveitis": {
        "symptoms": ["eye pain", "photophobia", "redness", "blurred vision"],
        "key_finding": "cells and flare in anterior chamber",
        "urgency": "URGENT - steroid treatment",
        "category": "Uveitis",
        "teaching": ["Look for systemic associations", "Cycloplegics for pain relief"]
    },
    "Pterygium": {
        "symptoms": ["redness", "foreign body sensation", "cosmetic concern"],
        "key_finding": "triangular fibrovascular growth from conjunctiva",
        "urgency": "ELECTIVE - if symptomatic",
        "category": "Cornea",
        "teaching": ["UV light exposure risk factor", "Surgery for growth toward visual axis"]
    },
    "Dry Eye Syndrome": {
        "symptoms": ["burning", "foreign body sensation", "redness", "blurry vision"],
        "key_finding": "reduced tear break-up time, corneal staining",
        "urgency": "ROUTINE - symptomatic treatment",
        "category": "Cornea",
        "teaching": ["Multifactorial condition", "Artificial tears first line"]
    },
    "Blepharitis": {
        "symptoms": ["eyelid crusting", "redness", "itching", "burning"],
        "key_finding": "eyelid margin inflammation, collarettes",
        "urgency": "ROUTINE - lid hygiene",
        "category": "Cornea",
        "teaching": ["Chronic condition", "Lid hygiene cornerstone of treatment"]
    },
    "Conjunctivitis (Bacterial)": {
        "symptoms": ["redness", "purulent discharge", "crusting"],
        "key_finding": "conjunctival injection, discharge",
        "urgency": "URGENT - antibiotic treatment",
        "category": "Cornea",
        "teaching": ["Purulent discharge characteristic", "Topical antibiotics effective"]
    },
    "Conjunctivitis (Viral)": {
        "symptoms": ["redness", "watery discharge", "preauricular lymphadenopathy"],
        "key_finding": "conjunctival injection, follicular reaction",
        "urgency": "URGENT - supportive care",
        "category": "Cornea",
        "teaching": ["Highly contagious", "Supportive treatment usually sufficient"]
    },
    "Conjunctivitis (Allergic)": {
        "symptoms": ["itching", "redness", "watery discharge", "seasonal"],
        "key_finding": "conjunctival injection, papillae",
        "urgency": "ROUTINE - allergen avoidance",
        "category": "Cornea",
        "teaching": ["Itching is hallmark symptom", "Allergen avoidance and antihistamines"]
    },
    "Episcleritis": {
        "symptoms": ["redness", "mild discomfort"],
        "key_finding": "sectoral injection, blanches with phenylephrine",
        "urgency": "ROUTINE - often self-limited",
        "category": "Cornea",
        "teaching": ["Benign condition", "Distinguish from scleritis"]
    },

    # NEURO-OPHTHALMOLOGY (10 diagnoses)
    "Optic Neuritis": {
        "symptoms": ["pain with eye movement", "color desaturation", "vision loss"],
        "key_finding": "APD, optic disc edema",
        "urgency": "URGENT - steroid consideration", 
        "category": "Neuro-Ophthalmology",
        "teaching": ["Often associated with MS", "Pain with movement classic"]
    },
    "Giant Cell Arteritis": {
        "symptoms": ["elderly", "headache", "jaw claudication", "vision loss"],
        "key_finding": "elevated ESR/CRP, disc edema",
        "urgency": "EMERGENT - immediate steroids",
        "category": "Neuro-Ophthalmology",
        "teaching": ["Risk of bilateral blindness", "Start steroids if suspected"]
    },
    "Non-Arteritic Ischemic Optic Neuropathy": {
        "symptoms": ["altitudinal vision loss", "often upon awakening"],
        "key_finding": "disc edema, altitudinal field defect",
        "urgency": "URGENT - vascular workup",
        "category": "Neuro-Ophthalmology",
        "teaching": ["Associated with vascular risk factors", "No proven treatment"]
    },
    "Papilledema": {
        "symptoms": ["transient visual obscurations", "headache", "nausea"],
        "key_finding": "bilateral optic disc edema",
        "urgency": "EMERGENT - rule out mass lesion",
        "category": "Neuro-Ophthalmology",
        "teaching": ["Always bilateral", "Requires neuroimaging and LP"]
    },
    "Third Nerve Palsy": {
        "symptoms": ["diplopia", "ptosis", "dilated pupil"],
        "key_finding": "impaired adduction, elevation, depression",
        "urgency": "EMERGENT - if pupil involved",
        "category": "Neuro-Ophthalmology",
        "teaching": ["Pupil involvement suggests compression", "Medical emergency if pupil involved"]
    },
    "Fourth Nerve Palsy": {
        "symptoms": ["vertical diplopia", "head tilt"],
        "key_finding": "hypertropia worse on contralateral gaze",
        "urgency": "URGENT - workup needed",
        "category": "Neuro-Ophthalmology",
        "teaching": ["Head tilt compensates for extorsion", "Congenital or acquired"]
    },
    "Sixth Nerve Palsy": {
        "symptoms": ["horizontal diplopia", "esotropia"],
        "key_finding": "impaired abduction",
        "urgency": "URGENT - workup needed",
        "category": "Neuro-Ophthalmology",
        "teaching": ["False localizing sign with ICP", "Workup for underlying cause"]
    },
    "Myasthenia Gravis": {
        "symptoms": ["variable ptosis", "diplopia", "fatigability"],
        "key_finding": "fatigable ptosis, ice pack test positive",
        "urgency": "URGENT - neurology referral",
        "category": "Neuro-Ophthalmology",
        "teaching": ["Fatigability characteristic", "Ice pack test diagnostic"]
    },
    "Homonymous Hemianopsia": {
        "symptoms": ["visual field loss", "reading difficulty"],
        "key_finding": "congruous homonymous field defect",
        "urgency": "EMERGENT - if acute",
        "category": "Neuro-Ophthalmology",
        "teaching": ["Localizes to contralateral optic tract", "Stroke workup if acute"]
    },
    "Pituitary Adenoma": {
        "symptoms": ["bitemporal hemianopsia", "headache", "endocrine symptoms"],
        "key_finding": "bitemporal field defect",
        "urgency": "URGENT - endocrine workup",
        "category": "Neuro-Ophthalmology",
        "teaching": ["Bitemporal pattern localizes to chiasm", "Endocrine evaluation essential"]
    }
}

# ===== STREAMLIT APP CONFIGURATION =====
st.set_page_config(
    page_title="Ophthalmology AI Trainer - Comprehensive",
    page_icon="👁️",
    layout="wide"
)

# Initialize session state
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# Calculate statistics
categories = {}
for dx_info in diagnoses.values():
    cat = dx_info["category"]
    categories[cat] = categories.get(cat, 0) + 1

total_diagnoses = len(diagnoses)

# Comprehensive header
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1A237E, #1565C0);
    color: white;
    padding: 2.5rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
">
    <h1 style="color: white; margin: 0; font-size: 2.5rem;">👁️ Ophthalmology AI Trainer</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.3rem; opacity: 0.9;">
        Comprehensive Edition - {total_diagnoses} Diagnoses
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.8;">
        {', '.join([f'{cat} ({count})' for cat, count in categories.items()])}
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar with comprehensive database info
with st.sidebar:
    st.markdown("### 🏥 Database Overview")
    st.metric("Total Diagnoses", total_diagnoses)
    st.metric("Medical Specialties", len(categories))
    
    st.markdown("### 📊 Specialty Distribution")
    for category, count in sorted(categories.items()):
        st.write(f"**{category}:** {count} diagnoses")
    
    st.markdown("### 👨‍⚕️ User Progress")
    accuracy = (st.session_state.correct_count / st.session_state.question_count * 100) if st.session_state.question_count > 0 else 0
    st.metric("Questions Answered", st.session_state.question_count)
    st.metric("Accuracy Rate", f"{accuracy:.1f}%")
    
    if st.button("🔄 Reset Progress", use_container_width=True):
        st.session_state.question_count = 0
        st.session_state.correct_count = 0
        st.session_state.current_question = None
        st.rerun()

# Main app content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💡 Comprehensive Case Training")
    
    if st.button("🎯 Generate New Case", type="primary", use_container_width=True):
        correct_dx = random.choice(list(diagnoses.keys()))
        dx_info = diagnoses[correct_dx]
        
        symptoms = random.sample(dx_info["symptoms"], min(2, len(dx_info["symptoms"])))
        question = f"A patient presents with **{', '.join(symptoms)}**. The most likely diagnosis is:"
        
        # Proper distractor selection for large database
        possible_distractors = [dx for dx in diagnoses.keys() if dx != correct_dx]
        num_distractors = min(3, len(possible_distractors))
        distractors = random.sample(possible_distractors, num_distractors)
        
        options = [correct_dx] + distractors
        random.shuffle(options)
        
        st.session_state.current_question = {
            "question": question,
            "options": options,
            "correct_answer": correct_dx,
            "explanation": f"**Key finding:** {dx_info['key_finding']}. **Urgency:** {dx_info['urgency']}",
            "teaching_points": dx_info["teaching"],
            "category": dx_info["category"]
        }
        st.rerun()

    if st.session_state.current_question:
        q = st.session_state.current_question
        
        st.markdown("#### 📋 Clinical Scenario")
        st.info(f"{q['question']}")
        st.caption(f"**Category:** {q['category']}")
        
        selected_option = st.radio("**Select your diagnosis:**", q["options"])
        
        if st.button("🔍 Submit Diagnosis", type="secondary", use_container_width=True):
            st.session_state.question_count += 1
            if selected_option == q["correct_answer"]:
                st.session_state.correct_count += 1
                st.success("### ✅ Correct Diagnosis!")
            else:
                st.error(f"### ❌ The correct diagnosis is: **{q['correct_answer']}**")
            
            st.markdown("---")
            st.markdown("#### 📖 Detailed Explanation")
            st.markdown(q["explanation"])
            
            st.markdown("#### 🎓 Key Learning Points")
            for i, point in enumerate(q["teaching_points"], 1):
                st.markdown(f"{i}. {point}")

with col2:
    st.markdown("### 🏥 Specialty Explorer")
    
    selected_category = st.selectbox("Filter by specialty:", ["All"] + list(categories.keys()))
    
    if selected_category == "All":
        st.write(f"**All {total_diagnoses} diagnoses available**")
        for category, count in sorted(categories.items()):
            with st.expander(f"{category} ({count} diagnoses)"):
                category_dx = [dx for dx, info in diagnoses.items() if info["category"] == category]
                for dx in category_dx[:5]:  # Show first 5
                    st.write(f"• {dx}")
                if len(category_dx) > 5:
                    st.write(f"• ... and {len(category_dx) - 5} more")
    else:
        st.write(f"**{selected_category} diagnoses:**")
        category_dx = [dx for dx, info in diagnoses.items() if info["category"] == selected_category]
        for dx in category_dx:
            with st.expander(dx):
                info = diagnoses[dx]
                st.write(f"**Urgency:** {info['urgency']}")
                st.write(f"**Key finding:** {info['key_finding']}")

# Comprehensive footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>Comprehensive Ophthalmology AI Trainer</strong> • {total_diagnoses} Diagnoses • {len(categories)} Specialties</p>
    <p><small>Professional medical education platform for ophthalmology training</small></p>
</div>
""", unsafe_allow_html=True)
