# Verification

Sprawdzenie projektu:

```bash
python3 -m unittest discover -s tests
python3 src/library_system.py
python3 src/service_weather_report.py
cat daily_report.yaml
```

Testy jednostkowe obejmują:

- wypożyczanie i zwracanie książek,
- wyszukiwanie książek po tytule, autorze i ISBN,
- enkapsulację kolekcji przez zwracanie krotek,
- blokadę usunięcia wypożyczonej książki,
- parsowanie danych pogodowych,
- strukturę raportu `services_status` i `environment_info`,
- generowanie treści YAML.
