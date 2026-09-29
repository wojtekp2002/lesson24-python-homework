# Lesson 24 - Python object-oriented and scripting homework

Projekt zawiera dwa zadania:

1. obiektowy system zarządzania biblioteką,
2. skrypt monitorujący status usług i pogodę, zapisujący raport YAML.

## Zadanie 1: system zarządzania biblioteką

Plik: `src/library_system.py`

Zaimplementowane klasy:

- `Book` - książka z tytułem, autorem, ISBN, rokiem wydania i dostępnością,
- `Reader` - czytelnik z numerem czytelnika i listą wypożyczonych książek,
- `Library` - biblioteka z enkapsulowaną kolekcją książek i czytelników.

Biblioteka umożliwia:

- dodawanie i usuwanie książek,
- rejestrowanie i usuwanie czytelników,
- wypożyczanie i zwracanie książek,
- wyszukiwanie książek po tytule, autorze albo ISBN,
- sprawdzanie wypożyczeń czytelnika.

Uruchomienie demonstracji:

```bash
python3 src/library_system.py
```

## Zadanie 2: monitor statusu usług i pogody

Plik: `src/service_weather_report.py`

Skrypt sprawdza listę adresów URL:

- `https://api.github.com`,
- `https://google.com`,

a następnie pobiera aktualną pogodę dla Dublina z:

```text
https://wttr.in/Dublin?format=j1
```

Wynik zapisuje do pliku `daily_report.yaml` w sekcjach:

- `services_status`,
- `environment_info`.

Uruchomienie:

```bash
python3 src/service_weather_report.py
```

Przykładowy fragment raportu:

```yaml
services_status:
  -
    url: "https://api.github.com"
    status: "UP"
    status_icon: "🟢"
    http_status: 200
environment_info:
  region: "Dublin"
  temperature_c: 12
```

## Testy

Projekt używa tylko standardowej biblioteki Pythona, więc do testów nie trzeba
instalować dodatkowych paczek.

```bash
python3 -m unittest discover -s tests
```

## Struktura projektu

```text
.
├── README.md
├── docs/
│   └── verification.md
├── src/
│   ├── library_system.py
│   └── service_weather_report.py
└── tests/
    ├── test_library_system.py
    └── test_service_weather_report.py
```
