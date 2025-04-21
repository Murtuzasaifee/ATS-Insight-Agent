from pymilvus import connections, utility

class Utility:
    
    def __init__(self):
        pass
    
    def drop_milvus_collection(self, connection, collection_name):
        connections.connect(
            alias="default",
            host="127.0.0.1",
            port="19530"
        )
         
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            print(f"Dropped Milvus collection: {collection_name}")
        else:
            print(f"No collection named '{collection_name}' found.")
    
    