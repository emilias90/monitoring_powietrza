# Monitor Jakości Powietrza (GUI z użyciem Tkinter)

Aplikacja desktopowa w Pythonie służąca do monitorowania jakości powietrza w wybranym mieście. Umożliwia pobieranie danych pomiarowych z API GIOŚ, ich wizualizację, analizę statystyczną oraz zapis do lokalnej bazy danych SQLite.

## Spis treści

- [Opis projektu](#opis-projektu)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Struktura projektu](#struktura-projektu)
- [Sposób użycia](#sposób-użycia)
- [Przykład działania](#przykład-działania)
- [Licencja](#licencja)

---

## Opis projektu

Projekt stworzony jako ************ (np. zaliczenie kursu, projekt własny, praca inżynierska). Aplikacja umożliwia:

- Wyszukiwanie stacji pomiarowych na podstawie miasta
- Wybór dostępnych czujników i zakresów dat
- Pobieranie danych pomiarowych z API
- Wyświetlanie statystyk (min, max, średnia)
- Rysowanie wykresu pomiarów
- Przechowywanie danych w lokalnej bazie SQLite
- Czyszczenie oraz resetowanie bazy danych

## Wymagania

- Python 3.10+ ********** (upewnij się, że wersja się zgadza)
- Biblioteki:
  - `tkinter`
  - `matplotlib`
  - `requests` ********** (dodaj, jeśli korzystasz w modułach `api/`)
  - `sqlite3` (wbudowany)

Zainstaluj brakujące biblioteki komendą:

```bash
pip install matplotlib requests
Instalacja
Sklonuj repozytorium:

bash
Kopiuj
Edytuj
git clone ********** # (tu podaj link do repozytorium, np. GitHub)
cd **********
Uruchom aplikację:

bash
Kopiuj
Edytuj
python app.py  ********** # (lub inny plik główny, jeśli ma inną nazwę)
Struktura projektu
bash
Kopiuj
Edytuj
├── api/
│   ├── stations.py         # Obsługa zapytań dot. stacji
│   └── sensors.py          # Obsługa zapytań dot. czujników
├── db/
│   └── database.py         # Operacje na bazie danych SQLite
├── visualization/
│   └── plotting.py         # Tworzenie wykresów i analiz
├── app.py                  # Główny plik z interfejsem GUI
├── README.md               # Ten plik
Uwaga: folder api/ powinien zawierać własne funkcje do zapytań do zewnętrznego API GIOŚ.
********** (Jeśli korzystasz z innego API, podaj jego nazwę i sposób działania)

Sposób użycia
Uruchom aplikację (app.py)

Wpisz nazwę miasta i kliknij "Pobierz stacje"

Wybierz stację i kliknij "Pobierz czujniki"

Wybierz czujnik i kliknij "Pobierz daty"

Wybierz zakres dat i kliknij "Pobierz dane"

Przeglądaj statystyki, rysuj wykresy i zarządzaj bazą danych

Przykład działania
(Tutaj możesz dodać zrzuty ekranu z aplikacji GUI pokazujące interfejs, np. screeny app.png, plot.png i dodać coś w stylu:)

scss
Kopiuj
Edytuj
![Interfejs główny](docs/screenshot1.png)
![Wykres pomiarów](docs/plot_example.png)
Uwagi
Aplikacja wykorzystuje dane z publicznego API. W przypadku problemów z połączeniem (np. brak internetu lub przeciążone API), pojawią się odpowiednie komunikaty.

Domyślna baza danych to plik SQLite zapisany lokalnie. Można go łatwo przenieść lub usunąć przy pomocy przycisku "Usuń dane z bazy".

Kod można łatwo rozbudować np. o inne formy wizualizacji, eksport danych do CSV, czy zapis konfiguracji użytkownika.

Licencja
Projekt udostępniany na licencji MIT **********
(Lub innej, jeśli wolisz – podaj szczegóły lub usuń, jeśli nie dotyczy.)

Autor
********** (Wpisz swoje imię i nazwisko lub pseudonim oraz kontakt/GitHub jeśli chcesz)

yaml
Kopiuj
Edytuj

---

Daj znać, jeśli chcesz, żebym przygotował również:

- plik `requirements.txt`
- plik `app.py` jako punkt wejścia, jeśli obecny kod powinien być w nim
- przykład `screenshot.png` do README

Albo jeśli chcesz wygenerować angielską wersję `README.md`.
