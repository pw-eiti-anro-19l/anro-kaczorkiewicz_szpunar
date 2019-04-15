import json
import math

data = {}
mainMatrix = [[0 ,0 ,0], [0 ,0 ,0], [0, 0, 0]]
temp = 0

with open('dh_parameters.json', 'r') as jsonFile:
    data = json.loads(jsonFile.read())

    for i in data.keys():
        temp += 1
        a, d, al, th = params[i]
        T  = [[1, 0, 0, 0],[0, math.cos(al), -math.sin(al), 0],[0, math.sin(al), math.cos(al), 0], [0,0,0,1]]


with open('urdf_vectors.yaml', 'w') as yamlFile:
    for k in data.keys():
        a, d, al, th = data[k]
        a, d, al, th = float(a), float(d), float(al), float(th)

        data[k] = [a, d, al, th]

        yamlFile.write(k + ':\n')
        yamlFile.write("  j_xyz: " + str(data[k][0]) + " 0 " + str(data[k][1]) + "\n")
        yamlFile.write("  j_rpy: " + str(data[k][2]) + " 0 " + str(data[k][3]) + "\n")
        yamlFile.write("  l_xyz: " + str(data[k][0]/2) + " 0 0\n")
        yamlFile.write("  l_rpy: 0 0 0\n")
        yamlFile.write("  l_len: " + str(data[k][0]) + "\n")
        yamlFile.write("  slide: " + str(-1*data[k][1]) + "\n")
