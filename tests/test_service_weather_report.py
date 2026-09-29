import unittest
from unittest.mock import patch

from src.service_weather_report import build_report, dump_yaml, parse_weather


class ServiceWeatherReportTest(unittest.TestCase):
    def test_parse_weather_extracts_current_temperature(self):
        weather = {
            "current_condition": [
                {
                    "temp_C": "11",
                    "FeelsLikeC": "9",
                    "weatherDesc": [{"value": "Partly cloudy"}],
                    "humidity": "80",
                }
            ]
        }

        self.assertEqual(
            parse_weather(weather, "Dublin"),
            {
                "region": "Dublin",
                "temperature_c": 11,
                "feels_like_c": 9,
                "description": "Partly cloudy",
                "humidity_percent": 80,
            },
        )

    def test_build_report_has_required_sections(self):
        fake_weather = {
            "current_condition": [
                {
                    "temp_C": "15",
                    "FeelsLikeC": "14",
                    "weatherDesc": [{"value": "Sunny"}],
                    "humidity": "60",
                }
            ]
        }

        with patch("src.service_weather_report.check_service") as check_service:
            with patch("src.service_weather_report.get_json", return_value=fake_weather):
                check_service.return_value = {
                    "url": "https://example.com",
                    "status": "UP",
                    "status_icon": "🟢",
                    "http_status": 200,
                }

                report = build_report(["https://example.com"])

        self.assertIn("services_status", report)
        self.assertIn("environment_info", report)
        self.assertEqual(report["environment_info"]["temperature_c"], 15)
        self.assertEqual(report["services_status"][0]["status"], "UP")

    def test_dump_yaml_contains_sections(self):
        content = dump_yaml(
            {
                "services_status": [{"url": "https://example.com", "status": "UP"}],
                "environment_info": {"temperature_c": 15},
            }
        )

        self.assertIn("services_status:", content)
        self.assertIn("environment_info:", content)
        self.assertIn('temperature_c: 15', content)


if __name__ == "__main__":
    unittest.main()
