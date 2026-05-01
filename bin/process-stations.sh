#!/bin/sh -f
echo "ROOT_DIR=\"${ROOT_DIR}\"" > .env.stations
echo "DEV_KEY=\"${DEV_KEY}\"" >> .env.stations
echo "DEV_SECRET=\"${DEV_SECRET}\"" >> .env.stations
echo "API_KEY=\"${API_KEY}\"" >> .env.stations
echo "ACCOUNT=\"${ACCOUNT}\"" >> .env.stations
echo "BASE_URL=\"${BASE_URL}\"" >> .env.stations

while true; do
    echo "Processing stations..."
     uv run python examples/process_stations.py
    sleep 86400
done
