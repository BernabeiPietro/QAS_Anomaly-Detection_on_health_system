# QAS_Anomaly-Detection_on_health_system
## Third-party tools needed
- NGROK
- Conda
## Setup Enviroment
### Setup Python Enviroment
```
conda env create
conda activate qas
```
### Setup Container Enviroment
```
ngrok tcp 9080
```
Copy the ngrok public ip and port into the malware.sh file at ./web-service-only-json/malware/ to substitue the "NGROK IP" and "NGROK PORT" placeholder.
```
docker compose build
docker compose up -d
```
Ngrok program can be replaced, safely by first running the docker compose procedure and then changing the contents of the malware.sh file through docker exec with the ip of the docker host machine.
### Setup issue manager program
#### Mandatory
```
docker ps --no-trunc
```
copy the containter id (of the target container) into the main.py file at ./PythonProject at the variable CID
```
docker network ls
```
copy the net id of the qas_anomaly-detection_on_health_system_default  into the main.py file at ./PythonProject at the variable NET_ID
#### Optional
Inside the main.py file there are some variable that modify the behaviour of the program:
- number_of_operation: if ==0 than the web clients operates until they are killed, if >0, they executes the quantity specified. Default: 0
- http_client: number of clients executed in parallel to emulate normal behavior. Default: 500
- csv_dir: output folder of csv file (raw and refined). Default: "./output_csv"
- up_bound_cycle: number of data point to collect for each issue. Default: 100
- number_of_simulation: Number of runs of each group of simulations. Default: 10

## Execute the issue simulation program
```
cd PythonProject
python3 main.py
```

