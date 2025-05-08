FROM python:3.12.6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /backend
WORKDIR /backend

COPY . /backend/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]