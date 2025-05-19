FROM python:3.10-slim

WORKDIR /deepchem_server

# Copy requirements file and install dependencies
COPY deepchem_server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY deepchem_server/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
