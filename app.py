from fastapi import FastAPI
from typing import List
from OPC_client import OPCClient_UA
import asyncio

app = FastAPI()

url = "opc.tcp://localhost:4840/freeopcua/server/"
namespace = "http://examples.freeopcua.github.io"

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/list_variables")
async def list_variables():
    """
    List all variables.
    """
    print('a')
    PLC1 = OPCClient_UA(url, namespace)
    print('b')
    await PLC1.connect()
    print('c')
    tmp = await PLC1.get_ListVar()
    print('d', tmp)
    await PLC1.disconnect()
    return tmp

@app.get("/read_variable/{variable_name}")
async def read_variable(variable_name: str):
    """
    Read a specific variable by its name.
    """
    PLC1 = OPCClient_UA(url, namespace)
    await PLC1.connect()
    tmp = await PLC1.read_value(variable_name)
    await PLC1.disconnect()
    if tmp is None :
        return f'No variable {variable_name} found'
    else:
        return tmp 
    
if __name__ == "__main__":
    
    asyncio.run(read_variable('MyVariable'))