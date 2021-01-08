# Covid19 Teststation appointments booking app

An appointment booking app, currently designed for works doctors from official institutes.

Developed for [LMU Division of Infectious Diseases and Tropical Medicine](http://www.klinikum.uni-muenchen.de/Abteilung-fuer-Infektions-und-Tropenmedizin/en/index.html) by [Mayflower GmbH](https://mayflower.de)

<img src=".github/show/booking-app-1.png"/>
<a href="screenshots.md">More Screenshots</a>

## Quickstart with docker-compose

1. start the docker-compose environment 
```
docker-compose up --build -d
```
2. get a shell in the _termine_ service 
```
docker-compose exec termine /bin/bash
```
3. create a admin user 
```
hug -f main.py -c add_user admin -r admin
```
4. add appointments to your system 
```
hug -f main.py -c create_appointments -y 2021 DAY MONTH
``` 
replace _**DAY**_ with the two digit day of the month and _**MONTH**_ with the two digit month 

Now browse the app with your browser at http://localhost:8000/

(**_HINT_**)
To persist the postgres database create a directory add follow lines to the postgres service:
```
 volumes:
  - ./postgres-data:/var/lib/postgresql/data
```
<br/>

## Configuration of running instance

### Environment Variables to setup the Backend Server

#### Setup The Database
1. Set with multiple Environment variables
    * DB_USERNAME => The usename to connect the database server
    * DB_PASSWORD => The password to connect the database server
    * DB_PORT     => the port of the database (Default: '5432')
    * DB_HOST     => The hostname of the database server (Default: 'localhost')
    * DB_DATABASE => The database to store the tables (Default: 'termine')
2. Set with one url variable
    * DB_URL => The url to connect the database (Default: 'postgresql://postgres:example@localhost:5432/termine')

#### Setup behaviour of the Application
* CLAIM_TIMEOUT_MIN   => Setup the timeout of claims for appointments (how long the slot is blocked after click in the bottom) (Default 5min)
* DISPLAY_SLOTS_COUNT => Maximal displayed slot counts (Default 150)
* TERMINE_TIME_ZONE   => Timezone of the Station (Default: 'Europe/Berlin')
* DISABLE_AUTH        => Set to 'true' to allow anybody to get a appointment. Without to Login/Auth (Default: 'False')
                         With this settings to 'true' you need only admin user! Doctor user are useless!

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
  [--form_fields STRING]
```

* `instance_name` is the short form of 
* `long_instance_name` that is shown in the header of the frontends 
* `contact_info_bookings` might be an email or phone number, and is shown when the number of possible bookings is depleted.
* `contact_info_appointments` might be an email or phone number,
if left out takes the value of `contact_info_bookings`, 
and is shown when there are no free slots left to book appointments for.
* `form_fields` comma separated list of form fields to be displayed in the appointment selector. possible values
are `"base,address,dayOfBirth,reason"`

## Current dev setup

### Start the database container

```bash
docker run -e POSTGRES_PASSWORD=example -e POSTGRES_DB=termine -p5432:5432 postgres:11
```

#### If you develop on the python server part

to make the python server pick up and serve the frontends at localhost:8000

````bash

## Update / Change translation strings
The translation sources are in the follow folders:
 * termine-fe/src/locales/de/messages.json
 * termine-fe/src/locales/en/messages.json

After change in the translation source you need to compile the changes to be applied to the used javascript code.
```bash
cd termine-fe
yarn run compile-i18n
````

## Update list of test reasons

Add your reasons to `termine-fe/src/config/reasons.json`. These are what is written in the database and printed in the excel.

If you want the test reasons to be translated, add the entries to:

`termine-fe/src/locales/de/messages.json` and

`termine-fe/src/locales/en/messages.json`

and then follow the section above

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

````

### Prepare your python environment and start the hug server
```bash
cd termine-be
pipenv install
pipenv shell
hug -f main.py -c init_db --for_real
hug -f main.py -c add_user --u user [--role admin]
hug -f main.py -c create_appointments $(date +"%-d %-m")
hug -f main.py
````

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
