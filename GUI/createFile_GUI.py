from tkinter import Tk, Canvas, Entry, Text, Button, Toplevel, messagebox
from fileSystem_GUI import FileSystem_GUI

class CreateFile(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent: FileSystem_GUI = parent
        self.title("Create File")
        self.geometry("750x550")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=550,
            width=750,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        canvas.create_text( 30.0, 32.0, anchor="nw", text="Nombre del archivo", fill="#000000", font=("Inter", 16 * -1) )

        # Text input: Directory path
        self.entry_1 = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        # To get the current directory absolute route
        #self.entry_1.insert(0, parent.fileSystem.currentDirectory.name)

        self.entry_1.place( x=30.00, y=65.00, width=690, height=35 )

        # Button: To save the content
        self.button_1 = Button(
            self,
            text = "Guardar",
            borderwidth=0,
            highlightthickness=0,
            command= lambda: self.createFile(),
            relief="flat"
        )
        self.button_1.place( x=30.00, y=130.00, width=110, height=35 )

        # Text input: To modify the content of the file
        self.entry_2 = Text(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place( x=155.00, y=130.00, width=570, height=400 )

    def getExtension(self, name):
        parts = name.split(".")
        if len(parts) > 1:
            return parts[-1]
        else:
            print("Falta ingresar la extension de la vara de la vara")
            return ""

    def getName(self, name):
        parts = name.split(".")
        return parts[0]

    def diskVerification(self):
        if not self.parent.fileSystem.disk == None:
            return True
        messagebox.showwarning("Disco no encontrado","Disco no creado. Favor crear un disco antes de intentar crear un archivo")
        return False


    def uniqueFileNameVerification(self, fileName):
        if not fileName in self.parent.fileSystem.currentDirectory.files:
            return True
        messagebox.showwarning("Archivo con mismo nombre","Se ha encontrado un archivo con el mismo nombre. Favor ingresar un nombre diferente al archivo.")
        return False

    # TODO: Validaciones necesarias para asegurar que el nombre sea apto
    def createFile(self):
        # Disk verification
        if not self.diskVerification():
            return

        # Name verification
        fullName = self.entry_1.get()
        fileName = self.getName(fullName)
        extension = self.getExtension(fullName)

        if not self.uniqueFileNameVerification(f"{fileName}.{extension}"):
            return

        content = self.entry_2.get("1.0", "end")
        if extension != "":
            self.parent.fileSystem.createFile(fileName, extension, content)
            self.parent.reloadFileSystem()
            self.destroy()
        else:
            messagebox.showwarning("Create File", "Falta de extension")
            print("Falta de extension")


