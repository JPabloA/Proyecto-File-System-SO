from tkinter import Canvas, Entry, Button, Toplevel
from src.file import File
from src.directory import Directory
from fileSystem_GUI import FileSystem_GUI

class CopyFiles(Toplevel):
    def __init__(self, parent: FileSystem_GUI, selected_obj: File | Directory):
        super().__init__(parent)

        self.parent = parent
        self.selected_obj = selected_obj
        self.isFile = True

        path_origin: str = ""
        if isinstance(selected_obj, File):
            path_origin = f"{self.parent.fileSystem.getCurrentWorkingDirectory()}/{selected_obj.name}.{selected_obj.extension}"
            self.isFile = True
        elif isinstance(selected_obj, Directory):
            path_origin = f"{self.parent.fileSystem.getCurrentWorkingDirectory()}/{selected_obj.name}"
            self.isFile = False
        else:
            print("Object could not be recognized")
            return

        self.title("Copy Files")
        self.geometry("750x593")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=593,
            width=750,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Text input: Directory path (Origin)
        self.entry_Origin = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.entry_Origin.insert(0, path_origin)
        self.entry_Origin.place(x=14.0, y=45.0, width=722.0, height=33.0)

        # Text input: Directory path (Destiny)
        self.entry_Destiny = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.entry_Destiny.insert(0, "/root/")
        self.entry_Destiny.place(x=14.0, y=146.0, width=722.0, height=33.0)

        # Button: First method to copy
        self.button_1 = Button( self, text = "Ruta real a ruta virtual", borderwidth=0, highlightthickness=0, command=self.__copy_RealToVirtual, relief="flat" )
        self.button_1.place(x=14.0, y=219.0, width=310.0, height=49.0)

        # Button: Second method to copy
        self.button_2 = Button( self, text = "Ruta virtual a ruta real", borderwidth=0, highlightthickness=0, command=self.__copy_VirtualToReal, relief="flat" )
        self.button_2.place(x=14.0, y=277.0, width=310.0, height=49.0)

        # Button: Third method to copy
        self.button_3 = Button( self, text = "Ruta virtual a ruta virtual", borderwidth=0, highlightthickness=0, command=self.__copy_VirtualToVirtual, relief="flat" )
        self.button_3.place(x=14.0, y=335.0, width=310.0, height=49.0)

        canvas.create_text( 14.0, 19.0, anchor="nw", text="Copiar desde:", fill="#000000", font=("Inter", 16 * -1) )
        canvas.create_text( 14.0, 118.0, anchor="nw", text="Hasta:", fill="#000000", font=("Inter", 16 * -1) )

    def __getInputPaths(self):
        path_origin: str  = self.entry_Origin.get()
        path_destiny: str = self.entry_Destiny.get()

        # Make sure the path_destiny finishes with "/"
        path_destiny += "/" if path_destiny[-1] != "/" else ""

        return path_origin, path_destiny

    def __copy_RealToVirtual(self):
        path_origin, path_destiny = self.__getInputPaths()
        print("")

    def __copy_VirtualToReal(self):
        path_origin, path_destiny = self.__getInputPaths()
        print("button_2 clicked")

    def __copy_VirtualToVirtual(self):
        path_origin, path_destiny = self.__getInputPaths()
        directory_destiny: Directory = self.parent.fileSystem.navigateToDirectory( path_destiny )

        if self.isFile:
            file_name = self.selected_obj.name
            file_extension = self.selected_obj.extension
            file_content = self.selected_obj.content

            self.parent.fileSystem.createFile( file_name, file_extension, file_content, directory_destiny )
        else:
            dir_name = self.selected_obj.name

            self.parent.fileSystem.createDirectory( dir_name, directory_destiny )

        self.destroy()
