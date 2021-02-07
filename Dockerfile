FROM python:3.7-slim-buster as base

FROM base as base_pipenv

RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv lock --requirements > requirements.txt
RUN pipenv lock --dev --requirements > dev_requirements.txt

FROM base as base_python
WORKDIR /app

COPY --from=base_pipenv requirements.txt .
RUN pip install -r requirements.txt

FROM node:13 as yarn_fe_installer
WORKDIR /app
COPY termine-fe/package.json .
COPY termine-fe/yarn.lock .
RUN yarn install --network-timeout 100000

FROM yarn_fe_installer as yarn_fe_builder
COPY termine-fe/.linguirc .
COPY termine-fe/jsconfig.json .
COPY termine-fe/src src/
COPY termine-fe/public public/
RUN yarn run compile-i18n
RUN yarn run format
RUN yarn build
# for debugging
CMD bash

FROM node:13 as yarn_bo_installer
WORKDIR /app
COPY termine-bo/package.json .
COPY termine-bo/yarn.lock .
RUN yarn install --network-timeout 100000

FROM yarn_bo_installer as yarn_bo_builder
COPY termine-bo/src src/
COPY termine-bo/public public/
ENV PUBLIC_URL "/admin"
RUN yarn build
# for debugging
CMD bash

FROM base_python as tester
COPY --from=base_pipenv dev_requirements.txt .
RUN pip install -r dev_requirements.txt
COPY termine-be/ .
ENTRYPOINT ["pytest"]

FROM base_python as base_server
RUN pip install gunicorn

FROM base as deployer
RUN pip install awscli
COPY cloudformation/ cloudformation/
CMD bash

FROM base_python as command
COPY termine-be/ .
ENTRYPOINT ["hug", "-f", "main.py", "-c"]
CMD ["help"]

FROM base_server as server
COPY entrypoint.sh .
COPY wait-for-it.sh .
COPY termine-be/ .
COPY --from=yarn_fe_builder /app/build/ build_fe/
COPY --from=yarn_bo_builder /app/build/ build_bo/
ENV FE_STATICS_DIR "build_fe"
ENV BO_STATICS_DIR "build_bo"
CMD ["./entrypoint.sh"]
