from enum import Enum

class SectorState(Enum):
    FREE = 0
    OCCUPIED = 1

class Disk:
    __file_name: str = "disk.txt"
    __num_sectors: int = 0
    __sector_size: int = 0

    # TODO: La lista de sectores libres se maneja en disco?
    __free_sectors: list = []

    # Constructor: Set the num_sectors
    def __init__(self, num_sectors: int, sector_size: int):
        self.__num_sectors = num_sectors
        self.__sector_size = sector_size
        self.__free_sectors = [(i, SectorState.FREE) for i in range(0, num_sectors)]

    # Private: Create disk file
    def __createFile(self):
        f = open(self.__file_name, "w")

        # TODO: Fill disk file with default structure
        for i in range(0, self.__num_sectors):
            f.write(f"{i}: { '0' * self.__sector_size }\n")

        f.close()

    # Private: Transform disk to list
    def __diskContentToList(self):
        with open(self.__file_name, "r") as file:
            lines = file.readlines()
        return lines

    # Private: Transform disk list to disk.txt
    def __listToDiskContent(self, lines: list):
        with open(self.__file_name, "w") as file:
            file.writelines(lines)

    # Create the virtual disk file
    def createDisk(self):
        print("Creating virtual disk...")
        self.__createFile()
        print("Virtual disk created!")

    # Write into the virtual disk
    def writeToDisk(self, sector_content: str):
        # 0. Divide the content in string chunks of the size of a sector
        content_chunks = [sector_content[i:i+self.__sector_size] for i in range(0, len(sector_content), self.__sector_size)]

        # 0.1 Fill the last sector with non-use space (Intern Fragmentation)
        content_chunks[-1] = content_chunks[-1].ljust(self.__sector_size, "0")

        # 1. Get the sector content size to check if there is space left
        sectors_required  = len(content_chunks)
        sectors_available = list( filter(lambda s: s[1] == SectorState.FREE, self.__free_sectors) )

        if (sectors_required > len(sectors_available)):
            print("Write: Space requested not available")
            return
        
        # 2. Get the sectors to be written
        selected_sectors = sectors_available[0:sectors_required]

        # 3. Get the disk as a list
        disk_list = self.__diskContentToList()

        # 4. Update the disk content based on the selected_sectors
        for sector, sector_content in zip(selected_sectors, content_chunks):
            disk_list[ sector[0] ] = f"{sector[0]}: {sector_content}\n"
            self.__free_sectors[ sector[0] ] = (self.__free_sectors[ sector[0] ], SectorState.OCCUPIED)

        # 5. Write the new content into disk
        self.__listToDiskContent( disk_list )

    # Read from the virtual disk
    def readFromDisk(self, sector_id: int):
        if sector_id < 0 or sector_id >= self.__num_sectors:
            print("Read: Sector ID out of sector bounds")
            return
        
        disk_list = self.__diskContentToList()
        return disk_list[ sector_id ]

    # Remove from the virtual disk
    def removeFromDisk(self, sectors_ids: list[int]):
        # 0. Get the disk as a list
        disk_list = self.__diskContentToList()

        # 1. Write the data from the sectors list
        for sector_id in sectors_ids:
            disk_list[ sector_id ] = f"{sector_id}: {'0' * self.__sector_size}\n"
            self.__free_sectors[ sector_id ] = (sector_id, SectorState.FREE)

        # 2. Write the clear content into disk
        self.__listToDiskContent( disk_list )