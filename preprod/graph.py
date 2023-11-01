import pyqtgraph as pg
from json import load

with open("results.json", "r+") as file:
    data = load(file)
plot = pg.plot(data)   # data can be a list of values or a numpy array
