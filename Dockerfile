FROM python:3.9-alpine


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk --update add
RUN apk add gcc libc-dev libffi-dev

RUN pip install --upgrade pip
RUN pip install "poetry==1.1.11"

WORKDIR /app
COPY poetry.lock pyproject.toml /

RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /app

ENTRYPOINT ["python", "./mini_task/main.py"]