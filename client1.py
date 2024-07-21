import asyncio

from asyncua import Client
from asyncua.common.node import Node
from asyncua.ua.uatypes import Variant
import json


#url = "opc.tcp://127.0.0.1:4840/"

url = "opc.tcp://172.16.12.1:4840/"

class OPCUA_Client():
    def __init__(self, url):
        self.url = url
        self.connected = False
        self.namespace = "http://opcfoundation.org/UA/"
        self.client = None
        self.Root = None
        self.DB = []
        self.dict_node = {}

    async def __get_list_nodes(self, node:Node):
        """
        retourne la liste des nodes

        """
        list_node_folder = []
        for element in node:
            list_node_folder.append(element)
        return list_node_folder

    async def __is_node_folder(self, node:Node):
        """
        retourne True si liste de Node
        """
        return len(await node.get_children())>1
    
    async def __read_value(self, node:Node)->Variant:
        return await node.read_data_value()
    
    async def __browse_nodes(self, node_parent:Node, level:int):
        nom = str(node_parent)
        if isinstance(node_parent, list):
            tmp = await(node_parent[0].get_parent())
            nom = (await tmp.read_browse_name()).Name
            nodes = node_parent
        else:
            nodes = await node_parent.get_children()
            nom = (await node_parent.read_browse_name()).Name
        structure = {}
        structure['nom'] = nom
        structure['contenu'] = []

        struct_node = {}
        struct_node['nom'] = nom
        struct_node['node'] = []

        for node in nodes:
            if not(await node.read_browse_name()).Name.startswith('#') and not(await node.read_browse_name()).Name.startswith('BMEP58_'):
                # print((await node.read_browse_name()).Name, ' :' ,await node.read_data_value())
                # print((await node.read_data_value()).Value.is_array)
                is_array = (await self.__read_value(node)).Value.is_array

                if await self.__is_node_folder(node) and not is_array:
                    
                    list_tmp = await node.get_children()
                    (st1, st2) = await self.__browse_nodes(list_tmp, (level+1))
                    structure['contenu'].append(st1)
                    struct_node['node'].append(st2)
                else:
                    struct_elem = {}
                    struct_elem['nom'] = (await node.read_browse_name()).Name

                    tmp_struct_node = {}
                    tmp_struct_node['nom'] = (await node.read_browse_name()).Name
                    try:
                        node_type = await node.read_node_class()
                    except:
                        node_type = -1

                    if node_type==2 :
                        struct_elem['nodeId'] = str(node)
                        struct_elem['isArray'] = str(is_array)
                        struct_elem['node_Description'] = str(await node.read_data_type())
                        struct_elem['node_VariantType'] = str(await node.read_data_type_as_variant_type())
                        struct_elem['node_path'] = str(await node.get_path(max_length=20, as_string=True))

                        tmp_struct_node['node'] = node

                    structure['contenu'].append(struct_elem)
                    struct_node['node'].append(tmp_struct_node)
        return (structure, struct_node )
    
    async def list_var(self)->dict:
        async with Client(url=url) as client:
            
            #await client.connect()
                               
            tmp = await client.nodes.root.get_children()
            
            obj_node = tmp[0]

            tmp1 = await obj_node.get_children()
            _idx = None
            for i, t in enumerate(tmp1):
                _name = str((await t.read_browse_name()).Name)
                if 'epac' in _name.lower():
                    _idx = i
                #print(i,'  ',await t.read_browse_name())
            if _idx is None:
                return
            else:
                epac_node = tmp1[_idx]

            structs = await self.__browse_nodes(epac_node, 0)
            # print(50*'@')
            # print(structs[1])
            self.dict_node = structs[1]
            return structs[0]
        
    def pull_node_from_dict(self, name:str):
        for element in self.dict_node['node']:
            if element['nom'] == name:
                return element['node']
        return None

        
    async def read_value(self, name:str)->Variant:
        await self.list_var()

        #noms = [element['nom'] for element in self.dict_node['node']]
        
        node_var = self.pull_node_from_dict(name)
        async with Client(url=url) as client:
            try:
                tmp = await client.get_node(node_var).read_data_value()
                return tmp
            
            except:
                return None
            
    
async def main2():
    cl = OPCUA_Client(url)
    
    await cl.list_var()

    await cl.read_value('a')

    with open('structure_nodes.json', 'w') as fichier_json:
             json.dump(await cl.list_var(), fichier_json, indent=4)  

async def main():

    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")
                         
        await client.connect()
                               
        tmp = await client.nodes.root.get_children()


        # print(20*'*')

        # list_nodes = await get_list_nodes(tmp)
        # for node in list_nodes:
        #     print(await node.read_browse_name())
        #     print(await is_node_folder(node))
        #     # if not(await is_node_folder(node)):
        #     #     print(await node.read_data_type_as_variant_type())

        # print(20*'*')


        obj_node = tmp[0]
        print(type(obj_node))
        print((await obj_node.read_browse_name()).Name)
        tmp1 = await obj_node.get_children()
        print(50*'!')

        # print(type(tmp1[0]))
        # print(await tmp1[0].read_node_class()) 
        epac_node = tmp1[2]
        tmp2 = await epac_node.get_children()
        #######################################################################
        struct = await browse_nodes(obj_node, 0)
        # print(struct)
        with open('structure_nodes.json', 'w') as fichier_json:
             json.dump(struct, fichier_json, indent=4)  

        return
        print('---')              
        for t in tmp2:                                    
            name = await t.read_browse_name()              
            print(name.Name)
        print('---')          

        tmp3 = await tmp2[0].read_value()
        print(await tmp2[0].read_data_type_as_variant_type()) 
        print(50*'!')
        print((tmp2[0])) # type = Node
        print(await tmp2[0].read_node_class()) 
        print((await tmp2[0].read_data_type()))  # type NodeId
        print(await tmp2[0].read_data_type_as_variant_type())    # type VariantType
                         
        print(f'value : {tmp3}')

        tmp4 = await tmp2[0].get_children()
        print(type(obj_node))
                           
        #await tmp2[0].write_value(34)        

        print('end......')
        await client.disconnect()

        
                                             
if __name__ == "__main__":  
    asyncio.run(main2())