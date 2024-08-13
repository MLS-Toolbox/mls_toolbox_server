FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

ENV MLS_CODE_GENERATOR_URI="mls_code_generator"
ENV MLS_CODE_GENERATOR_PORT="5050"

ENTRYPOINT ["python3"]
CMD ["server.py"]