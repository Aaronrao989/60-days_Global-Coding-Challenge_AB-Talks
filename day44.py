import math
BLOCK_SIZE = 5   
REPLICATION_FACTOR = 2
class NameNode:
    def __init__(self):
        self.metadata = {}  
    def add_file(self, file_name, blocks_info):
        self.metadata[file_name] = blocks_info
    def get_file_blocks(self, file_name):
        return self.metadata.get(file_name, None)
    def display_metadata(self):
        print("\n NameNode Metadata:")
        for file, blocks in self.metadata.items():
            print(f"\nFile: {file}")
            for i, (block, nodes) in enumerate(blocks):
                print(f"  Block {i}: '{block}' stored in {nodes}")
class DataNode:
    def __init__(self, name):
        self.name = name
        self.storage = []
    def store_block(self, block):
        self.storage.append(block)
    def get_blocks(self):
        return self.storage
class HDFS:
    def __init__(self):
        self.namenode = NameNode()
        self.datanodes = [
            DataNode("Node1"),
            DataNode("Node2"),
            DataNode("Node3")
        ]
    def split_file(self, data):
        return [data[i:i + BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]
    def store_file(self, file_name, data):
        print("\n Uploading file to HDFS...")
        blocks = self.split_file(data)
        blocks_info = []
        for i, block in enumerate(blocks):
            assigned_nodes = []
            for j in range(REPLICATION_FACTOR):
                node = self.datanodes[(i + j) % len(self.datanodes)]
                node.store_block(block)
                assigned_nodes.append(node.name)
            blocks_info.append((block, assigned_nodes))
        self.namenode.add_file(file_name, blocks_info)
        print(" File stored successfully with replication!")
    def read_file(self, file_name):
        print("\n Reading file from HDFS...")
        blocks_info = self.namenode.get_file_blocks(file_name)
        if not blocks_info:
            print("File not found!")
            return
        data = ""
        for block, nodes in blocks_info:
            data += block
        print(f"\n File Content: {data}")
    def show_datanodes(self):
        print("\n DataNode Storage:")
        for node in self.datanodes:
            print(f"{node.name}: {node.get_blocks()}")
def main():
    print("\n" + "="*70)
    print("MINI HDFS SIMULATOR")
    print("="*70)
    hdfs = HDFS()
    file_name = "sample.txt"
    data = "Big data systems require distributed storage like HDFS"
    hdfs.store_file(file_name, data)
    hdfs.namenode.display_metadata()
    hdfs.show_datanodes()
    hdfs.read_file(file_name)
if __name__ == "__main__":
    main()