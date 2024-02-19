import requests
import cbor
import time
from utils.response import Response

def download(url, config, logger=None):
    host, port = config.cache_server
    #check header of resp it find out if it's valid
    resp = requests.get(
        f"http://{host}:{port}/",
        params=[("q", f"{url}"), ("u", f"{config.user_agent}")])
    try:
        if resp and resp.content:
            x =  Response(cbor.loads(resp.content))
 
            return x
    except (EOFError, ValueError) as e:
        pass
    print(resp)
    logger.error(f"Spacetime Response error {resp} with url {url}.")
    return Response({
        "error": f"Spacetime Response error {resp} with url {url}.",
        "status": resp.status_code,
        "url": url})
