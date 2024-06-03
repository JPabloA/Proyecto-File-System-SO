from tkinter import Tk, Canvas, Entry, Text, Button, Toplevel

class CreateFile(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
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
        
        self.entry_1.insert(0, "Nombre")
        self.entry_1.place(x=9.0, y=10.0, width=722.0, height=33.0)

        # Button: To save the content
        self.button_1 = Button(
            self,
            text = "Guardar",
            borderwidth=0,
            highlightthickness=0,
            command=self.button_1_clicked,
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
        self.entry_2.insert("1.0", "Contenido")
        self.entry_2.place(x=171.0, y=67.0, width=558.0, height=459.0)

    def getExtension(self, name):
        parts = name.split(".")
        if len(parts) > 1:
            return parts[-1]
        else:
            print("Falta ingresar la extension de la vara de la vara")
            return ""
        
    def button_1_clicked(self):
        name = self.entry_1.get()
        extension = self.getExtension(name)
        content = self.entry_2.get()
        print("nombre ", name)
        if extension != "":
            print("\nextension ", extension)
        else:
            print("Falta de extension")
        print("\ncontent", content)
        #parent.fileSystem.createFile(name, extension, content)
        print("button_1 clicked")
