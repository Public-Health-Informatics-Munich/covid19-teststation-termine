# Covid19 Teststation appointments booking app

An appointment booking app, currently designed for works doctors from official institutes.

Developed for [LMU Division of Infectious Diseases and Tropical Medicine](http://www.klinikum.uni-muenchen.de/Abteilung-fuer-Infektions-und-Tropenmedizin/en/index.html) by	[Mayflower GmbH](https://mayflower.de)


<img src=".github/show/booking-app-1.png"/>
<a href="screenshots.md">More Screenshots</a>

## Configuration of running instance

### To generate or update the frontend configuration for the client (required for frontends)
```bash
cd termine-be
pipenv install
pipenv shell
hug -f main.py -c set_frontend_config \
  --instance_name STRING \
  --long_instance_name STRING \
  --contact_info_bookings EMAIL|PHONE \
  [--contact_info_appointments EMAIL|PHONE]
```
`instance_name`         is the short form of
`long_instance_name`    that is shown in the header of the frontends
`contact_info_bookings` might be an email or phone number, and is shown when the number of possible bookings is depleted.
`contact_info_appointments` might be an email or phone number,
                            if left out takes the value of `contact_info_bookings`,
                            and is shown when there are no free slots left to book appointments for.


## Current dev setup

### Start the database container
```bash
docker run -e POSTGRES_PASSWORD=example -e POSTGRES_DB=termine -p5432:5432 postgres:11
```
#### If you develop on the python server part
to make the python server pick up and serve the frontends at localhost:8000
```bash

## Update / Change translation strings
The translation sources are in the follow folders:
 * termine-fe/src/locales/de/messages.json
 * termine-fe/src/locales/en/messages.json

After change in the translation source you need to compile the changes to be applied to the used javascript code.
```bash
cd termine-fe
yarn run compile-i18n
```

# works doctor facing at localhost:8000/
cd termine-fe
yarn install
yarn run compile-i18n
yarn build

# admin facing at localhost:8000/admin
cd termine-bo
yarn install
yarn run compile-i18n
yarn build
```

### Prepare your python environment and start the hug server
```bash
cd termine-be
pipenv install
pipenv shell
hug -f main.py -c init_db --for_real
hug -f main.py -c add_user --u user [--role admin]
hug -f main.py -c create_appointments $(date +"%-d %-m")
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
