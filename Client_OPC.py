
import asyncio

from asyncua import Client

# url = "opc.tcp://172.16.12.1:4840/"
url = "opc.tcp://127.0.0.1:4840/"

namespace = "http://opcfoundation.org/UA/"

async def main():

    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")

        await client.connect()

        tmp = await client.nodes.root.get_children()
        print(10*'-')
        for t in tmp:
            name = await t.read_browse_name()
            print(name.Name)
        print(10*'-')
        obj_node = tmp[0]
        tmp1 = await obj_node.get_children()

        print(20*'-')
        for t in tmp1:
            name = await t.read_browse_name()
            print(name.Name)
        print(20*'-')

        epac_node = tmp1[2]
        tmp2 = await epac_node.get_children()

        print(30*'-')
        for t in tmp2:
            name = await t.read_browse_name()
            print(name.Name)
        print(30*'-')

        print('---')
        for t in tmp2:
            name = await t.read_browse_name()
            print(name.Name)
        print('---')

        tmp3 = await tmp2[0].read_value()

        print(f'value : {tmp3}')
        #await tmp2[0].write_value(34)

        print('end......')
        await client.disconnect()
        
if __name__ == "__main__":
        asyncio.run(main())
