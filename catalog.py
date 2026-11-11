"""Structured content used by detail pages, college matching and the local chatbot.

The dictionaries are intentionally plain Python so second-year students can edit
the content without learning a new framework or content-management system.
"""

import re


def slugify(value):
    value = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def _course(name, category, duration, eligibility, subjects, exams, careers, salary, overview=None):
    return {
        "slug": slugify(name),
        "title": name,
        "kind": "course",
        "category": category,
        "overview": overview or f"{name} develops academic knowledge and practical foundations for careers connected to {category}.",
        "eligibility": eligibility,
        "duration": duration,
        "subjects": subjects,
        "entrance_exams": exams,
        "skills": ["Communication", "Problem solving", "Project work"],
        "opportunities": careers,
        "salary": salary,
        "roadmap": ["Check programme-specific eligibility", "Prepare for the required entrance route", "Build projects or practical exposure", "Complete internships and choose a specialisation"],
    }


COURSE_DETAILS = {
    item["slug"]: item
    for item in [
        _course("B.Tech CSE / AI & ML", "Technology", "Usually 4 years", "Class 12 with Physics and Mathematics; institute-specific percentage and subject rules apply.", ["Programming", "Data Structures", "Algorithms", "Databases", "AI and Machine Learning"], ["JEE Main/Advanced", "State CETs", "University entrance tests"], ["Software Developer", "AI/ML Engineer", "Cybersecurity Analyst"], "Common early-career range in India: roughly ₹4–18 LPA; role, skill and employer strongly affect pay."),
        _course("BCA", "Technology", "Usually 3 years; some universities offer 4-year honours structures", "Class 12; mathematics or computer science requirements vary by university.", ["Programming", "Web Development", "Databases", "Computer Networks"], ["CUET UG or university/merit routes"], ["Application Developer", "Web Developer", "IT Support Specialist"], "Often ₹3–10 LPA initially in India, with wide variation."),
        _course("B.Sc Computer Science", "Technology", "Usually 3–4 years", "Class 12, commonly with Mathematics; exact rules vary.", ["Programming", "Algorithms", "Operating Systems", "Computer Architecture"], ["CUET UG", "University admission tests or merit"], ["Software Developer", "Systems Analyst", "Data Analyst"], "Often ₹3–12 LPA initially in India, depending on role and skills."),
        _course("B.Sc Data Science", "Analytical & Research", "Usually 3–4 years", "Class 12, commonly with Mathematics or Statistics.", ["Statistics", "Python", "Data Visualisation", "Machine Learning"], ["CUET UG", "University-specific admission"], ["Data Analyst", "Junior Data Scientist", "Business Intelligence Analyst"], "Often ₹4–14 LPA initially in India; portfolio and internships matter."),
        _course("B.Sc Mathematics", "Analytical & Research", "Usually 3–4 years", "Class 12 with Mathematics and programme-specific marks.", ["Calculus", "Linear Algebra", "Probability", "Real Analysis"], ["CUET UG", "University-specific admission"], ["Statistician", "Actuarial Analyst", "Research Assistant"], "Varies widely; analytics roles commonly begin around ₹4–12 LPA in India."),
        _course("B.Stat / Economics", "Analytical & Research", "Usually 3–4 years", "Class 12 with Mathematics; competitive institutes may have additional tests.", ["Statistics", "Econometrics", "Microeconomics", "Probability"], ["CUET UG", "ISI Admission Test or institute-specific routes"], ["Statistician", "Economist", "Research Analyst"], "Often ₹4–16 LPA initially in analytics/economic research roles."),
        _course("B.Des", "Creative & Design", "Usually 4 years", "Class 12 in a recognised stream; portfolio/test rules vary.", ["Design Fundamentals", "Visual Communication", "User Research", "Prototyping"], ["UCEED", "NID DAT", "Institute design tests"], ["UI/UX Designer", "Product Designer", "Visual Designer"], "Often ₹3–14 LPA initially in India; portfolio quality is important."),
        _course("BA Media & Communication", "Creative & Design", "Usually 3–4 years", "Class 12; programme-specific language/portfolio rules may apply.", ["Media Studies", "Writing", "Digital Production", "Communication Theory"], ["CUET UG", "University tests/interviews"], ["Content Strategist", "Media Planner", "Communications Executive"], "Often ₹3–10 LPA initially in India."),
        _course("BFA / Animation", "Creative & Design", "Usually 3–4 years", "Class 12; many institutes use aptitude tests or portfolios.", ["Drawing", "Animation Principles", "Storyboarding", "Digital Tools"], ["University aptitude tests", "Portfolio/interview"], ["Animator", "Illustrator", "Motion Designer"], "Often ₹3–12 LPA initially in India; freelance income varies."),
        _course("BA Psychology", "People & Service", "Usually 3–4 years", "Class 12; university-specific subject and percentage rules apply.", ["Developmental Psychology", "Social Psychology", "Research Methods", "Statistics"], ["CUET UG", "University-specific admission"], ["HR Associate", "Behavioural Research Assistant", "Counsellor after required higher qualification"], "Often ₹3–9 LPA initially; regulated practice normally needs higher qualifications."),
        _course("B.Ed", "People & Service", "Commonly 2 years after an eligible bachelor's degree", "A recognised bachelor's degree and applicable marks; state/university rules differ.", ["Pedagogy", "Educational Psychology", "Assessment", "Teaching Practice"], ["State/university B.Ed entrance tests"], ["School Teacher", "Education Coordinator", "Curriculum Assistant"], "Often ₹3–8 LPA initially, varying by school system and region."),
        _course("BSW / Sociology", "People & Service", "Usually 3–4 years", "Class 12; institution-specific requirements apply.", ["Social Work", "Sociology", "Community Development", "Fieldwork"], ["CUET UG", "University merit/tests"], ["Social Worker", "Programme Coordinator", "Community Outreach Officer"], "Often ₹3–8 LPA initially in India."),
        _course("BBA", "Business & Leadership", "Usually 3–4 years", "Class 12; mathematics and percentage requirements vary.", ["Management", "Marketing", "Accounting", "Business Analytics"], ["CUET UG", "IPMAT or university tests"], ["Business Analyst", "Marketing Executive", "Operations Associate"], "Often ₹3–12 LPA initially in India."),
        _course("B.Com", "Business & Leadership", "Usually 3–4 years", "Class 12 with programme-specific subject combinations.", ["Accounting", "Finance", "Taxation", "Business Law"], ["CUET UG", "University merit/admission routes"], ["Accountant", "Financial Analyst", "Banking Associate"], "Often ₹3–10 LPA initially; professional qualifications can change outcomes."),
        _course("Economics / Entrepreneurship", "Business & Leadership", "Usually 3–4 years", "Class 12; Economics programmes often require Mathematics.", ["Economics", "Finance", "Innovation", "Business Planning"], ["CUET UG", "University-specific tests"], ["Economist", "Startup Associate", "Entrepreneur"], "Employment ranges vary; entrepreneurship has no guaranteed salary."),
        _course("MBBS / Allied Health", "Health & Life Science", "MBBS is typically 5.5 years including internship; allied-health courses vary", "Class 12 with Physics, Chemistry, Biology/Biotechnology and English under current admission rules.", ["Anatomy", "Physiology", "Pathology", "Clinical Practice"], ["NEET UG for MBBS and applicable counselling", "Institute routes for some allied-health programmes"], ["Doctor after licensing requirements", "Clinical Research Associate", "Allied Health Professional"], "Highly variable by qualification, specialisation, sector and experience."),
        _course("B.Pharm", "Health & Life Science", "Usually 4 years", "Class 12 with Physics, Chemistry and accepted third subject under institute rules.", ["Pharmaceutics", "Pharmacology", "Medicinal Chemistry", "Pharmacognosy"], ["State CETs", "University/institute admission routes"], ["Pharmacist after registration requirements", "Quality Analyst", "Clinical Research Associate"], "Often ₹3–9 LPA initially in India."),
        _course("B.Sc Biotechnology", "Health & Life Science", "Usually 3–4 years", "Class 12 with Biology/Biotechnology or relevant science subjects.", ["Genetics", "Microbiology", "Biochemistry", "Molecular Biology"], ["CUET UG", "University-specific admission"], ["Biotechnologist", "Laboratory Analyst", "Research Assistant"], "Often ₹3–9 LPA initially; research roles may require postgraduate study."),
    ]
}


def _career(name, category, overview, subjects, skills, salary, roadmap):
    return {
        "slug": slugify(name), "title": name, "kind": "career", "category": category,
        "overview": overview, "eligibility": "No single universal qualification. Employers normally expect a relevant degree, demonstrable skills and/or professional requirements for regulated roles.",
        "duration": "Preparation time depends on the education route and specialisation.",
        "subjects": subjects, "entrance_exams": ["Depends on the chosen course and institution"],
        "skills": skills, "opportunities": [name, "Related specialist roles", "Team lead or consulting roles with experience"],
        "salary": salary, "roadmap": roadmap,
    }


CAREER_DETAILS = {
    item["slug"]: item
    for item in [
        _career("Software Developer", "Technology", "Designs, builds, tests and maintains software products.", ["Programming", "Algorithms", "Databases"], ["Coding", "Debugging", "Teamwork"], "Common Indian early-career range: roughly ₹4–12 LPA.", ["Learn one language well", "Build 3–4 projects", "Practise data structures", "Complete an internship and apply"]),
        _career("AI/ML Engineer", "Technology", "Builds data-driven systems that learn patterns or automate predictions.", ["Python", "Statistics", "Machine Learning"], ["Model evaluation", "Data preparation", "Software engineering"], "Common Indian early-career range: roughly ₹6–18 LPA.", ["Master Python and mathematics", "Study ML fundamentals", "Build reproducible projects", "Learn deployment and apply"]),
        _career("Cybersecurity Analyst", "Technology", "Monitors systems, investigates risks and helps protect digital assets.", ["Networks", "Operating Systems", "Security"], ["Threat analysis", "Documentation", "Ethical judgement"], "Common Indian early-career range: roughly ₹4–12 LPA.", ["Learn networking and Linux", "Use legal practice labs", "Study security fundamentals", "Pursue internships/certifications"]),
        _career("Data Analyst", "Analytical & Research", "Turns data into reports, explanations and decision-support insights.", ["Statistics", "SQL", "Visualisation"], ["Data cleaning", "Critical thinking", "Communication"], "Common Indian early-career range: roughly ₹4–10 LPA.", ["Learn spreadsheets and SQL", "Add Python/R", "Build dashboards", "Create a portfolio"]),
        _career("Research Analyst", "Analytical & Research", "Collects evidence, evaluates information and prepares defensible findings.", ["Research Methods", "Statistics", "Domain Knowledge"], ["Source evaluation", "Writing", "Analysis"], "Common Indian early-career range: roughly ₹4–12 LPA.", ["Choose a domain", "Learn research methods", "Write sample reports", "Seek internships"]),
        _career("Statistician", "Analytical & Research", "Applies probability and statistical models to real-world questions.", ["Probability", "Inference", "Regression"], ["Mathematical reasoning", "R/Python", "Interpretation"], "Common Indian range varies widely; postgraduate study is frequent.", ["Build mathematics foundation", "Learn statistical software", "Complete applied projects", "Consider postgraduate study"]),
        _career("UI/UX Designer", "Creative & Design", "Researches user needs and designs usable digital experiences.", ["Interaction Design", "User Research", "Visual Design"], ["Prototyping", "Empathy", "Usability testing"], "Common Indian early-career range: roughly ₹4–12 LPA.", ["Learn design principles", "Master a prototyping tool", "Create case studies", "Test with users and build portfolio"]),
        _career("Content Strategist", "Creative & Design", "Plans useful, consistent content for audiences and business goals.", ["Writing", "Media", "Marketing"], ["Editing", "Audience research", "Planning"], "Common Indian early-career range: roughly ₹3–10 LPA.", ["Build writing samples", "Learn content research", "Measure content results", "Create portfolio"]),
        _career("Animator", "Creative & Design", "Creates motion and visual storytelling for film, games, education or advertising.", ["Drawing", "Animation", "Storytelling"], ["Timing", "Software tools", "Observation"], "Common Indian early-career range: roughly ₹3–10 LPA.", ["Learn fundamentals", "Choose 2D/3D focus", "Create a showreel", "Apply to studios/freelance"]),
        _career("Counsellor", "People & Service", "Supports people through structured listening and evidence-informed guidance.", ["Psychology", "Counselling", "Ethics"], ["Listening", "Empathy", "Boundaries"], "Varies by qualification, setting and region.", ["Study psychology/counselling", "Complete supervised training", "Meet applicable professional requirements", "Build ethical experience"]),
        _career("Teacher", "People & Service", "Plans learning, explains concepts and assesses student progress.", ["Subject Knowledge", "Pedagogy", "Assessment"], ["Explanation", "Classroom management", "Patience"], "Varies by school system, qualification and location.", ["Complete subject degree", "Earn required teacher qualification", "Practice teaching", "Apply through relevant recruitment routes"]),
        _career("Human Resources Specialist", "People & Service", "Supports recruitment, learning, performance and workplace processes.", ["Management", "Psychology", "Labour Context"], ["Communication", "Confidentiality", "Organisation"], "Common Indian early-career range: roughly ₹3–9 LPA.", ["Study HR/business", "Learn HR processes", "Intern with an HR team", "Build analytics and communication skills"]),
        _career("Business Analyst", "Business & Leadership", "Clarifies business problems and translates needs into workable improvements.", ["Business Processes", "Data", "Requirements"], ["Analysis", "Documentation", "Stakeholder communication"], "Common Indian early-career range: roughly ₹5–14 LPA.", ["Learn process mapping", "Build SQL/data basics", "Practise requirement documents", "Seek internships"]),
        _career("Marketing Manager", "Business & Leadership", "Plans campaigns, studies audiences and manages brand or growth activity.", ["Marketing", "Consumer Behaviour", "Analytics"], ["Communication", "Experimentation", "Planning"], "Entry roles often start around ₹3–10 LPA; manager pay requires experience.", ["Learn marketing basics", "Run small campaigns", "Measure results", "Progress from executive to manager"]),
        _career("Entrepreneur", "Business & Leadership", "Builds an organisation around a problem, customer and sustainable business model.", ["Finance", "Marketing", "Operations"], ["Resilience", "Selling", "Decision-making"], "No guaranteed salary; income and risk vary substantially.", ["Validate a real problem", "Test a small solution", "Track costs and customers", "Scale only after evidence"]),
        _career("Doctor / Allied Health Professional", "Health & Life Science", "Diagnoses, treats or supports health needs within defined professional scopes.", ["Biology", "Clinical Sciences", "Patient Care"], ["Precision", "Communication", "Ethics"], "Varies greatly by profession, qualification, sector and experience.", ["Meet science eligibility", "Qualify through the correct admission route", "Complete degree and clinical training", "Meet registration/licensing rules"]),
        _career("Pharmacist", "Health & Life Science", "Supports safe and appropriate use of medicines in community, hospital or industry settings.", ["Pharmacology", "Pharmaceutics", "Chemistry"], ["Accuracy", "Patient communication", "Compliance"], "Common Indian early-career range: roughly ₹3–8 LPA.", ["Complete B.Pharm/D.Pharm route", "Meet registration rules", "Gain supervised experience", "Choose community/hospital/industry path"]),
        _career("Biotechnologist", "Health & Life Science", "Uses biological systems and laboratory methods in research, health, food or industry.", ["Genetics", "Microbiology", "Biochemistry"], ["Laboratory technique", "Data recording", "Scientific reasoning"], "Common Indian early-career range: roughly ₹3–9 LPA.", ["Complete relevant science degree", "Build lab competence", "Gain research/industry internship", "Consider postgraduate specialisation"]),
    ]
}


SKILL_NAMES = {
    "Technology": ["Programming", "Logical thinking", "Problem solving"],
    "Analytical & Research": ["Mathematics", "Data interpretation", "Critical thinking"],
    "Creative & Design": ["Visual communication", "Storytelling", "Design tools"],
    "People & Service": ["Communication", "Empathy", "Listening"],
    "Business & Leadership": ["Leadership", "Financial awareness", "Negotiation"],
    "Health & Life Science": ["Biology", "Observation", "Precision"],
}

SKILL_DETAILS = {}
for category, names in SKILL_NAMES.items():
    for name in names:
        SKILL_DETAILS[slugify(name)] = {
            "slug": slugify(name), "title": name, "kind": "skill", "category": category,
            "overview": f"{name} is a transferable capability used in {category.lower()} study and work.",
            "eligibility": "No formal eligibility; it can be developed through deliberate practice.",
            "duration": "Developed continuously through projects, feedback and experience.",
            "subjects": ["Foundations", "Applied practice", "Communication of results"],
            "entrance_exams": ["Not applicable"], "skills": [name, "Reflection", "Consistent practice"],
            "opportunities": [f"Projects requiring {name.lower()}", "Internships", "Entry-level portfolio work"],
            "salary": "A skill does not have a salary by itself; it improves suitability for related roles.",
            "roadmap": ["Learn the foundation", "Practise on a small task", "Request feedback", "Show evidence in a portfolio"],
        }


TECHNOLOGY_NAMES = {
    "Technology": ["Python", "Cloud Computing", "Cybersecurity Tools"],
    "Analytical & Research": ["SQL", "Power BI", "R Programming"],
    "Creative & Design": ["Figma", "Adobe Creative Cloud", "Blender"],
    "People & Service": ["Learning Management Systems", "Survey Tools", "HR Information Systems"],
    "Business & Leadership": ["Spreadsheets", "CRM Platforms", "Business Intelligence"],
    "Health & Life Science": ["Laboratory Information Systems", "Bioinformatics", "Electronic Health Records"],
}

TECHNOLOGY_DETAILS = {}
for category, names in TECHNOLOGY_NAMES.items():
    for name in names:
        TECHNOLOGY_DETAILS[slugify(name)] = {
            "slug": slugify(name), "title": name, "kind": "technology", "category": category,
            "overview": f"{name} is a commonly encountered technology area or tool in {category.lower()} pathways.",
            "eligibility": "No universal eligibility. Start with introductory tutorials and safe practice projects.",
            "duration": "Basic familiarity may take weeks; professional competence requires repeated project use.",
            "subjects": ["Core concepts", "Hands-on workflow", "Responsible use"],
            "entrance_exams": ["Not applicable"], "skills": ["Tool literacy", "Problem solving", "Documentation"],
            "opportunities": ["Student projects", "Internships", "Role-specific workflows"],
            "salary": "Technology proficiency supports a career but does not guarantee a salary.",
            "roadmap": ["Learn terminology", "Follow one guided project", "Build an independent mini-project", "Document and improve it"],
        }


COLLEGES = [
    {
        "slug": "iit-bombay", "name": "Indian Institute of Technology Bombay", "city": "Mumbai", "state": "Maharashtra", "country": "India", "region": "India", "ownership": "Government",
        "courses": ["B.Tech CSE / AI & ML", "B.Sc Mathematics", "B.Des"],
        "eligibility": "Undergraduate routes include JEE Advanced/JoSAA for engineering and UCEED for design; consult the current programme rules.",
        "admission": "Apply through the applicable national examination and allocation process.",
        "fees": "Official 2024 UG entrant schedule listed ₹1,23,350 academic fees plus ₹16,900 hostel fees for the autumn semester for GEN/EWS/OBC-NCL Indian students; current fees may differ.",
        "fee_currency": "INR", "annual_fee_amount": 280500,
        "official_url": "https://www.iitb.ac.in/", "admission_url": "https://acad.iitb.ac.in/admissions/bachelors", "fee_url": "https://acad.iitb.ac.in/fees-structure-prospective-students",
        "source_note": "Admission and fee links are official IIT Bombay pages.",
    },
    {
        "slug": "university-of-delhi", "name": "University of Delhi", "city": "Delhi", "state": "Delhi", "country": "India", "region": "India", "ownership": "Government",
        "courses": ["B.Com", "BA Psychology", "B.Sc Computer Science", "Economics / Entrepreneurship"],
        "eligibility": "Programme-specific CUET UG subject combinations and eligibility apply.",
        "admission": "For most regular UG programmes, candidates appear for CUET UG and complete the University CSAS process.",
        "fees": "Fees vary by constituent college and programme; verify on the allotted college's official website.",
        "fee_currency": "INR", "annual_fee_amount": None,
        "official_url": "https://www.du.ac.in/", "admission_url": "https://admission.uod.ac.in/", "fee_url": "https://admission.uod.ac.in/",
        "source_note": "The official 2026 FAQ states that CUET UG is mandatory for most regular UG admissions and fees vary by college.",
    },
    {
        "slug": "nid-ahmedabad", "name": "National Institute of Design Ahmedabad", "city": "Ahmedabad", "state": "Gujarat", "country": "India", "region": "India", "ownership": "Government",
        "courses": ["B.Des"],
        "eligibility": "Class 12 or equivalent under the current B.Des handbook, followed by the Design Aptitude Test process.",
        "admission": "Apply only through the official NID admissions portal and follow DAT Prelims/Mains requirements.",
        "fees": "The official fee PDF must be checked for the applicant's nationality and joining batch; hostel and mess charges are separate or variable.",
        "fee_currency": "INR", "annual_fee_amount": None,
        "official_url": "https://www.nid.edu/", "admission_url": "https://admissions.nid.edu/", "fee_url": "https://admissions.nid.edu/NIDA2026/download/BDES_FeeSturcture_202627.pdf",
        "source_note": "NID warns applicants to use only nid.edu and admissions.nid.edu.",
    },
    {
        "slug": "aiims-new-delhi", "name": "AIIMS New Delhi", "city": "New Delhi", "state": "Delhi", "country": "India", "region": "India", "ownership": "Government",
        "courses": ["MBBS / Allied Health", "B.Sc Biotechnology"],
        "eligibility": "For MBBS, current NEET UG eligibility and counselling rules apply; allied-health routes have separate notices.",
        "admission": "MBBS admission is through NEET UG and the applicable counselling/allocation process.",
        "fees": "Refer to the current official prospectus and reporting notice; the portal publishes programme-specific payments.",
        "fee_currency": "INR", "annual_fee_amount": None,
        "official_url": "https://www.aiims.edu/", "admission_url": "https://www.aiimsexams.ac.in/", "fee_url": "https://www.aiimsexams.ac.in/",
        "source_note": "The official AIIMS examination portal publishes MBBS and allied-health notices.",
    },
    {
        "slug": "mit", "name": "Massachusetts Institute of Technology", "city": "Cambridge", "state": "Massachusetts", "country": "United States", "region": "Abroad", "ownership": "Private",
        "courses": ["B.Tech CSE / AI & ML", "B.Sc Mathematics", "B.Sc Data Science", "Economics / Entrepreneurship"],
        "eligibility": "International applicants follow MIT's first-year application requirements, including school records and current testing/language guidance.",
        "admission": "Apply through MIT Admissions; selection is holistic and highly competitive.",
        "fees": "For 2026–27, standard undergraduate tuition is US$33,360 per fall/spring term; MIT lists total cost of attendance before aid as US$92,760.",
        "fee_currency": "USD", "annual_fee_amount": 66720,
        "official_url": "https://www.mit.edu/", "admission_url": "https://mitadmissions.org/apply/", "fee_url": "https://registrar.mit.edu/registration-academics/tuition-fees/undergraduate",
        "source_note": "Tuition and application links are official MIT pages; financial aid can substantially change net price.",
    },
    {
        "slug": "university-of-toronto", "name": "University of Toronto", "city": "Toronto", "state": "Ontario", "country": "Canada", "region": "Abroad", "ownership": "Government",
        "courses": ["B.Sc Computer Science", "B.Sc Data Science", "B.Sc Biotechnology", "B.Com"],
        "eligibility": "Applicants need a recognised secondary qualification, required programme subjects and proof of English where applicable.",
        "admission": "Apply through the official future-students process; requirements differ by campus and admission category.",
        "fees": "The official 2026–27 Tuition Explorer lists C$69,130.13 total for a full-time first-year international St. George admission stream example; programme/campus totals vary.",
        "fee_currency": "CAD", "annual_fee_amount": 69130,
        "official_url": "https://www.utoronto.ca/", "admission_url": "https://future.utoronto.ca/apply/", "fee_url": "https://tuitionexplorer.registrar.utoronto.ca/",
        "source_note": "Use Tuition Explorer for the exact campus, programme, study level and residency.",
    },
    {
        "slug": "university-of-melbourne", "name": "University of Melbourne", "city": "Melbourne", "state": "Victoria", "country": "Australia", "region": "Abroad", "ownership": "Government",
        "courses": ["B.Des", "B.Com", "B.Sc Data Science", "B.Sc Biotechnology"],
        "eligibility": "A recognised secondary qualification, course prerequisites and English-language requirements apply.",
        "admission": "International applicants can apply directly or through an authorised education agent; course pages list intake details.",
        "fees": "International fees depend on enrolled subjects and study load. The official page states a minimum AUD$17,000 deposit is required when accepting an offer.",
        "fee_currency": "AUD", "annual_fee_amount": None,
        "official_url": "https://www.unimelb.edu.au/", "admission_url": "https://study.unimelb.edu.au/how-to-apply/undergraduate-study/international-applications", "fee_url": "https://study.unimelb.edu.au/how-to-apply/undergraduate-study/international-applications/fees-and-payments",
        "source_note": "Course-specific fee estimates should be checked with the official tuition estimator.",
    },
    {
        "slug": "nus", "name": "National University of Singapore", "city": "Singapore", "state": "Singapore", "country": "Singapore", "region": "Abroad", "ownership": "Government",
        "courses": ["B.Sc Computer Science", "B.Sc Data Science", "BBA", "B.Com"],
        "eligibility": "NUS publishes accepted international qualifications and programme prerequisites; computing expects strong mathematics preparation.",
        "admission": "International applicants apply through the official NUS Office of Admissions.",
        "fees": "NUS Computing's official 2026 FAQ cites recent international computing tuition of about S$17,950–18,900 with applicable subsidy, or S$39,200 without the MOE Tuition Grant; verify the current cohort table.",
        "fee_currency": "SGD", "annual_fee_amount": 18900,
        "official_url": "https://www.nus.edu.sg/", "admission_url": "https://nus.edu.sg/oam/admissions", "fee_url": "https://www.nus.edu.sg/registrar/administrative-policies-procedures/undergraduate/undergraduate-fees",
        "source_note": "International students who accept an MOE Tuition Grant should review its conditions.",
    },
]


CATALOGS = {
    "course": COURSE_DETAILS,
    "career": CAREER_DETAILS,
    "skill": SKILL_DETAILS,
    "technology": TECHNOLOGY_DETAILS,
}


def find_catalog_item(kind, slug):
    return CATALOGS.get(kind, {}).get(slug)

