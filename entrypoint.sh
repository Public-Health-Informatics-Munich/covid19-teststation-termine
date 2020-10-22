#!/usr/bin/env bash

echo Init Database and of if it is already init run migration instade
hug -f main.py -c init_db --for_real || hug -f main.py -c run_migrations --for_real

if [ "${FRONTEND_CONF_JSON}" != "" ]; then
  echo Load frontend config from given jsonfile
  hug -f main.py -c load_frontend_config "${FRONTEND_CONF_JSON}" --for_real
fi

gunicorn --bind=0.0.0.0:8000 main:__hug_wsgi__
