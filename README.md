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

Projekt stworzony jako zaliczenie studiów podyplomowych "Akademia Programowania w Pythonie". 
Aplikacja umożliwia:

- Wyszukiwanie stacji pomiarowych na podstawie miasta
- Wybór dostępnych czujników i zakresów dat
- Pobieranie danych pomiarowych z API
- Wyświetlanie statystyk (min, max, średnia)
- Rysowanie wykresu pomiarów
- Przechowywanie danych w lokalnej bazie SQLite
- Czyszczenie oraz resetowanie bazy danych

## Wymagania

- Python 3.13
- Biblioteki:
  - `tkinter`
  - `matplotlib`
  - `requests` 
  - `sqlite3` (wbudowany)


Instalacja
git clone ********** # (tu podam później link do ostatecznego repozytorium, np. GitHub)
cd **********
Uruchom aplikację:


projekt_zaliczeniowy
Struktura projektu

├── api/

│   ├── stations.py         # Obsługa zapytań dot. stacji

│   └── sensors.py          # Obsługa zapytań dot. czujników

├── db/

│   └── database.py         # Operacje na bazie danych SQLite

├── visualization/

│   └── plotting.py         # Tworzenie wykresów i analiz

├── app.py                  # Główny plik z interfejsem GUI

├── main.py                 # Plik do uruchomienia GUI

├── README.md               # Ten plik



Sposób użycia:

Uruchom aplikację (main.py)

Wpisz nazwę miasta i kliknij "Pobierz stacje"

Wybierz stację i kliknij "Pobierz czujniki"

Wybierz czujnik i kliknij "Pobierz daty"

Wybierz zakres dat i kliknij "Pobierz dane"

Przeglądaj statystyki, rysuj wykresy i zarządzaj bazą danych

Przykład działania

(Tutaj możesz dodać zrzuty ekranu z aplikacji GUI pokazujące interfejs, np. screeny app.png, plot.png i dodać coś w stylu:)

![image](https://github.com/user-attachments/assets/751a4d7e-5af3-41c6-81e5-8fd08058b6f8)

![Interfejs główny](docs/screenshot1.png)
![Wykres pomiarów](docs/plot_example.png)
Uwagi
Aplikacja wykorzystuje dane z publicznego API. W przypadku problemów z połączeniem (np. brak internetu lub przeciążone API), pojawią się odpowiednie komunikaty.

Domyślna baza danych to plik SQLite zapisany lokalnie. Można go łatwo przenieść lub usunąć przy pomocy przycisku "Usuń dane z bazy".

Kod można łatwo rozbudować np. o inne formy wizualizacji, eksport danych do CSV, czy zapis konfiguracji użytkownika.


Autor:
Emilia Staśkowiak
