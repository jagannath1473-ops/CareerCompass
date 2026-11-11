import json
import os
import shutil
import sqlite3
import tempfile
import unittest
from urllib.parse import urlencode


TEMP_DIR = tempfile.TemporaryDirectory()
TEST_DB = os.path.join(TEMP_DIR.name, "careercompass-test.db")
os.environ["CAREERCOMPASS_DATABASE"] = TEST_DB
os.environ["SECRET_KEY"] = "automated-test-secret"

import app as app_module  # noqa: E402
from college_data import COLLEGES  # noqa: E402
from course_catalog import COURSE_CATALOG  # noqa: E402
from geo_data import INDIA_LOCATIONS  # noqa: E402
from recommendation import recommend, sort_results  # noqa: E402


class CareerCompassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app_module.app.config.update(TESTING=True)
        cls.client = app_module.app.test_client()

    @classmethod
    def tearDownClass(cls):
        TEMP_DIR.cleanup()

    def search(self, course, scope, country, state="", city=""):
        query = urlencode({
            "preferred_course": course, "study_scope": scope,
            "preferred_country": country, "preferred_state": state,
            "preferred_city": city, "institution_type": "Either",
        })
        response = self.client.get("/api/colleges/search?" + query)
        self.assertEqual(response.status_code, 200)
        return response.get_json()

    def test_catalogue_minimums(self):
        indian = [college for college in COLLEGES if college["country"] == "India"]
        international = [college for college in COLLEGES if college["country"] != "India"]
        self.assertGreaterEqual(len(indian), 150)
        self.assertGreaterEqual(len(international), 80)
        self.assertGreaterEqual(len(COURSE_CATALOG), 150)
        self.assertLessEqual(len(COURSE_CATALOG), 250)
        self.assertEqual(len(COURSE_CATALOG), len({item["name"] for item in COURSE_CATALOG}))
        self.assertEqual({item["category"] for item in COURSE_CATALOG}, set(app_module.CAREER_FIELDS))

    def test_vijayawada_private_cse_is_strict(self):
        query = urlencode({
            "preferred_course": "B.Tech Computer Science Engineering", "study_scope": "India",
            "preferred_country": "India", "preferred_state": "Andhra Pradesh",
            "preferred_city": "Vijayawada", "institution_type": "Private",
        })
        data = self.client.get("/api/colleges/search?" + query).get_json()
        self.assertGreaterEqual(data["exact_count"], 3)
        self.assertEqual(data["alternative_count"], 0)
        self.assertTrue(all(item["country"] == "India" and item["state"] == "Andhra Pradesh" and item["city"] == "Vijayawada" and item["ownership"] == "Private" for item in data["results"]))

    def test_wrong_state_never_leaks_without_opt_in(self):
        base = {"preferred_course": "B.Tech Computer Science Engineering", "study_scope": "India",
                "preferred_country": "India", "preferred_state": "Andhra Pradesh",
                "preferred_city": "Imaginary City", "institution_type": "Private"}
        exact = self.client.get("/api/colleges/search?" + urlencode(base)).get_json()
        self.assertEqual(exact["total"], 0)
        self.assertEqual(exact["alternative_count"], 0)
        broader = self.client.get("/api/colleges/search?" + urlencode({**base, "show_alternatives": 1})).get_json()
        self.assertGreater(broader["alternative_count"], 0)
        self.assertTrue(all(item["country"] == "India" for item in broader["results"]))

    def test_institution_type_and_unknown_fee_are_strict(self):
        preference = {"preferred_course": "B.Tech Computer Science Engineering", "study_scope": "India",
                      "preferred_country": "India", "preferred_state": "Andhra Pradesh",
                      "preferred_city": "Vijayawada", "institution_type": "Government"}
        self.assertEqual(recommend(COLLEGES, preference), [])
        preference.update({"institution_type": "Private", "budget_amount": 400000,
                           "budget_currency": "INR", "budget_mode": "strict"})
        self.assertEqual(recommend(COLLEGES, preference), [])

    def test_course_api_filters_by_category(self):
        data = self.client.get("/api/courses?category=Creative%20and%20Design").get_json()
        self.assertGreater(data["count"], 20)
        self.assertTrue(all(item["category"] == "Creative and Design" for item in data["courses"]))

    def test_all_indian_states_and_union_territories_selectable(self):
        response = self.client.get("/api/locations/subdivisions?country=India")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["subdivisions"]), 36)
        self.assertEqual(len(INDIA_LOCATIONS), 36)

    def test_required_indian_searches(self):
        cases = [
            ("B.Tech CSE", "Karnataka", "Bengaluru"), ("MBBS", "Maharashtra", "Mumbai"),
            ("B.Des", "Gujarat", "Ahmedabad"), ("BBA", "Delhi", ""),
            ("Mechanical Engineering", "Tamil Nadu", "Chennai"),
            ("Artificial Intelligence", "Telangana", "Hyderabad"),
            ("Computer Science", "Kerala", ""), ("Engineering", "Rajasthan", ""),
            ("Business Administration", "Uttar Pradesh", ""),
            ("Life Sciences", "West Bengal", ""),
        ]
        for course, state, city in cases:
            with self.subTest(course=course, state=state, city=city):
                data = self.search(course, "India", "India", state, city)
                self.assertGreater(data["exact_count"], 0)
                self.assertGreater(data["total"], 0)

    def test_required_international_searches(self):
        cases = [
            ("Computer Science", "United States", "California"),
            ("Artificial Intelligence", "Canada", "Ontario"),
            ("Engineering", "Germany", "Bavaria"),
            ("Business", "United Kingdom", "England"),
            ("Computer Science", "Australia", "Victoria"),
            ("Design", "Singapore", ""), ("Science", "Japan", "Tokyo"),
        ]
        for course, country, state in cases:
            with self.subTest(course=course, country=country, state=state):
                data = self.search(course, "Abroad", country, state)
                self.assertGreater(data["exact_count"], 0)

        toronto = self.search("Business Administration", "Abroad", "Canada", "Ontario", "Toronto")
        self.assertGreater(toronto["exact_count"], 0)
        self.assertTrue(all(item["city"] == "Toronto" and item["state"] == "Ontario" for item in toronto["results"]))

    def test_inaccurate_course_matches_are_excluded(self):
        data = self.search("B.Tech CSE", "India", "India", "Delhi")
        names = {result["name"] for result in data["results"]}
        self.assertNotIn("All India Institute of Medical Sciences New Delhi", names)

    def test_locations_change_results(self):
        bengaluru = self.search("B.Tech CSE", "India", "India", "Karnataka", "Bengaluru")
        chennai = self.search("B.Tech CSE", "India", "India", "Tamil Nadu", "Chennai")
        self.assertNotEqual(bengaluru["results"][0]["name"], chennai["results"][0]["name"])

    def test_load_more_pagination_has_no_duplicate_rows(self):
        base = {"preferred_course": "Computer Science", "study_scope": "Both", "institution_type": "Either"}
        first = self.client.get("/api/colleges/search?" + urlencode({**base, "page": 1})).get_json()
        second = self.client.get("/api/colleges/search?" + urlencode({**base, "page": 2})).get_json()
        first_slugs = {item["slug"] for item in first["results"]}
        second_slugs = {item["slug"] for item in second["results"]}
        self.assertTrue(first["has_more"])
        self.assertFalse(first_slugs & second_slugs)

    def test_strict_budget_uses_only_verified_fees(self):
        preferences = {
            "preferred_course": "Computer Science", "study_scope": "Abroad",
            "preferred_country": "United States", "preferred_state": "Massachusetts",
            "preferred_city": "Cambridge", "institution_type": "Either",
            "budget_amount": 70000, "budget_currency": "USD", "budget_mode": "strict",
        }
        results = recommend(COLLEGES, preferences)
        self.assertTrue(results)
        self.assertTrue(all(item["budget_status"] == "Confirmed within budget" for item in results))
        self.assertIn("Massachusetts Institute of Technology", {item["name"] for item in results})
        preferences["budget_amount"] = 60000
        self.assertNotIn("Massachusetts Institute of Technology", {item["name"] for item in recommend(COLLEGES, preferences)})

    def test_original_quiz_still_works(self):
        data = {"name": "Automated Student", "email": ""}
        data.update({f"q{index}": "0" for index in range(12)})
        response = self.client.post("/quiz", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Top direction", response.data)

    def test_chatbot_uses_college_database_and_history(self):
        created = self.client.post("/api/chat/conversations", json={}).get_json()
        conversation_id = created["id"]
        reply = self.client.post(
            f"/api/chat/conversations/{conversation_id}/messages",
            json={"message": "Which colleges offer B.Des in Gujarat?"},
        ).get_json()
        self.assertIn("National Institute of Design Ahmedabad", reply["content"])
        self.assertTrue(reply["links"])
        history = self.client.get(f"/api/chat/conversations/{conversation_id}").get_json()
        self.assertGreaterEqual(len(history["messages"]), 3)


class MigrationPreservationTest(unittest.TestCase):
    def test_existing_quiz_row_survives_migration(self):
        migration_dir = tempfile.mkdtemp()
        legacy_path = os.path.join(migration_dir, "legacy.db")
        connection = sqlite3.connect(legacy_path)
        connection.execute("CREATE TABLE quiz_results (id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT NOT NULL, email TEXT, scores_json TEXT NOT NULL, top_category TEXT NOT NULL, created_at TEXT NOT NULL)")
        connection.execute("INSERT INTO quiz_results (student_name,email,scores_json,top_category,created_at) VALUES ('Existing Student','',?, 'technology','2026-01-01')", (json.dumps({"technology": 1}),))
        connection.commit(); connection.close()
        original = app_module.DATABASE
        app_module.DATABASE = legacy_path
        try:
            app_module.init_db()
            connection = sqlite3.connect(legacy_path)
            self.assertEqual(connection.execute("SELECT student_name FROM quiz_results").fetchone()[0], "Existing Student")
            self.assertIsNotNone(connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_messages'").fetchone())
            connection.close()
        finally:
            app_module.DATABASE = original
            shutil.rmtree(migration_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
