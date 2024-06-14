from tkinter import Tk, Canvas, Entry, Text, Button, Toplevel, messagebox
from src.file import File
class EditFile(Toplevel):
    def __init__(self, parent, fileObj: File, content):
        super().__init__(parent)

        self.file = fileObj
        self.parent = parent
        self.title("Edit File")
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

        # Text input: Directory path
        self.entry_1 = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.insert(0, fileObj.name + "." + fileObj.extension)
        self.entry_1.place(x=9.0, y=10.0, width=722.0, height=33.0)
        self.entry_1.config( state="disabled" )

        # Button: To save changes
        self.button_1 = Button(
            self,
            text = "Guardar",
            borderwidth=0,
            highlightthickness=0,
            command=self.saveButton,
            relief="flat"
        )
        self.button_1.place(x=9.0, y=67.0, width=149.0000762939453, height=49.0)

        # Text input: To modify the content of the file
        self.entry_2 = Text(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.insert("1.0", content)
        self.entry_2.place(x=171.0, y=67.0, width=558.0, height=459.0)

    def getName(self, name):
        parts = name.split(".")
        return parts[0]

    def getExtension(self, name):
        parts = name.split(".")
        if len(parts) > 1:
            return parts[-1]
        else:
            return ""

    def saveButton(self):
        #Name
        fullName = self.entry_1.get()
        fileName = self.getName(fullName)

        #Extension
        extension = self.getExtension(fullName)

        #Content
        content = self.entry_2.get("1.0", "end")
        content = content.strip()

        #Extension verification
        if extension == "":
            messagebox.showwarning("Falta de extension del archivo", "El nombre del archivo debe poseer la extension deseada.")
            return

        # To obtain the sectors list
        oldSectorsList = self.parent.fileSystem.fat.getFileSectors(self.file.fat_index)

        # To write the new content
        newSectorsList = self.parent.fileSystem.disk.writeToDisk(content, oldSectorsList)
        if (newSectorsList == -1):
            self.parent.fileSystem.fat.freeFATEntries(self.file.fat_index)
            self.file.fat_index = -1
        elif (newSectorsList != []):
            # To free and update the FAT
            self.parent.fileSystem.fat.freeFATEntries(self.file.fat_index)
            newStartingIndex = self.parent.fileSystem.fat.assingSectorList(newSectorsList)

            # To update directory in case that the user modify file name or extension
            currentDirectory = self.parent.fileSystem.currentDirectory
            currentDirectory.changeFileNameInDict(self.file.name + "." + self.file.extension, fullName)

            self.file.assignSectors(newStartingIndex)

        # To update the file object
        self.file.modifyContent( fileName, extension, content)

        self.parent.reloadFileSystem()
        self.parent.updateDiskState()
        self.destroy()
