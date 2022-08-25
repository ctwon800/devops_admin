FROM python:3.10-buster
COPY . /app/
RUN cd /app && pip install -r requirements.txt
WORKDIR /app
CMD ["python", "manager.py", "runserver", "0.0.0.0:8000"]