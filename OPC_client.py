
import time
import asyncio

from asyncua import Client

#url = "opc.tcp://172.16.12.1:4840/"
#url = "opc.tcp://localhost:4840/freeopcua/server/"
url = "opc.tcp://mx80_ua:4840"

namespace = "http://examples.freeopcua.github.io"

class OPCClient_UA():
    def __init__(self, url, namespace):
        self.url = url
        self.connected = False
        self.namespace = namespace
        self.client = None
        self.Root = None
        self.DB = []

    async def connect(self):
        self.client = Client(self.url)
        await self.client.connect()
        await self.__list_var()
        self.connected = True


    async def disconnect(self):
        await self.client.disconnect()
        self.connected = False
                
    async def __process_nodes(self):
        tmp = await self.client.nodes.root.get_children()
        for child in tmp:
            browse_name = await child.read_browse_name()
            #print('nodes : ',browse_name.Name)
            if 'Objects' in browse_name.Name:
                await self.__process_objects(child)

    async def __process_objects(self, node):
        children = await node.get_children()
        for child in children:
            browse_name = await child.read_browse_name()
            #print('     objects : ',browse_name.Name)
            if 'ePAC' in browse_name.Name:
                #await self.process_epac(child)
                self.Root = child
            
    async def __process_epac(self, node):
        children = await node.get_children()
        for child in children:
            browse_name = await child.read_browse_name()
            val = await child.read_value()
            #print(f'            {browse_name.Name} :  {val} ')
            self.DB.append({browse_name.Name: child})
    
    async def get_ListVar(self):
        if self.connected == False :
            return None
        items = []
        for item in self.DB:
            items.append(list(item.keys())[0])
        return items
    
    async def read_value(self, name):
        resp = None
        if self.connected == False :
            return None
        for item in self.DB:
            if name in item:
                resp = await item[name].read_value()
        await self.disconnect()
        print(resp)
        return resp

    async def __list_var(self):
        nsidx = await self.client.get_namespace_index(self.namespace)
        #print(f"Namespace Index for '{self.namespace}': {nsidx}")
        tmp = await self.client.nodes.root.get_children()
        await self.__process_nodes()
        await self.__process_epac(self.Root)
        

async def main():
    opc_client = OPCClient_UA(url, namespace)
    await opc_client.connect()
    print(await opc_client.get_ListVar())
    #print(await opc_client.read_value('MyVariable'))
    await opc_client.disconnect()
    print('done')


if __name__ == "__main__":
    asyncio.run(main())
    
