FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
ENV PYTHONPATH="/app:${PYTHONPATH}"

RUN apt-get update \
    && apt-get install -y build-essential python3-dev \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade pydantic
RUN pip install --no-cache-dir --upgrade fastapi
RUN pip install --no-cache-dir --upgrade pydantic_settings sqlalchemy
COPY . /app/

EXPOSE 8000

CMD ["uvicorn","server:app","--host","0.0.0.0","--port","8000"]
