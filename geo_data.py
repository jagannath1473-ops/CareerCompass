"""Offline location catalogue used by the preference form and Flask APIs.

The lists are deliberately bundled with the project so the selectors work without
a paid geocoding service.  Indian state/UT names follow Government of India usage;
international subdivision labels follow the terminology used in each country.
Users can always type a city that is not present in the curated city list.
"""

COUNTRIES = sorted("""
Afghanistan|Albania|Algeria|American Samoa|Andorra|Angola|Anguilla|Antarctica|Antigua and Barbuda|Argentina|Armenia|Aruba|Australia|Austria|Azerbaijan|Bahamas|Bahrain|Bangladesh|Barbados|Belarus|Belgium|Belize|Benin|Bermuda|Bhutan|Bolivia|Bonaire, Sint Eustatius and Saba|Bosnia and Herzegovina|Botswana|Bouvet Island|Brazil|British Indian Ocean Territory|Brunei|Bulgaria|Burkina Faso|Burundi|Cabo Verde|Cambodia|Cameroon|Canada|Cayman Islands|Central African Republic|Chad|Chile|China|Christmas Island|Cocos Islands|Colombia|Comoros|Congo|Cook Islands|Costa Rica|Cote d'Ivoire|Croatia|Cuba|Curacao|Cyprus|Czechia|Democratic Republic of the Congo|Denmark|Djibouti|Dominica|Dominican Republic|Ecuador|Egypt|El Salvador|Equatorial Guinea|Eritrea|Estonia|Eswatini|Ethiopia|Falkland Islands|Faroe Islands|Fiji|Finland|France|French Guiana|French Polynesia|French Southern Territories|Gabon|Gambia|Georgia|Germany|Ghana|Gibraltar|Greece|Greenland|Grenada|Guadeloupe|Guam|Guatemala|Guernsey|Guinea|Guinea-Bissau|Guyana|Haiti|Heard Island and McDonald Islands|Holy See|Honduras|Hong Kong|Hungary|Iceland|India|Indonesia|Iran|Iraq|Ireland|Isle of Man|Israel|Italy|Jamaica|Japan|Jersey|Jordan|Kazakhstan|Kenya|Kiribati|Kosovo|Kuwait|Kyrgyzstan|Laos|Latvia|Lebanon|Lesotho|Liberia|Libya|Liechtenstein|Lithuania|Luxembourg|Macao|Madagascar|Malawi|Malaysia|Maldives|Mali|Malta|Marshall Islands|Martinique|Mauritania|Mauritius|Mayotte|Mexico|Micronesia|Moldova|Monaco|Mongolia|Montenegro|Montserrat|Morocco|Mozambique|Myanmar|Namibia|Nauru|Nepal|Netherlands|New Caledonia|New Zealand|Nicaragua|Niger|Nigeria|Niue|Norfolk Island|North Korea|North Macedonia|Northern Mariana Islands|Norway|Oman|Pakistan|Palau|Palestine|Panama|Papua New Guinea|Paraguay|Peru|Philippines|Pitcairn|Poland|Portugal|Puerto Rico|Qatar|Reunion|Romania|Russia|Rwanda|Saint Barthelemy|Saint Helena|Saint Kitts and Nevis|Saint Lucia|Saint Martin|Saint Pierre and Miquelon|Saint Vincent and the Grenadines|Samoa|San Marino|Sao Tome and Principe|Saudi Arabia|Senegal|Serbia|Seychelles|Sierra Leone|Singapore|Sint Maarten|Slovakia|Slovenia|Solomon Islands|Somalia|South Africa|South Georgia and the South Sandwich Islands|South Korea|South Sudan|Spain|Sri Lanka|Sudan|Suriname|Svalbard and Jan Mayen|Sweden|Switzerland|Syria|Taiwan|Tajikistan|Tanzania|Thailand|Timor-Leste|Togo|Tokelau|Tonga|Trinidad and Tobago|Tunisia|Turkiye|Turkmenistan|Turks and Caicos Islands|Tuvalu|Uganda|Ukraine|United Arab Emirates|United Kingdom|United States|United States Minor Outlying Islands|Uruguay|Uzbekistan|Vanuatu|Venezuela|Vietnam|Virgin Islands, British|Virgin Islands, U.S.|Wallis and Futuna|Western Sahara|Yemen|Zambia|Zimbabwe
""".strip().split("|"))

INDIA_LOCATIONS = {
    "Andhra Pradesh": ["Amaravati", "Anantapur", "Bhimavaram", "Guntur", "Kakinada", "Kurnool", "Nellore", "Rajahmundry", "Tirupati", "Vijayawada", "Visakhapatnam"],
    "Arunachal Pradesh": ["Aalo", "Bomdila", "Itanagar", "Namsai", "Naharlagun", "Pasighat", "Tawang", "Ziro"],
    "Assam": ["Dibrugarh", "Guwahati", "Jorhat", "Nagaon", "Silchar", "Tezpur", "Tinsukia"],
    "Bihar": ["Arrah", "Bhagalpur", "Bihar Sharif", "Darbhanga", "Gaya", "Muzaffarpur", "Patna", "Purnia"],
    "Chhattisgarh": ["Bhilai", "Bilaspur", "Durg", "Jagdalpur", "Korba", "Raigarh", "Raipur"],
    "Goa": ["Mapusa", "Margao", "Panaji", "Ponda", "Vasco da Gama"],
    "Gujarat": ["Ahmedabad", "Anand", "Bhavnagar", "Gandhinagar", "Jamnagar", "Junagadh", "Rajkot", "Surat", "Vadodara", "Vallabh Vidyanagar"],
    "Haryana": ["Ambala", "Faridabad", "Gurugram", "Hisar", "Karnal", "Kurukshetra", "Panipat", "Rohtak", "Sonipat"],
    "Himachal Pradesh": ["Dharamshala", "Hamirpur", "Kangra", "Mandi", "Palampur", "Shimla", "Solan"],
    "Jharkhand": ["Bokaro", "Deoghar", "Dhanbad", "Hazaribagh", "Jamshedpur", "Ranchi"],
    "Karnataka": ["Belagavi", "Ballari", "Bengaluru", "Bidar", "Davanagere", "Dharwad", "Hubballi", "Kalaburagi", "Mangaluru", "Manipal", "Mysuru", "Shivamogga", "Tumakuru", "Udupi"],
    "Kerala": ["Alappuzha", "Ernakulam", "Kannur", "Kochi", "Kollam", "Kottayam", "Kozhikode", "Palakkad", "Thiruvananthapuram", "Thrissur"],
    "Madhya Pradesh": ["Bhopal", "Gwalior", "Indore", "Jabalpur", "Rewa", "Sagar", "Ujjain"],
    "Maharashtra": ["Amravati", "Aurangabad", "Jalgaon", "Kolhapur", "Mumbai", "Nagpur", "Nanded", "Nashik", "Navi Mumbai", "Pune", "Sangli", "Solapur", "Thane"],
    "Manipur": ["Churachandpur", "Imphal", "Senapati", "Thoubal", "Ukhrul"],
    "Meghalaya": ["Jowai", "Nongpoh", "Shillong", "Tura"],
    "Mizoram": ["Aizawl", "Champhai", "Kolasib", "Lunglei", "Serchhip"],
    "Nagaland": ["Dimapur", "Kohima", "Mokokchung", "Tuensang", "Wokha"],
    "Odisha": ["Balasore", "Berhampur", "Bhubaneswar", "Cuttack", "Puri", "Rourkela", "Sambalpur"],
    "Punjab": ["Amritsar", "Bathinda", "Jalandhar", "Ludhiana", "Mohali", "Patiala", "Phagwara"],
    "Rajasthan": ["Ajmer", "Alwar", "Bikaner", "Jaipur", "Jodhpur", "Kota", "Pilani", "Udaipur"],
    "Sikkim": ["Gangtok", "Gyalshing", "Namchi", "Rangpo"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Erode", "Kanchipuram", "Madurai", "Salem", "Thanjavur", "Tiruchirappalli", "Tirunelveli", "Vellore"],
    "Telangana": ["Hyderabad", "Karimnagar", "Khammam", "Mahbubnagar", "Nalgonda", "Nizamabad", "Warangal"],
    "Tripura": ["Agartala", "Dharmanagar", "Kailasahar", "Udaipur"],
    "Uttar Pradesh": ["Agra", "Aligarh", "Allahabad", "Bareilly", "Ghaziabad", "Gorakhpur", "Greater Noida", "Kanpur", "Lucknow", "Meerut", "Noida", "Prayagraj", "Varanasi"],
    "Uttarakhand": ["Dehradun", "Haldwani", "Haridwar", "Nainital", "Pantnagar", "Roorkee", "Srinagar"],
    "West Bengal": ["Asansol", "Durgapur", "Howrah", "Kharagpur", "Kolkata", "Siliguri"],
    "Andaman and Nicobar Islands": ["Diglipur", "Port Blair"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa"],
    "Delhi": ["Delhi", "New Delhi"],
    "Jammu and Kashmir": ["Anantnag", "Jammu", "Srinagar"],
    "Ladakh": ["Kargil", "Leh"],
    "Lakshadweep": ["Agatti", "Andrott", "Kavaratti"],
    "Puducherry": ["Karaikal", "Mahe", "Puducherry", "Yanam"],
}

WORLD_LOCATIONS = {
    "United States": {
        "California": ["Berkeley", "Davis", "Irvine", "Los Angeles", "Pasadena", "San Diego", "Stanford"],
        "Massachusetts": ["Amherst", "Boston", "Cambridge", "Worcester"],
        "New York": ["Buffalo", "Ithaca", "New York", "Rochester", "Stony Brook"],
        "Illinois": ["Chicago", "Evanston", "Urbana-Champaign"],
        "Pennsylvania": ["Philadelphia", "Pittsburgh", "State College"],
        "Texas": ["Austin", "College Station", "Dallas", "Houston", "Richardson"],
        "Georgia": ["Atlanta"], "Michigan": ["Ann Arbor", "East Lansing"], "Washington": ["Pullman", "Seattle"],
    },
    "Canada": {"Ontario": ["Hamilton", "Kingston", "Ottawa", "Toronto", "Waterloo"], "British Columbia": ["Burnaby", "Kelowna", "Vancouver", "Victoria"], "Quebec": ["Montreal", "Quebec City", "Sherbrooke"], "Alberta": ["Calgary", "Edmonton"], "Nova Scotia": ["Halifax"]},
    "United Kingdom": {"England": ["Birmingham", "Bristol", "Cambridge", "Coventry", "Leeds", "London", "Manchester", "Nottingham", "Oxford", "Sheffield", "Southampton"], "Scotland": ["Edinburgh", "Glasgow", "St Andrews"], "Wales": ["Cardiff", "Swansea"], "Northern Ireland": ["Belfast"]},
    "Australia": {"Victoria": ["Geelong", "Melbourne"], "New South Wales": ["Newcastle", "Sydney", "Wollongong"], "Queensland": ["Brisbane", "Gold Coast"], "Western Australia": ["Perth"], "South Australia": ["Adelaide"], "Australian Capital Territory": ["Canberra"], "Tasmania": ["Hobart"]},
    "Germany": {"Bavaria": ["Erlangen", "Munich", "Nuremberg"], "Baden-Wurttemberg": ["Freiburg", "Heidelberg", "Karlsruhe", "Stuttgart", "Tubingen"], "North Rhine-Westphalia": ["Aachen", "Bonn", "Cologne", "Dortmund"], "Berlin": ["Berlin"], "Hesse": ["Darmstadt", "Frankfurt"], "Saxony": ["Dresden", "Leipzig"], "Lower Saxony": ["Gottingen", "Hanover"]},
    "France": {"Ile-de-France": ["Cergy", "Paris", "Saclay"], "Auvergne-Rhone-Alpes": ["Grenoble", "Lyon"], "Occitanie": ["Montpellier", "Toulouse"], "Provence-Alpes-Cote d'Azur": ["Marseille", "Nice"], "Grand Est": ["Strasbourg"]},
    "Ireland": {"Leinster": ["Dublin", "Maynooth"], "Munster": ["Cork", "Limerick"], "Connacht": ["Galway"]},
    "Netherlands": {"North Holland": ["Amsterdam"], "South Holland": ["Delft", "Leiden", "Rotterdam"], "Utrecht": ["Utrecht"], "North Brabant": ["Eindhoven", "Tilburg"], "Groningen": ["Groningen"], "Gelderland": ["Nijmegen", "Wageningen"], "Overijssel": ["Enschede"]},
    "Switzerland": {"Zurich": ["Zurich"], "Vaud": ["Lausanne"], "Geneva": ["Geneva"], "Basel-Stadt": ["Basel"], "Bern": ["Bern"]},
    "Singapore": {"Singapore": ["Singapore"]},
    "Japan": {"Tokyo": ["Tokyo"], "Kyoto": ["Kyoto"], "Osaka": ["Osaka", "Suita"], "Aichi": ["Nagoya"], "Miyagi": ["Sendai"], "Fukuoka": ["Fukuoka"], "Hokkaido": ["Sapporo"]},
    "South Korea": {"Seoul": ["Seoul"], "Daejeon": ["Daejeon"], "Busan": ["Busan"], "Pohang": ["Pohang"], "Suwon": ["Suwon"]},
    "United Arab Emirates": {"Abu Dhabi": ["Abu Dhabi", "Al Ain"], "Dubai": ["Dubai"], "Sharjah": ["Sharjah"]},
    "New Zealand": {"Auckland": ["Auckland"], "Wellington": ["Wellington"], "Canterbury": ["Christchurch"], "Otago": ["Dunedin"], "Waikato": ["Hamilton"]},
    "Malaysia": {"Kuala Lumpur": ["Kuala Lumpur"], "Selangor": ["Bandar Sunway", "Petaling Jaya", "Serdang"], "Johor": ["Johor Bahru"], "Penang": ["George Town"], "Perak": ["Kampar"]},
}

CITY_ALIASES = {"bangalore": "bengaluru", "bombay": "mumbai", "calcutta": "kolkata", "madras": "chennai", "poona": "pune", "trivandrum": "thiruvananthapuram", "cochin": "kochi", "allahabad": "prayagraj"}


def subdivisions_for(country):
    if country == "India":
        return list(INDIA_LOCATIONS)
    return list(WORLD_LOCATIONS.get(country, {}))


def cities_for(country, subdivision):
    if country == "India":
        return INDIA_LOCATIONS.get(subdivision, [])
    return WORLD_LOCATIONS.get(country, {}).get(subdivision, [])


def normalise_city(value):
    value = (value or "").strip().lower()
    return CITY_ALIASES.get(value, value)
