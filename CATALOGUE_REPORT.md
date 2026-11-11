# CareerCompass strict recommendation upgrade report

Generated 5 November 2026 from the bundled source catalogue and automated tests.

## Delivered data

- Academic course catalogue: **235** unique programmes (40 Technology, 38 Analytical/Research, 39 Creative/Design, 40 People/Service, 38 Business/Leadership, 40 Health/Life Sciences).
- Programme levels: undergraduate, postgraduate and diploma.
- Institutions: **296** total — **207 India** and **89 international**.
- Indian location selector: all **28 states + 8 Union Territories**.
- Global selector: **249 countries/territories**, offline subdivision/city lists for supported study destinations, and manual-city fallback.
- Institution records with a stored numeric annual tuition: **2**. All other fees remain explicitly unverified; the application does not infer affordability.

The course catalogue is independent of institution offerings. Adding a course to the selector cannot make an institution eligible. The recommendation gate compares it only with that institution's stored programme list or a narrow, explicit equivalence.

## Indian institution coverage

| State / UT | Records | State / UT | Records |
|---|---:|---|---:|
| Andhra Pradesh | 8 | Arunachal Pradesh | 2 |
| Assam | 8 | Bihar | 4 |
| Chandigarh | 3 | Chhattisgarh | 4 |
| Delhi | 11 | Goa | 3 |
| Gujarat | 9 | Haryana | 6 |
| Himachal Pradesh | 4 | Jammu and Kashmir | 5 |
| Jharkhand | 3 | Karnataka | 15 |
| Kerala | 10 | Madhya Pradesh | 7 |
| Maharashtra | 17 | Manipur | 3 |
| Meghalaya | 3 | Mizoram | 2 |
| Nagaland | 2 | Odisha | 10 |
| Puducherry | 3 | Punjab | 7 |
| Rajasthan | 7 | Sikkim | 2 |
| Tamil Nadu | 14 | Telangana | 7 |
| Tripura | 2 | Uttar Pradesh | 11 |
| Uttarakhand | 4 | West Bengal | 11 |

The selector includes all 36 states/UTs, but four Union Territories currently have no bundled institution row. The UI correctly returns zero exact matches for unsupported combinations.

### Vijayawada improvement

The database now includes three private Vijayawada engineering institutions whose CSE offerings were checked on official pages:

- Siddhartha Academy of Higher Education
- Prasad V. Potluri Siddhartha Institute of Technology
- Andhra Loyola Institute of Engineering and Technology

No annual tuition number was stored because a comparable current official figure was not confirmed. Therefore, strict ₹4 lakh filtering intentionally returns zero rather than calling unknown fees affordable.

## International coverage

| Country | Records | Country | Records |
|---|---:|---|---:|
| Australia | 8 | Canada | 10 |
| France | 4 | Germany | 8 |
| Ireland | 3 | Japan | 6 |
| Malaysia | 4 | Netherlands | 4 |
| New Zealand | 3 | Singapore | 4 |
| South Korea | 4 | Switzerland | 3 |
| United Arab Emirates | 3 | United Kingdom | 10 |
| United States | 15 |  |  |

Other countries remain selectable for geographical completeness, but a selector entry is not a claim that the catalogue contains a university there.

## Strict filtering behaviour

Default results enforce country, subdivision, city, programme, institution type, career field (when supplied), study scope and strict same-currency budget. Ranking occurs afterward. Unknown tuition is excluded in strict-budget mode.

If there are no exact matches, the page displays: **“No colleges found matching all your selected preferences.”** It does not silently relax a filter. The separate **Explore colleges outside my selected location** control performs a second query and labels every broader result as an alternative.

The Preferences page, College Explorer, `/api/colleges/search`, and chatbot all call the same `recommend()` implementation. Its default is `include_alternatives=False`.

## Demonstrated searches

| Search | Exact matches observed | Example result(s) |
|---|---:|---|
| Private B.Tech CSE — Vijayawada, Andhra Pradesh | 3 | ALIET, PVPSIT, Siddhartha Academy |
| B.Tech CSE — Bengaluru, Karnataka | 8 | IISc, BMSCE, Christ, IIIT Bangalore |
| BBA — Pune, Maharashtra | 1 | Symbiosis International University |
| MBBS — Kerala | 1 | Government Medical College Thiruvananthapuram |
| B.Des — Ahmedabad, Gujarat | 3 | NID Ahmedabad, CEPT, Anant National University |
| Mechanical Engineering — Chennai, Tamil Nadu | 4 | IIT Madras, Anna University, SRMIST, IIITDM Kancheepuram |
| Computer Science — California, United States | 6 | Stanford, UC Berkeley, UCLA, Caltech |
| Business Administration — Toronto, Ontario | 1 | York University (Schulich BBA) |
| Engineering — Bavaria, Germany | 2 | TUM, University of Erlangen–Nuremberg |

## Automated verification

Command: `py -m unittest discover -s tests -v`

Result: **15 tests passed**. Coverage includes:

- all 36 Indian state/UT selector values;
- course count, uniqueness and all six categories;
- mandatory India/international searches;
- exact Vijayawada/private/CSE boundary;
- no wrong-state leakage without explicit opt-in;
- alternatives only after `show_alternatives=1`;
- strict institution type and unknown-fee exclusion;
- course-category API;
- pagination without duplicates;
- AIIMS exclusion for B.Tech CSE;
- quiz regression;
- database-backed chatbot and history;
- survival of a pre-existing quiz row through migration.

The Flask development server and rendered Preferences page were also checked at `http://127.0.0.1:5002`; both JavaScript files passed `node --check`.

## Sources and limitations

Institution names and domains are drawn from official institution sites. Ranking labels already present in the starting project identify NIRF or QS where available. New Vijayawada programme links point to official institution pages, and York University's BBA points to the official Schulich page.

Remaining limitations are intentionally visible:

- Most annual tuition is unknown, so strict-budget searches may return zero.
- The 235-course discovery catalogue is broader than the verified institution-offering catalogue.
- Many existing records retain conservative programme-family data from the supplied 293-record project; specialised branches are not inferred.
- Offline international city/subdivision coverage is not exhaustive; manual city entry remains available.
- Admissions, programme availability, fees and rankings change. Students must verify the linked official page before applying.

