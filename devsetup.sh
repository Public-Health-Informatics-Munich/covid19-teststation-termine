#!/bin/sh
docker run -e POSTGRES_PASSWORD=example -e POSTGRES_DB=termine -p5432:5432 postgres:11

cd termine-fe
yarn install
yarn build

cd ../termine-bo

yarn install
yarn build

cd ../termine-be

pipenv install

pipenv run hug -f main.py -c set_frontend_config \
  --instance_name DevInstance \
  --long_instance_name DevelopmentInstance \
  --contact_info_bookings "test@support.com" --for_real

pipenv run hug -f main.py -c init_db --for_real
pipenv run hug -f main.py -c add_user --u user --role admin
pipenv run hug -f main.py -c create_appointments $(date +"%-d %-m")
pipenv run hug -f main.py