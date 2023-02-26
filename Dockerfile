FROM python:3.9
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY ./src /app/src
CMD ["uvicorn", "src.main:app","--host", "0.0.0.0", "--port", "86"]