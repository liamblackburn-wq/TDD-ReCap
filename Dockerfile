FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python seed_db.py

EXPOSE 80

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port==80"]