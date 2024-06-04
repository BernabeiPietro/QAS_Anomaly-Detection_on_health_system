
import asyncio
from itertools import permutations
import logging
import logging.config
import random
import sys
import time

from collect_metrics.refactoring_csv import calculate_deltas, refactor
from normal_execution.normal_execution_web_service_simple import random_navigation
from attack.attack import integrity_attack, malware_attack_client, malware_attack_client_kill, malware_attack_server, malware_integrity_attack_kill
from collect_metrics.collect import collect_process
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

URL= "http://localhost:80"
#if number_of_operation == 0, the web clients operates until they are killed, 
#if number_of_operation > 0, the web clients executes a number_of_operation operations.
number_of_operation=0
# normal behaviour: quantity of web clients
thread=500

#Container id to identify the right CGroup.
CID="cbba32564ebb69a885a84a1471c90db03fcfefa4c73aa147f98ee69cceded38c" #CHANGE ME
#To identify docker network bridge id: docker network ls and copy the associate NETWORK ID of "qas_anomaly-detection_on_health_system_default"
NET_ID="51633e7d9442" #CHANGE ME
# output folder of csv file (raw and refined)
csv_dir = "./output_csv"
#number of data point to collect for each issue
up_bound_cycle=100

number_of_simulation=10

async def main():
  function_list=[normal_behaviour,malware_behaviour,DOS_behaviour,integrity_behaviour]
  logging.basicConfig(filename='myapp.log', level=logging.INFO)  

  file_operation=['w','a']
  perm = permutations([0, 1, 2, 3]) 
  perm=list(perm)
  for i in range(0,number_of_simulation):
    time_name=time.strftime("%Y%m%d-%H%M%S")
    raw_name="raw_"+time_name+".csv"
    ref_name_csv="refined_"+time_name+".csv"
    ref_name_xls="refined_"+time_name+".xls"
    tasks_execution = [ asyncio.create_task(random_navigation(URL, i, number_of_operation)) for i in range(thread) ]
    random_exe_index=random.randint(0,23)
    file_op_index=0
    for phase in perm[random_exe_index]:
      await function_list[phase](raw_name, file_operation[file_op_index])
      file_op_index=1
    for task in tasks_execution:
        task.cancel()
    await refactor(f'{csv_dir}/{raw_name}', f'{csv_dir}/{ref_name_csv}',f'{csv_dir}/{ref_name_xls}')


async def integrity_behaviour(raw_name, file_operation):
    """
    This function starts the collect_process to measure the integrity behaviour statistic and it enables on the target container the integrity issue activity .

    Args:
        raw_name (string): name of the csv file where it is stored the raw data
        file_operation (string): how the collect process has to operate [a,w]

    Returns:
        nothing.
    """ 
    logging.info("Start phase 3 - integrity attack behaviour")
    task_collect = asyncio.create_task(collect_process(CID,NET_ID, up_bound_cycle, 3, file_operation, csv_dir,raw_name))
    val= await integrity_attack() 
    while not task_collect.done():
      if val.returncode!=None:
        logging.info(" ")
        logging.info(" ")
        logging.info(" ")
        logging.info("start a new integrity attack")
        val= await integrity_attack()
      await asyncio.sleep(int(5))
    await asyncio.gather(task_collect)
    await asyncio.gather(malware_integrity_attack_kill())
    await asyncio.sleep(5)

async def DOS_behaviour(raw_name, file_operation):
    """
    This function starts the collect_process to measure the DoS behaviour statistic and it spawn an addictional quantity of web clients, with the aim to simulate a DoS activity.

    Args:
        raw_name (string): name of the csv file where it is stored the raw data
        file_operation (string): how the collect process has to operate [a,w]

    Returns:
        nothing.
    """ 
    logging.info("Start phase 2 - DOS attack behaviour")
    task_dos=[ asyncio.create_task(random_navigation(URL, i, number_of_operation)) for i in range(600) ]
    task_collect = asyncio.create_task(collect_process(CID,NET_ID, up_bound_cycle, 2, file_operation, csv_dir,raw_name))
    await asyncio.gather(task_collect)
    for task in task_dos:
      task.cancel()
    await asyncio.sleep(5)

async def malware_behaviour(raw_name, file_operation):
    """
    This function starts the collect_process to measure the malware behaviour statistic and it starts the malware client and server.

    Args:
        raw_name (string): name of the csv file where it is stored the raw data
        file_operation (string): how the collect process has to operate [a,w]

    Returns:
        nothing.
    """ 
    logging.info("Start phase 1 - malware attack behaviour")
    task_collect = asyncio.create_task(collect_process(CID,NET_ID, up_bound_cycle, 1, file_operation, csv_dir,raw_name))
    server=await malware_attack_server()
    await malware_attack_client()
    await asyncio.gather(task_collect)
    await asyncio.gather(malware_attack_client_kill())
    server.kill()
    await asyncio.sleep(5)

async def normal_behaviour(raw_name, file_operation):
    """
    This function starts the collect_process to measure the normal behaviour statistic.

    Args:
        raw_name (string): name of the csv file where it is stored the raw data
        file_operation (string): how the collect process has to operate [a,w]

    Returns:
        nothing.
    """  
    logging.info("Start phase 0 - normal behaviour")
    task_collect = asyncio.create_task(collect_process(CID,NET_ID, up_bound_cycle, 0, file_operation, csv_dir,raw_name))
    await asyncio.gather(task_collect)
    await asyncio.sleep(5)

asyncio.run(main()) 
