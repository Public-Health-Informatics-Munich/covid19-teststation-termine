# Covid19 Teststation appointments booking app

An appointment booking app, currently designed for works doctors from official institutes.

Developed for [LMU Division of Infectious Diseases and Tropical Medicine](http://www.klinikum.uni-muenchen.de/Abteilung-fuer-Infektions-und-Tropenmedizin/en/index.html) by	[Mayflower GmbH](https://mayflower.de)

## Current dev setup

### Start the database container
```bash
docker run -e POSTGRES_PASSWORD=example -e POSTGRES_DB=termine -p5432:5432 postgres:11
```
#### If you develop on the python server part
to make the python server pick up and serve the frontends at localhost:8000
```bash
# works doctor facing at localhost:8000/
cd termine-fe
yarn install
yarn build

# admin facing at localhost:8000/admin
cd termine-bo
yarn install
yarn build
```

### Prepare your python environment and start the hug server
```bash
cd termine-be
pipenv install
pipenv shell
hug -f main.py -c db init_db --for_real
hug -f main.py -c db add_user --u user [--role admin]
hug -f main.py -c db create_appointments $(date +"%-d %-m")
hug -f main.py
```

#### If you develop on the frontend part
To have the webpack dev server serve the project at localhost:3000
```bash
# works doctor facing at localhost:3000/
cd termine-fe
yarn install
yarn start

# admin facing at localhost:3001/
cd termine-bo
yarn install
yarn start

```

Stay safe!

![LMU Division of Infectious Diseases and Tropical Medicine](https://github.com/Public-Health-Informatics-Munich/covid19-teststation-termine/raw/master/Logo-LMU-Abteilung-Infektions-und-Tropenmedizin.png)
![Mayflower GmbH](https://mayflower.de/wp-content/uploads/2014/04/Mayflower-Logo-440.png)
