# Advanced Conditional CI/CD Workflow

Ten plik opisuje workflow `Advanced Conditional CI/CD` z zadania domowego.
Workflow znajduje się w `.github/workflows/advanced-conditional-workflow.yml`.

## Uruchamianie

Workflow uruchamia się dla:

- `push` na dowolną gałąź,
- `pull_request` na dowolną gałąź.

## Zmienne środowiskowe

Workflow używa zmiennych globalnych:

- `APP_NAME` - nazwa aplikacji używana w logach i raportach,
- `PYTHON_VERSION` - wersja Pythona dla jobów build/test,
- `ARTIFACT_RETENTION_DAYS` - liczba dni przechowywania artefaktów.

Dodatkowo joby ustawiają `APP_ENV`, np. `build`, `test` albo `production`.

## Job: Build

Job `Build` działa dla `push` i `pull_request`.

Kroki:

1. Pobiera kod repozytorium.
2. Instaluje wybraną wersję Pythona.
3. Pokazuje kontekst uruchomienia.
4. Uruchamia `scripts/build.sh`.
5. Zapisuje artefakt `build-report-*`, ale tylko dla gałęzi `main`.

Warunek joba:

```yaml
if: github.event_name == 'push' || github.event_name == 'pull_request'
```

Warunkowy krok artefaktu:

```yaml
if: github.ref == 'refs/heads/main'
```

## Job: Test

Job `Test` uruchamia się dopiero po poprawnym zakończeniu joba `Build`.

Kroki:

1. Pobiera kod repozytorium.
2. Instaluje Pythona.
3. Uruchamia testy jednostkowe komendą `python -m unittest discover -s tests`.
4. Tworzy krótkie podsumowanie testów.
5. Zapisuje artefakt `test-summary-*`, ale tylko dla gałęzi `main`.

Warunek joba:

```yaml
if: needs.build.result == 'success'
```

## Job: Deploy to prod

Job `Deploy to prod` wykonuje symulowane wdrożenie produkcyjne.
Uruchamia się wyłącznie przy `push` do gałęzi `main` i tylko jeśli testy przeszły poprawnie.

Warunek:

```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/main' && needs.test.result == 'success'
```

Kroki:

1. Pobiera kod repozytorium.
2. Uruchamia `scripts/deploy.sh`.
3. Zapisuje artefakt `deploy-report-*`.

Dzięki temu pull requesty oraz pushe do innych gałęzi nie uruchamiają wdrożenia.

## Job: Workflow status report

Job `Workflow status report` działa zawsze, niezależnie od wyniku wcześniejszych jobów.
Jego zadaniem jest wypisanie końcowego statusu:

```text
[success] Build
[success] Test
[success] Deploy to prod
```

Jeżeli wdrożenie zostało pominięte, job wypisuje informację, że deploy działa tylko dla `push` do `main`.
Jeżeli build albo testy zakończą się błędem, job raportujący również kończy workflow błędem.

## Lokalne uruchomienie

Do lokalnego sprawdzenia nie jest wymagany Docker:

```bash
./scripts/build.sh
python -m unittest discover -s tests
APP_ENV=production ./scripts/deploy.sh
```

Opcjonalnie można uruchomić te same komendy w kontenerze:

```bash
docker run --rm -v "$PWD:/app" -w /app python:3.11-slim bash -lc \
  "./scripts/build.sh && python -m unittest discover -s tests"
```

## Artefakty

Artefakty są zapisywane tylko dla gałęzi `main`.
Po udanym workflow w zakładce Actions można pobrać:

- raport budowania,
- podsumowanie testów,
- raport wdrożenia.
