FROM python:3.10-alpine

# install dependencies
RUN apk add build-base && \
    python -m pip install --upgrade pip

EXPOSE 5000
WORKDIR /app
ENV SQLALCHEMY_DATABASE_URI="sqlite:///data.db"

COPY requirements.txt .

# install requirements
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

ENTRYPOINT python -u app.py