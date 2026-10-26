# JWT Mini-API

## Projekti kirjeldus

See projekt on Pythonis loodud Flaski rakendus, mis kasutab JWT-d kasutajate autentimiseks ja ligipääsu kontrollimiseks.

## Kasutatud tehnoloogiad

- Python
- Flask
- PyJWT
- python-dotenv
- Postman

## API lõpp-punktid

| Meetod | Lõpp-punkt | Kirjeldus |
|---|---|---|
| POST | /login | Kontrollib kasutaja andmeid ja väljastab JWT |
| GET | /profiil | Tagastab kehtiva JWT põhjal kasutaja andmed |
| GET | /admin | Lubab ligipääsu ainult administraatorile |

## JWT turvalisus

- Kasutatakse HS256 algoritmi.
- Token kehtib 5 minutit.
- Salavõti asub `.env` failis.
- Vigane või aegunud token tagastab HTTP 401.
- Puuduvate õiguste korral tagastatakse HTTP 403.

## Rakenduse käivitamine

1. Paigalda vajalikud teegid:

   `pip install -r requirements.txt`

2. Loo `.env` fail ja lisa sinna `JWT_SECRET_KEY` koos turvalise juhusliku võtmega.

3. Käivita rakendus:

   `python app.py`

4. API töötab aadressil:

   `http://127.0.0.1:5000`

## Testimine

Rakendust testiti Postmaniga. Kõik 7 testjuhtumit läbisid testi edukalt. Testide tulemused ja kuvatõmmised on lisatud Notioni lehele.
