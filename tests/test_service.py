import unittest

from app.main import (
    forecast_metric,
    generate_metric_insights,
    health,
    narrate_report,
    record_feedback,
    run_nl_query,
)
from app.models.schemas import UserContext
from scripts_seed_data import seed


class TestBIService(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        seed()

    def test_health(self) -> None:
        self.assertEqual(health()["status"], "ok")

    def test_nl_query_with_rls(self) -> None:
        context = UserContext(user_id="u1", role="analyst", region="EU")
        result = run_nl_query("why did revenue drop last week?", context)
        self.assertIn("region = 'EU'", result.sql)
        self.assertGreater(len(result.rows), 0)

    def test_insight_generation(self) -> None:
        context = UserContext(user_id="u2", role="analyst", region="NA")
        output = generate_metric_insights("revenue", 14, context)
        self.assertEqual(output["metric"], "revenue")
        self.assertGreaterEqual(len(output["insights"]), 1)

    def test_forecast_generation(self) -> None:
        context = UserContext(user_id="u3", role="executive", region=None)
        output = forecast_metric("revenue", 5, context)
        self.assertEqual(len(output["points"]), 5)

    def test_narration_and_feedback(self) -> None:
        summary = narrate_report("executive", "Weekly Revenue", ["Revenue +5% WoW"], 0.8)
        self.assertIn("Weekly Revenue", summary)
        context = UserContext(user_id="u4", role="analyst", region="APAC")
        status = record_feedback("check revenue", True, "looks good", context)
        self.assertEqual(status["status"], "recorded")


if __name__ == "__main__":
    unittest.main()
