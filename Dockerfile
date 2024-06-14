FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "wsgi:app"]
RUN mkdir -p /data
VOLUME /data
RUN ln -s /data /app/data
EXPOSE 8000
ENV PORT=8000