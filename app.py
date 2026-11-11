import json
import os
import re
import secrets
import shutil
import sqlite3
from datetime import datetime, timezone

from flask import Flask, abort, flash, g, jsonify, redirect, render_template, request, session, url_for

from catalog import (
    CAREER_DETAILS,
    CATALOGS,
    COURSE_DETAILS,
    SKILL_DETAILS,
    TECHNOLOGY_DETAILS,
    TECHNOLOGY_NAMES,
    find_catalog_item,
    slugify,
)
from college_data import COLLEGES
from course_catalog import COURSE_CATALOG, catalogue_payload
from geo_data import COUNTRIES, INDIA_LOCATIONS, cities_for, subdivisions_for
from recommendation import CAREER_FIELDS, COURSE_OPTIONS, recommend, sort_results


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IS_VERCEL = bool(os.environ.get("VERCEL"))
# Vercel functions have a read-only project filesystem and a writable /tmp.
# Local runs keep the original persistent SQLite file beside app.py.
DATABASE = os.environ.get(
    "CAREERCOMPASS_DATABASE",
    "/tmp/career_guide.db" if IS_VERCEL else os.path.join(BASE_DIR, "career_guide.db"),
)

app = Flask(__name__)


def load_secret_key():
    """Keep anonymous browser sessions private and stable across local restarts."""
    configured = os.environ.get("SECRET_KEY")
    if configured:
        return configured
    if IS_VERCEL:
        # Configure SECRET_KEY in Vercel for stable anonymous sessions. This
        # fallback keeps first deployment usable without writing to source.
        return secrets.token_hex(32)
    secret_path = os.path.join(BASE_DIR, ".careercompass_secret")
    if os.path.exists(secret_path):
        with open(secret_path, "r", encoding="utf-8") as secret_file:
            return secret_file.read().strip()
    generated = secrets.token_hex(32)
    with open(secret_path, "w", encoding="utf-8") as secret_file:
        secret_file.write(generated)
    return generated


app.config.update(
    SECRET_KEY=load_secret_key(),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


CATEGORIES = {
    "technology": {
        "label": "Technology",
        "icon": "bi-cpu",
        "description": "You enjoy building, coding and understanding how technology works.",
        "courses": ["B.Tech CSE / AI & ML", "BCA", "B.Sc Computer Science"],
        "careers": ["Software Developer", "AI/ML Engineer", "Cybersecurity Analyst"],
        "skills": ["Programming", "Logical thinking", "Problem solving"],
        "salary": "₹4–18 LPA (varies by skill and experience)",
    },
    "analytical": {
        "label": "Analytical & Research",
        "icon": "bi-graph-up-arrow",
        "description": "You like patterns, numbers, investigation and evidence-based decisions.",
        "courses": ["B.Sc Data Science", "B.Sc Mathematics", "B.Stat / Economics"],
        "careers": ["Data Analyst", "Research Analyst", "Statistician"],
        "skills": ["Mathematics", "Data interpretation", "Critical thinking"],
        "salary": "₹4–16 LPA (varies by role and experience)",
    },
    "creative": {
        "label": "Creative & Design",
        "icon": "bi-palette",
        "description": "You are drawn to visual ideas, storytelling and original expression.",
        "courses": ["B.Des", "BA Media & Communication", "BFA / Animation"],
        "careers": ["UI/UX Designer", "Content Strategist", "Animator"],
        "skills": ["Visual communication", "Storytelling", "Design tools"],
        "salary": "₹3–14 LPA (portfolio and experience matter)",
    },
    "people": {
        "label": "People & Service",
        "icon": "bi-people",
        "description": "You enjoy guiding, teaching and improving other people's lives.",
        "courses": ["BA Psychology", "B.Ed", "BSW / Sociology"],
        "careers": ["Counsellor", "Teacher", "Human Resources Specialist"],
        "skills": ["Communication", "Empathy", "Listening"],
        "salary": "₹3–12 LPA (depends on specialization)",
    },
    "business": {
        "label": "Business & Leadership",
        "icon": "bi-briefcase",
        "description": "You enjoy organizing resources, influencing decisions and leading teams.",
        "courses": ["BBA", "B.Com", "Economics / Entrepreneurship"],
        "careers": ["Business Analyst", "Marketing Manager", "Entrepreneur"],
        "skills": ["Leadership", "Financial awareness", "Negotiation"],
        "salary": "₹4–20+ LPA (wide range by role and business)",
    },
    "health": {
        "label": "Health & Life Science",
        "icon": "bi-heart-pulse",
        "description": "You are interested in living systems, health and careful practical work.",
        "courses": ["MBBS / Allied Health", "B.Pharm", "B.Sc Biotechnology"],
        "careers": ["Doctor / Allied Health Professional", "Pharmacist", "Biotechnologist"],
        "skills": ["Biology", "Observation", "Precision"],
        "salary": "₹3–20+ LPA (strongly depends on qualification)",
    },
}

for category in CATEGORIES.values():
    category["technologies"] = TECHNOLOGY_NAMES.get(category["label"], [])


QUESTIONS = [
    {
        "text": "Which activity sounds most enjoyable to you?",
        "options": [
            ("Building an app or automating a task", "technology"),
            ("Finding patterns in a large set of data", "analytical"),
            ("Designing a poster, video or story", "creative"),
            ("Helping someone solve a personal problem", "people"),
            ("Planning how to sell a new product", "business"),
            ("Learning how the human body works", "health"),
        ],
    },
    {
        "text": "In a group project, which role do you naturally choose?",
        "options": [
            ("Developing the technical solution", "technology"),
            ("Checking facts, calculations and evidence", "analytical"),
            ("Creating the design and presentation", "creative"),
            ("Making sure everyone is heard", "people"),
            ("Coordinating the team and deadline", "business"),
            ("Checking safety and human impact", "health"),
        ],
    },
    {
        "text": "Which subject area interests you most?",
        "options": [
            ("Computer Science", "technology"),
            ("Mathematics or Statistics", "analytical"),
            ("Art, Languages or Media", "creative"),
            ("Psychology or Social Science", "people"),
            ("Commerce or Economics", "business"),
            ("Biology or Chemistry", "health"),
        ],
    },
    {
        "text": "What type of problem would you most like to solve?",
        "options": [
            ("A slow or insecure computer system", "technology"),
            ("A decision with confusing numbers", "analytical"),
            ("A message that fails to attract attention", "creative"),
            ("A student struggling to learn", "people"),
            ("A company losing customers", "business"),
            ("A community health challenge", "health"),
        ],
    },
    {
        "text": "Which achievement would make you proudest?",
        "options": [
            ("Launching useful software", "technology"),
            ("Discovering an important insight", "analytical"),
            ("Creating work that inspires people", "creative"),
            ("Helping someone grow or recover", "people"),
            ("Building a successful organization", "business"),
            ("Improving a treatment or health process", "health"),
        ],
    },
    {
        "text": "Which work environment appeals to you?",
        "options": [
            ("A product or engineering team", "technology"),
            ("A research or analytics lab", "analytical"),
            ("A design studio or media team", "creative"),
            ("A school, community or counselling centre", "people"),
            ("A company, startup or consulting team", "business"),
            ("A hospital, pharmacy or biotech lab", "health"),
        ],
    },
    {
        "text": "When learning something new, what do you prefer?",
        "options": [
            ("Experimenting with tools and code", "technology"),
            ("Understanding the theory and testing it", "analytical"),
            ("Using pictures, examples and imagination", "creative"),
            ("Discussing it with other people", "people"),
            ("Connecting it to real-world value", "business"),
            ("Practising carefully with clear procedures", "health"),
        ],
    },
    {
        "text": "Which skill would you most like to master?",
        "options": [
            ("Programming and system design", "technology"),
            ("Research and data interpretation", "analytical"),
            ("Visual design and storytelling", "creative"),
            ("Communication and counselling", "people"),
            ("Leadership and negotiation", "business"),
            ("Clinical or laboratory techniques", "health"),
        ],
    },
    {
        "text": "What do friends most often ask your help with?",
        "options": [
            ("Devices, software or technical issues", "technology"),
            ("Calculations and logical decisions", "analytical"),
            ("Ideas, writing or presentation design", "creative"),
            ("Advice and emotional support", "people"),
            ("Planning, money or organizing work", "business"),
            ("Health, science or careful practical tasks", "health"),
        ],
    },
    {
        "text": "Which result matters most in your future work?",
        "options": [
            ("Making systems faster and smarter", "technology"),
            ("Producing accurate knowledge", "analytical"),
            ("Making ideas memorable", "creative"),
            ("Creating positive human impact", "people"),
            ("Achieving growth and measurable results", "business"),
            ("Protecting life and well-being", "health"),
        ],
    },
    {
        "text": "A difficult task appears. What is your first move?",
        "options": [
            ("Try tools and build a small prototype", "technology"),
            ("Break it into facts and variables", "analytical"),
            ("Look for a fresh and unusual approach", "creative"),
            ("Ask who is affected and what they need", "people"),
            ("Set priorities, resources and a plan", "business"),
            ("Follow a safe, tested process", "health"),
        ],
    },
    {
        "text": "Which college event would you join first?",
        "options": [
            ("Hackathon or robotics contest", "technology"),
            ("Quiz, research poster or data challenge", "analytical"),
            ("Film, design or cultural festival", "creative"),
            ("Teaching, volunteering or wellness club", "people"),
            ("Business plan or entrepreneurship event", "business"),
            ("Health camp or science exhibition", "health"),
        ],
    },
]


COURSE_COMPARISON = [
    {"course": "B.Tech CSE / AI & ML", "duration": "4 years", "best_for": "Technology + logic", "entrance": "JEE / CET / university exam", "paths": "Software, AI, cloud, cybersecurity"},
    {"course": "BCA", "duration": "3 years", "best_for": "Practical computing", "entrance": "Merit / university exam", "paths": "Development, IT support, MCA"},
    {"course": "BBA", "duration": "3 years", "best_for": "Business + leadership", "entrance": "Merit / university exam", "paths": "Marketing, HR, operations, MBA"},
    {"course": "B.Com", "duration": "3 years", "best_for": "Commerce + finance", "entrance": "Merit / CUET", "paths": "Accounting, banking, CA, finance"},
    {"course": "B.Des", "duration": "4 years", "best_for": "Creative problem-solving", "entrance": "UCEED / NID DAT / portfolio", "paths": "UX, product, graphic design"},
    {"course": "B.Sc Biotechnology", "duration": "3–4 years", "best_for": "Biology + research", "entrance": "Merit / CUET", "paths": "Biotech, labs, higher studies"},
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def ensure_column(db, table, column, definition):
    """Add a column without rebuilding a user's existing SQLite table."""
    existing = {row[1] for row in db.execute(f"PRAGMA table_info({table})")}
    if column not in existing:
        db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def init_db():
    # One recoverable snapshot is created before the first upgrade of an
    # existing database.  It is never overwritten on later starts.
    backup_path = DATABASE + ".pre_strict_upgrade_backup"
    if os.path.exists(DATABASE) and not os.path.exists(backup_path):
        shutil.copy2(DATABASE, backup_path)
    db = sqlite3.connect(DATABASE)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            email TEXT,
            scores_json TEXT NOT NULL,
            top_category TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS knowledge_items (
            kind TEXT NOT NULL,
            slug TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            summary TEXT NOT NULL,
            keywords TEXT NOT NULL,
            details_json TEXT NOT NULL,
            detail_url TEXT NOT NULL,
            PRIMARY KEY (kind, slug)
        );

        CREATE TABLE IF NOT EXISTS colleges (
            slug TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            country TEXT NOT NULL,
            region TEXT NOT NULL,
            ownership TEXT NOT NULL,
            courses_json TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            admission TEXT NOT NULL,
            fees TEXT NOT NULL,
            fee_currency TEXT,
            annual_fee_amount REAL,
            official_url TEXT NOT NULL,
            admission_url TEXT NOT NULL,
            fee_url TEXT NOT NULL,
            source_note TEXT NOT NULL,
            career_fields_json TEXT NOT NULL DEFAULT '[]',
            entrance_exams_json TEXT NOT NULL DEFAULT '[]',
            ranking_info TEXT,
            rank_value INTEGER,
            last_verified TEXT
        );

        CREATE TABLE IF NOT EXISTS student_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_token TEXT NOT NULL,
            country TEXT,
            state TEXT,
            city TEXT,
            preferred_course TEXT,
            study_scope TEXT NOT NULL,
            institution_type TEXT NOT NULL,
            budget_amount REAL,
            budget_currency TEXT,
            preferred_location TEXT,
            accessibility TEXT,
            created_at TEXT NOT NULL,
            career_field TEXT,
            preferred_country TEXT,
            preferred_state TEXT,
            preferred_city TEXT,
            budget_mode TEXT DEFAULT 'prefer'
        );

        CREATE TABLE IF NOT EXISTS chat_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_token TEXT NOT NULL,
            title TEXT NOT NULL DEFAULT 'New conversation',
            current_topic TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            sender TEXT NOT NULL CHECK(sender IN ('user', 'bot')),
            content TEXT NOT NULL,
            link_text TEXT,
            link_url TEXT,
            links_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES chat_conversations(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_chat_owner ON chat_conversations(owner_token);
        CREATE INDEX IF NOT EXISTS idx_preferences_owner ON student_preferences(owner_token);
        """
    )

    # Additive migrations preserve quiz results, preferences and chat history from
    # earlier CareerCompass versions.
    for column, definition in [
        ("career_fields_json", "TEXT NOT NULL DEFAULT '[]'"),
        ("entrance_exams_json", "TEXT NOT NULL DEFAULT '[]'"),
        ("ranking_info", "TEXT"), ("rank_value", "INTEGER"),
        ("last_verified", "TEXT"),
    ]:
        ensure_column(db, "colleges", column, definition)
    for column, definition in [
        ("career_field", "TEXT"), ("preferred_country", "TEXT"),
        ("preferred_state", "TEXT"), ("preferred_city", "TEXT"),
        ("budget_mode", "TEXT DEFAULT 'prefer'"),
    ]:
        ensure_column(db, "student_preferences", column, definition)
    ensure_column(db, "chat_messages", "links_json", "TEXT NOT NULL DEFAULT '[]'")

    for kind, items in CATALOGS.items():
        for item in items.values():
            keywords = " ".join(
                [item["title"], item["category"]]
                + item.get("subjects", [])
                + item.get("skills", [])
                + item.get("opportunities", [])
            ).lower()
            db.execute(
                """
                INSERT INTO knowledge_items
                (kind, slug, title, category, summary, keywords, details_json, detail_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(kind, slug) DO UPDATE SET
                    title=excluded.title, category=excluded.category,
                    summary=excluded.summary, keywords=excluded.keywords,
                    details_json=excluded.details_json, detail_url=excluded.detail_url
                """,
                (
                    kind,
                    item["slug"],
                    item["title"],
                    item["category"],
                    item["overview"],
                    keywords,
                    json.dumps(item),
                    f"/explore/{kind}/{item['slug']}",
                ),
            )

    for college in COLLEGES:
        db.execute(
            """
            INSERT INTO colleges
            (slug, name, city, state, country, region, ownership, courses_json,
             eligibility, admission, fees, fee_currency, annual_fee_amount,
             official_url, admission_url, fee_url, source_note, career_fields_json,
             entrance_exams_json, ranking_info, rank_value, last_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                name=excluded.name, city=excluded.city, state=excluded.state,
                country=excluded.country, region=excluded.region,
                ownership=excluded.ownership, courses_json=excluded.courses_json,
                eligibility=excluded.eligibility, admission=excluded.admission,
                fees=excluded.fees, fee_currency=excluded.fee_currency,
                annual_fee_amount=excluded.annual_fee_amount,
                official_url=excluded.official_url, admission_url=excluded.admission_url,
                fee_url=excluded.fee_url, source_note=excluded.source_note
                ,career_fields_json=excluded.career_fields_json,
                entrance_exams_json=excluded.entrance_exams_json,
                ranking_info=excluded.ranking_info, rank_value=excluded.rank_value,
                last_verified=excluded.last_verified
            """,
            (
                college["slug"], college["name"], college["city"], college["state"],
                college["country"], college["region"], college["ownership"],
                json.dumps(college["courses"]), college["eligibility"], college["admission"],
                college["fees"], college["fee_currency"], college["annual_fee_amount"],
                college["official_url"], college["admission_url"], college["fee_url"],
                college["source_note"], json.dumps(college.get("career_fields", [])),
                json.dumps(college.get("entrance_exams", [])), college.get("ranking_info"),
                college.get("rank_value"), college.get("last_verified"),
            ),
        )
    db.commit()
    db.close()


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.context_processor
def inject_year():
    return {
        "current_year": datetime.now().year,
        "slugify": slugify,
        "all_categories": CATEGORIES,
        "course_details": COURSE_DETAILS,
    }


def get_owner_token():
    if "visitor_token" not in session:
        session["visitor_token"] = secrets.token_urlsafe(24)
    return session["visitor_token"]


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def college_from_row(row):
    college = dict(row)
    college["courses"] = json.loads(college.pop("courses_json"))
    college["career_fields"] = json.loads(college.pop("career_fields_json", "[]") or "[]")
    college["entrance_exams"] = json.loads(college.pop("entrance_exams_json", "[]") or "[]")
    return college


@app.route("/")
def home():
    return render_template("index.html", categories=CATEGORIES)


@app.get("/health")
def health():
    """Small deployment probe used by Vercel and project demos."""
    row = get_db().execute("SELECT COUNT(*) AS count FROM colleges").fetchone()
    return jsonify({"status": "ok", "service": "CareerCompass", "colleges": row["count"]})


@app.get("/api/stats")
def api_stats():
    db = get_db()
    total = db.execute("SELECT COUNT(*) AS count FROM colleges").fetchone()["count"]
    india = db.execute("SELECT COUNT(*) AS count FROM colleges WHERE country = 'India'").fetchone()["count"]
    return jsonify({"courses": len(COURSE_CATALOG), "institutions": total,
                    "indian_institutions": india, "international_institutions": total - india,
                    "indian_states_and_uts": len(INDIA_LOCATIONS)})


@app.route("/category/<category_key>")
def category_detail(category_key):
    category = CATEGORIES.get(category_key)
    if category is None:
        abort(404)
    return render_template(
        "category.html",
        category_key=category_key,
        category=category,
        courses=[item for item in COURSE_DETAILS.values() if item["category"] == category["label"]],
        careers=[item for item in CAREER_DETAILS.values() if item["category"] == category["label"]],
        skills=[item for item in SKILL_DETAILS.values() if item["category"] == category["label"]],
        technologies=[item for item in TECHNOLOGY_DETAILS.values() if item["category"] == category["label"]],
    )


@app.route("/explore/<kind>/<slug>")
def explore_detail(kind, slug):
    item = find_catalog_item(kind, slug)
    if item is None:
        abort(404)
    related = [
        candidate for candidate in CATALOGS.get(kind, {}).values()
        if candidate["category"] == item["category"] and candidate["slug"] != slug
    ][:3]
    return render_template("detail.html", item=item, kind=kind, related=related)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "GET":
        return render_template("quiz.html", questions=QUESTIONS)

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    if not name:
        flash("Please enter your name before submitting the quiz.", "danger")
        return redirect(url_for("quiz"))

    scores = {key: 0 for key in CATEGORIES}
    missing = []

    for index, question in enumerate(QUESTIONS):
        answer = request.form.get(f"q{index}")
        if answer is None:
            missing.append(index + 1)
            continue
        try:
            option_index = int(answer)
            category = question["options"][option_index][1]
            scores[category] += 1
        except (ValueError, IndexError):
            missing.append(index + 1)

    if missing:
        flash(f"Please answer every question. Missing: {', '.join(map(str, missing))}.", "warning")
        return render_template("quiz.html", questions=QUESTIONS, entered_name=name, entered_email=email)

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    top_key = ranked[0][0]

    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO quiz_results
        (student_name, email, scores_json, top_category, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, json.dumps(scores), top_key, datetime.now(timezone.utc).isoformat()),
    )
    db.commit()

    return redirect(url_for("result", result_id=cursor.lastrowid))


@app.route("/result/<int:result_id>")
def result(result_id):
    row = get_db().execute("SELECT * FROM quiz_results WHERE id = ?", (result_id,)).fetchone()
    if row is None:
        return render_template("404.html"), 404

    scores = json.loads(row["scores_json"])
    ranked_keys = sorted(scores, key=lambda key: (-scores[key], key))
    max_score = max(scores.values()) or 1
    score_rows = [
        {
            "key": key,
            "label": CATEGORIES[key]["label"],
            "score": scores[key],
            "percent": round(scores[key] / max_score * 100),
        }
        for key in ranked_keys
    ]
    primary = CATEGORIES[ranked_keys[0]]
    secondary = CATEGORIES[ranked_keys[1]]

    return render_template(
        "result.html",
        result=row,
        primary=primary,
        secondary=secondary,
        score_rows=score_rows,
        primary_key=ranked_keys[0],
        secondary_key=ranked_keys[1],
    )


@app.route("/courses")
def courses():
    return render_template(
        "courses.html",
        courses=COURSE_COMPARISON,
        categories=CATEGORIES,
        course_details=COURSE_DETAILS,
        career_details=CAREER_DETAILS,
        skill_details=SKILL_DETAILS,
        technology_details=TECHNOLOGY_DETAILS,
    )


def all_colleges():
    return [college_from_row(row) for row in get_db().execute("SELECT * FROM colleges").fetchall()]


def parse_preference(source):
    values = {key: (source.get(key, "") or "").strip() for key in [
        "country", "state", "city", "career_field", "preferred_course",
        "study_scope", "institution_type", "budget_currency", "budget_mode",
        "preferred_country", "preferred_state", "preferred_city", "accessibility",
        "sort",
    ]}
    values["study_scope"] = values["study_scope"] or "Both"
    values["institution_type"] = values["institution_type"] or "Either"
    values["budget_currency"] = values["budget_currency"] or "INR"
    values["budget_mode"] = values["budget_mode"] or "prefer"
    values["sort"] = values["sort"] or "relevance"
    if values["study_scope"] == "India":
        values["preferred_country"] = "India"
    try:
        values["budget_amount"] = float(source.get("budget_amount", "") or 0) or None
    except (TypeError, ValueError):
        values["budget_amount"] = None
    try:
        values["page"] = max(1, int(source.get("page", 1) or 1))
    except (TypeError, ValueError):
        values["page"] = 1
    values["show_alternatives"] = str(source.get("show_alternatives", "")).lower() in {"1", "true", "yes", "on"}
    return values


def recommendation_bundle(preference):
    colleges = all_colleges()
    exact = sort_results(recommend(colleges, preference), preference.get("sort", "relevance"))
    alternatives = []
    if preference.get("show_alternatives"):
        alternatives = sort_results(recommend(colleges, preference, include_alternatives=True), preference.get("sort", "relevance"))
    page_size = 12
    page = preference.get("page", 1)
    ordered = exact + alternatives
    start = (page - 1) * page_size
    return {
        "exact": exact, "alternatives": alternatives, "all": ordered,
        "page_items": ordered[start:start + page_size], "total": len(ordered),
        "exact_count": len(exact), "alternative_count": len(alternatives),
        "page": page, "page_size": page_size,
        "has_more": start + page_size < len(ordered),
    }


@app.route("/colleges")
def colleges():
    values = parse_preference(request.args)
    bundle = recommendation_bundle(values)
    query = (request.args.get("q") or "").strip().lower()
    if query:
        def contains(item):
            haystack = " ".join([item["name"], item["city"], item["state"], item["country"]] + item["courses"] + item["career_fields"]).lower()
            return query in haystack
        filtered = [item for item in bundle["all"] if contains(item)]
        bundle["all"] = filtered
        bundle["page_items"] = filtered[:bundle["page_size"]]
        bundle["total"] = len(filtered)
        bundle["has_more"] = len(filtered) > bundle["page_size"]
    return render_template(
        "colleges.html", bundle=bundle, values=values, query=query,
        countries=COUNTRIES, courses=COURSE_OPTIONS, course_catalog=catalogue_payload(), career_fields=CAREER_FIELDS,
        india_state_count=len(INDIA_LOCATIONS),
    )


@app.route("/colleges/<slug>")
def college_detail(slug):
    row = get_db().execute("SELECT * FROM colleges WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        abort(404)
    return render_template("college_detail.html", college=college_from_row(row))


@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    bundle = None
    values = parse_preference(request.form if request.method == "POST" else request.args)
    if request.method == "POST":
        db = get_db()
        db.execute(
            """
            INSERT INTO student_preferences
            (owner_token, country, state, city, preferred_course, study_scope,
             institution_type, budget_amount, budget_currency, preferred_location,
             accessibility, created_at, career_field, preferred_country,
             preferred_state, preferred_city, budget_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                get_owner_token(), values["country"], values["state"], values["city"],
                values["preferred_course"], values["study_scope"], values["institution_type"],
                values["budget_amount"], values["budget_currency"],
                " / ".join(filter(None, [values["preferred_country"], values["preferred_state"], values["preferred_city"]])),
                values["accessibility"], utc_now(), values["career_field"],
                values["preferred_country"], values["preferred_state"],
                values["preferred_city"], values["budget_mode"],
            ),
        )
        db.commit()
        bundle = recommendation_bundle(values)
    return render_template(
        "preferences.html", values=values, bundle=bundle, countries=COUNTRIES,
        courses=COURSE_OPTIONS, course_catalog=catalogue_payload(), career_fields=CAREER_FIELDS,
    )


@app.get("/api/locations/countries")
def api_countries():
    return jsonify({"countries": COUNTRIES})


@app.get("/api/courses")
def api_courses():
    category = (request.args.get("category") or "").strip()
    query = (request.args.get("q") or "").strip().lower()
    rows = [item for item in COURSE_CATALOG if not category or item["category"] == category]
    if query:
        rows = [item for item in rows if query in " ".join([item["name"], *item["aliases"]]).lower()]
    return jsonify({"count": len(rows), "courses": rows})


@app.get("/api/locations/subdivisions")
def api_subdivisions():
    country = (request.args.get("country") or "").strip()
    label = "State / Union Territory" if country == "India" else "State / province / region"
    return jsonify({"country": country, "label": label, "subdivisions": subdivisions_for(country)})


@app.get("/api/locations/cities")
def api_cities():
    country = (request.args.get("country") or "").strip()
    subdivision = (request.args.get("subdivision") or "").strip()
    return jsonify({"country": country, "subdivision": subdivision, "cities": cities_for(country, subdivision), "manual_entry_supported": True})


@app.get("/api/colleges/search")
def api_college_search():
    values = parse_preference(request.args)
    bundle = recommendation_bundle(values)
    fields = ["slug", "name", "city", "state", "country", "ownership", "courses",
              "career_fields", "matched_course", "location_label", "budget_status",
              "ranking_info", "fees", "official_url", "admission_url", "match_reasons"]
    return jsonify({
        "total": bundle["total"], "exact_count": bundle["exact_count"],
        "alternative_count": bundle["alternative_count"], "page": bundle["page"],
        "has_more": bundle["has_more"],
        "results": [{key: item.get(key) for key in fields} for item in bundle["page_items"]],
    })


def owned_conversation(conversation_id):
    row = get_db().execute(
        "SELECT * FROM chat_conversations WHERE id = ? AND owner_token = ?",
        (conversation_id, get_owner_token()),
    ).fetchone()
    if row is None:
        abort(404)
    return row


@app.get("/api/chat/conversations")
def list_conversations():
    rows = get_db().execute(
        "SELECT id, title, created_at, updated_at FROM chat_conversations WHERE owner_token = ? ORDER BY updated_at DESC",
        (get_owner_token(),),
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.post("/api/chat/conversations")
def create_conversation():
    now = utc_now()
    db = get_db()
    cursor = db.execute(
        "INSERT INTO chat_conversations (owner_token, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (get_owner_token(), "New conversation", now, now),
    )
    conversation_id = cursor.lastrowid
    db.execute(
        "INSERT INTO chat_messages (conversation_id, sender, content, created_at) VALUES (?, 'bot', ?, ?)",
        (conversation_id, "Hi! Ask me for colleges by course, country, state, city or budget—or ask why a recommendation appeared. I use CareerCompass's local SQLite database and no external AI service.", now),
    )
    db.commit()
    return jsonify({"id": conversation_id, "title": "New conversation"}), 201


@app.get("/api/chat/conversations/<int:conversation_id>")
def conversation_messages(conversation_id):
    conversation = owned_conversation(conversation_id)
    rows = get_db().execute(
        "SELECT id, sender, content, link_text, link_url, links_json, created_at FROM chat_messages WHERE conversation_id = ? ORDER BY id",
        (conversation_id,),
    ).fetchall()
    messages = []
    for row in rows:
        item = dict(row)
        item["links"] = json.loads(item.pop("links_json", "[]") or "[]")
        if not item["links"] and item.get("link_url"):
            item["links"] = [{"text": item.get("link_text") or "View details", "url": item["link_url"]}]
        messages.append(item)
    return jsonify({"conversation": dict(conversation), "messages": messages})


@app.delete("/api/chat/conversations/<int:conversation_id>")
def delete_conversation(conversation_id):
    owned_conversation(conversation_id)
    db = get_db()
    db.execute("DELETE FROM chat_conversations WHERE id = ? AND owner_token = ?", (conversation_id, get_owner_token()))
    db.commit()
    return jsonify({"deleted": True})


STOP_WORDS = {"what", "which", "where", "about", "tell", "please", "could", "would", "should", "with", "from", "that", "this", "have", "does", "career", "course", "show", "suggest", "best"}


def latest_preference():
    row = get_db().execute(
        "SELECT * FROM student_preferences WHERE owner_token = ? ORDER BY id DESC LIMIT 1",
        (get_owner_token(),),
    ).fetchone()
    if row is None:
        return parse_preference({})
    values = dict(row)
    values["budget_mode"] = values.get("budget_mode") or "prefer"
    values["preferred_country"] = values.get("preferred_country") or ("India" if values.get("study_scope") == "India" else "")
    values["preferred_state"] = values.get("preferred_state") or ""
    values["preferred_city"] = values.get("preferred_city") or ""
    values["career_field"] = values.get("career_field") or ""
    values["sort"] = "relevance"
    values["page"] = 1
    return values


def detect_course(query):
    # Prefer the longest catalogue name/alias so "artificial intelligence and
    # machine learning" is not reduced to the broader "artificial intelligence".
    catalogue_terms = []
    for item in COURSE_CATALOG:
        for term in [item["name"], *item["aliases"]]:
            catalogue_terms.append((term.lower(), item["name"]))
    for term, name in sorted(catalogue_terms, key=lambda pair: len(pair[0]), reverse=True):
        if term and term in query:
            return name
    aliases = {
        "btech cse": "B.Tech Computer Science Engineering", "b tech cse": "B.Tech Computer Science Engineering",
        "computer science": "Computer Science", "cse": "Computer Science", " cs ": "Computer Science",
        "artificial intelligence": "Artificial Intelligence", "ai and ml": "Artificial Intelligence",
        "ai ml": "Artificial Intelligence", "mechanical": "Mechanical Engineering",
        "engineering": "Engineering", "mbbs": "MBBS", "medical": "Medicine",
        "medicine": "Medicine", "b.des": "B.Des", "b des": "B.Des", "bdes": "B.Des", "design": "Design",
        "bba": "BBA", "business administration": "Business Administration", "business": "Business",
        "life science": "Life Sciences", "science": "Science", "psychology": "Psychology",
    }
    for alias in sorted(aliases, key=len, reverse=True):
        if alias in query:
            return aliases[alias]
    return ""


def detect_location(query, colleges):
    found = {"preferred_country": "", "preferred_state": "", "preferred_city": ""}
    country_names = sorted({college["country"] for college in colleges}, key=len, reverse=True)
    country_aliases = {"usa": "United States", "u.s.a": "United States", "uk": "United Kingdom", "u.k": "United Kingdom", "uae": "United Arab Emirates"}
    for alias, country in country_aliases.items():
        if re.search(rf"\b{re.escape(alias)}\b", query):
            found["preferred_country"] = country
            break
    if not found["preferred_country"]:
        for country in country_names:
            if country.lower() in query:
                found["preferred_country"] = country
                break
    subdivisions = sorted({college["state"] for college in colleges}, key=len, reverse=True)
    for subdivision in subdivisions:
        if subdivision.lower() in query:
            found["preferred_state"] = subdivision
            break
    cities = sorted({college["city"] for college in colleges}, key=len, reverse=True)
    city_aliases = {"bangalore": "Bengaluru", "bombay": "Mumbai", "calcutta": "Kolkata", "madras": "Chennai"}
    for alias, city in city_aliases.items():
        if alias in query:
            found["preferred_city"] = city
            break
    if not found["preferred_city"]:
        for city in cities:
            if city.lower() in query:
                found["preferred_city"] = city
                break
    if found["preferred_country"] == "India" or found["preferred_state"] in INDIA_LOCATIONS:
        found["preferred_country"] = "India"
    if found["preferred_city"]:
        city_rows = [college for college in colleges if college["city"].lower() == found["preferred_city"].lower()]
        states = {college["state"] for college in city_rows}
        countries = {college["country"] for college in city_rows}
        if len(states) == 1 and not found["preferred_state"]:
            found["preferred_state"] = states.pop()
        if len(countries) == 1 and not found["preferred_country"]:
            found["preferred_country"] = countries.pop()
    return found


def chat_college_search(query, conversation):
    colleges = all_colleges()
    preference = latest_preference()
    detected_course = detect_course(query)
    if detected_course:
        preference["preferred_course"] = detected_course
        preference["career_field"] = ""
    detected_location = detect_location(query, colleges)
    if detected_location["preferred_country"]:
        preference["preferred_country"] = detected_location["preferred_country"]
        if not detected_location["preferred_state"]:
            preference["preferred_state"] = ""
            preference["preferred_city"] = ""
    if detected_location["preferred_state"]:
        preference["preferred_state"] = detected_location["preferred_state"]
        if not detected_location["preferred_city"]:
            preference["preferred_city"] = ""
    if detected_location["preferred_city"]:
        preference["preferred_city"] = detected_location["preferred_city"]
    if "india" in query:
        preference["study_scope"] = "India"
        preference["preferred_country"] = "India"
    elif preference.get("preferred_country") and preference["preferred_country"] != "India":
        preference["study_scope"] = "Abroad"
    if "government" in query or "public" in query:
        preference["institution_type"] = "Government"
    elif "private" in query:
        preference["institution_type"] = "Private"
    lakh_match = re.search(r"(?:₹|inr\s*)?([0-9]+(?:\.[0-9]+)?)\s*(?:lakh|lac)", query)
    if lakh_match:
        preference["budget_amount"] = float(lakh_match.group(1)) * 100000
        preference["budget_currency"] = "INR"
        preference["budget_mode"] = "strict"
    preference["sort"] = "ranking" if "best" in query or "top" in query else "relevance"

    current_topic = conversation["current_topic"] or ""
    if ("why did" in query or "why this" in query or "why was" in query) and current_topic.startswith("college:"):
        slug = current_topic.split(":", 1)[1]
        college = next((item for item in colleges if item["slug"] == slug), None)
        if college:
            explanation = recommend([college], preference)
            if explanation:
                reasons = "; ".join(explanation[0]["match_reasons"])
                return f"{college['name']} appeared because it {reasons}. Course relevance is checked before location, budget and ranking order.", [{"text": "View college", "url": url_for("college_detail", slug=slug)}], current_topic
            return f"{college['name']} appeared in the preceding chat search because its stored programme and location matched that question. Your separately saved preference form currently has different filters, so it would not appear there now.", [{"text": "View college", "url": url_for("college_detail", slug=slug)}, {"text": "Review saved preferences", "url": url_for("preferences")}], current_topic

    if "why" in query and ("only four" in query or "4 college" in query):
        return f"The earlier version had only eight seeded institutions—four in India and four abroad. This version has {len(COLLEGES)} database records and filters them by actual programme family before location, budget and ranking evidence.", [{"text": "Open expanded explorer", "url": url_for("colleges")}], None

    wants_alternatives = any(phrase in query for phrase in ["outside", "alternative", "broader location", "other city", "other state"])
    results = sort_results(recommend(colleges, preference, include_alternatives=wants_alternatives), preference["sort"])
    if "no college" in query or "no match" in query or "not matching" in query:
        if results:
            return f"Your latest saved filters produce {len(results)} exact records. Country, state, city, course, institution type and strict budget were enforced before ranking. Unknown fees are not treated as affordable.", [{"text": "Review results", "url": url_for("preferences")}], None
        return "No institution passed all latest filters. The usual causes are an exact course with no catalogue coverage in that location, a restrictive institution type, or strict budget mode when fees are unverified. CareerCompass will not fill the gap with an unrelated college.", [{"text": "Broaden preferences", "url": url_for("preferences")}], None

    if not results:
        return "No colleges found matching all your selected preferences. I enforced the selected country, state, city, programme, institution type and strict budget. Ask ‘show alternatives outside my preferred city’ only if you want a separately labelled broader search.", [{"text": "Adjust preferences", "url": url_for("preferences")}], None
    top = results[:5]
    exact_count = sum(1 for item in results if item["location_tier"] == 0)
    alternative_count = len(results) - exact_count
    lines = [f"{index}. {college['name']} — {college['city']}, {college['state']} ({college['matched_course']}; {college['budget_status']})" for index, college in enumerate(top, 1)]
    context_bits = [preference.get("preferred_course"), preference.get("preferred_city"), preference.get("preferred_state"), preference.get("preferred_country")]
    context = ", ".join(bit for bit in context_bits if bit) or "your latest saved filters"
    if wants_alternatives:
        answer = f"You explicitly requested broader locations. I found {alternative_count} separately labelled alternatives for {context}; none is presented as an exact match. Top results:\n" + "\n".join(lines)
    else:
        answer = f"I found {exact_count} exact matches for {context}. All mandatory filters were applied before ranking. Top results:\n" + "\n".join(lines)
    links = [{"text": college["name"], "url": url_for("college_detail", slug=college["slug"])} for college in top]
    links.append({"text": "Open full filtered explorer", "url": url_for("colleges", preferred_course=preference.get("preferred_course", ""), preferred_country=preference.get("preferred_country", ""), preferred_state=preference.get("preferred_state", ""), preferred_city=preference.get("preferred_city", ""), study_scope=preference.get("study_scope", "Both"))})
    return answer, links, f"college:{top[0]['slug']}"


def build_chat_answer(message, conversation):
    query = message.lower().strip()
    if query in {"hi", "hello", "hey"} or any(greeting in query for greeting in ["good morning", "good evening"]):
        return "Hello! Ask for colleges by course and location, why a recommendation appeared, budget matches, entrance exams, or any CareerCompass course/career topic.", [], None
    if "quiz" in query:
        return "The 12-question aptitude and interest quiz compares six career dimensions and saves your result locally.", [{"text": "Take the quiz", "url": url_for("quiz")}], None
    if "why" in query and ("four college" in query or "4 college" in query or "only four" in query):
        return chat_college_search(query, conversation)

    db = get_db()
    current_topic = conversation["current_topic"] or ""
    college_words = {"college", "colleges", "university", "universities", "institute", "institutions", "recommendation", "recommendations", "budget", "selected state", "no match", "no colleges"}
    if any(word in query for word in college_words) or (detect_course(query) and any(word in query for word in ["show", "suggest", "best", "available", "offer"])):
        return chat_college_search(query, conversation)

    if current_topic.startswith("college:") and any(word in query for word in ["exam", "entrance", "eligibility", "fee", "admission"]):
        slug = current_topic.split(":", 1)[1]
        row = db.execute("SELECT * FROM colleges WHERE slug = ?", (slug,)).fetchone()
        if row:
            college = college_from_row(row)
            if "exam" in query or "entrance" in query:
                answer = f"{college['name']} lists these relevant admission routes in CareerCompass: {', '.join(college['entrance_exams'])}. Verify the current official admission notice."
            elif "fee" in query:
                answer = f"{college['name']}: {college['fees']} Unknown fees are not classified as within budget."
            elif "eligibility" in query:
                answer = f"{college['name']}: {college['eligibility']}"
            else:
                answer = college["admission"]
            return answer, [{"text": "View college details", "url": url_for("college_detail", slug=slug)}, {"text": "Official admissions", "url": college["admission_url"]}], current_topic

    tokens = [token for token in re.findall(r"[a-z0-9+#.]+", query) if len(token) > 2 and token not in STOP_WORDS]
    follow_up_words = {"salary", "eligibility", "duration", "subjects", "skills", "exams", "roadmap", "opportunities"}
    use_current = current_topic and any(word in query for word in follow_up_words) and len(tokens) <= 4
    selected = None
    if use_current and current_topic.startswith(("course:", "career:", "skill:", "technology:")):
        current_kind, current_slug = current_topic.split(":", 1)
        selected = db.execute("SELECT * FROM knowledge_items WHERE kind = ? AND slug = ?", (current_kind, current_slug)).fetchone()
    if selected is None:
        scored = []
        for row in db.execute("SELECT * FROM knowledge_items").fetchall():
            title = row["title"].lower(); haystack = f"{title} {row['keywords']}"
            score = (8 if title in query else 0) + sum(3 if token in title else 1 for token in tokens if token in haystack)
            if score: scored.append((score, row))
        if scored: selected = sorted(scored, key=lambda pair: (-pair[0], pair[1]["title"]))[0][1]
    if selected is None:
        return "I could not find a confident local-database answer. Name a course, career or location—for example, 'B.Des colleges in Gujarat' or 'BCA eligibility'.", [{"text": "Browse colleges", "url": url_for("colleges")}, {"text": "Browse careers", "url": url_for("courses")}], None
    details = json.loads(selected["details_json"])
    if "salary" in query: answer = f"{details['title']}: {details['salary']} These are broad orientation figures, not guarantees."
    elif "eligibility" in query: answer = f"Eligibility for {details['title']}: {details['eligibility']} Always verify institution rules."
    elif "duration" in query or "how long" in query: answer = f"Typical duration/preparation for {details['title']}: {details['duration']}"
    elif "subject" in query: answer = f"Important subjects for {details['title']}: {', '.join(details['subjects'])}."
    elif "exam" in query or "entrance" in query: answer = f"Common entrance routes for {details['title']}: {', '.join(details['entrance_exams'])}."
    elif "skill" in query: answer = f"Useful skills for {details['title']}: {', '.join(details['skills'])}."
    elif "roadmap" in query or "how to become" in query: answer = "A simple roadmap: " + " → ".join(details["roadmap"]) + "."
    elif "opportun" in query or "job" in query: answer = f"Related opportunities: {', '.join(details['opportunities'])}."
    else: answer = f"{details['title']}: {details['overview']} Typical duration/preparation: {details['duration']}"
    return answer, [{"text": f"View {details['title']}", "url": selected["detail_url"]}], f"{selected['kind']}:{selected['slug']}"


@app.post("/api/chat/conversations/<int:conversation_id>/messages")
def send_chat_message(conversation_id):
    conversation = owned_conversation(conversation_id)
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Message is required."}), 400
    if len(message) > 500:
        return jsonify({"error": "Please keep the message under 500 characters."}), 400

    answer, links, topic = build_chat_answer(message, conversation)
    first_link = links[0] if links else {}
    now = utc_now()
    db = get_db()
    db.execute(
        "INSERT INTO chat_messages (conversation_id, sender, content, created_at) VALUES (?, 'user', ?, ?)",
        (conversation_id, message, now),
    )
    cursor = db.execute(
        "INSERT INTO chat_messages (conversation_id, sender, content, link_text, link_url, links_json, created_at) VALUES (?, 'bot', ?, ?, ?, ?, ?)",
        (conversation_id, answer, first_link.get("text"), first_link.get("url"), json.dumps(links), now),
    )
    title = conversation["title"]
    if title == "New conversation":
        title = message[:42] + ("…" if len(message) > 42 else "")
    db.execute(
        "UPDATE chat_conversations SET title = ?, current_topic = COALESCE(?, current_topic), updated_at = ? WHERE id = ? AND owner_token = ?",
        (title, topic, now, conversation_id, get_owner_token()),
    )
    db.commit()
    return jsonify({
        "id": cursor.lastrowid, "sender": "bot", "content": answer,
        "link_text": first_link.get("text"), "link_url": first_link.get("url"),
        "links": links, "created_at": now,
    })


@app.route("/history")
def history():
    rows = get_db().execute(
        "SELECT id, student_name, top_category, created_at FROM quiz_results ORDER BY id DESC LIMIT 20"
    ).fetchall()
    return render_template("history.html", rows=rows, categories=CATEGORIES)


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


init_db()


if __name__ == "__main__":
    app.run(debug=True, port=5002, use_reloader=False)
