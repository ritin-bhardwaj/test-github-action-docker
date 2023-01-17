FROM python:3.8-slim-buster
ADD main.py .
RUN pip install requests
RUN pip install actions_toolkit
CMD ["python3", "./main.py"]