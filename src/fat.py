
class FAT:
    Table: list[ tuple[ int, int ] ]

    def __init__(self):
        self.Table = []

    def printFAT(self):
        for entry in self.Table:
            print(f"Sector ID: {entry[0]}\tNext FAT index: {entry[1]} ")

    def createTable(self, sector_count):
        self.Table = [(-1, -1) for i in range(0, sector_count)]

    def assingSectorList(self, sector_list: list[int]):
        first_table_entry = -1
        prev_table_index = 0
        table_index = 0
        sector_index = 0

        table_entries_available = list(filter( lambda entry: entry[0] == -1, self.Table ))

        if len(sector_list) > len(table_entries_available):
            print("FAT: Space not available in the file allocation table")
            return -1

        # Get the first available FAT entry
        for index, entry in enumerate(self.Table):
            if entry[0] == -1:
                first_table_entry = index
                break

        if first_table_entry == -1:
            print("FAT ERROR: This is not supposed to happen -> Not allocating anything")
            return

        table_index = first_table_entry

        # Save the sector pointers in the FAT
        while sector_index < len( sector_list ):
            table_entry = self.Table[ table_index ]

            # If that table entry has not been assigned
            if table_entry[0] == -1:
                self.Table[ table_index ] = (sector_list[ sector_index ], -1)

                if sector_index != 0:
                    self.Table[ prev_table_index ] = ( self.Table[ prev_table_index ][0], table_index )

                prev_table_index = table_index
                sector_index += 1
            table_index += 1

        # Return the first table index
        return first_table_entry

