"""Curated institution catalogue for CareerCompass.

The catalogue stores only real institutions and official institution domains.
When a current fee or a direct admissions page was not confirmed, the record says
so instead of estimating.  Programme families are intentionally conservative and
are used by the recommendation engine as an eligibility gate.
"""

from datetime import date
import re


VERIFIED_ON = "2026-11-05"

PROFILE_COURSES = {
    "tech": ["B.Tech Computer Science", "Computer Science", "Mechanical Engineering", "Engineering"],
    "tech_cs": ["B.Tech Computer Science", "Computer Science", "Engineering"],
    "medical": ["MBBS", "Medicine", "Life Sciences"],
    "design": ["B.Des", "Design"],
    "business": ["BBA", "Business Administration", "Business"],
    "science": ["Computer Science", "Life Sciences", "Science", "Analytical & Research"],
    "comprehensive": ["Computer Science", "Business", "Life Sciences", "Science", "Psychology", "Education"],
    "tech_science": ["B.Tech Computer Science", "Computer Science", "Mechanical Engineering", "Engineering", "Life Sciences", "Science"],
    "international": ["Computer Science", "Engineering", "Business", "Life Sciences", "Science"],
    "international_tech": ["Computer Science", "Mechanical Engineering", "Engineering", "Science"],
    "international_business": ["Business", "Business Administration", "Science"],
    "international_design": ["Design", "Computer Science", "Business"],
    "international_medical": ["Medicine", "Life Sciences", "Science"],
}

PROFILE_FIELDS = {
    "tech": ["Technology and Computer Science", "Analytical and Research"],
    "tech_cs": ["Technology and Computer Science", "Analytical and Research"],
    "medical": ["Health and Life Sciences"],
    "design": ["Creative and Design"],
    "business": ["Business and Leadership"],
    "science": ["Analytical and Research", "Health and Life Sciences", "Technology and Computer Science"],
    "comprehensive": ["Technology and Computer Science", "Analytical and Research", "People and Service", "Business and Leadership", "Health and Life Sciences"],
    "tech_science": ["Technology and Computer Science", "Analytical and Research", "Health and Life Sciences"],
    "international": ["Technology and Computer Science", "Analytical and Research", "Creative and Design", "Business and Leadership", "Health and Life Sciences"],
    "international_tech": ["Technology and Computer Science", "Analytical and Research"],
    "international_business": ["Business and Leadership", "Analytical and Research"],
    "international_design": ["Creative and Design", "Technology and Computer Science", "Business and Leadership"],
    "international_medical": ["Health and Life Sciences", "Analytical and Research"],
}


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def make_record(name, city, subdivision, country, ownership, profile, official_url,
                quality="", rank_value=None, admission_url="", exams=None,
                fee_amount=None, fee_currency=None, fee_text="", fee_url=""):
    india = country == "India"
    if profile == "medical":
        eligibility = "Class 12 with Physics, Chemistry and Biology; current regulatory and institution rules apply."
        admission = "Undergraduate medical admission is normally through NEET-UG and the applicable counselling process; verify the official notice."
        default_exams = ["NEET-UG"] if india else ["Institution-specific requirements"]
    elif profile == "design" or profile == "international_design":
        eligibility = "Recognised secondary-school qualification; portfolio or design-aptitude requirements vary by programme."
        admission = "Apply through the institution's official admission process and check portfolio/design entrance requirements."
        default_exams = ["NID DAT / UCEED / NIFT Entrance or institution process"] if india else ["Portfolio / institution process"]
    elif profile == "business" or profile == "international_business":
        eligibility = "Recognised Class 12 or equivalent qualification; subject and score requirements vary."
        admission = "Merit, CUET or an institution-specific selection process may apply; verify the current official prospectus."
        default_exams = ["CUET / institution-specific process"] if india else ["Institution-specific requirements"]
    elif profile in {"tech", "tech_cs", "tech_science"}:
        eligibility = "Class 12 with Mathematics and the required science subjects; programme-specific rules apply."
        admission = "JEE, state counselling or an institution-specific process may apply; verify the current official notice."
        default_exams = ["JEE Main / JEE Advanced / state or institution entrance"]
    elif profile.startswith("international"):
        eligibility = "Recognised secondary-school qualification meeting programme prerequisites; language evidence may be required."
        admission = "Apply through the university's official international/undergraduate admissions process."
        default_exams = ["Institution requirements; English-language evidence where applicable"]
    else:
        eligibility = "Recognised Class 12 or equivalent qualification; programme prerequisites vary."
        admission = "Admission may use merit, CUET or an institution-specific process; verify the official programme page."
        default_exams = ["CUET / institution-specific process"] if india else ["Institution-specific requirements"]

    if not fee_text:
        fee_text = "Current annual tuition not verified in the bundled catalogue; check the official fee page before applying."
    return {
        "slug": slugify(name), "name": name, "city": city, "state": subdivision,
        "country": country, "region": "India" if india else "Abroad",
        "ownership": ownership, "courses": list(PROFILE_COURSES[profile]),
        "career_fields": list(PROFILE_FIELDS[profile]), "eligibility": eligibility,
        "admission": admission, "entrance_exams": exams or default_exams,
        "fees": fee_text, "fee_currency": fee_currency, "annual_fee_amount": fee_amount,
        "official_url": official_url, "admission_url": admission_url or official_url,
        "fee_url": fee_url or official_url, "ranking_info": quality,
        "rank_value": rank_value, "last_verified": VERIFIED_ON,
        "source_note": "Official institution website; ranking text is included only when an identified source is stated.",
    }


# name, city, state/UT, ownership, profile, official URL, quality/ranking note, rank value
INDIA_ROWS = [
    ("Indian Institute of Science", "Bengaluru", "Karnataka", "Government", "science", "https://iisc.ac.in", "NIRF 2025 University ranking: 1", 1),
    ("Indian Institute of Technology Madras", "Chennai", "Tamil Nadu", "Government", "tech_science", "https://www.iitm.ac.in", "NIRF 2025 Engineering ranking: 1", 1),
    ("Indian Institute of Technology Delhi", "New Delhi", "Delhi", "Government", "tech_science", "https://home.iitd.ac.in", "NIRF 2025 Engineering ranking: 2", 2),
    ("Indian Institute of Technology Bombay", "Mumbai", "Maharashtra", "Government", "tech_science", "https://www.iitb.ac.in", "NIRF 2025 Engineering ranking: 3", 3),
    ("Indian Institute of Technology Kanpur", "Kanpur", "Uttar Pradesh", "Government", "tech_science", "https://www.iitk.ac.in", "NIRF 2025 Engineering ranking: 4", 4),
    ("Indian Institute of Technology Kharagpur", "Kharagpur", "West Bengal", "Government", "tech_science", "https://www.iitkgp.ac.in", "NIRF 2025 Engineering ranking: 5", 5),
    ("Indian Institute of Technology Roorkee", "Roorkee", "Uttarakhand", "Government", "tech_science", "https://www.iitr.ac.in", "NIRF 2025 Engineering ranking: 6", 6),
    ("Indian Institute of Technology Hyderabad", "Hyderabad", "Telangana", "Government", "tech_science", "https://www.iith.ac.in", "NIRF 2025 Engineering ranking: 7", 7),
    ("Indian Institute of Technology Guwahati", "Guwahati", "Assam", "Government", "tech_science", "https://www.iitg.ac.in", "NIRF 2025 Engineering ranking: 8", 8),
    ("National Institute of Technology Tiruchirappalli", "Tiruchirappalli", "Tamil Nadu", "Government", "tech", "https://www.nitt.edu", "NIRF 2025 Engineering ranking: 9", 9),
    ("IIT (BHU) Varanasi", "Varanasi", "Uttar Pradesh", "Government", "tech_science", "https://www.iitbhu.ac.in", "NIRF 2025 Engineering ranking: 10", 10),
    ("BITS Pilani", "Pilani", "Rajasthan", "Private", "tech_science", "https://www.bits-pilani.ac.in", "NIRF 2025 Engineering ranking: 11", 11),
    ("Indian Institute of Technology Indore", "Indore", "Madhya Pradesh", "Government", "tech_science", "https://www.iiti.ac.in", "NIRF 2025 Engineering ranking: 12", 12),
    ("National Institute of Technology Rourkela", "Rourkela", "Odisha", "Government", "tech", "https://www.nitrkl.ac.in", "NIRF 2025 Engineering ranking: 13", 13),
    ("SRM Institute of Science and Technology", "Chennai", "Tamil Nadu", "Private", "tech", "https://www.srmist.edu.in", "NIRF 2025 Engineering ranking: 14", 14),
    ("IIT (ISM) Dhanbad", "Dhanbad", "Jharkhand", "Government", "tech_science", "https://www.iitism.ac.in", "NIRF 2025 Engineering ranking: 15", 15),
    ("Vellore Institute of Technology", "Vellore", "Tamil Nadu", "Private", "tech", "https://vit.ac.in", "NIRF 2025 Engineering ranking: 16", 16),
    ("National Institute of Technology Karnataka Surathkal", "Mangaluru", "Karnataka", "Government", "tech", "https://www.nitk.ac.in", "NIRF 2025 Engineering ranking: 17", 17),
    ("Jadavpur University", "Kolkata", "West Bengal", "Government", "tech_science", "https://jadavpuruniversity.in", "NIRF 2025 Engineering ranking: 18", 18),
    ("Indian Institute of Technology Patna", "Patna", "Bihar", "Government", "tech_science", "https://www.iitp.ac.in", "NIRF 2025 Engineering ranking: 19", 19),
    ("Anna University", "Chennai", "Tamil Nadu", "Government", "tech", "https://www.annauniv.edu", "NIRF 2025 Engineering ranking: 20", 20),
    ("National Institute of Technology Calicut", "Kozhikode", "Kerala", "Government", "tech", "https://nitc.ac.in", "NIRF 2025 Engineering ranking: 21", 21),
    ("Siksha O Anusandhan", "Bhubaneswar", "Odisha", "Private", "tech_science", "https://www.soa.ac.in", "NIRF 2025 Engineering ranking: 22", 22),
    ("Amrita Vishwa Vidyapeetham", "Coimbatore", "Tamil Nadu", "Private", "tech_science", "https://www.amrita.edu", "NIRF 2025 Engineering ranking: 23", 23),
    ("Jamia Millia Islamia", "New Delhi", "Delhi", "Government", "comprehensive", "https://jmi.ac.in", "NIRF 2025 Engineering ranking: 24", 24),
    ("Indian Institute of Technology Gandhinagar", "Gandhinagar", "Gujarat", "Government", "tech_science", "https://iitgn.ac.in", "NIRF 2025 Engineering ranking: 25", 25),
    ("Indian Institute of Technology Bhubaneswar", "Bhubaneswar", "Odisha", "Government", "tech_science", "https://www.iitbbs.ac.in", "NIRF 2025 Engineering top 50", 39),
    ("Institute of Chemical Technology", "Mumbai", "Maharashtra", "Government", "tech_science", "https://www.ictmumbai.edu.in", "NIRF 2025 Engineering top 50", 41),
    ("Malaviya National Institute of Technology Jaipur", "Jaipur", "Rajasthan", "Government", "tech", "https://mnit.ac.in", "Listed in NIRF 2025 Engineering", 42),
    ("Delhi Technological University", "New Delhi", "Delhi", "Government", "tech", "https://dtu.ac.in", "Listed in NIRF 2025 Engineering", 30),
    ("Birla Institute of Technology Mesra", "Ranchi", "Jharkhand", "Private", "tech", "https://www.bitmesra.ac.in", "Listed in NIRF 2025 Engineering", 48),
    ("Aligarh Muslim University", "Aligarh", "Uttar Pradesh", "Government", "comprehensive", "https://www.amu.ac.in", "Listed in NIRF 2025 rankings", None),
    ("Banaras Hindu University", "Varanasi", "Uttar Pradesh", "Government", "comprehensive", "https://www.bhu.ac.in", "Listed in NIRF 2025 rankings", None),
    ("University of Delhi", "Delhi", "Delhi", "Government", "comprehensive", "https://www.du.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("University of Hyderabad", "Hyderabad", "Telangana", "Government", "science", "https://uohyd.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("University of Calcutta", "Kolkata", "West Bengal", "Government", "comprehensive", "https://www.caluniv.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("Cochin University of Science and Technology", "Kochi", "Kerala", "Government", "tech_science", "https://cusat.ac.in", "Listed in NIRF 2025 rankings", None),
    ("Panjab University", "Chandigarh", "Chandigarh", "Government", "comprehensive", "https://puchd.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("Savitribai Phule Pune University", "Pune", "Maharashtra", "Government", "comprehensive", "https://www.unipune.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("University of Madras", "Chennai", "Tamil Nadu", "Government", "comprehensive", "https://www.unom.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("Osmania University", "Hyderabad", "Telangana", "Government", "comprehensive", "https://www.osmania.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("University of Kerala", "Thiruvananthapuram", "Kerala", "Government", "comprehensive", "https://www.keralauniversity.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("Gauhati University", "Guwahati", "Assam", "Government", "comprehensive", "https://gauhati.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("University of Kashmir", "Srinagar", "Jammu and Kashmir", "Government", "comprehensive", "https://www.kashmiruniversity.net", "Listed in NIRF rankings", None),
    ("Pondicherry University", "Puducherry", "Puducherry", "Government", "comprehensive", "https://www.pondiuni.edu.in", "Central university", None),
    ("Goa University", "Panaji", "Goa", "Government", "comprehensive", "https://www.unigoa.ac.in", "State public university", None),
    ("Sikkim University", "Gangtok", "Sikkim", "Government", "comprehensive", "https://cus.ac.in", "Central university", None),
    ("Mizoram University", "Aizawl", "Mizoram", "Government", "comprehensive", "https://mzu.edu.in", "Central university", None),
    ("Nagaland University", "Kohima", "Nagaland", "Government", "comprehensive", "https://nagalanduniversity.ac.in", "Central university", None),
    ("Manipur University", "Imphal", "Manipur", "Government", "comprehensive", "https://www.manipuruniv.ac.in", "Central university", None),
    ("North-Eastern Hill University", "Shillong", "Meghalaya", "Government", "comprehensive", "https://nehu.ac.in", "Central university", None),
    ("Tripura University", "Agartala", "Tripura", "Government", "comprehensive", "https://tripurauniv.ac.in", "Central university", None),
    ("Rajiv Gandhi University", "Itanagar", "Arunachal Pradesh", "Government", "comprehensive", "https://rgu.ac.in", "Central university", None),
    ("Central University of Haryana", "Mahendragarh", "Haryana", "Government", "comprehensive", "https://www.cuh.ac.in", "Central university", None),
    ("Central University of Himachal Pradesh", "Dharamshala", "Himachal Pradesh", "Government", "comprehensive", "https://www.cuhimachal.ac.in", "Central university", None),
    ("Central University of Punjab", "Bathinda", "Punjab", "Government", "comprehensive", "https://cup.edu.in", "Central university", None),
    ("Central University of Rajasthan", "Ajmer", "Rajasthan", "Government", "comprehensive", "https://www.curaj.ac.in", "Central university", None),
    ("Central University of South Bihar", "Gaya", "Bihar", "Government", "comprehensive", "https://www.cusb.ac.in", "Central university", None),
    ("Guru Ghasidas Vishwavidyalaya", "Bilaspur", "Chhattisgarh", "Government", "comprehensive", "https://www.ggu.ac.in", "Central university", None),
    ("Hemvati Nandan Bahuguna Garhwal University", "Srinagar", "Uttarakhand", "Government", "comprehensive", "https://www.hnbgu.ac.in", "Central university", None),
    ("Mahatma Gandhi Central University", "Motihari", "Bihar", "Government", "comprehensive", "https://mgcub.ac.in", "Central university", None),
    ("Central University of Jharkhand", "Ranchi", "Jharkhand", "Government", "comprehensive", "https://cuj.ac.in", "Central university", None),
    ("Central University of Karnataka", "Kalaburagi", "Karnataka", "Government", "comprehensive", "https://www.cuk.ac.in", "Central university", None),
    ("Central University of Kerala", "Kasaragod", "Kerala", "Government", "comprehensive", "https://www.cukerala.ac.in", "Central university", None),
    ("Indira Gandhi National Tribal University", "Amarkantak", "Madhya Pradesh", "Government", "comprehensive", "https://igntu.ac.in", "Central university", None),
    ("Central University of Odisha", "Koraput", "Odisha", "Government", "comprehensive", "https://cuo.ac.in", "Central university", None),
    ("Tamil Nadu Central University", "Thiruvarur", "Tamil Nadu", "Government", "comprehensive", "https://cutn.ac.in", "Central university", None),
    ("Maulana Azad National Urdu University", "Hyderabad", "Telangana", "Government", "comprehensive", "https://manuu.edu.in", "Central university", None),
    ("Visva-Bharati", "Santiniketan", "West Bengal", "Government", "comprehensive", "https://www.visvabharati.ac.in", "Central university", None),
    ("National Institute of Technology Warangal", "Warangal", "Telangana", "Government", "tech", "https://www.nitw.ac.in", "Listed in NIRF 2025 Engineering", None),
    ("National Institute of Technology Durgapur", "Durgapur", "West Bengal", "Government", "tech", "https://nitdgp.ac.in", "Listed in NIRF 2025 Engineering", None),
    ("National Institute of Technology Silchar", "Silchar", "Assam", "Government", "tech", "https://www.nits.ac.in", "Listed in NIRF 2025 Engineering", None),
    ("National Institute of Technology Hamirpur", "Hamirpur", "Himachal Pradesh", "Government", "tech", "https://nith.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Jalandhar", "Jalandhar", "Punjab", "Government", "tech", "https://www.nitj.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Kurukshetra", "Kurukshetra", "Haryana", "Government", "tech", "https://nitkkr.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Patna", "Patna", "Bihar", "Government", "tech", "https://www.nitp.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Raipur", "Raipur", "Chhattisgarh", "Government", "tech", "https://nitrr.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Agartala", "Agartala", "Tripura", "Government", "tech", "https://www.nita.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Manipur", "Imphal", "Manipur", "Government", "tech", "https://www.nitmanipur.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Meghalaya", "Shillong", "Meghalaya", "Government", "tech", "https://www.nitm.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Mizoram", "Aizawl", "Mizoram", "Government", "tech", "https://www.nitmz.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Nagaland", "Dimapur", "Nagaland", "Government", "tech", "https://nitnagaland.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Arunachal Pradesh", "Yupia", "Arunachal Pradesh", "Government", "tech", "https://www.nitap.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Sikkim", "Ravangla", "Sikkim", "Government", "tech", "https://nitsikkim.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Srinagar", "Srinagar", "Jammu and Kashmir", "Government", "tech", "https://nitsri.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Goa", "Ponda", "Goa", "Government", "tech", "https://www.nitgoa.ac.in", "Institute of National Importance", None),
    ("National Institute of Technology Puducherry", "Karaikal", "Puducherry", "Government", "tech", "https://www.nitpy.ac.in", "Institute of National Importance", None),
    ("IIIT Bangalore", "Bengaluru", "Karnataka", "Private", "tech_cs", "https://www.iiitb.ac.in", "Deemed university focused on information technology", None),
    ("International Institute of Information Technology Hyderabad", "Hyderabad", "Telangana", "Private", "tech_cs", "https://www.iiit.ac.in", "Research university focused on information technology", None),
    ("IIIT Delhi", "New Delhi", "Delhi", "Government", "tech_cs", "https://www.iiitd.ac.in", "State university focused on information technology", None),
    ("IIIT Allahabad", "Prayagraj", "Uttar Pradesh", "Government", "tech_cs", "https://www.iiita.ac.in", "Institute of National Importance", None),
    ("IIIT Gwalior", "Gwalior", "Madhya Pradesh", "Government", "tech_cs", "https://www.iiitm.ac.in", "Institute of National Importance", None),
    ("IIITDM Jabalpur", "Jabalpur", "Madhya Pradesh", "Government", "tech", "https://www.iiitdmj.ac.in", "Institute of National Importance", None),
    ("IIITDM Kancheepuram", "Chennai", "Tamil Nadu", "Government", "tech", "https://www.iiitdm.ac.in", "Institute of National Importance", None),
    ("IIIT Kottayam", "Kottayam", "Kerala", "Government", "tech_cs", "https://www.iiitkottayam.ac.in", "Institute of National Importance", None),
    ("IIIT Kota", "Kota", "Rajasthan", "Government", "tech_cs", "https://iiitkota.ac.in", "Institute of National Importance", None),
    ("IIIT Vadodara", "Gandhinagar", "Gujarat", "Government", "tech_cs", "https://iiitvadodara.ac.in", "Institute of National Importance", None),
    ("IIIT Sri City", "Sri City", "Andhra Pradesh", "Government", "tech_cs", "https://www.iiits.ac.in", "Institute of National Importance", None),
    ("IIIT Guwahati", "Guwahati", "Assam", "Government", "tech_cs", "https://www.iiitg.ac.in", "Institute of National Importance", None),
    ("IIIT Bhubaneswar", "Bhubaneswar", "Odisha", "Government", "tech_cs", "https://www.iiit-bh.ac.in", "State university focused on IT", None),
    ("IIIT Naya Raipur", "Raipur", "Chhattisgarh", "Government", "tech_cs", "https://www.iiitnr.ac.in", "State university focused on IT", None),
    ("RV College of Engineering", "Bengaluru", "Karnataka", "Private", "tech", "https://rvce.edu.in", "Autonomous engineering institution", None),
    ("BMS College of Engineering", "Bengaluru", "Karnataka", "Private", "tech", "https://bmsce.ac.in", "Autonomous engineering institution", None),
    ("Ramaiah Institute of Technology", "Bengaluru", "Karnataka", "Private", "tech", "https://www.msrit.edu", "Autonomous engineering institution", None),
    ("PES University", "Bengaluru", "Karnataka", "Private", "tech", "https://pes.edu", "Private university", None),
    ("Jain University", "Bengaluru", "Karnataka", "Private", "comprehensive", "https://www.jainuniversity.ac.in", "Deemed-to-be university", None),
    ("College of Engineering Trivandrum", "Thiruvananthapuram", "Kerala", "Government", "tech", "https://www.cet.ac.in", "Government engineering college", None),
    ("Government Engineering College Thrissur", "Thrissur", "Kerala", "Government", "tech", "https://gectcr.ac.in", "Government engineering college", None),
    ("College of Engineering Pune", "Pune", "Maharashtra", "Government", "tech", "https://www.coeptech.ac.in", "Public technological university", None),
    ("Veermata Jijabai Technological Institute", "Mumbai", "Maharashtra", "Government", "tech", "https://vjti.ac.in", "Government-aided autonomous institute", None),
    ("Visvesvaraya National Institute of Technology Nagpur", "Nagpur", "Maharashtra", "Government", "tech", "https://vnit.ac.in", "Institute of National Importance", None),
    ("Sardar Vallabhbhai National Institute of Technology Surat", "Surat", "Gujarat", "Government", "tech", "https://www.svnit.ac.in", "Institute of National Importance", None),
    ("DA-IICT", "Gandhinagar", "Gujarat", "Private", "tech_cs", "https://www.daiict.ac.in", "Private university focused on ICT", None),
    ("LNMIIT Jaipur", "Jaipur", "Rajasthan", "Private", "tech", "https://www.lnmiit.ac.in", "Deemed-to-be university", None),
    ("Thapar Institute of Engineering and Technology", "Patiala", "Punjab", "Private", "tech", "https://www.thapar.edu", "Deemed-to-be university", None),
    ("Punjab Engineering College", "Chandigarh", "Chandigarh", "Government", "tech", "https://pec.ac.in", "Deemed-to-be university", None),
    ("IIT Mandi", "Mandi", "Himachal Pradesh", "Government", "tech_science", "https://www.iitmandi.ac.in", "Institute of National Importance", None),
    ("IIT Jodhpur", "Jodhpur", "Rajasthan", "Government", "tech_science", "https://www.iitj.ac.in", "Institute of National Importance", None),
    ("IIT Ropar", "Rupnagar", "Punjab", "Government", "tech_science", "https://www.iitrpr.ac.in", "Institute of National Importance", None),
    ("IIT Palakkad", "Palakkad", "Kerala", "Government", "tech_science", "https://iitpkd.ac.in", "Institute of National Importance", None),
    ("IIT Tirupati", "Tirupati", "Andhra Pradesh", "Government", "tech_science", "https://www.iittp.ac.in", "Institute of National Importance", None),
    ("IIT Jammu", "Jammu", "Jammu and Kashmir", "Government", "tech_science", "https://iitjammu.ac.in", "Institute of National Importance", None),
    ("IIT Goa", "Ponda", "Goa", "Government", "tech_science", "https://iitgoa.ac.in", "Institute of National Importance", None),
    ("IIT Bhilai", "Bhilai", "Chhattisgarh", "Government", "tech_science", "https://www.iitbhilai.ac.in", "Institute of National Importance", None),
    ("Dibrugarh University", "Dibrugarh", "Assam", "Government", "comprehensive", "https://dibru.ac.in", "State public university", None),
    ("Tezpur University", "Tezpur", "Assam", "Government", "tech_science", "https://www.tezu.ernet.in", "Central university", None),
    ("KIIT Deemed to be University", "Bhubaneswar", "Odisha", "Private", "comprehensive", "https://kiit.ac.in", "Deemed-to-be university", None),
    ("Manipal Academy of Higher Education", "Manipal", "Karnataka", "Private", "comprehensive", "https://www.manipal.edu", "Deemed-to-be university", None),
    ("Christ University", "Bengaluru", "Karnataka", "Private", "comprehensive", "https://christuniversity.in", "Deemed-to-be university", None),
    ("Symbiosis International University", "Pune", "Maharashtra", "Private", "comprehensive", "https://www.siu.edu.in", "Deemed-to-be university", None),
    ("Amity University Noida", "Noida", "Uttar Pradesh", "Private", "comprehensive", "https://www.amity.edu", "Private university", None),
    ("Sharda University", "Greater Noida", "Uttar Pradesh", "Private", "comprehensive", "https://www.sharda.ac.in", "Private university", None),
    ("Galgotias University", "Greater Noida", "Uttar Pradesh", "Private", "comprehensive", "https://www.galgotiasuniversity.edu.in", "Private university", None),
    ("Lovely Professional University", "Phagwara", "Punjab", "Private", "comprehensive", "https://www.lpu.in", "Private university", None),
    ("Chandigarh University", "Mohali", "Punjab", "Private", "comprehensive", "https://www.cuchd.in", "Private university", None),
    ("O.P. Jindal Global University", "Sonipat", "Haryana", "Private", "comprehensive", "https://jgu.edu.in", "Institution of Eminence", None),
    ("Ashoka University", "Sonipat", "Haryana", "Private", "comprehensive", "https://www.ashoka.edu.in", "Private university", None),
    ("Shiv Nadar University", "Greater Noida", "Uttar Pradesh", "Private", "tech_science", "https://snu.edu.in", "Institution of Eminence", None),
    ("University of Petroleum and Energy Studies", "Dehradun", "Uttarakhand", "Private", "comprehensive", "https://www.upes.ac.in", "Private university", None),
    ("Graphic Era University", "Dehradun", "Uttarakhand", "Private", "tech", "https://geu.ac.in", "Deemed-to-be university", None),
    ("Xavier University Bhubaneswar", "Bhubaneswar", "Odisha", "Private", "business", "https://xim.edu.in", "Private university", None),
    ("Shaheed Sukhdev College of Business Studies", "Delhi", "Delhi", "Government", "business", "https://sscbs.du.ac.in", "University of Delhi college offering BMS/BBA(FIA)", None),
    ("Jamia Hamdard", "New Delhi", "Delhi", "Private", "comprehensive", "https://jamiahamdard.edu", "Deemed-to-be university", None),
    ("Maharaja Surajmal Institute", "Delhi", "Delhi", "Private", "business", "https://www.msit.in", "GGSIPU-affiliated institution", None),
    ("Indian Institute of Management Indore", "Indore", "Madhya Pradesh", "Government", "business", "https://www.iimidr.ac.in", "Institute of National Importance; integrated management programme", None),
    ("Indian Institute of Management Rohtak", "Rohtak", "Haryana", "Government", "business", "https://www.iimrohtak.ac.in", "Institute of National Importance; integrated management programme", None),
    ("Indian Institute of Management Jammu", "Jammu", "Jammu and Kashmir", "Government", "business", "https://www.iimj.ac.in", "Institute of National Importance; integrated management programme", None),
    ("National Institute of Design Ahmedabad", "Ahmedabad", "Gujarat", "Government", "design", "https://www.nid.edu", "Institute of National Importance", None),
    ("National Institute of Design Andhra Pradesh", "Guntur", "Andhra Pradesh", "Government", "design", "https://www.nid.ac.in", "Institute of National Importance", None),
    ("National Institute of Design Haryana", "Kurukshetra", "Haryana", "Government", "design", "https://www.nidh.ac.in", "Institute of National Importance", None),
    ("National Institute of Design Madhya Pradesh", "Bhopal", "Madhya Pradesh", "Government", "design", "https://nidmp.ac.in", "Institute of National Importance", None),
    ("National Institute of Design Assam", "Jorhat", "Assam", "Government", "design", "https://nidj.ac.in", "Institute of National Importance", None),
    ("National Institute of Fashion Technology Gandhinagar", "Gandhinagar", "Gujarat", "Government", "design", "https://www.nift.ac.in/gandhinagar", "NIFT campus", None),
    ("National Institute of Fashion Technology Delhi", "New Delhi", "Delhi", "Government", "design", "https://www.nift.ac.in/delhi", "NIFT campus", None),
    ("National Institute of Fashion Technology Mumbai", "Mumbai", "Maharashtra", "Government", "design", "https://www.nift.ac.in/mumbai", "NIFT campus", None),
    ("National Institute of Fashion Technology Bengaluru", "Bengaluru", "Karnataka", "Government", "design", "https://www.nift.ac.in/bengaluru", "NIFT campus", None),
    ("National Institute of Fashion Technology Chennai", "Chennai", "Tamil Nadu", "Government", "design", "https://www.nift.ac.in/chennai", "NIFT campus", None),
    ("Anant National University", "Ahmedabad", "Gujarat", "Private", "design", "https://anu.edu.in", "Private design-focused university", None),
    ("CEPT University", "Ahmedabad", "Gujarat", "Private", "design", "https://cept.ac.in", "University focused on built environment and design", None),
    ("MIT Institute of Design", "Pune", "Maharashtra", "Private", "design", "https://www.mitid.edu.in", "Design institution", None),
    ("Srishti Manipal Institute of Art Design and Technology", "Bengaluru", "Karnataka", "Private", "design", "https://srishtimanipalinstitute.in", "Design and arts institution", None),
    ("All India Institute of Medical Sciences New Delhi", "New Delhi", "Delhi", "Government", "medical", "https://www.aiims.edu", "NIRF 2025 Medical ranking: 1", 1),
    ("Postgraduate Institute of Medical Education and Research", "Chandigarh", "Chandigarh", "Government", "medical", "https://pgimer.edu.in", "Listed in NIRF 2025 Medical ranking", None),
    ("Christian Medical College Vellore", "Vellore", "Tamil Nadu", "Private", "medical", "https://www.cmch-vellore.edu", "Listed in NIRF 2025 Medical ranking", None),
    ("Jawaharlal Institute of Postgraduate Medical Education and Research", "Puducherry", "Puducherry", "Government", "medical", "https://jipmer.edu.in", "Institute of National Importance", None),
    ("Seth GS Medical College", "Mumbai", "Maharashtra", "Government", "medical", "https://www.kem.edu", "Municipal medical college attached to KEM Hospital", None),
    ("Grant Government Medical College", "Mumbai", "Maharashtra", "Government", "medical", "https://gmcjjh.edu.in", "Government medical college", None),
    ("Lokmanya Tilak Municipal Medical College", "Mumbai", "Maharashtra", "Government", "medical", "https://ltmgh.com", "Municipal medical college", None),
    ("Topiwala National Medical College", "Mumbai", "Maharashtra", "Government", "medical", "https://tnmcnair.edu.in", "Municipal medical college", None),
    ("K J Somaiya Medical College", "Mumbai", "Maharashtra", "Private", "medical", "https://kjsmc.somaiya.edu.in", "Private medical college", None),
    ("Armed Forces Medical College", "Pune", "Maharashtra", "Government", "medical", "https://afmc.nic.in", "Armed Forces medical institution", None),
    ("King George's Medical University", "Lucknow", "Uttar Pradesh", "Government", "medical", "https://www.kgmu.org", "State medical university", None),
    ("Institute of Medical Sciences BHU", "Varanasi", "Uttar Pradesh", "Government", "medical", "https://www.bhu.ac.in/Site/UnitHomeTemplate/1_3316_6411_3316", "University medical institute", None),
    ("Madras Medical College", "Chennai", "Tamil Nadu", "Government", "medical", "https://www.mmc.ac.in", "Government medical college", None),
    ("Stanley Medical College", "Chennai", "Tamil Nadu", "Government", "medical", "https://stanleymedicalcollege.ac.in", "Government medical college", None),
    ("Bangalore Medical College and Research Institute", "Bengaluru", "Karnataka", "Government", "medical", "https://bmcribengaluru.karnataka.gov.in", "Government medical college", None),
    ("Kasturba Medical College Manipal", "Manipal", "Karnataka", "Private", "medical", "https://www.manipal.edu/kmc-manipal.html", "Medical college of MAHE", None),
    ("Government Medical College Thiruvananthapuram", "Thiruvananthapuram", "Kerala", "Government", "medical", "https://www.tmc.kerala.gov.in", "Government medical college", None),
    ("Medical College Kolkata", "Kolkata", "West Bengal", "Government", "medical", "https://www.medicalcollegekolkata.in", "Government medical college", None),
    ("Nil Ratan Sircar Medical College", "Kolkata", "West Bengal", "Government", "medical", "https://nrsmc.edu.in", "Government medical college", None),
    ("B. J. Medical College Ahmedabad", "Ahmedabad", "Gujarat", "Government", "medical", "https://www.bjmcabd.edu.in", "Government medical college", None),
    ("Sawai Man Singh Medical College", "Jaipur", "Rajasthan", "Government", "medical", "https://education.rajasthan.gov.in/smsmcjaipur", "Government medical college", None),
    ("Gandhi Medical College Hyderabad", "Hyderabad", "Telangana", "Government", "medical", "https://gandhihospital.telangana.gov.in", "Government medical college", None),
    ("Andhra Medical College", "Visakhapatnam", "Andhra Pradesh", "Government", "medical", "https://amc.edu.in", "Government medical college", None),
    ("SCB Medical College", "Cuttack", "Odisha", "Government", "medical", "https://scbmch.in", "Government medical college", None),
    ("Gauhati Medical College", "Guwahati", "Assam", "Government", "medical", "https://gmchassam.gov.in", "Government medical college", None),
    ("Indira Gandhi Medical College Shimla", "Shimla", "Himachal Pradesh", "Government", "medical", "https://igmcshimla.edu.in", "Government medical college", None),
    ("Government Medical College Srinagar", "Srinagar", "Jammu and Kashmir", "Government", "medical", "https://www.gmcs.edu.in", "Government medical college", None),
    ("Regional Institute of Medical Sciences", "Imphal", "Manipur", "Government", "medical", "https://www.rims.edu.in", "Medical institute under Ministry of Health and Family Welfare", None),
    ("North Eastern Indira Gandhi Regional Institute of Health and Medical Sciences", "Shillong", "Meghalaya", "Government", "medical", "https://neigrihms.gov.in", "Autonomous medical institute", None),
    ("IISER Kolkata", "Kolkata", "West Bengal", "Government", "science", "https://www.iiserkol.ac.in", "Institute of National Importance", None),
    ("IISER Pune", "Pune", "Maharashtra", "Government", "science", "https://www.iiserpune.ac.in", "Institute of National Importance", None),
    ("IISER Mohali", "Mohali", "Punjab", "Government", "science", "https://www.iisermohali.ac.in", "Institute of National Importance", None),
    ("IISER Bhopal", "Bhopal", "Madhya Pradesh", "Government", "science", "https://www.iiserb.ac.in", "Institute of National Importance", None),
    ("IISER Thiruvananthapuram", "Thiruvananthapuram", "Kerala", "Government", "science", "https://www.iisertvm.ac.in", "Institute of National Importance", None),
    ("IISER Tirupati", "Tirupati", "Andhra Pradesh", "Government", "science", "https://www.iisertirupati.ac.in", "Institute of National Importance", None),
    ("IISER Berhampur", "Berhampur", "Odisha", "Government", "science", "https://www.iiserbpr.ac.in", "Institute of National Importance", None),
    ("Indian Statistical Institute", "Kolkata", "West Bengal", "Government", "science", "https://www.isical.ac.in", "Institute of National Importance", None),
    ("Chennai Mathematical Institute", "Chennai", "Tamil Nadu", "Private", "science", "https://www.cmi.ac.in", "Deemed university focused on mathematics and computer science", None),
    ("Tata Institute of Fundamental Research", "Mumbai", "Maharashtra", "Government", "science", "https://www.tifr.res.in", "Deemed university and research institution", None),
    ("Indian Institute of Science Education and Research Berhampur", "Berhampur", "Odisha", "Government", "science", "https://www.iiserbpr.ac.in", "Institute of National Importance", None),
    ("Jawaharlal Nehru University", "New Delhi", "Delhi", "Government", "comprehensive", "https://www.jnu.ac.in", "Listed in NIRF 2025 University ranking", None),
    ("Presidency University Kolkata", "Kolkata", "West Bengal", "Government", "science", "https://www.presiuniv.ac.in", "State public university", None),
    ("St. Xavier's College Kolkata", "Kolkata", "West Bengal", "Private", "comprehensive", "https://www.sxccal.edu", "Autonomous college", None),
    # Vijayawada programmes checked against the institutions' official programme/admission pages.
    ("Siddhartha Academy of Higher Education", "Vijayawada", "Andhra Pradesh", "Private", "tech", "https://www.vrsiddhartha.ac.in", "Deemed-to-be university; official UG page lists CSE and allied B.Tech programmes", None),
    ("Prasad V. Potluri Siddhartha Institute of Technology", "Vijayawada", "Andhra Pradesh", "Private", "tech", "https://www.pvpsiddhartha.ac.in", "Autonomous self-financed institution; official page lists CSE and allied B.Tech programmes", None),
    ("Andhra Loyola Institute of Engineering and Technology", "Vijayawada", "Andhra Pradesh", "Private", "tech", "https://aliet.ac.in", "Autonomous engineering institution; official admissions page lists CSE and allied B.Tech programmes", None),
]


INTERNATIONAL_ROWS = [
    ("Massachusetts Institute of Technology", "Cambridge", "Massachusetts", "United States", "Private", "international_tech", "https://www.mit.edu", "QS World University Rankings 2026: 1", 1),
    ("Stanford University", "Stanford", "California", "United States", "Private", "international", "https://www.stanford.edu", "QS World University Rankings 2026: top 10", 3),
    ("University of California Berkeley", "Berkeley", "California", "United States", "Government", "international", "https://www.berkeley.edu", "Public research university", None),
    ("California Institute of Technology", "Pasadena", "California", "United States", "Private", "international_tech", "https://www.caltech.edu", "Research university", None),
    ("University of California Los Angeles", "Los Angeles", "California", "United States", "Government", "international", "https://www.ucla.edu", "Public research university", None),
    ("University of California San Diego", "San Diego", "California", "United States", "Government", "international", "https://www.ucsd.edu", "Public research university", None),
    ("University of Southern California", "Los Angeles", "California", "United States", "Private", "international", "https://www.usc.edu", "Private research university", None),
    ("Carnegie Mellon University", "Pittsburgh", "Pennsylvania", "United States", "Private", "international_tech", "https://www.cmu.edu", "Research university known for computing", None),
    ("University of Illinois Urbana-Champaign", "Urbana-Champaign", "Illinois", "United States", "Government", "international_tech", "https://illinois.edu", "Public research university", None),
    ("Georgia Institute of Technology", "Atlanta", "Georgia", "United States", "Government", "international_tech", "https://www.gatech.edu", "Public technological university", None),
    ("University of Washington", "Seattle", "Washington", "United States", "Government", "international", "https://www.washington.edu", "Public research university", None),
    ("University of Michigan", "Ann Arbor", "Michigan", "United States", "Government", "international", "https://umich.edu", "Public research university", None),
    ("Cornell University", "Ithaca", "New York", "United States", "Private", "international", "https://www.cornell.edu", "Private research university", None),
    ("Columbia University", "New York", "New York", "United States", "Private", "international", "https://www.columbia.edu", "Private research university", None),
    ("University of Texas at Austin", "Austin", "Texas", "United States", "Government", "international", "https://www.utexas.edu", "Public research university", None),
    ("University of Toronto", "Toronto", "Ontario", "Canada", "Government", "international", "https://www.utoronto.ca", "Public research university", None),
    ("University of Waterloo", "Waterloo", "Ontario", "Canada", "Government", "international_tech", "https://uwaterloo.ca", "Public research university", None),
    ("McMaster University", "Hamilton", "Ontario", "Canada", "Government", "international", "https://www.mcmaster.ca", "Public research university", None),
    ("Queen's University", "Kingston", "Ontario", "Canada", "Government", "international", "https://www.queensu.ca", "Public research university", None),
    ("University of Ottawa", "Ottawa", "Ontario", "Canada", "Government", "international", "https://www.uottawa.ca", "Public research university", None),
    ("York University", "Toronto", "Ontario", "Canada", "Government", "international", "https://www.yorku.ca", "Public research university", None),
    ("University of British Columbia", "Vancouver", "British Columbia", "Canada", "Government", "international", "https://www.ubc.ca", "Public research university", None),
    ("Simon Fraser University", "Burnaby", "British Columbia", "Canada", "Government", "international", "https://www.sfu.ca", "Public research university", None),
    ("McGill University", "Montreal", "Quebec", "Canada", "Government", "international", "https://www.mcgill.ca", "Public research university", None),
    ("University of Alberta", "Edmonton", "Alberta", "Canada", "Government", "international", "https://www.ualberta.ca", "Public research university", None),
    ("University of Oxford", "Oxford", "England", "United Kingdom", "Government", "international", "https://www.ox.ac.uk", "QS World University Rankings 2026: top 5", 4),
    ("University of Cambridge", "Cambridge", "England", "United Kingdom", "Government", "international", "https://www.cam.ac.uk", "QS World University Rankings 2026: top 10", 6),
    ("Imperial College London", "London", "England", "United Kingdom", "Government", "international_tech", "https://www.imperial.ac.uk", "QS World University Rankings 2026: top 5", 2),
    ("University College London", "London", "England", "United Kingdom", "Government", "international", "https://www.ucl.ac.uk", "QS World University Rankings 2026: top 10", 9),
    ("University of Edinburgh", "Edinburgh", "Scotland", "United Kingdom", "Government", "international", "https://www.ed.ac.uk", "Public research university", None),
    ("University of Manchester", "Manchester", "England", "United Kingdom", "Government", "international", "https://www.manchester.ac.uk", "Public research university", None),
    ("University of Bristol", "Bristol", "England", "United Kingdom", "Government", "international", "https://www.bristol.ac.uk", "Public research university", None),
    ("University of Warwick", "Coventry", "England", "United Kingdom", "Government", "international_business", "https://warwick.ac.uk", "Public research university", None),
    ("London School of Economics and Political Science", "London", "England", "United Kingdom", "Government", "international_business", "https://www.lse.ac.uk", "Public social-science university", None),
    ("University of the Arts London", "London", "England", "United Kingdom", "Government", "international_design", "https://www.arts.ac.uk", "Specialist arts and design university", None),
    ("University of Melbourne", "Melbourne", "Victoria", "Australia", "Government", "international", "https://www.unimelb.edu.au", "Public research university", None),
    ("Monash University", "Melbourne", "Victoria", "Australia", "Government", "international", "https://www.monash.edu", "Public research university", None),
    ("RMIT University", "Melbourne", "Victoria", "Australia", "Government", "international_design", "https://www.rmit.edu.au", "Public technological and design university", None),
    ("Deakin University", "Geelong", "Victoria", "Australia", "Government", "international", "https://www.deakin.edu.au", "Public university", None),
    ("University of Sydney", "Sydney", "New South Wales", "Australia", "Government", "international", "https://www.sydney.edu.au", "Public research university", None),
    ("University of New South Wales", "Sydney", "New South Wales", "Australia", "Government", "international_tech", "https://www.unsw.edu.au", "Public research university", None),
    ("Australian National University", "Canberra", "Australian Capital Territory", "Australia", "Government", "international", "https://www.anu.edu.au", "National research university", None),
    ("University of Queensland", "Brisbane", "Queensland", "Australia", "Government", "international", "https://www.uq.edu.au", "Public research university", None),
    ("Technical University of Munich", "Munich", "Bavaria", "Germany", "Government", "international_tech", "https://www.tum.de", "Public technical university", None),
    ("Ludwig Maximilian University of Munich", "Munich", "Bavaria", "Germany", "Government", "international", "https://www.lmu.de", "Public research university", None),
    ("University of Erlangen-Nuremberg", "Erlangen", "Bavaria", "Germany", "Government", "international", "https://www.fau.eu", "Public research university", None),
    ("RWTH Aachen University", "Aachen", "North Rhine-Westphalia", "Germany", "Government", "international_tech", "https://www.rwth-aachen.de", "Public technical university", None),
    ("Karlsruhe Institute of Technology", "Karlsruhe", "Baden-Wurttemberg", "Germany", "Government", "international_tech", "https://www.kit.edu", "Public research university", None),
    ("Technical University of Berlin", "Berlin", "Berlin", "Germany", "Government", "international_tech", "https://www.tu.berlin", "Public technical university", None),
    ("TU Dresden", "Dresden", "Saxony", "Germany", "Government", "international_tech", "https://tu-dresden.de", "Public technical university", None),
    ("Heidelberg University", "Heidelberg", "Baden-Wurttemberg", "Germany", "Government", "international_medical", "https://www.uni-heidelberg.de", "Public research university", None),
    ("Universite Paris-Saclay", "Saclay", "Ile-de-France", "France", "Government", "international_tech", "https://www.universite-paris-saclay.fr", "Public research university", None),
    ("Sorbonne University", "Paris", "Ile-de-France", "France", "Government", "international", "https://www.sorbonne-universite.fr", "Public research university", None),
    ("Institut Polytechnique de Paris", "Paris", "Ile-de-France", "France", "Government", "international_tech", "https://www.ip-paris.fr", "Public science and technology institute", None),
    ("Sciences Po", "Paris", "Ile-de-France", "France", "Government", "international_business", "https://www.sciencespo.fr", "Public social-science institution", None),
    ("Trinity College Dublin", "Dublin", "Leinster", "Ireland", "Government", "international", "https://www.tcd.ie", "Public research university", None),
    ("University College Dublin", "Dublin", "Leinster", "Ireland", "Government", "international", "https://www.ucd.ie", "Public research university", None),
    ("University College Cork", "Cork", "Munster", "Ireland", "Government", "international", "https://www.ucc.ie", "Public university", None),
    ("Delft University of Technology", "Delft", "South Holland", "Netherlands", "Government", "international_tech", "https://www.tudelft.nl", "Public technical university", None),
    ("University of Amsterdam", "Amsterdam", "North Holland", "Netherlands", "Government", "international", "https://www.uva.nl", "Public research university", None),
    ("Eindhoven University of Technology", "Eindhoven", "North Brabant", "Netherlands", "Government", "international_tech", "https://www.tue.nl", "Public technical university", None),
    ("Utrecht University", "Utrecht", "Utrecht", "Netherlands", "Government", "international", "https://www.uu.nl", "Public research university", None),
    ("ETH Zurich", "Zurich", "Zurich", "Switzerland", "Government", "international_tech", "https://ethz.ch", "QS World University Rankings 2026: top 10", 7),
    ("EPFL", "Lausanne", "Vaud", "Switzerland", "Government", "international_tech", "https://www.epfl.ch", "Public research university", None),
    ("University of Zurich", "Zurich", "Zurich", "Switzerland", "Government", "international", "https://www.uzh.ch", "Public research university", None),
    ("National University of Singapore", "Singapore", "Singapore", "Singapore", "Government", "international", "https://www.nus.edu.sg", "QS World University Rankings 2026: top 10", 8),
    ("Nanyang Technological University", "Singapore", "Singapore", "Singapore", "Government", "international_tech", "https://www.ntu.edu.sg", "Public research university", None),
    ("Singapore Management University", "Singapore", "Singapore", "Singapore", "Government", "international_business", "https://www.smu.edu.sg", "Public autonomous university", None),
    ("Singapore University of Technology and Design", "Singapore", "Singapore", "Singapore", "Government", "international_design", "https://www.sutd.edu.sg", "Public autonomous university", None),
    ("University of Tokyo", "Tokyo", "Tokyo", "Japan", "Government", "international", "https://www.u-tokyo.ac.jp/en/", "National university", None),
    ("Tokyo Institute of Science", "Tokyo", "Tokyo", "Japan", "Government", "international_tech", "https://www.isct.ac.jp/en", "National science and technology university", None),
    ("Waseda University", "Tokyo", "Tokyo", "Japan", "Private", "international", "https://www.waseda.jp/top/en", "Private research university", None),
    ("Keio University", "Tokyo", "Tokyo", "Japan", "Private", "international", "https://www.keio.ac.jp/en/", "Private research university", None),
    ("Kyoto University", "Kyoto", "Kyoto", "Japan", "Government", "international", "https://www.kyoto-u.ac.jp/en", "National university", None),
    ("Osaka University", "Suita", "Osaka", "Japan", "Government", "international", "https://www.osaka-u.ac.jp/en", "National university", None),
    ("Seoul National University", "Seoul", "Seoul", "South Korea", "Government", "international", "https://en.snu.ac.kr", "National university", None),
    ("KAIST", "Daejeon", "Daejeon", "South Korea", "Government", "international_tech", "https://www.kaist.ac.kr/en/", "National science and technology institute", None),
    ("POSTECH", "Pohang", "Pohang", "South Korea", "Private", "international_tech", "https://www.postech.ac.kr/eng/", "Private research university", None),
    ("Yonsei University", "Seoul", "Seoul", "South Korea", "Private", "international", "https://www.yonsei.ac.kr/en_sc/", "Private research university", None),
    ("Khalifa University", "Abu Dhabi", "Abu Dhabi", "United Arab Emirates", "Government", "international_tech", "https://www.ku.ac.ae", "Public research university", None),
    ("United Arab Emirates University", "Al Ain", "Abu Dhabi", "United Arab Emirates", "Government", "international", "https://www.uaeu.ac.ae/en/", "National university", None),
    ("American University of Sharjah", "Sharjah", "Sharjah", "United Arab Emirates", "Private", "international", "https://www.aus.edu", "Private university", None),
    ("University of Auckland", "Auckland", "Auckland", "New Zealand", "Government", "international", "https://www.auckland.ac.nz", "Public research university", None),
    ("University of Otago", "Dunedin", "Otago", "New Zealand", "Government", "international", "https://www.otago.ac.nz", "Public research university", None),
    ("University of Canterbury", "Christchurch", "Canterbury", "New Zealand", "Government", "international_tech", "https://www.canterbury.ac.nz", "Public university", None),
    ("University of Malaya", "Kuala Lumpur", "Kuala Lumpur", "Malaysia", "Government", "international", "https://www.um.edu.my", "Public research university", None),
    ("Universiti Putra Malaysia", "Serdang", "Selangor", "Malaysia", "Government", "international", "https://www.upm.edu.my", "Public research university", None),
    ("Universiti Teknologi Malaysia", "Johor Bahru", "Johor", "Malaysia", "Government", "international_tech", "https://www.utm.my", "Public technological university", None),
    ("Monash University Malaysia", "Bandar Sunway", "Selangor", "Malaysia", "Private", "international", "https://www.monash.edu.my", "Branch campus of Monash University", None),
]


COLLEGES = [make_record(row[0], row[1], row[2], "India", row[3], row[4], row[5], quality=row[6], rank_value=row[7]) for row in INDIA_ROWS]
COLLEGES += [make_record(row[0], row[1], row[2], row[3], row[4], row[5], row[6], quality=row[7], rank_value=row[8]) for row in INTERNATIONAL_ROWS]

# Records with institution-specific admission/fee links or verified fee notes.
OVERRIDES = {
    "indian-institute-of-technology-bombay": {"admission_url": "https://www.iitb.ac.in/newacadhome/toadmission.jsp", "fee_url": "https://acad.iitb.ac.in/admissions/fees-structure", "fees": "2026-27 standard UG tuition is ₹100,000 per semester (₹200,000 annually); non-tuition charges and category exemptions vary.", "fee_currency": "INR", "annual_fee_amount": 200000, "entrance_exams": ["JEE Advanced"]},
    "national-institute-of-design-ahmedabad": {"admission_url": "https://admissions.nid.edu", "fee_url": "https://admissions.nid.edu", "entrance_exams": ["NID DAT"]},
    "all-india-institute-of-medical-sciences-new-delhi": {"admission_url": "https://www.aiimsexams.ac.in", "fee_url": "https://www.aiims.edu", "entrance_exams": ["NEET-UG"]},
    "university-of-delhi": {"admission_url": "https://admission.uod.ac.in", "fee_url": "https://www.du.ac.in", "entrance_exams": ["CUET-UG / programme-specific process"]},
    "massachusetts-institute-of-technology": {"admission_url": "https://mitadmissions.org", "fee_url": "https://sfs.mit.edu/undergraduate-students/the-cost-of-attendance/coa/", "fees": "MIT's official 2026-27 undergraduate tuition is USD 66,720; total cost of attendance is higher and financial aid can change net cost.", "fee_currency": "USD", "annual_fee_amount": 66720},
    "university-of-toronto": {"admission_url": "https://future.utoronto.ca/apply/", "fee_url": "https://planningandbudget.utoronto.ca/tuition-fee-lookup-tool/", "fees": "Use the official tuition fee lookup; fees depend on programme, campus and status.", "fee_currency": "CAD"},
    "university-of-melbourne": {"admission_url": "https://study.unimelb.edu.au/how-to-apply", "fee_url": "https://study.unimelb.edu.au/how-to-apply/fees", "fees": "Use the official course fee calculator; fees vary by course and study load.", "fee_currency": "AUD"},
    "national-university-of-singapore": {"admission_url": "https://nus.edu.sg/oam/admissions", "fee_url": "https://www.nus.edu.sg/registrar/administrative-policies-procedures/undergraduate/undergraduate-fees", "fees": "See NUS Registrar's official undergraduate fee schedule.", "fee_currency": "SGD"},
    "york-university": {"admission_url": "https://schulich.yorku.ca/admissions/how-to-apply-undergrad/", "source_note": "York University's official Schulich BBA programme and admissions pages checked 2026-11-05; tuition remains unverified in this catalogue."},
    "siddhartha-academy-of-higher-education": {"admission_url": "https://www.vrsiddhartha.ac.in/ugprogrammes/", "entrance_exams": ["AP EAPCET / institution admission process"], "source_note": "Official UG programmes page checked 2026-11-05; current tuition not stored because a comparable annual official figure was not confirmed."},
    "prasad-v-potluri-siddhartha-institute-of-technology": {"admission_url": "https://www.pvpsiddhartha.ac.in/programesoffered_n.html", "entrance_exams": ["AP EAPCET / institution admission process"], "source_note": "Official programmes page checked 2026-11-05; current tuition not stored because a comparable annual official figure was not confirmed."},
    "andhra-loyola-institute-of-engineering-and-technology": {"admission_url": "https://aliet.ac.in/pages/admissions", "entrance_exams": ["AP EAPCET", "AP ICET for MBA"], "source_note": "Official admissions page checked 2026-11-05; current tuition not stored because a comparable annual official figure was not confirmed."},
}

for college in COLLEGES:
    college.update(OVERRIDES.get(college["slug"], {}))

COURSE_ADDITIONS = {
    "university-of-delhi": ["BBA"],
    "jamia-hamdard": ["BBA"],
    "christ-university": ["BBA", "B.Tech Computer Science"],
    "jain-university": ["BBA", "B.Tech Computer Science"],
    "amity-university-noida": ["BBA", "B.Tech Computer Science"],
    "sharda-university": ["BBA", "B.Tech Computer Science"],
    "galgotias-university": ["BBA", "B.Tech Computer Science"],
    "lovely-professional-university": ["BBA", "B.Tech Computer Science"],
    "chandigarh-university": ["BBA", "B.Tech Computer Science"],
    "symbiosis-international-university": ["BBA"],
    "pes-university": ["BBA"],
    "indian-institute-of-technology-hyderabad": ["Artificial Intelligence"],
    "international-institute-of-information-technology-hyderabad": ["Artificial Intelligence"],
    "siddhartha-academy-of-higher-education": ["Artificial Intelligence"],
    "prasad-v-potluri-siddhartha-institute-of-technology": ["Artificial Intelligence"],
    "andhra-loyola-institute-of-engineering-and-technology": ["Artificial Intelligence"],
    "university-of-toronto": ["Artificial Intelligence"],
    "university-of-waterloo": ["Artificial Intelligence"],
    "york-university": ["Business Administration"],
    "national-university-of-singapore": ["Design"],
}
for college in COLLEGES:
    for course in COURSE_ADDITIONS.get(college["slug"], []):
        if course not in college["courses"]:
            college["courses"].append(course)

COURSE_REMOVALS = {
    "ludwig-maximilian-university-of-munich": ["Mechanical Engineering", "Engineering", "Design"],
}
for college in COLLEGES:
    removals = COURSE_REMOVALS.get(college["slug"], [])
    college["courses"] = [course for course in college["courses"] if course not in removals]

