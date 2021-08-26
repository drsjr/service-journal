FROM python:3.7

EXPOSE 8000

COPY . /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]