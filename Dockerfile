FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python seed_db.py

ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=80
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 80

CMD ["flask", "run"]