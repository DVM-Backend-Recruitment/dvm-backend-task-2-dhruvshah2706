FROM python:3.12-slim

#  Install dependencies including netcat-openbsd
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    libpq-dev \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

#  Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

#  Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#  Copy entrypoint script
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

#  Copy the rest of the application code
COPY . .

EXPOSE 8000

#  Set entrypoint to script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
