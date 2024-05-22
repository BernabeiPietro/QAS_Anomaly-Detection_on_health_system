import asyncio
import csv
import logging
import os

#file_list_net = ["collisions","rx_bytes","rx_crc_errors","rx_errors","rx_frame_errors","rx_missed_errors","rx_over_errors","tx_aborted_errors","tx_carrier_errors","tx_dropped","tx_fifo_errors","tx_packets",
#"multicast","rx_compressed","rx_dropped","rx_fifo_errors","rx_length_errors","rx_nohandler","rx_packets","tx_bytes","tx_compressed","tx_errors","tx_heartbeat_errors","tx_window_errors"]



logger = logging.getLogger(__name__)


# Lista di file da leggere
file_list_cpu = ["cpu.stat"]
file_list_memory = ["memory.stat", "memory.swap.current","memory.current"]
file_list_io = ["io.stat"]
file_list_net = ["rx_bytes","tx_packets","multicast","rx_packets","tx_bytes"]

# Intervallo di lettura in secondi
interval = 5


async def collect_process(CID, NET_ID, up_bound_cycle, status, file_operation, output_dir, file_name):

    cgroup_path=f"/sys/fs/cgroup/system.slice/docker-{CID}.scope/"
    net_path=f"/sys/class/net/br-{NET_ID}/statistics/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_list=file_list_cpu+file_list_io+file_list_memory
    # Generare nome file CSV
    csv_filename = os.path.join(output_dir, file_name)
    if(file_operation=='w'):
        csv_column, _ = await read_data_file(cgroup_path, net_path, file_list)
        csv_column.append("status")
        init_csv(csv_filename,csv_column)

    for count in range(up_bound_cycle):
        _ , csv_data = await read_data_file(cgroup_path, net_path, file_list)
        csv_data.append(status)
        # Scrivere i dati nel file CSV
        update_csv(csv_filename, csv_data)

        logging.info(f"Collect data n:{count}")
        # Attendere l'intervallo specificato
        await asyncio.sleep(interval)
    

async def read_data_file(cgroup_path, net_path, file_list):
    csv_column_cgroup, csv_data_cgroup = await collect_data_cgroup(cgroup_path, file_list)
    csv_column_net, csv_data_net= await collect_data_net(net_path, file_list_net)
    csv_column=csv_column_cgroup+csv_column_net
    csv_data=csv_data_cgroup+csv_data_net
    return csv_column,csv_data

def init_csv(csv_filename, csv_column):
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        logging.info("Create CSV file")
        writer.writerow(csv_column)
        logging.info("Generate header column")

def update_csv(csv_filename, csv_data):
    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_data)

async def collect_data_cgroup(cgroup_path, file_list):
    csv_column = []
    csv_data = []
    # Nomi colonne e linea valori
    for filename in file_list:
        with open(f"{cgroup_path}/{filename}", "r") as f:
                    # Leggere i dati
                    data = f.readlines()

                # Creare una lista di valori da scrivere nel CSV
            
                    for line in data:
                        if filename == "memory.swap.current" or filename == "memory.current":
                            csv_column.append(filename)
                            value=line.strip()
                        elif filename =="io.stat":
                            col, val=await split_token(line)
                            csv_column=csv_column+col
                            csv_data=csv_data+val
                            break
                        else:
                    # Estrarre i valori necessari dalla riga
                            column, value = line.strip().split(" ", 1)
                            csv_column.append(column)
                        csv_data.append(value)
    return csv_column,csv_data

async def collect_data_net(net_path, file_list):
    csv_column = []
    csv_data = []
    # Nomi colonne e linea valori
    for filename in file_list:
        with open(f"{net_path}/{filename}", "r") as f:
                    # Leggere i dati
                    data = f.readlines()

                # Creare una lista di valori da scrivere nel CSV        
                    for line in data:
                            csv_column.append(filename)
                            csv_data.append(line.strip())
    return csv_column,csv_data

async def split_token(value):
    tokens = value.strip().split(" ")

    # Creare una lista di nomi e valori
    column = []
    data=[]
    for token in tokens[1:]:
        # Dividere il token in nome e valore
        name, value = token.split("=")
        column.append(name)
        data.append(value)
    return column,data


