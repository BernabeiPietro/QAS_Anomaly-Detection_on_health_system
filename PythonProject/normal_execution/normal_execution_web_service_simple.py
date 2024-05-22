import asyncio
import logging
import random
import aiohttp
from aiohttp import client_exceptions
from aiohttp.client_exceptions import InvalidURL


logger = logging.getLogger(__name__)


async def random_navigation(url, task_id, number_of_operation):
      """
         Executes a json web client. 
         Args:
            url (String): Target URL
            task_id (integer): id of the web client
            number_of_operation (integer): number of requests to be executed

         Returns:
            nothing.
      """ 
      while True if number_of_operation == 0 else number_of_operation > 0:
        if number_of_operation>0:  
         number_of_operation -= 1
        await asyncio.sleep(random.randint(1, 10))
        link_indice = random.randint(1,1000)
        url = f"{url}/data_{link_indice}.json"
          
        try:
          async with aiohttp.ClientSession() as session:
              async with session.get(url) as response:
                  await response.read()
                  logger.debug(f"Task N {str(task_id)}: Navigazione verso: ({url})")

        except InvalidURL:
           logger.exception(f"Wrong file {task_id}")
           continue
        except client_exceptions.ClientOSError:
           logger.exception(f"Wrong file {task_id} ClientOSError")
           continue
        except client_exceptions.ServerDisconnectedError:
           logger.exception(f"Wrong file {task_id}")
           continue 



