export DATA_DIR=./local_datastore

# Build Deepchem server image
docker-compose build --no-cache

# Run deepchem server
docker-compose up -d