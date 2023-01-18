FROM python:3.8-slim-buster

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install actions_toolkit

# Run the application:
ADD runAutomation.py .
CMD ["python3", "./runAutomation.py"]