import streamlit as st
import random
from datetime import datetime, timedelta
import numpy as np

# ===== COMPREHENSIVE OPHTHALMOLOGY DATABASE (60+ DIAGNOSES) =====

# ===== Initialize session state variables (added by ChatGPT patch) =====
def _init_ss():
    if "current_mode" not in st.session_state:
        st.session_state["current_mode"] = None
    if "current_patient_case" not in st.session_state:
        st.session_state["current_patient_case"] = None
    if "current_question" not in st.session_state:
        st.session_state["current_question"] = None
    if "program_id" not in st.session_state:
        st.session_state["program_id"] = None
    if "resident_id" not in st.session_state:
        st.session_state["resident_id"] = None
    if "resident_tracking" not in st.session_state:
        st.session_state["resident_tracking"] = {}
    if "user_type" not in st.session_state:
        st.session_state["user_type"] = None
_init_ss()

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
    },

    # PEDIATRIC OPHTHALMOLOGY (8 diagnoses)
    "Amblyopia": {
        "symptoms": ["reduced vision one eye", "asymptomatic in children"],
        "key_finding": "vision loss without structural abnormality",
        "urgency": "URGENT - critical period treatment",
        "category": "Pediatrics",
        "teaching": ["Treatment effective before age 7-10", "Patching mainstay of therapy"]
    },
    "Strabismus": {
        "symptoms": ["misaligned eyes", "diplopia", "head tilt"],
        "key_finding": "ocular misalignment on cover test",
        "urgency": "URGENT - pediatric referral",
        "category": "Pediatrics",
        "teaching": ["Early treatment prevents amblyopia", "Surgical and non-surgical options"]
    },
    "Congenital Cataract": {
        "symptoms": ["leukocoria", "nystagmus", "poor fixation"],
        "key_finding": "lens opacity in infant",
        "urgency": "EMERGENT - surgical timing critical",
        "category": "Pediatrics",
        "teaching": ["Surgery within first 6-8 weeks", "Risk of amblyopia high"]
    },
    "Retinopathy of Prematurity": {
        "symptoms": ["asymptomatic in premature infant"],
        "key_finding": "peripheral retinal neovascularization",
        "urgency": "URGENT - serial screening needed",
        "category": "Pediatrics",
        "teaching": ["Screen infants <1500g or <30 weeks", "Laser treatment for plus disease"]
    },
    "Congenital Nasolacrimal Duct Obstruction": {
        "symptoms": ["tearing", "mucoid discharge", "no redness"],
        "key_finding": "increased tear film, reflux on pressure",
        "urgency": "ROUTINE - most resolve spontaneously",
        "category": "Pediatrics",
        "teaching": ["90% resolve by 12 months", "Probing if persistent after 1 year"]
    },
    "Pediatric Uveitis": {
        "symptoms": ["asymptomatic", "redness", "photophobia"],
        "key_finding": "anterior chamber inflammation",
        "urgency": "URGENT - JIA association",
        "category": "Pediatrics",
        "teaching": ["Often associated with juvenile idiopathic arthritis", "Screen for asymptomatic uveitis"]
    },
    "Coats Disease": {
        "symptoms": ["leukocoria", "strabismus", "vision loss"],
        "key_finding": "retinal telangiectasia, exudation",
        "urgency": "URGENT - pediatric referral",
        "category": "Pediatrics",
        "teaching": ["Typically unilateral in young males", "Laser or cryotherapy treatment"]
    },
    "Persistent Fetal Vasculature": {
        "symptoms": ["leukocoria", "microphthalmia", "cataract"],
        "key_finding": "retrolental membrane, stretched ciliary processes",
        "urgency": "URGENT - surgical consideration",
        "category": "Pediatrics",
        "teaching": ["Unilateral congenital anomaly", "Poor visual prognosis typically"]
    },

    # OCULOPLASTICS (7 diagnoses)
    "Basal Cell Carcinoma": {
        "symptoms": ["pearly nodule", "ulceration", "telangiectasia"],
        "key_finding": "rodent ulcer with rolled borders",
        "urgency": "URGENT - excision needed",
        "category": "Oculoplastics",
        "teaching": ["Most common eyelid malignancy", "Sun exposure major risk factor"]
    },
    "Thyroid Eye Disease": {
        "symptoms": ["proptosis", "lid retraction", "diplopia"],
        "key_finding": "exophthalmos, lid lag, restrictive strabismus",
        "urgency": "URGENT - thyroid workup",
        "category": "Oculoplastics",
        "teaching": ["Associated with Graves disease", "Monitor for optic neuropathy"]
    },
    "Ptosis": {
        "symptoms": ["droopy eyelid", "visual field obstruction", "forehead fatigue"],
        "key_finding": "low marginal reflex distance",
        "urgency": "ELECTIVE - functional or cosmetic",
        "category": "Oculoplastics",
        "teaching": ["Measure levator function", "Rule out myasthenia gravis"]
    },
    "Dacryocystitis": {
        "symptoms": ["pain", "redness medial canthus", "purulent discharge"],
        "key_finding": "tender mass medial canthus, reflux pus",
        "urgency": "URGENT - antibiotic treatment",
        "category": "Oculoplastics",
        "teaching": ["Nasolacrimal duct obstruction", "DCR surgery for recurrence"]
    },
    "Orbital Cellulitis": {
        "symptoms": ["pain", "proptosis", "decreased motility", "fever"],
        "key_finding": "orbital signs with systemic symptoms",
        "urgency": "EMERGENT - IV antibiotics",
        "category": "Oculoplastics",
        "teaching": ["Often sinusitis complication", "CT scan to rule out abscess"]
    },
    "Chalazion": {
        "symptoms": ["painless lid lump", "mild redness", "cosmetic concern"],
        "key_finding": "non-tender meibomian gland nodule",
        "urgency": "ROUTINE - conservative management",
        "category": "Oculoplastics",
        "teaching": ["Chronic granulomatous inflammation", "Warm compresses first line"]
    },
    "Ectropion/Entropion": {
        "symptoms": ["watering", "irritation", "redness"],
        "key_finding": "eyelid turning outward/inward",
        "urgency": "ELECTIVE - surgical correction",
        "category": "Oculoplastics",
        "teaching": ["Common in elderly", "Surgical repair effective"]
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
        "images": {
            "fundus": "👁️ Moderate NPDR with dot-blot hemorrhages",
            "oct": "📊 Central macular thickness 320μm",
            "fa": "🔬 Microaneurysms with late leakage"
        },
        "vitals": {"BP": "165/95", "HR": "88", "BMI": "32"},
        "labs": {"HbA1c": "9.2%", "Creatinine": "1.2", "LDL": "145"},
        "timeline": [
            {"time": "Initial", "findings": "Mild NPDR, no DME"},
            {"time": "6 months", "findings": "Moderate NPDR, early DME"},
            {"time": "12 months", "findings": "Severe NPDR, clinically significant DME"}
        ],
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
        "correct_diagnosis": "Diabetic Macular Edema with NPDR",
        "differential_diagnosis": ["Macular degeneration", "Retinal vein occlusion", "Vitreomacular traction"],
        "teaching_points": [
            "Tight glycemic control slows progression",
            "Anti-VEGF first-line for center-involving DME", 
            "Monitor for progression to PDR"
        ],
        "category": "Retina",
        "difficulty": "Intermediate",
        "urgency": "URGENT - needs treatment"
    },
    "case_002": {
        "title": "Acute Angle Closure Crisis",
        "patient": "62yo female with hyperopia",
        "history": "No significant medical history, family history of glaucoma",
        "presentation": "Sudden eye pain, headache, nausea, and halos around lights",
        "symptoms": ["severe eye pain", "headache", "nausea", "halos", "vision loss"],
        "images": {
            "slit_lamp": "🔍 Corneal edema, shallow anterior chamber",
            "gonioscopy": "📐 Closed angles in all quadrants",
            "iop": "📊 IOP: 52 mmHg"
        },
        "vitals": {"BP": "180/100", "HR": "102", "Pain": "10/10"},
        "emergency_actions": [
            "Immediate IOP-lowering medications",
            "Systemic acetazolamide 500mg IV",
            "Topical beta-blockers and alpha-agonists",
            "Laser iridotomy within 12-24 hours"
        ],
        "correct_diagnosis": "Acute Angle Closure Glaucoma",
        "urgency": "EMERGENT",
        "category": "Glaucoma",
        "difficulty": "Advanced"
    },
    "case_003": {
        "title": "Pediatric Vision Screening",
        "patient": "4yo female with failed preschool vision screening",
        "history": "Full-term birth, no medical issues, normal development",
        "presentation": "Parents noticed occasional eye turning",
        "symptoms": ["asymptomatic", "occasional eye deviation"],
        "images": {
            "vision": "📏 OD: 20/100, OS: 20/25",
            "refraction": "👓 OD: +3.50, OS: +1.00",
            "alignment": "🎯 Intermittent esotropia"
        },
        "assessment": "Amblyopia secondary to anisometropia and strabismus",
        "treatment_plan": [
            "Full cycloplegic refraction",
            "Glasses prescription",
            "Patching OD 2-4 hours daily",
            "Follow-up in 3 months"
        ],
        "correct_diagnosis": "Amblyopia with Strabismus",
        "category": "Pediatrics",
        "difficulty": "Intermediate"
    }
}

# ===== BOARD EXAM QUESTION BANK =====
board_questions = {
    "q_001": {
        "type": "board_single_best",
        "stem": "A 65-year-old woman presents with sudden, painless loss of vision in her right eye. Examination reveals a relative afferent pupillary defect and a cherry-red spot. The most likely diagnosis is:",
        "options": [
            "A: Central retinal vein occlusion",
            "B: Branch retinal artery occlusion", 
            "C: Central retinal artery occlusion",
            "D: Ischemic optic neuropathy",
            "E: Retinal detachment"
        ],
        "correct_answer": "C: Central retinal artery occlusion",
        "explanation": "**Correct Answer: C - Central retinal artery occlusion**\n\n**Key Points:**\n- Cherry-red spot is pathognomonic for CRAO\n- Sudden, painless vision loss with APD\n- 90-minute window for potential intervention\n- Emergency ophthalmology consultation required",
        "category": "Retina",
        "difficulty": "High",
        "references": ["AAO BCSC: Retina and Vitreous", "Ophthalmology, 4th ed., Yanoff & Duker"]
    },
    "q_002": {
        "type": "board_single_best",
        "stem": "A 72-year-old man with hypertension presents with gradual vision loss. Funduscopy reveals arteriovenous nicking, copper wiring, and flame-shaped hemorrhages. The most likely diagnosis is:",
        "options": [
            "A: Diabetic retinopathy",
            "B: Hypertensive retinopathy",
            "C: Retinal vein occlusion",
            "D: Macular degeneration",
            "E: Optic neuritis"
        ],
        "correct_answer": "B: Hypertensive retinopathy",
        "explanation": "**Correct Answer: B - Hypertensive retinopathy**\n\n**Key Points:**\n- AV nicking and copper wiring characteristic of hypertension\n- Reflects systemic vascular damage\n- Requires urgent blood pressure management",
        "category": "Retina",
        "difficulty": "Medium"
    }
}

# ===== RESIDENCY PROGRAM MANAGEMENT =====
residency_programs = {
    "UCSF_Ophthalmology": {
        "program_id": "UCSF_2024",
        "name": "UCSF Department of Ophthalmology",
        "director": "Dr. Sarah Jenkins",
        "curriculum": {
            "PGY1": ["Basic optics", "Refraction", "Common conjunctivitides"],
            "PGY2": ["Cataract surgery basics", "Glaucoma workup", "Retina fundamentals"],
            "PGY3": ["Advanced surgical techniques", "Neuro-ophthalmology", "Uveitis"],
            "PGY4": ["Complex cases", "Subspecialty depth", "Chief resident cases"]
        },
        "required_competencies": {
            "Retina": 25, "Glaucoma": 20, "Cornea": 15, "Neuro-Ophthalmology": 10, "Pediatrics": 10
        },
        "residents": ["smith_j", "johnson_m", "lee_r", "garcia_p"],
        "faculty": ["jenkins_s", "wong_k", "patel_r"],
        "current_rotation": "Retina"
    },
    "Hopkins_Eye": {
        "program_id": "HOPKINS_2024",
        "name": "Wilmer Eye Institute",
        "director": "Dr. Michael Chen",
        "residents": ["davis_r", "martinez_j", "brown_k"],
        "current_rotation": "Glaucoma"
    }
}

# ===== ENHANCED QUESTION SYSTEM =====
question_templates = [
    {"type": "symptoms_to_diagnosis", "template": "A patient presents with **{symptoms}**. The most likely diagnosis is:", "data_field": "symptoms"},
    {"type": "finding_to_diagnosis", "template": "Which condition is characterized by **{key_finding}**?", "data_field": "key_finding"},
    {"type": "urgency_recognition", "template": "A patient with **{symptoms}** requires what level of urgency?", "data_field": "symptoms"}
]

# ===== AI ADAPTIVE LEARNING ENGINE (No Plotly) =====
def initialize_resident_diagnosis_tracking(resident_id):
    """Initialize detailed tracking for each diagnosis"""
    categories = list(set([info["category"] for info in diagnoses.values()]))
    
    if resident_id not in st.session_state.resident_tracking:
        st.session_state.resident_tracking[resident_id] = {
            "question_count": 0,
            "correct_count": 0,
            "category_performance": {category: {"correct": 0, "total": 0} for category in categories},
            "diagnosis_performance": {dx: {"correct": 0, "total": 0, "last_seen": None} for dx in diagnoses.keys()},
            "first_login": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "training_mode": "Adaptive Learning"
        }

def get_adaptive_question(resident_id):
    """Intelligent question selection based on performance"""
    if resident_id not in st.session_state.resident_tracking:
        return random.choice(list(diagnoses.keys()))
    
    resident_data = st.session_state.resident_tracking[resident_id]
    
    # Find weakest category
    weak_categories = []
    for category, perf in resident_data["category_performance"].items():
        if perf["total"] > 2 and (perf["correct"] / perf["total"]) < 0.6:
            weak_categories.append(category)
    
    if weak_categories:
        selected_category = random.choice(weak_categories)
    else:
        selected_category = random.choice(list(set([info["category"] for info in diagnoses.values()])))
    
    # Get diagnoses from selected category
    category_diagnoses = [dx for dx, info in diagnoses.items() if info["category"] == selected_category]
    return random.choice(category_diagnoses)

# ===== SIMPLIFIED ANALYTICS (No Plotly) =====
def create_text_progress_bar(percentage, width=20):
    """Create a text-based progress bar"""
    filled = "█" * int(percentage * width / 100)
    empty = "░" * (width - len(filled))
    return f"{filled}{empty} {percentage:.1f}%"

def create_program_dashboard(program_id):
    """Create program dashboard without Plotly"""
    if program_id not in residency_programs:
        return None
    
    program = residency_programs[program_id]
    residents_data = []
    
    for resident_id in program["residents"]:
        if resident_id in st.session_state.resident_tracking:
            resident_data = st.session_state.resident_tracking[resident_id]
            accuracy = (resident_data["correct_count"] / resident_data["question_count"] * 100) if resident_data["question_count"] > 0 else 0
            residents_data.append({
                "id": resident_id,
                "questions_answered": resident_data["question_count"],
                "accuracy": accuracy
            })
    
    return residents_data

# ===== STREAMLIT APP CONFIGURATION =====
st.set_page_config(
    page_title="Ophthalmology AI Trainer - Enterprise Edition",
    page_icon="👁️",
    layout="wide"
)

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

# Calculate statistics
categories = list(set([info["category"] for info in diagnoses.values()]))
category_counts = {}
for dx_info in diagnoses.values():
    cat = dx_info["category"]
    category_counts[cat] = category_counts.get(cat, 0) + 1
total_diagnoses = len(diagnoses)

# ===== ENHANCED UI HEADER =====
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
    <p style="margin: 0.5rem 0 0 0;">{total_diagnoses} Diagnoses • 6 Specialties • AI-Powered Learning</p>
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
            initialize_resident_diagnosis_tracking(resident_id)
            st.session_state.resident_tracking[resident_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            st.success(f"✅ **Resident:** {resident_id}")
            
            # Training mode selection
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
                    cat_accuracy = (perf["correct"] / perf["total"] * 100)
                    st.write(f"**{category}:** {perf['correct']}/{perf['total']}")
                    st.progress(perf["correct"] / perf["total"])
    
    elif user_type == "Program Director":
        program_id = st.selectbox("Select Program:", list(residency_programs.keys()))
        if program_id:
            st.success(f"👨‍🏫 **Program:** {residency_programs[program_id]['name']}")

# ===== TRAINING MODULES =====
def show_adaptive_learning():
    """Adaptive learning interface"""
    st.markdown("### 🧠 Adaptive Learning")
    
    if st.session_state.user_type == "Resident" and "resident_id" in locals():
        resident_id = st.session_state.resident_id
        
        if st.button("🎯 Generate Smart Question", type="primary", use_container_width=True):
            correct_dx = get_adaptive_question(resident_id)
            dx_info = diagnoses[correct_dx]
            
            question_template = random.choice(question_templates)
            
            if question_template["type"] == "urgency_recognition":
                symptoms = random.sample(dx_info["symptoms"], min(2, len(dx_info["symptoms"])))
                question = question_template["template"].format(symptoms=", ".join(symptoms))
                options = ["EMERGENT", "URGENT", "ROUTINE", "ELECTIVE"]
                correct_answer = dx_info["urgency"].split(" - ")[0]
            else:
                data_to_show = dx_info[question_template["data_field"]]
                if isinstance(data_to_show, list):
                    data_to_show = random.sample(data_to_show, min(2, len(data_to_show)))
                question = question_template["template"].format(**{question_template["data_field"]: ", ".join(data_to_show) if isinstance(data_to_show, list) else data_to_show})
                
                distractors = [dx for dx in diagnoses.keys() if dx != correct_dx]
                options = [correct_dx] + random.sample(distractors, 3)
                correct_answer = correct_dx
            
            random.shuffle(options)
            
            st.session_state.current_question = {
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "diagnosis": correct_dx,
                "explanation": f"**Category:** {dx_info['category']}\n**Key Finding:** {dx_info['key_finding']}\n**Urgency:** {dx_info['urgency']}",
                "teaching_points": dx_info["teaching"],
                "mode": "adaptive"
            }

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
            if 'vitals' in case:
                st.write("**Vitals:**")
                for k, v in case['vitals'].items():
                    st.write(f"- {k}: {v}")
            if 'images' in case:
                st.write("**Findings:**")
                for k, v in case['images'].items():
                    st.write(f"- {k}: {v}")
    
    with col2:
        st.markdown("#### ⚡ Urgency")
        st.info(case.get('urgency', 'URGENT'))
        
        st.markdown("#### 🔍 Differential")
        for dx in case.get('differential_diagnosis', [])[:3]:
            st.write(f"• {dx}")
    
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

def show_board_prep():
    """Board exam preparation"""
    st.markdown("### 📚 Board Exam Prep")
    
    if st.button("📝 Generate Board Question", type="primary", use_container_width=True):
        question = random.choice(list(board_questions.values()))
        st.session_state.current_question = {
            "question": question["stem"],
            "options": question["options"],
            "correct_answer": question["correct_answer"],
            "explanation": question["explanation"],
            "mode": "board_prep"
        }

def show_program_dashboard():
    """Program director dashboard"""
    if "program_id" not in st.session_state or not st.session_state.program_id:
        st.info("Please select a program from the sidebar")
        return
    
    program_id = st.session_state.program_id
    program = residency_programs[program_id]
    
    st.markdown(f"### 👨‍🏫 Program Dashboard - {program['name']}")
    
    residents_data = create_program_dashboard(program_id)
    
    if not residents_data:
        st.info("No resident data available yet")
        return
    
    # Summary metrics
    total_questions = sum([r["questions_answered"] for r in residents_data])
    avg_accuracy = np.mean([r["accuracy"] for r in residents_data]) if residents_data else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Residents", len(residents_data))
    with col2:
        st.metric("Total Questions", total_questions)
    with col3:
        st.metric("Avg Accuracy", f"{avg_accuracy:.1f}%")
    
    # Resident details
    st.markdown("#### 📊 Resident Performance")
    for resident in residents_data:
        with st.expander(f"Resident {resident['id']}"):
            st.write(f"**Questions Answered:** {resident['questions_answered']}")
            st.write(f"**Accuracy:** {resident['accuracy']:.1f}%")
            st.progress(resident['accuracy'] / 100)

# ===== MAIN APP =====
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
            q = st.session_state.current_question
            
            st.markdown("---")
            st.markdown("#### 📋 Clinical Question")
            st.info(q["question"])
            
            selected = st.radio("Select your answer:", q["options"], key="answer_selection")
            
            if st.button("✅ Submit Answer", type="secondary", use_container_width=True):
                if st.session_state.user_type == "Resident" and "resident_id" in locals():
                    resident_id = st.session_state.resident_id
                    resident_data = st.session_state.resident_tracking[resident_id]
                    
                    resident_data["question_count"] += 1
                    if 'diagnosis' in q:
                        dx_info = diagnoses[q['diagnosis']]
                        resident_data["category_performance"][dx_info["category"]]["total"] += 1
                    
                    if selected == q["correct_answer"]:
                        resident_data["correct_count"] += 1
                        if 'diagnosis' in q:
                            resident_data["category_performance"][dx_info["category"]]["correct"] += 1
                        st.success("### ✅ Correct!")
                    else:
                        st.error(f"### ❌ Correct: {q['correct_answer']}")
                    
                    resident_data["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                st.markdown("#### 📖 Explanation")
                st.write(q["explanation"])
                
                if "teaching_points" in q:
                    st.markdown("#### 🎓 Key Points")
                    for point in q["teaching_points"]:
                        st.write(f"• {point}")
                
                if st.button("🔄 New Question", type="primary"):
                    st.session_state.current_question = None
                    if st.session_state.current_mode == "Virtual Patients":
                        st.session_state.current_patient_case = None
                    st.rerun()

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
    for category, count in list(category_counts.items())[:6]:
        st.write(f"• **{category}:** {count} diagnoses")
    
    if st.session_state.user_type == "Resident" and "resident_id" in locals():
        resident_data = st.session_state.resident_tracking.get(st.session_state.resident_id, {})
        if resident_data:
            accuracy = (resident_data["correct_count"] / resident_data["question_count"] * 100) if resident_data["question_count"] > 0 else 0
            st.metric("Your Accuracy", f"{accuracy:.1f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>Ophthalmology AI Trainer</strong> • Medical Education Platform</p>
</div>
""", unsafe_allow_html=True)
