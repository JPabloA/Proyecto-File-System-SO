from enum import Enum
from tkinter import messagebox

class SectorState(Enum):
    FREE = 0
    OCCUPIED = 1

class Disk:
    __file_name: str = "./src/disk.txt"
    __num_sectors: int = 0
    __sector_size: int = 0
    __free_sectors: list = []

    # Constructor: Set the num_sectors
    def __init__(self, num_sectors: int, sector_size: int):
        self.__num_sectors = num_sectors
        self.__sector_size = sector_size
        self.__free_sectors = [(i, SectorState.FREE) for i in range(0, num_sectors)]

    # Private: Create disk file
    def __createFile(self):
        f = open(self.__file_name, "w")

        for i in range(0, self.__num_sectors):
            f.write(f"{i}:{ '0' * self.__sector_size }\n")

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

    # Private: Divide the content in string chunks of the size of a sector
    def __splitContentInChunks(self, content):
        content_chunks: list[str] = [content[i:i + self.__sector_size] for i in range(0, len(content), self.__sector_size)]

        if len(content_chunks) > 0:
            # To remove line jump
            content_chunks[-1] = content_chunks[-1]

            # Fill the last sector with non-use space (Intern Fragmentation)
            content_chunks[-1] = content_chunks[-1].ljust(self.__sector_size, "0")

        return content_chunks

    # Create the virtual disk file
    def createDisk(self):
        print("Creating virtual disk...")
        self.__createFile()
        print("Virtual disk created!")

    # Write into the virtual disk
    def writeToDisk(self, sector_content: str, sectors_list: list[int] = []):
        
        # validation (test)
        if sector_content == "" and len(sectors_list) > 0:
            self.removeFromDisk(sectors_list)
            return -1
        
        # Quick fix
        #sector_content = sector_content if len( sector_content ) > 0 else "\0"
        sector_content = sector_content.encode("utf-8").hex()

        # 0. Split content in chunks of the size of the sector
        content_chunks = self.__splitContentInChunks( sector_content )

        # 1. Get the disk as a list
        disk_list = self.__diskContentToList()

        # 2. Get the list of available sectors
        sectors_available = list( filter(lambda s: s[1] == SectorState.FREE, self.__free_sectors) )

        occupied_sectors = []

        # Case: Creating an non-existing file
        if len(sectors_list) == 0:
            # 3. Get the count of sectors required to check if there is space left
            sectors_required  = len(content_chunks)

            if (sectors_required > len(sectors_available)):
                messagebox.showwarning("Espacio insuficiente en disco", "No hay suficiente espacio en disco para almacenar el archivo")
                return []

            # 4. Get the sectors to be written
            selected_sectors = sectors_available[0:sectors_required]

            # 5. Update the disk content based on the selected_sectors
            for i in range(0, len(selected_sectors)):
                sector_id = selected_sectors[i][0]
                sector_content = content_chunks[i]

                occupied_sectors.append( sector_id )

                disk_list[ sector_id ] = f"{sector_id}:{sector_content}\n"
                self.__free_sectors[ sector_id ] = (sector_id, SectorState.OCCUPIED)

        # Case: Modifying an existing file
        else:
            # 3. Check if the modification requieres more space
            sectors_required = len(content_chunks) - len(sectors_list)

            if (sectors_required > 0 and sectors_required > len(sectors_available)):
                messagebox.showwarning("Espacio insuficiente en disco", "No hay suficiente espacio en disco para almacenar el archivo")
                return []

            # 4. Get the sectors to be written
            selected_sectors = sectors_available[0:sectors_required]

            # 5: Modify the existing data
            for index, sector_id in enumerate(sectors_list):
                if index < len(content_chunks):
                    sector_content = content_chunks[index]
                    disk_list[sector_id] = f"{sector_id}:{sector_content}\n"
                else:
                    break

            occupied_sectors = sectors_list[0:len(content_chunks)]

            # Case 1: The file is equal or bigger in size (Requiered 0 or more sectors)
            if sectors_required >= 0:
                # Second: Add the left data
                selected_sectors_index = 0
                for i in range(len( sectors_list ), len( content_chunks )):
                    sector_id = selected_sectors[ selected_sectors_index ][0]
                    sector_content = content_chunks[i]

                    selected_sectors_index += 1
                    occupied_sectors.append( sector_id )

                    disk_list[ sector_id ] = f"{sector_id}:{sector_content}\n"
                    self.__free_sectors[ sector_id ] = (sector_id, SectorState.OCCUPIED)

            # Case 2: The file is smaller in size (Requiered free sectors)
            else:
                # First. Write the modified data
                self.__listToDiskContent( disk_list )
                # Second: Remove the usused occupied space
                self.removeFromDisk( sectors_list[ len( content_chunks ): ] )
                return occupied_sectors


        # 5. Write the new content into disk
        self.__listToDiskContent( disk_list )

        # 6. Return the list of ocuppied sectors
        return occupied_sectors

    # Read from the virtual disk
    def readFromDisk(self, sectors_list: list[int]):

        disk_list = self.__diskContentToList()

        content = ""
        for sector_id in sectors_list:
            if sector_id < 0 or sector_id >= self.__num_sectors:
                continue

            disk_line = disk_list[ sector_id ].split(":")
            content += disk_line[1].strip("\n")

        content = bytes.fromhex( content ).decode("utf-8")
        content = content.rstrip("0")
        return content

    # Remove from the virtual disk
    def removeFromDisk(self, sectors_list: list[int]):
        # 0. Get the disk as a list
        disk_list = self.__diskContentToList()

        # 1. Write the data from the sectors list
        for sector_id in sectors_list:
            if sector_id < 0 or sector_id >= self.__num_sectors:
                continue

            disk_list[ sector_id ] = f"{sector_id}:{'0' * self.__sector_size}\n"
            self.__free_sectors[ sector_id ] = (sector_id, SectorState.FREE)

        # 2. Write the clear content into disk
        self.__listToDiskContent( disk_list )

    def getDiskUsedPercentage(self):
        sectors_available = list( filter(lambda s: s[1] == SectorState.FREE, self.__free_sectors) )
        x = self.__num_sectors * len( sectors_available )
        value = ((1 - (1 / self.__num_sectors) * len( sectors_available )) * 100) if x > 0 else 99.9
        return value