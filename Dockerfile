FROM python:3.8-slim-buster
RUN pip install --upgrade pip
ADD runAutomation.py .
RUN pip install requests
RUN pip install actions_toolkit
CMD ["python3", "./runAutomation.py"]