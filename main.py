from FileSystem import FileSystem
from disk import Disk

fileSystem = FileSystem()

fileSystem.create_disk(20, 20)

fileSystem.createFile("Hola", ".txt", "Hola soy el contenido")

# fileSystem.createFile("Hola", ".txt", "Hola soy el contenido")

fileSystem.createFile("Hola2", ".txt", "Soy algo completamente diferente")

fileSystem.createDirectory("Carpeta")

fileSystem.listDirectory()