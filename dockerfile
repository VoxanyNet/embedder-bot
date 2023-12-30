FROM python:3.10.13-bookworm

WORKDIR /usr/src/app

# make module folder
RUN mkdir embedder_bot

# copy contents of the module to the module folder in container
COPY ./embedder_bot ./embedder_bot

RUN pip install -r ./embedder_bot/requirements.txt

CMD ["python", "-m", "embedder_bot"]
