from Model.AnfatecDriver import VirtualLockin

lock = VirtualLockin()

for i in range(200):
    print(lock.amplitude)
