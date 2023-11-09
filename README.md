# Cinema database

## Generating database
To generate database go to file [generate_db.py](db_generation/generate_db.py) and run the script.
Output should appear in the [db_generation](db_generation) directory in file [output.sql](db_generation/output.sql)
along with overall summary located in [output.csv](db_generation/output.csv).

## Manifest (in polish)
Baza danych służy wsparciu obsługi kina. Kino to organizuje seanse filmów w swoich salach
kinowych. Na te seanse sprzedaje bilety na konkretne miejsca. Jednym z kanałów
sprzedaży biletów jest serwis internetowy. Filmy są wyświetlane w kinie w różnych wersjach
językowych i różnych wymiarach (2D, 3D). Niektóre rodzaje filmów wymagają specjalnego
wyposażenia sali. Poszczególne sale mogą mieć sponsorów tytularnych. Niektóre miejsca
na sali są na podwójnych kanapach. Specjalnie oznaczone miejsca mają podwyższoną
cenę.

![img.png](schema.png)

1. Dodaj plik [TEST.dmp](https://drive.google.com/drive/folders/15HuhsffRxjsD-GPD9ZBhHe51mn2Gkg8j) do folderu db_generation/volume_data.
2. Uruchom container bazy oraz przygotuj volumeny poprzez uruchomienie `make pod-init`
3. Następnie załaduj dane do bazy poprzez uruchomienie `make pod-init-db`
4. Uruchom mierzenie czasu `make pod-run-measurement`
