import png
from Model.scaler import lin_list, log_list, square_list

n = 21
split = int(n/2)
array = []
color_list = []
points = lin_list(0, 255, split+1)
for i in range(split):
    color_list.append([int(points[i]), 255, 0])
color_list.append([255, 255, 0])
for i in range(split+1, n):
    color_list.append([255, int(points[n-i-1]), 0])
for i in range(221):
    array.append([])

width = 880

for x in range(221):
    for y in range(width):
        i = 0
        for j in range(n+1):
            if y > (width / n)*(i+1):
                i = j
        array[x].extend(color_list[i])

png.from_array(array, "RGB").save("color_scale_lin.png")
