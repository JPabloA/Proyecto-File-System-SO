from tkinter import Canvas, Entry, Button, Toplevel, messagebox
from src.file import File
from src.directory import Directory
import os

class CopyFiles(Toplevel):
    def __init__(self, parent, selected_obj: File | Directory = None):
        super().__init__(parent)

        self.parent = parent
        self.selected_obj = selected_obj
        self.isFile = True

        path_origin: str = ""
        if selected_obj is not None:
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
        self.geometry("750x405")
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

        if self.parent.fileSystem.disk is None:
            messagebox.showwarning("No se encontro ningún disco", "Asegúrese de crear un disco antes de copiar un archivo al file system")
            self.entry_Origin.config( state="disabled" )
            self.entry_Destiny.config( state="disabled" )
            self.button_1.config( state="disabled" )
            self.button_2.config( state="disabled" )
            self.button_3.config( state="disabled" )

    def __getInputPaths(self):
        path_origin: str  = self.entry_Origin.get()
        path_destiny: str = self.entry_Destiny.get()

        # Make sure the path_destiny finishes with "/"
        path_destiny += "/" if path_destiny[-1] != "/" else ""

        return path_origin, path_destiny

    def __copy_DirectoryContentRecursively(self, directory_origin: Directory, directory_destiny: Directory):
        # Copy its files in the directory_destiny
        for file in directory_origin.files.values():
            file_name = file.name
            file_extension = file.extension
            file_content = file.content

            self.parent.fileSystem.createFile( file_name, file_extension, file_content, directory_destiny )

        # Copy its directories in the directory_destiny
        for subdirectory in directory_origin.directories.values():
            dir_name = subdirectory.name
            self.parent.fileSystem.createDirectory( dir_name, directory_destiny )

        for sub_origin, sub_destiny in zip(directory_origin.directories.values(), directory_destiny.directories.values()):
            self.__copy_DirectoryContentRecursively( sub_origin, sub_destiny )

    def __copy_RealToVirtual(self):
        path_origin, path_destiny = self.__getInputPaths()
        directory_destiny: Directory = self.parent.fileSystem.navigateToDirectory( path_destiny )

        if os.path.isfile(path_origin):
            if not os.path.isfile(path_origin):
                print(f"El archivo en la ruta {path_origin} no existe.")
                return

            # Obtener el nombre del archivo y su extensión
            file_name = os.path.basename(path_origin)
            nombre, extension = os.path.splitext(file_name)
            extension = extension.lstrip('.')  # Eliminar el punto inicial de la extensión

            if not self.parent.isUniqueInDestinyDir( f"{file_name}.{extension}", "File", path_destiny ):
                messagebox.showwarning("Archivo existe en el destino", "Existe un archivo con el mismo nombre en el destino, por favor cambie el nombre del archivo o seleccione otra ruta")
                return

            # Leer el contenido del archivo
            with open(path_origin, 'r') as archivo:
                file_content = archivo.read()

            self.parent.fileSystem.createFile(nombre, extension, file_content, directory_destiny)

            print(f"Archivo {file_name} copiado a la memoria virtual.")
        
        elif os.path.isdir(path_origin):
            dir_name = os.path.basename(os.path.normpath(path_origin))

            if not self.parent.isUniqueInDestinyDir( dir_name, "Directory", path_destiny ):
                messagebox.showwarning("Directorio existe en el destino", "Existe un directorio con el mismo nombre en el destino, por favor cambie el nombre del directorio o seleccione otra ruta")
            else:
                directory_destiny = self.parent.fileSystem.createDirectory( dir_name, directory_destiny )
                print(f"Directorio {dir_name} copiado a la memoria virtual.")
        else:
            print("Tipo de archivo no compatible")

    def __copy_VirtualToReal(self):
        if self.selected_obj is None:
            messagebox.showerror("No existe ningún objeto seleccionado", "La ruta ingresada no corresponde a ningún objeto dentro del file system")
            return

        path_origin, path_destiny = self.__getInputPaths()

        if self.isFile:
            file_name = self.selected_obj.name
            file_extension = self.selected_obj.extension
            file_content = self.selected_obj.content

            path_destiny = os.path.join( os.path.split( path_destiny )[0], f"{file_name}.{file_extension}" )

            if os.path.isfile(path_destiny):
                messagebox.showwarning("Archivo existe en el destino", "Existe un archivo con el mismo nombre en el destino, por favor cambie el nombre del archivo o seleccione otra ruta")
            else:
            # Crear o sobrescribir el archivo en la ruta especificada
                with open(path_destiny, 'w') as archivo:
                    archivo.write(file_content)  # Puedes escribir contenido en el archivo si lo deseas
                print(f"Archivo creado en: {path_destiny}")
                self.destroy()
        else:
            dir_name = self.selected_obj.name
            path_destiny = os.path.join( os.path.split( path_destiny )[0], f"{dir_name}" )

            if os.path.isdir(path_destiny):
                messagebox.showwarning("Directorio existe en el destino", "Existe un directorio con el mismo nombre en el destino, por favor cambie el nombre del directorio o seleccione otra ruta")
            else:
                try:
                    # Crear el directorio y todos los directorios intermedios necesarios
                    os.makedirs(path_destiny, exist_ok=True)
                    print(f"Directorio creado en: {path_destiny}")
                except OSError as e:
                    print(f"Error al crear el directorio: {e}")

                # Copy its content recursively
                #self.__copy_DirectoryContentRecursively(self.selected_obj, path_destiny)
                self.destroy()

    def __copy_VirtualToVirtual(self):

        if self.selected_obj is None:
            messagebox.showerror("No existe ningún objeto seleccionado", "La ruta ingresada no corresponde a ningún objeto dentro del file system")
            return

        path_origin, path_destiny = self.__getInputPaths()
        directory_destiny: Directory = self.parent.fileSystem.navigateToDirectory( path_destiny )

        if directory_destiny is None:
            messagebox.showerror("Directorio destino no existe", "El directorio de destino no pudo ser encontrado, por favor ingrese una ruta válida")
            return

        if self.isFile:
            file_name = self.selected_obj.name
            file_extension = self.selected_obj.extension
            file_content = self.selected_obj.content

            if not self.parent.isUniqueInDestinyDir( f"{file_name}.{file_extension}", "File", path_destiny ):
                messagebox.showwarning("Archivo existe en el destino", "Existe un archivo con el mismo nombre en el destino, por favor cambie el nombre del archivo o seleccione otra ruta")
            else:
                self.parent.fileSystem.createFile( file_name, file_extension, file_content, directory_destiny )
                self.destroy()
        else:
            dir_name = self.selected_obj.name

            if not self.parent.isUniqueInDestinyDir( dir_name, "Directory", path_destiny ):
                messagebox.showwarning("Directorio existe en el destino", "Existe un directorio con el mismo nombre en el destino, por favor cambie el nombre del directorio o seleccione otra ruta")
            else:
                # Create the directory in its destiny
                directory_destiny = self.parent.fileSystem.createDirectory( dir_name, directory_destiny )

                # Copy its content recursively
                self.__copy_DirectoryContentRecursively(self.selected_obj, directory_destiny)
                self.destroy()
