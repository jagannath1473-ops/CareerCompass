"""Independent academic course catalogue.

This catalogue drives discovery only.  A course appearing here never implies that
an institution offers it; eligibility is always checked against that institution's
stored ``courses`` list by recommendation.py.
"""

import re


CATEGORIES = [
    "Technology and Computer Science", "Analytical and Research",
    "Creative and Design", "People and Service", "Business and Leadership",
    "Health and Life Sciences",
]


def _rows(category, level, names):
    rows = []
    for entry in names:
        parts = [part.strip() for part in entry.split("|")]
        rows.append({"name": parts[0], "category": category, "level": level,
                     "aliases": parts[1:]})
    return rows


COURSE_CATALOG = []

# Technology and Computer Science
COURSE_CATALOG += _rows(CATEGORIES[0], "Undergraduate", [
    "B.Tech Computer Science Engineering|B.Tech Computer Science|BTech CSE|CSE",
    "B.Tech Artificial Intelligence and Machine Learning|BTech AI ML|AI and ML",
    "B.Tech Artificial Intelligence|BTech AI", "B.Tech Data Science|BTech DS",
    "B.Tech Cybersecurity|BTech Cyber Security", "B.Tech Information Technology|BTech IT",
    "B.Tech Software Engineering", "B.Tech Computer Engineering",
    "B.Tech Electronics and Communication Engineering|BTech ECE|ECE",
    "B.Tech Electrical and Electronics Engineering|BTech EEE|EEE",
    "B.Tech Electrical Engineering|BTech EE", "B.Tech Mechanical Engineering|BTech Mechanical",
    "B.Tech Civil Engineering|BTech Civil", "B.Tech Chemical Engineering|BTech Chemical",
    "B.Tech Aerospace Engineering", "B.Tech Aeronautical Engineering",
    "B.Tech Automobile Engineering", "B.Tech Robotics Engineering",
    "B.Tech Mechatronics Engineering", "B.Tech Biotechnology Engineering",
    "B.Tech Biomedical Engineering", "B.Tech Industrial Engineering",
    "B.Tech Production Engineering", "B.Tech Marine Engineering",
    "B.Tech Mining Engineering", "B.Tech Petroleum Engineering",
    "B.Tech Agricultural Engineering", "B.Tech Food Technology",
    "B.Tech Environmental Engineering", "B.Tech Instrumentation Engineering",
    "B.Tech Metallurgical and Materials Engineering", "B.Tech Textile Technology",
    "BCA|Bachelor of Computer Applications", "B.Sc Computer Science|BSc CS",
    "B.Sc Information Technology|BSc IT", "B.Sc Artificial Intelligence|BSc AI",
    "B.Sc Data Science", "B.Sc Cybersecurity", "B.Sc Software Engineering",
    "Bachelor of Information Systems", "Bachelor of Computer Science",
])
COURSE_CATALOG += _rows(CATEGORIES[0], "Postgraduate", [
    "M.Tech Computer Science Engineering|MTech CSE", "M.Tech Artificial Intelligence",
    "M.Tech Data Science", "M.Tech Cybersecurity", "M.Tech Information Technology",
    "M.Tech VLSI Design", "M.Tech Embedded Systems", "M.Tech Robotics",
    "M.Tech Cloud Computing", "M.Tech Structural Engineering", "M.Tech Thermal Engineering",
    "MCA|Master of Computer Applications", "M.Sc Computer Science|MSc CS",
    "M.Sc Data Science", "M.Sc Artificial Intelligence", "M.Sc Cybersecurity",
])
COURSE_CATALOG += _rows(CATEGORIES[0], "Diploma", [
    "Diploma in Computer Engineering", "Diploma in Information Technology",
    "Diploma in Mechanical Engineering", "Diploma in Civil Engineering",
    "Diploma in Electronics Engineering", "Diploma in Electrical Engineering",
    "Diploma in Cloud Computing", "Diploma in Web Development",
])

# Analytical and Research
COURSE_CATALOG += _rows(CATEGORIES[1], "Undergraduate", [
    "B.Sc Mathematics|BSc Mathematics", "B.Sc Applied Mathematics",
    "B.Sc Statistics", "B.Stat|Bachelor of Statistics", "B.Sc Physics",
    "B.Sc Chemistry", "B.Sc Economics", "BA Economics", "B.Sc Econometrics",
    "B.Sc Data Analytics", "B.Sc Astronomy", "B.Sc Astrophysics",
    "B.Sc Environmental Science", "B.Sc Forensic Science", "B.Sc Geology",
    "B.Sc Geography", "B.Sc Computational Science", "B.Sc Actuarial Science",
    "B.Sc Operations Research", "B.Sc Earth Science", "B.Sc Oceanography",
    "B.Sc Meteorology", "B.Sc Materials Science", "Bachelor of Science|BSc",
])
COURSE_CATALOG += _rows(CATEGORIES[1], "Postgraduate", [
    "M.Sc Mathematics", "M.Sc Applied Mathematics", "M.Sc Statistics",
    "M.Stat|Master of Statistics", "M.Sc Physics", "M.Sc Chemistry",
    "M.Sc Economics", "MA Economics", "M.Sc Data Analytics",
    "M.Sc Astronomy", "M.Sc Astrophysics", "M.Sc Environmental Science",
    "M.Sc Forensic Science", "M.Sc Geology", "M.Sc Computational Science",
    "M.Sc Operations Research", "M.Sc Materials Science", "Master of Science|MSc",
])
COURSE_CATALOG += _rows(CATEGORIES[1], "Diploma", [
    "Postgraduate Diploma in Data Analytics", "Postgraduate Diploma in Applied Statistics",
    "Diploma in Forensic Science", "Diploma in Environmental Science",
])

# Creative and Design
COURSE_CATALOG += _rows(CATEGORIES[2], "Undergraduate", [
    "Bachelor of Design|B.Des|BDes", "B.Des Fashion Design", "B.Des Interior Design",
    "B.Des Product Design", "B.Des Graphic Design", "B.Des UI UX Design|UI/UX Design",
    "B.Des Animation", "B.Des Visual Communication", "B.Des Communication Design",
    "B.Des Industrial Design", "B.Des Interaction Design", "B.Des Textile Design",
    "B.Des Accessory Design", "B.Des Transportation Design", "B.Des Game Design",
    "Bachelor of Architecture|B.Arch|BArch", "Bachelor of Fine Arts|BFA",
    "BA Film Studies", "BA Photography", "BA Performing Arts", "BA Music",
    "BA Theatre", "BA Digital Media", "BA Animation and VFX|Animation and VFX",
    "Bachelor of Fashion Technology|BFTech", "Bachelor of Planning|B.Plan",
])
COURSE_CATALOG += _rows(CATEGORIES[2], "Postgraduate", [
    "Master of Design|M.Des|MDes", "M.Des Product Design", "M.Des Interaction Design",
    "M.Des Communication Design", "M.Des Industrial Design", "Master of Architecture|M.Arch",
    "Master of Fine Arts|MFA", "MA Film Studies", "MA Visual Communication",
])
COURSE_CATALOG += _rows(CATEGORIES[2], "Diploma", [
    "Diploma in Graphic Design", "Diploma in Interior Design", "Diploma in Fashion Design",
    "Diploma in Animation and VFX", "Diploma in Photography", "Diploma in UI UX Design",
])

# People and Service
COURSE_CATALOG += _rows(CATEGORIES[3], "Undergraduate", [
    "BA Psychology", "B.Sc Psychology", "Bachelor of Laws|LLB", "BA LLB",
    "BBA LLB", "B.Com LLB", "Bachelor of Education|B.Ed", "Bachelor of Social Work|BSW",
    "BA Sociology", "BA Political Science", "BA Public Administration",
    "BA Journalism", "BA Mass Communication", "BA Journalism and Mass Communication|BJMC",
    "Bachelor of Hotel Management|BHM", "Bachelor of Hospitality Management",
    "Bachelor of Tourism Management", "BA International Relations", "BA History",
    "BA Philosophy", "BA English", "BA Linguistics", "Bachelor of Library Science|B.Lib",
    "Bachelor of Elementary Education|B.El.Ed", "Bachelor of Physical Education|B.P.Ed",
    "BA Anthropology", "BA Criminology", "BA Development Studies",
])
COURSE_CATALOG += _rows(CATEGORIES[3], "Postgraduate", [
    "MA Psychology", "M.Sc Psychology", "Master of Laws|LLM", "Master of Education|M.Ed",
    "Master of Social Work|MSW", "MA Sociology", "MA Political Science",
    "Master of Public Administration|MPA", "MA Journalism and Mass Communication",
    "Master of Hotel Management", "Master of Tourism Management",
    "MA International Relations", "MA Development Studies", "Master of Library Science|M.Lib",
])
COURSE_CATALOG += _rows(CATEGORIES[3], "Diploma", [
    "Diploma in Education|D.Ed", "Diploma in Hotel Management",
    "Diploma in Travel and Tourism", "Diploma in Journalism",
    "Postgraduate Diploma in Counselling Psychology",
])

# Business and Leadership
COURSE_CATALOG += _rows(CATEGORIES[4], "Undergraduate", [
    "Bachelor of Business Administration|BBA", "BBA Finance", "BBA Marketing",
    "BBA Human Resource Management|BBA HR", "BBA Business Analytics",
    "BBA International Business", "BBA Entrepreneurship", "BBA Logistics and Supply Chain",
    "Bachelor of Commerce|B.Com|BCom", "B.Com Accounting and Finance",
    "B.Com Banking and Insurance", "B.Com Taxation", "B.Com Corporate Secretaryship",
    "Bachelor of Management Studies|BMS", "Bachelor of Financial Markets|BFM",
    "Bachelor of Banking and Insurance|BBI", "BA Business Economics",
    "Bachelor of Accounting", "Bachelor of Finance", "Bachelor of Marketing",
    "Bachelor of International Business", "Bachelor of Supply Chain Management",
    "Bachelor of Hospitality Business Management",
])
COURSE_CATALOG += _rows(CATEGORIES[4], "Postgraduate", [
    "Master of Business Administration|MBA", "MBA Finance", "MBA Marketing",
    "MBA Human Resource Management|MBA HR", "MBA Business Analytics",
    "MBA International Business", "MBA Entrepreneurship", "MBA Operations Management",
    "MBA Supply Chain Management", "MBA Healthcare Management", "MBA Information Technology",
    "Master of Commerce|M.Com|MCom", "Master of Management Studies|MMS",
    "Master of Finance", "Master of Accounting", "Master of International Business",
])
COURSE_CATALOG += _rows(CATEGORIES[4], "Diploma", [
    "Postgraduate Diploma in Management|PGDM", "PGDM Finance", "PGDM Marketing",
    "PGDM Human Resource Management", "Diploma in Banking and Finance",
    "Diploma in Logistics and Supply Chain Management", "Diploma in Retail Management",
])

# Health and Life Sciences
COURSE_CATALOG += _rows(CATEGORIES[5], "Undergraduate", [
    "Bachelor of Medicine and Bachelor of Surgery|MBBS", "Bachelor of Dental Surgery|BDS",
    "Bachelor of Science Nursing|B.Sc Nursing", "General Nursing and Midwifery|GNM",
    "Bachelor of Pharmacy|B.Pharm|BPharm", "Doctor of Pharmacy|PharmD",
    "Bachelor of Physiotherapy|BPT", "Bachelor of Occupational Therapy|BOT",
    "B.Sc Biotechnology", "B.Sc Microbiology", "B.Sc Biochemistry", "B.Sc Genetics",
    "B.Sc Biomedical Science", "B.Sc Nutrition and Dietetics", "Bachelor of Public Health|BPH",
    "B.Sc Medical Laboratory Technology|BMLT", "B.Sc Radiology and Imaging Technology",
    "Bachelor of Veterinary Science|BVSc", "B.Sc Agriculture", "B.Sc Horticulture",
    "B.Sc Forestry", "B.Sc Food Science", "B.Sc Zoology", "B.Sc Botany",
    "B.Sc Neuroscience", "B.Sc Allied Health Sciences", "Bachelor of Audiology and Speech Language Pathology|BASLP",
    "Bachelor of Optometry|B.Optom", "Bachelor of Ayurvedic Medicine and Surgery|BAMS",
    "Bachelor of Homoeopathic Medicine and Surgery|BHMS", "Bachelor of Unani Medicine and Surgery|BUMS",
    "Bachelor of Naturopathy and Yogic Sciences|BNYS", "B.Sc Anaesthesia Technology",
    "B.Sc Operation Theatre Technology", "B.Sc Cardiac Care Technology",
    "B.Sc Dialysis Technology", "B.Sc Emergency Medical Technology",
])
COURSE_CATALOG += _rows(CATEGORIES[5], "Postgraduate", [
    "Doctor of Medicine|MD", "Master of Surgery|MS", "Master of Dental Surgery|MDS",
    "M.Sc Nursing", "Master of Pharmacy|M.Pharm", "Master of Physiotherapy|MPT",
    "Master of Public Health|MPH", "M.Sc Biotechnology", "M.Sc Microbiology",
    "M.Sc Biochemistry", "M.Sc Genetics", "M.Sc Biomedical Science",
    "M.Sc Nutrition and Dietetics", "M.Sc Medical Laboratory Technology",
    "M.Sc Agriculture", "Master of Veterinary Science|MVSc",
])
COURSE_CATALOG += _rows(CATEGORIES[5], "Diploma", [
    "Diploma in Pharmacy|D.Pharm", "Auxiliary Nurse Midwifery|ANM",
    "Diploma in Medical Laboratory Technology|DMLT", "Diploma in Radiology Technology",
    "Diploma in Operation Theatre Technology", "Diploma in Nutrition and Dietetics",
])

# Keep the student-facing catalogue deliberately manageable: up to 25 UG,
# 10 PG and 5 diploma choices per category (239 distinct programmes today).
# The longer source lists above make future expansion a data-only change.
_expanded_catalog = COURSE_CATALOG
COURSE_CATALOG = []
for _category in CATEGORIES:
    for _level, _limit in (("Undergraduate", 25), ("Postgraduate", 10), ("Diploma", 5)):
        COURSE_CATALOG.extend([
            item for item in _expanded_catalog
            if item["category"] == _category and item["level"] == _level
        ][:_limit])


def clean(value):
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


_BY_NAME = {clean(item["name"]): item for item in COURSE_CATALOG}
_BY_ALIAS = {}
for _item in COURSE_CATALOG:
    for _alias in [_item["name"], *_item["aliases"]]:
        _BY_ALIAS.setdefault(clean(_alias), _item)


def resolve_course(value):
    """Return a catalogue row for an exact name/alias, or None."""
    return _BY_ALIAS.get(clean(value))


def course_options(category=""):
    return [item for item in COURSE_CATALOG if not category or item["category"] == category]


def catalogue_payload():
    return [{"name": item["name"], "category": item["category"], "level": item["level"],
             "aliases": item["aliases"]} for item in COURSE_CATALOG]

