"""Monitor statusu usług i pogody zapisujący raport YAML."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SERVICES = ["https://api.github.com", "https://google.com"]
WEATHER_URL = "https://wttr.in/Dublin?format=j1"
REPORT_PATH = Path("daily_report.yaml")


def get_json(url: str, timeout: int = 10) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "lesson24-python-homework/1.0"})
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def check_service(url: str, timeout: int = 10) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "lesson24-python-homework/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            status_code = response.getcode()
        is_up = 200 <= status_code < 400
        return {
            "url": url,
            "status": "UP" if is_up else "DOWN",
            "status_icon": "🟢" if is_up else "🔴",
            "http_status": status_code,
        }
    except (HTTPError, URLError, TimeoutError) as error:
        status_code = error.code if isinstance(error, HTTPError) else None
        return {
            "url": url,
            "status": "DOWN",
            "status_icon": "🔴",
            "http_status": status_code,
            "error": str(error),
        }


def parse_weather(data: dict[str, Any], region: str) -> dict[str, Any]:
    current = data.get("current_condition", [{}])[0]
    return {
        "region": region,
        "temperature_c": int(current.get("temp_C", 0)),
        "feels_like_c": int(current.get("FeelsLikeC", 0)),
        "description": current.get("weatherDesc", [{}])[0].get("value", "unknown"),
        "humidity_percent": int(current.get("humidity", 0)),
    }


def build_report(
    services: list[str] | None = None,
    weather_url: str = WEATHER_URL,
    region: str = "Dublin",
) -> dict[str, Any]:
    checked_services = [check_service(url) for url in (services or SERVICES)]
    weather_data = get_json(weather_url)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "services_status": checked_services,
        "environment_info": parse_weather(weather_data, region),
    }


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def dump_yaml(data: Any, indent: int = 0) -> str:
    prefix = " " * indent
    lines: list[str] = []

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.append(dump_yaml(value, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {yaml_scalar(value)}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                lines.append(f"{prefix}-")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{prefix}- {yaml_scalar(item)}")
    else:
        lines.append(f"{prefix}{yaml_scalar(data)}")

    return "\n".join(lines)


def save_report(report: dict[str, Any], path: Path = REPORT_PATH) -> None:
    path.write_text(dump_yaml(report) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    save_report(report)
    print(f"Zapisano raport do pliku {REPORT_PATH}")


if __name__ == "__main__":
    main()
