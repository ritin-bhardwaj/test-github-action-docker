FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip install --target=/app requests
RUN pip install --target=/app json
CMD python3 main.py