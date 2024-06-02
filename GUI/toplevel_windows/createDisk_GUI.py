import sys
import os
from tkinter import Canvas, Entry, Button, Toplevel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import FileSystem

class CreateDisk_GUI(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Display directory tree")
        self.geometry("750x267")
        self.configure(bg = "#FFFFFF")

        canvas = Canvas( self, bg = "#FFFFFF", height = 267, width = 750, bd = 0, highlightthickness = 0, relief = "ridge" )

        canvas.place(x = 0, y = 0)
        canvas.create_text( 11.0, 10.0, anchor="nw", text="¿Cuántos sectores?", fill="#000000", font=("Inter", 16 * -1) )
        canvas.create_text( 11.0, 82.0, anchor="nw", text="¿Cuál es el tamaño de cada sector en bytes?", fill="#000000", font=("Inter", 16 * -1) )
        canvas.create_text( 344.0, 161.0, anchor="nw", text="IMPORTANTE: Se usan 4 bytes para los punteros de sectores\nSi se ingresa 30 bytes = 4 bytes para punteros + 26 bytes para datos", fill="#000000", font=("Inter", 12 * -1) )

        textInput_NumSector = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        textInput_NumSector.place( x=11.0, y=38.0, width=727.0, height=33.0 )

        textInput_SectorSize = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        textInput_SectorSize.place( x=11.0, y=110.0, width=727.0, height=33.0 )

        button_1 = Button( self, text="Crear disco", borderwidth=0, highlightthickness=0, command=lambda: self.__createDisk(textInput_NumSector, textInput_SectorSize), relief="flat" )
        button_1.place( x=11.0, y=209.0, width=149.0000762939453, height=49.0 )

    def __createDisk(self, input_NumSector: Entry, input_SectorSize: Entry):
        numSector = input_NumSector.get()
        sectorSize = input_SectorSize.get()

        if not numSector.isnumeric() or not sectorSize.isnumeric():
            return

        filesystem = FileSystem.FileSystem()
        filesystem.create_disk( int(numSector), int(sectorSize) )

        self.destroy()
