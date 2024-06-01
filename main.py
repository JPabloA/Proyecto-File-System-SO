from disk import Disk

# 4: pointer y 16 data = 20 bytes en total
obj = Disk(8, 20)

obj.createDisk()

obj.writeToDisk("Si cabe pero en 2 partes mi bro")
obj.writeToDisk("Esto se elimina de una vez y muchísimo más extenso")
obj.writeToDisk("Si cabe pero en 2 partes mi bro")

obj.removeFromDisk(2)

obj.readFromDisk(0)