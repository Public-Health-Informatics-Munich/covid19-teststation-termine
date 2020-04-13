# Termine-BE

## COMMANDS

### testdatenbank starten
```bash
docker run -e POSTGRES_PASSWORD=example -e POSTGRES_DB=termine -p5432:5432 postgres:11
```

### environment vorbereiten und umgebung starten

```bash
pipenv install
pipenv shell
hug -f main.py -c init_db --for_real
hug -f main.py -c add_user --u user [--role admin]
hug -f main.py -c create_appointments $(date +"%-d %-m")
hug -f main.py
```

