FROM python:3.10.13-bookworm

WORKDIR /usr/src/app

# make module folder
RUN mkdir ifunnybot

# copy contents of the module to the module folder in container
COPY ./ifunnybot ./ifunnybot

RUN pip install -r ./ifunnybot/requirements.txt

CMD ["python", "-m", "ifunnybot"]
