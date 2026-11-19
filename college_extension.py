"""Nationwide Indian institution extension.

Each row uses an official institution domain and a deliberately small programme
list.  Unknown tuition remains unknown.  The list complements (and does not
replace) the original catalogue.  NIRF 2025 and the institutions' own academic
pages were used as the catalogue-selection and programme-checking sources.
"""

TECH = "Technology and Computer Science"
RESEARCH = "Analytical and Research"
DESIGN = "Creative and Design"
PEOPLE = "People and Service"
BUSINESS = "Business and Leadership"
HEALTH = "Health and Life Sciences"


def row(name, city, state, ownership, official_url, courses, fields, note=""):
    return {
        "name": name, "city": city, "state": state, "ownership": ownership,
        "official_url": official_url, "courses": courses, "career_fields": fields,
        "source_note": note or "Official institution website and academic/programme pages; catalogue entry reviewed 2026-11-19.",
    }


# Programme names are intentionally explicit.  A college is not made eligible
# for every course merely because it is an engineering, medical or university
# institution.
INDIAN_INSTITUTIONS = [
    # Andhra Pradesh — extra coverage includes every city requested by the project.
    row("Andhra University College of Engineering", "Visakhapatnam", "Andhra Pradesh", "Government", "https://www.andhrauniversity.edu.in/college/college-of-engineering/engineering-home.html", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH, RESEARCH], "Andhra University official programme list includes B.Tech CSE, Mechanical and other engineering branches; checked 2026-11-19."),
    row("GITAM School of Technology Visakhapatnam", "Visakhapatnam", "Andhra Pradesh", "Private", "https://www.gitam.edu/visakhapatnam", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH, RESEARCH], "GITAM official Visakhapatnam programme pages list B.Tech CSE and engineering programmes; checked 2026-11-19."),
    row("Gayatri Vidya Parishad College of Engineering", "Visakhapatnam", "Andhra Pradesh", "Private", "https://www.gvpce.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH], "Official departments and admissions pages reviewed 2026-11-19."),
    row("Anil Neerukonda Institute of Technology and Sciences", "Visakhapatnam", "Andhra Pradesh", "Private", "https://www.anits.edu.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH], "Official departments and programmes pages reviewed 2026-11-19."),
    row("Raghu Engineering College", "Visakhapatnam", "Andhra Pradesh", "Private", "https://www.raghuenggcollege.com", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH], "Official academic programmes pages reviewed 2026-11-19."),
    row("Raghu Institute of Technology", "Visakhapatnam", "Andhra Pradesh", "Private", "https://www.raghuinstech.com", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH], "Official academic programmes pages reviewed 2026-11-19."),
    row("Jawaharlal Nehru Technological University Kakinada", "Kakinada", "Andhra Pradesh", "Government", "https://www.jntuk.edu.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH, RESEARCH]),
    row("Adikavi Nannaya University", "Rajahmundry", "Andhra Pradesh", "Government", "https://aknu.edu.in", ["Computer Science", "Business", "Life Sciences", "Science"], [TECH, RESEARCH, BUSINESS, HEALTH]),
    row("Vignan's Foundation for Science Technology and Research", "Guntur", "Andhra Pradesh", "Private", "https://vignan.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH, RESEARCH]),
    row("Koneru Lakshmaiah Education Foundation", "Guntur", "Andhra Pradesh", "Private", "https://www.kluniversity.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering", "BBA"], [TECH, BUSINESS]),
    row("Sri Venkateswara University College of Engineering", "Tirupati", "Andhra Pradesh", "Government", "https://svuniversity.edu.in/college-of-engineering", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Narayana Medical College", "Nellore", "Andhra Pradesh", "Private", "https://www.narayanamedicalcollege.com", ["MBBS", "Medicine"], [HEALTH]),

    # Telangana
    row("Osmania University College of Engineering", "Hyderabad", "Telangana", "Government", "https://www.uceou.edu", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("JNTUH University College of Engineering Science and Technology", "Hyderabad", "Telangana", "Government", "https://jntuh.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH, RESEARCH]),
    row("Chaitanya Bharathi Institute of Technology", "Hyderabad", "Telangana", "Private", "https://www.cbit.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Vasavi College of Engineering", "Hyderabad", "Telangana", "Private", "https://www.vce.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("VNR Vignana Jyothi Institute of Engineering and Technology", "Hyderabad", "Telangana", "Private", "https://vnrvjiet.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Kakatiya University", "Warangal", "Telangana", "Government", "https://kakatiya.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, RESEARCH, BUSINESS, HEALTH, PEOPLE]),
    row("National Institute of Technology Warangal", "Warangal", "Telangana", "Government", "https://www.nitw.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH, RESEARCH]),
    row("Kaloji Narayana Rao University of Health Sciences", "Warangal", "Telangana", "Government", "https://www.knruhs.telangana.gov.in", ["Medicine", "Life Sciences"], [HEALTH]),

    # Tamil Nadu
    row("PSG College of Technology", "Coimbatore", "Tamil Nadu", "Private", "https://www.psgtech.edu", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Coimbatore Institute of Technology", "Coimbatore", "Tamil Nadu", "Private", "https://www.cit.edu.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Government College of Technology Coimbatore", "Coimbatore", "Tamil Nadu", "Government", "https://gct.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Thiagarajar College of Engineering", "Madurai", "Tamil Nadu", "Private", "https://www.tce.edu", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Kalasalingam Academy of Research and Education", "Krishnankoil", "Tamil Nadu", "Private", "https://www.kalasalingam.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH, RESEARCH]),
    row("SASTRA Deemed University", "Thanjavur", "Tamil Nadu", "Private", "https://www.sastra.edu", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering", "Science"], [TECH, RESEARCH]),
    row("Alagappa University", "Karaikudi", "Tamil Nadu", "Government", "https://www.alagappauniversity.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Bharathiar University", "Coimbatore", "Tamil Nadu", "Government", "https://b-u.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Psychology", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("National Institute of Fashion Technology Chennai", "Chennai", "Tamil Nadu", "Government", "https://www.nift.ac.in/chennai", ["B.Des", "Design"], [DESIGN]),
    row("Madurai Medical College", "Madurai", "Tamil Nadu", "Government", "https://maduraimedicalcollege.ac.in", ["MBBS", "Medicine"], [HEALTH]),

    # Karnataka
    row("University Visvesvaraya College of Engineering", "Bengaluru", "Karnataka", "Government", "https://uvce.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Dayananda Sagar College of Engineering", "Bengaluru", "Karnataka", "Private", "https://www.dsce.edu.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("New Horizon College of Engineering", "Bengaluru", "Karnataka", "Private", "https://newhorizoncollegeofengineering.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("JSS Science and Technology University", "Mysuru", "Karnataka", "Private", "https://jssstuniv.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("The National Institute of Engineering", "Mysuru", "Karnataka", "Private", "https://nie.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("KLE Technological University", "Hubballi", "Karnataka", "Private", "https://www.kletech.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Karnatak University", "Dharwad", "Karnataka", "Government", "https://www.kud.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Mysore Medical College and Research Institute", "Mysuru", "Karnataka", "Government", "https://mmcri.karnataka.gov.in", ["MBBS", "Medicine"], [HEALTH]),

    # Maharashtra
    row("Walchand College of Engineering", "Sangli", "Maharashtra", "Government", "https://www.walchandsangli.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Pune Institute of Computer Technology", "Pune", "Maharashtra", "Private", "https://pict.edu", ["B.Tech Computer Science", "Engineering"], [TECH]),
    row("Vishwakarma Institute of Technology", "Pune", "Maharashtra", "Private", "https://www.vit.edu", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("MIT World Peace University", "Pune", "Maharashtra", "Private", "https://mitwpu.edu.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering", "BBA", "Design"], [TECH, BUSINESS, DESIGN]),
    row("Bharati Vidyapeeth Deemed University", "Pune", "Maharashtra", "Private", "https://www.bvuniversity.edu.in", ["B.Tech Computer Science", "Engineering", "BBA", "Medicine", "Life Sciences"], [TECH, BUSINESS, HEALTH]),
    row("Shri Ramdeobaba College of Engineering and Management", "Nagpur", "Maharashtra", "Private", "https://www.rknec.edu", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Government College of Engineering Aurangabad", "Chhatrapati Sambhajinagar", "Maharashtra", "Government", "https://geca.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Dr. Babasaheb Ambedkar Marathwada University", "Chhatrapati Sambhajinagar", "Maharashtra", "Government", "https://www.bamu.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Shivaji University", "Kolhapur", "Maharashtra", "Government", "https://www.unishivaji.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Government Medical College Nagpur", "Nagpur", "Maharashtra", "Government", "https://gmcnagpur.org", ["MBBS", "Medicine"], [HEALTH]),

    # Kerala
    row("TKM College of Engineering", "Kollam", "Kerala", "Government", "https://tkmce.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Rajagiri School of Engineering and Technology", "Kochi", "Kerala", "Private", "https://www.rajagiritech.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Model Engineering College", "Kochi", "Kerala", "Government", "https://www.mec.ac.in", ["B.Tech Computer Science", "Engineering"], [TECH]),
    row("University of Calicut", "Malappuram", "Kerala", "Government", "https://uoc.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Psychology", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Mahatma Gandhi University Kerala", "Kottayam", "Kerala", "Government", "https://www.mgu.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Psychology", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Government Medical College Kozhikode", "Kozhikode", "Kerala", "Government", "https://www.govtmedicalcollegekozhikode.ac.in", ["MBBS", "Medicine"], [HEALTH]),

    # Gujarat and Rajasthan
    row("Nirma University", "Ahmedabad", "Gujarat", "Private", "https://nirmauni.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering", "BBA"], [TECH, BUSINESS]),
    row("Ahmedabad University", "Ahmedabad", "Gujarat", "Private", "https://ahduni.edu.in", ["Computer Science", "Business", "Life Sciences", "Science"], [TECH, BUSINESS, HEALTH, RESEARCH]),
    row("Gujarat Technological University", "Ahmedabad", "Gujarat", "Government", "https://www.gtu.ac.in", ["Engineering", "Business", "Pharmacy"], [TECH, BUSINESS, HEALTH]),
    row("Pandit Deendayal Energy University", "Gandhinagar", "Gujarat", "Private", "https://www.pdeu.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Maharaja Sayajirao University of Baroda", "Vadodara", "Gujarat", "Government", "https://msubaroda.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Design", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, DESIGN, PEOPLE]),
    row("Government Medical College Surat", "Surat", "Gujarat", "Government", "https://gmcsurat.edu.in", ["MBBS", "Medicine"], [HEALTH]),
    row("Rajasthan Technical University", "Kota", "Rajasthan", "Government", "https://www.rtu.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("MBM University", "Jodhpur", "Rajasthan", "Government", "https://www.mbm.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Manipal University Jaipur", "Jaipur", "Rajasthan", "Private", "https://jaipur.manipal.edu", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering", "BBA", "Design"], [TECH, BUSINESS, DESIGN]),
    row("JECRC University", "Jaipur", "Rajasthan", "Private", "https://jecrcuniversity.edu.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering", "BBA"], [TECH, BUSINESS]),
    row("Mohanlal Sukhadia University", "Udaipur", "Rajasthan", "Government", "https://www.mlsu.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Dr. Sampurnanand Medical College", "Jodhpur", "Rajasthan", "Government", "https://education.rajasthan.gov.in/smcjodhpur", ["MBBS", "Medicine"], [HEALTH]),

    # Uttar Pradesh, Bihar and Jharkhand
    row("Harcourt Butler Technical University", "Kanpur", "Uttar Pradesh", "Government", "https://hbtu.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Madan Mohan Malaviya University of Technology", "Gorakhpur", "Uttar Pradesh", "Government", "https://www.mmmut.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Motilal Nehru National Institute of Technology Allahabad", "Prayagraj", "Uttar Pradesh", "Government", "https://www.mnnit.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Jaypee Institute of Information Technology", "Noida", "Uttar Pradesh", "Private", "https://www.jiit.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Engineering"], [TECH]),
    row("GLA University", "Mathura", "Uttar Pradesh", "Private", "https://www.gla.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering", "BBA"], [TECH, BUSINESS]),
    row("University of Lucknow", "Lucknow", "Uttar Pradesh", "Government", "https://www.lkouniv.ac.in", ["Computer Science", "BBA", "Business", "Life Sciences", "Science", "Psychology", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Babasaheb Bhimrao Ambedkar University", "Lucknow", "Uttar Pradesh", "Government", "https://www.bbau.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Indian Institute of Management Lucknow", "Lucknow", "Uttar Pradesh", "Government", "https://www.iiml.ac.in", ["Business", "Business Administration"], [BUSINESS]),
    row("Uttar Pradesh University of Medical Sciences", "Saifai", "Uttar Pradesh", "Government", "https://www.upums.ac.in", ["MBBS", "Medicine", "Life Sciences"], [HEALTH]),
    row("Banaras Hindu University Faculty of Visual Arts", "Varanasi", "Uttar Pradesh", "Government", "https://www.bhu.ac.in/Site/UnitHomeTemplate/1_3255_6475_3255", ["Design", "Fine Arts"], [DESIGN]),
    row("National Institute of Technology Patna", "Patna", "Bihar", "Government", "https://www.nitp.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Patna University", "Patna", "Bihar", "Government", "https://pup.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Psychology", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Central University of South Bihar", "Gaya", "Bihar", "Government", "https://www.cusb.ac.in", ["Computer Science", "Life Sciences", "Science", "Psychology", "Education"], [TECH, HEALTH, RESEARCH, PEOPLE]),
    row("Aryabhatta Knowledge University", "Patna", "Bihar", "Government", "https://akubihar.ac.in", ["Engineering", "Medicine", "Business", "Life Sciences"], [TECH, HEALTH, BUSINESS]),
    row("Nalanda University", "Rajgir", "Bihar", "Government", "https://nalandauniv.edu.in", ["Science", "Business", "History", "Environmental Science"], [RESEARCH, BUSINESS, PEOPLE]),
    row("National Institute of Technology Jamshedpur", "Jamshedpur", "Jharkhand", "Government", "https://www.nitjsr.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("National University of Study and Research in Law", "Ranchi", "Jharkhand", "Government", "https://www.nusrlranchi.ac.in", ["Law"], [PEOPLE]),
    row("Central University of Jharkhand", "Ranchi", "Jharkhand", "Government", "https://cuj.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Rajendra Institute of Medical Sciences", "Ranchi", "Jharkhand", "Government", "https://www.rimsranchi.ac.in", ["MBBS", "Medicine"], [HEALTH]),

    # Madhya Pradesh, Chhattisgarh and Odisha
    row("Maulana Azad National Institute of Technology", "Bhopal", "Madhya Pradesh", "Government", "https://www.manit.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Shri Govindram Seksaria Institute of Technology and Science", "Indore", "Madhya Pradesh", "Government", "https://www.sgsits.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Jabalpur Engineering College", "Jabalpur", "Madhya Pradesh", "Government", "https://www.jecjabalpur.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Devi Ahilya Vishwavidyalaya", "Indore", "Madhya Pradesh", "Government", "https://www.dauniv.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Lakshmi Narain College of Technology Bhopal", "Bhopal", "Madhya Pradesh", "Private", "https://lnct.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Gandhi Medical College Bhopal", "Bhopal", "Madhya Pradesh", "Government", "https://gmcbhopal.net", ["MBBS", "Medicine"], [HEALTH]),
    row("Bhilai Institute of Technology Durg", "Durg", "Chhattisgarh", "Private", "https://bitdurg.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Guru Ghasidas Vishwavidyalaya", "Bilaspur", "Chhattisgarh", "Government", "https://www.ggu.ac.in", ["Computer Science", "Engineering", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Pt. Ravishankar Shukla University", "Raipur", "Chhattisgarh", "Government", "https://www.prsu.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("All India Institute of Medical Sciences Raipur", "Raipur", "Chhattisgarh", "Government", "https://www.aiimsraipur.edu.in", ["MBBS", "Medicine"], [HEALTH]),
    row("Veer Surendra Sai University of Technology", "Burla", "Odisha", "Government", "https://www.vssut.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Odisha University of Technology and Research", "Bhubaneswar", "Odisha", "Government", "https://outr.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Utkal University", "Bhubaneswar", "Odisha", "Government", "https://utkaluniversity.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Psychology", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Ravenshaw University", "Cuttack", "Odisha", "Government", "https://ravenshawuniversity.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Psychology"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("All India Institute of Medical Sciences Bhubaneswar", "Bhubaneswar", "Odisha", "Government", "https://aiimsbhubaneswar.nic.in", ["MBBS", "Medicine"], [HEALTH]),

    # West Bengal and the North East
    row("Indian Institute of Engineering Science and Technology Shibpur", "Howrah", "West Bengal", "Government", "https://www.iiests.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH, RESEARCH]),
    row("Kalyani Government Engineering College", "Kalyani", "West Bengal", "Government", "https://kgec.edu.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Heritage Institute of Technology", "Kolkata", "West Bengal", "Private", "https://www.heritageit.edu", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Maulana Abul Kalam Azad University of Technology", "Kolkata", "West Bengal", "Government", "https://makautwb.ac.in", ["Computer Science", "Engineering", "Business", "Science"], [TECH, BUSINESS, RESEARCH]),
    row("University of North Bengal", "Siliguri", "West Bengal", "Government", "https://www.nbu.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Institute of Post Graduate Medical Education and Research Kolkata", "Kolkata", "West Bengal", "Government", "https://ipgmer.gov.in", ["MBBS", "Medicine"], [HEALTH]),
    row("Assam Engineering College", "Guwahati", "Assam", "Government", "https://www.aec.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Assam University", "Silchar", "Assam", "Government", "https://www.aus.ac.in", ["Computer Science", "Engineering", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Cotton University", "Guwahati", "Assam", "Government", "https://cottonuniversity.ac.in", ["Computer Science", "Life Sciences", "Science", "Psychology"], [TECH, HEALTH, RESEARCH, PEOPLE]),
    row("Manipur University", "Imphal", "Manipur", "Government", "https://www.manipuruniv.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("North Eastern Hill University", "Shillong", "Meghalaya", "Government", "https://www.nehu.ac.in", ["Computer Science", "Engineering", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Mizoram University", "Aizawl", "Mizoram", "Government", "https://mzu.edu.in", ["Computer Science", "Engineering", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Nagaland University", "Lumami", "Nagaland", "Government", "https://nagalanduniversity.ac.in", ["Computer Science", "Engineering", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Tripura University", "Agartala", "Tripura", "Government", "https://tripurauniv.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Sikkim University", "Gangtok", "Sikkim", "Government", "https://cus.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Psychology", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Rajiv Gandhi University", "Itanagar", "Arunachal Pradesh", "Government", "https://rgu.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),

    # Punjab, Haryana, hill states, Goa and Union Territories
    row("Guru Nanak Dev University", "Amritsar", "Punjab", "Government", "https://online.gndu.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Dr. B. R. Ambedkar National Institute of Technology Jalandhar", "Jalandhar", "Punjab", "Government", "https://www.nitj.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Punjab Agricultural University", "Ludhiana", "Punjab", "Government", "https://www.pau.edu", ["Agriculture", "Biotechnology", "Life Sciences", "Science"], [HEALTH, RESEARCH]),
    row("National Institute of Technology Kurukshetra", "Kurukshetra", "Haryana", "Government", "https://nitkkr.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Deenbandhu Chhotu Ram University of Science and Technology", "Sonipat", "Haryana", "Government", "https://www.dcrustm.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering", "Science"], [TECH, RESEARCH]),
    row("Maharshi Dayanand University", "Rohtak", "Haryana", "Government", "https://mdu.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("National Institute of Technology Hamirpur", "Hamirpur", "Himachal Pradesh", "Government", "https://nith.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Himachal Pradesh University", "Shimla", "Himachal Pradesh", "Government", "https://www.hpuniv.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Govind Ballabh Pant University of Agriculture and Technology", "Pantnagar", "Uttarakhand", "Government", "https://www.gbpuat.ac.in", ["Engineering", "Agriculture", "Biotechnology", "Life Sciences", "Science"], [TECH, HEALTH, RESEARCH]),
    row("Doon University", "Dehradun", "Uttarakhand", "Government", "https://www.doonuniversity.ac.in", ["Computer Science", "Business", "Design", "Science", "Psychology"], [TECH, BUSINESS, DESIGN, RESEARCH, PEOPLE]),
    row("University of Kashmir", "Srinagar", "Jammu and Kashmir", "Government", "https://www.kashmiruniversity.net", ["Computer Science", "Business", "Life Sciences", "Science", "Psychology", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Shri Mata Vaishno Devi University", "Katra", "Jammu and Kashmir", "Government", "https://www.smvdu.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering", "Business"], [TECH, BUSINESS]),
    row("University of Ladakh", "Leh", "Ladakh", "Government", "https://uol.ac.in", ["Computer Science", "Business", "Science", "Education"], [TECH, BUSINESS, RESEARCH, PEOPLE]),
    row("Goa University", "Panaji", "Goa", "Government", "https://www.unigoa.ac.in", ["Computer Science", "Business", "Life Sciences", "Science", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Goa College of Engineering", "Ponda", "Goa", "Government", "https://www.gec.ac.in", ["B.Tech Computer Science", "Mechanical Engineering", "Engineering"], [TECH]),
    row("Pondicherry University", "Puducherry", "Puducherry", "Government", "https://www.pondiuni.edu.in", ["Computer Science", "Business", "Life Sciences", "Science", "Psychology", "Education"], [TECH, BUSINESS, HEALTH, RESEARCH, PEOPLE]),
    row("Delhi Pharmaceutical Sciences and Research University", "New Delhi", "Delhi", "Government", "https://dpsru.edu.in", ["Pharmacy", "Public Health", "Life Sciences"], [HEALTH]),
    row("National Institute of Technology Delhi", "New Delhi", "Delhi", "Government", "https://nitdelhi.ac.in", ["B.Tech Computer Science", "Artificial Intelligence", "Mechanical Engineering", "Engineering"], [TECH]),
]
