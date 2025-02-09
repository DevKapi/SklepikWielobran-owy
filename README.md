# SklepikWielobranzowy
Sklepik internetowy wielobranżowy to sklepik w którym użytkownicy mogą dodawać mogą filtrować, kupować czy czytać opisy produktów.


**Funkcje aplikacji**  
 Lista produktów z możliwością wyszukiwania i filtrowania  
 System koszyka – dodawanie/usuwanie produktów  
 Finalizacja zamówienia  
 Logowanie i rejestracja użytkowników  
 Panel administracyjny Django  
 Stylizacja za pomocą Bootstrap 5  

**Panel admina**  
user: kowal  
p: test

**Panel użytkownika**  
user: Zuzia  
p: testSWPS





##  **Instalacja i uruchomienie**  

**Sklonuj repozytorium**  
```bash
git clone https://github.com/DevKapi/SklepikWielobranzowy.git
cd SklepikWielobranzowy

pip install -r requirements.txt

python manage.py migrate
```
Uruchom serwer Django
```
python manage.py runserver
```
Aplikacja będzie dostępna pod adresem http://127.0.0.1:8000/.
