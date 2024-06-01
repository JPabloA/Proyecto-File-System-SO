from enum import Enum

class SectorState(Enum):
    FREE = 0
    OCCUPIED = 1

class Disk:
    __file_name: str = "disk.txt"
    __num_sectors: int = 0
    __sector_size: int = 0
    __pointer_size: int = 4

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
            f.write(f"{i}:00-1:{ '0' * (self.__sector_size - self.__pointer_size) }\n")

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
    def writeToDisk(self, sector_content: str, sector_id: int = -1):

        # If is an existing file (Modification), delete its previous content
        if (sector_id != -1):
            self.removeFromDisk( sector_id )

        data_size = self.__sector_size - self.__pointer_size

        # 0. Divide the content in string chunks of the size of a sector
        content_chunks = [sector_content[i:i + data_size] for i in range(0, len(sector_content), data_size)]

        # 0.1 Fill the last sector with non-use space (Intern Fragmentation)
        content_chunks[-1] = content_chunks[-1].ljust(data_size, "0")

        # 1. Get the sector content size to check if there is space left
        sectors_required  = len(content_chunks)
        sectors_available = list( filter(lambda s: s[1] == SectorState.FREE, self.__free_sectors) )

        if (sectors_required > len(sectors_available)):
            print("Write: Space requested not available")
            return -1
        
        # 2. Get the sectors to be written
        selected_sectors = sectors_available[0:sectors_required]

        # 3. Get the disk as a list
        disk_list = self.__diskContentToList()

        # 4. Update the disk content based on the selected_sectors
        for i in range(0, len(selected_sectors)):
            sector_id = selected_sectors[i][0]
            sector_content = content_chunks[i]
            next_sector_id = selected_sectors[i + 1][0] if (i + 1) < len(selected_sectors) else -1
            next_sector_id = str(next_sector_id).rjust(self.__pointer_size, "0")

            disk_list[ sector_id ] = f"{sector_id}:{next_sector_id}:{sector_content}\n"
            self.__free_sectors[ sector_id ] = (self.__free_sectors[ sector_id ], SectorState.OCCUPIED)

        # 5. Write the new content into disk
        self.__listToDiskContent( disk_list )

        # 6. Return the list of ocuppied sectors
        return selected_sectors[0][0]

    # Read from the virtual disk
    def readFromDisk(self, sector_id: int):
        if sector_id < 0 or sector_id >= self.__num_sectors:
            print("Read: Sector ID out of sector bounds")
            return
        
        disk_list = self.__diskContentToList()
        disk_pointer = sector_id

        content = ""
        while disk_pointer != -1:
            disk_line = disk_list[disk_pointer].split(":")
            content += disk_line[2].strip("\n")

            disk_pointer = -1 if disk_line[1] == "00-1" else int(disk_line[1])

        content = content.rstrip("0")
        print(content)
        return content

    # Remove from the virtual disk
    def removeFromDisk(self, sector_id: int):
        # 0. Get the disk as a list
        disk_list = self.__diskContentToList()
        disk_pointer = sector_id

        # 1. Write the data from the sectors list
        while disk_pointer != -1:
            disk_line = disk_list[disk_pointer].split(":")

            disk_list[disk_pointer] = f"{disk_pointer}:00-1:{ '0' * (self.__sector_size - self.__pointer_size) }\n"
            self.__free_sectors[ disk_pointer ] = (disk_pointer, SectorState.FREE)

            disk_pointer = -1 if disk_line[1] == "00-1" else int(disk_line[1])

        # 2. Write the clear content into disk
        self.__listToDiskContent( disk_list )