FROM python:3.11-alpine
WORKDIR /app
COPY . /app/
RUN pip install flask
RUN pip install dotenv
CMD ["python3", "/app/main.py"]