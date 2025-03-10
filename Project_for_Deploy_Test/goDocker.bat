:: MIAA-2024-2025
:: by lufer

docker build -t prediction-api .
docker run -d --name miaa-fastapi -p 8000:8000 prediction-api