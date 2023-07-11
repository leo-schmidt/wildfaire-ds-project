FROM python:3.10.6-buster

WORKDIR /app

# First, pip install dependencies to avoid reinstalling packages at every rebuild
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Then install wildfaire package
COPY wildfaire wildfaire
COPY wildfaire-390716-f2d2375165e9.json wildfaire-390716-f2d2375165e9.json
COPY setup.py setup.py
COPY Makefile Makefile
RUN pip install .

CMD  uvicorn wildfaire.api.fast:app --host 0.0.0.0 --port 8080
