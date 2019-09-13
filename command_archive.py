from Model.AnfatecDriver import AnfatecAMU24
from Model.frequency_scan import frequency_scanner_linear
from pandas import read_csv
import plotly.express as px

#log_to_screen(INFO)
inst = AnfatecAMU24(time_constant=5, roll_off=2)
result = frequency_scanner_linear(inst, 180000, 220000, 100)

output = open("output.csv","w+",encoding="utf-8")

output.write("Frequency" + ",")
output.write("Amplitude" + "\n")

for result_list in result:
    output.write(str(result_list[0])+",")
    output.write(str(result_list[3].magnitude))
    output.write("\n")

output.close()
data = read_csv("output.csv")
fig = px.scatter(data, x="Frequency", y="Amplitude")
fig.show()
