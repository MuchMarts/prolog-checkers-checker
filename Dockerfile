FROM python:3.11-slim

# Install SWI-Prolog
RUN apt-get update && apt-get install -y swi-prolog

# Install pyswip
RUN pip install pyswip

WORKDIR /app
COPY . .

CMD ["python", "main.py"]