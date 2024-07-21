from fastapi import FastAPI
from typing import List
from client1 import OPCUA_Client
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
    PLC1 = OPCUA_Client(url)
    tmp = await PLC1.list_var()
    return tmp

@app.get("/read_variable/{variable_name}")
async def read_variable(variable_name: str):
    """
    Read a specific variable by its name.
    """
    PLC1 = OPCUA_Client(url)
    tmp = await PLC1.read_value(str(variable_name))
    if tmp is None :
        return f'No variable {variable_name} found'
    else:
        return tmp.Value.Value 
    
if __name__ == "__main__":
    
    asyncio.run(read_variable('MyVariable'))