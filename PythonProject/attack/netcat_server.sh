#!/bin/bash


# Avvia netcat in ascolto sulla porta specificata
while true; do
  nc -v -l 9080| tar -x
done



