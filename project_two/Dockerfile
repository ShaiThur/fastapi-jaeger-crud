FROM python:3.12

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

COPY project_two/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY project_two /project_two
WORKDIR /project_two

CMD ["python", "main.py"]