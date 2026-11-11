# CareerCompass

> A full-stack career-guidance platform that helps students discover suitable career directions, compare courses, and build strict college shortlists across India and major international study destinations.

[![Flask](https://img.shields.io/badge/Flask-3.1-111827?logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-15%20passing-16a34a)](#testing)

## Live application

**Vercel:** [careercompass-mmjagannath.vercel.app](https://careercompass-mmjagannath.vercel.app)

## What CareerCompass does

CareerCompass combines a transparent 12-question aptitude and interest quiz with detailed course, career and college information. Students can search by programme, country, state or province, city, institution type and annual tuition budget without the system silently relaxing their selections.

### Main features

- Six interactive career categories with Bootstrap information popups.
- Aptitude and interest quiz with saved result history.
- **235** searchable undergraduate, postgraduate and diploma programmes.
- **296** institution records: **207 Indian** and **89 international**.
- All 28 Indian states and 8 Union Territories in the location selector.
- Dynamic country → subdivision → city selection with manual city fallback.
- Strict course, country, state, city, ownership and budget filtering.
- Broader location alternatives only after explicit student consent.
- Detailed course, career and institution pages.
- Rule-based, database-backed chatbot with conversation history.
- Local college shortlist and comparison drawer using browser storage.
- Responsive Bootstrap interface with light and dark themes.
- Deployment health and catalogue statistics APIs.

## Recommendation rules

CareerCompass ranks only after mandatory filtering:

1. The institution must contain the selected programme or a narrow defined equivalent.
2. Country, state/province and city are enforced whenever selected.
3. Government/private ownership is enforced.
4. Strict-budget mode accepts only verified same-currency annual tuition at or below the limit.
5. Unknown tuition is never presented as confirmed affordable.
6. Ranking and accreditation evidence influence ordering only after all filters pass.

If nothing satisfies every condition, the application returns zero exact matches and explains which filters were applied. Broader alternatives are a separate user-controlled action.

## Technology stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons |
| Backend | Python, Flask |
| Database | SQLite |
| Hosting | Vercel Python Functions |
| Tests | Python `unittest`, Flask test client |

## Project structure

```text
career-guidance-website/
├── app.py                    Flask routes, APIs, migrations, quiz and chatbot
├── recommendation.py         Shared strict recommendation engine
├── course_catalog.py         Independent 235-programme catalogue
├── college_data.py           Indian and international institution records
├── geo_data.py               Countries, subdivisions, cities and aliases
├── catalog.py                Career, course, skill and technology details
├── templates/                Responsive Jinja templates
├── static/
│   ├── css/style.css         Design system, themes and responsive styles
│   └── js/
│       ├── main.js           UI, locations, shortlist and load-more logic
│       └── chatbot.js        Chat interface and history
├── tests/test_app.py         Regression and migration tests
├── vercel.json               Vercel Python deployment configuration
├── CATALOGUE_REPORT.md       Coverage, tests, evidence and limitations
└── requirements.txt
```

## Run locally on Windows

### 1. Extract or clone

Open the project folder in File Explorer, click the address bar, type `cmd`, and press Enter.

### 2. Create the virtual environment

```bat
py -m venv venv
venv\Scripts\activate
```

### 3. Install and start

```bat
py -m pip install -r requirements.txt
py app.py
```

Open **http://127.0.0.1:5002**. Keep Command Prompt open while using the site.

To reopen later:

```bat
venv\Scripts\activate
py app.py
```

## Preserve an existing database

1. Stop the old server with `Ctrl+C`.
2. Copy the old `career_guide.db` into this project folder.
3. Start `py app.py`.

Migrations are additive and preserve quiz results, preferences and conversations. Before migrating an existing local database, the application creates `career_guide.db.pre_strict_upgrade_backup` once.

## Testing

```bat
py -m unittest discover -s tests -v
```

Current result: **15 tests passing**. The suite covers:

- strict Vijayawada/private/CSE matching;
- wrong-state leakage regression;
- explicit alternative opt-in;
- all 36 Indian state and UT selector values;
- course catalogue uniqueness and category filtering;
- strict institution type and budget behaviour;
- required India and international searches;
- quiz and chatbot regressions;
- preservation of legacy SQLite records.

## Useful API endpoints

| Endpoint | Purpose |
|---|---|
| `/health` | Deployment and database health |
| `/api/stats` | Catalogue summary |
| `/api/courses` | Search/filter course catalogue |
| `/api/locations/countries` | Country selector data |
| `/api/locations/subdivisions` | State/province/region data |
| `/api/locations/cities` | City selector data |
| `/api/colleges/search` | Strict recommendation results |

## Deployment note

Vercel functions use a writable temporary SQLite database generated from the bundled catalogue. The complete application works online, but user-created quiz results, preferences and chat history are not guaranteed to persist across serverless cold starts. Local execution retains the original persistent SQLite behaviour. A hosted production database can be added later without changing the recommendation engine.

## Data responsibility

CareerCompass does not invent missing tuition figures or admissions information. Unknown values remain labelled as unverified, and students are directed to official institution and admission links before applying. See [CATALOGUE_REPORT.md](CATALOGUE_REPORT.md) for exact coverage and remaining limitations.

## Author

Developed as a B.Tech CSE–AIML college project by **MM Jagannath and team**.

