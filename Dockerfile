FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]