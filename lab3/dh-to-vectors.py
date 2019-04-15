import json
import math
import numpy

data = {}
params = {}
T_list = {}
mainMatrix = [[0 ,0 ,0], [0 ,0 ,0], [0, 0, 0]]
temp = 0

with open('dh_parameters.json', 'r') as jsonFile:
    data = json.loads(jsonFile.read())
    params = data

    for i in data.keys():
        a, d, al, th = params[i]
        T_rotx  = [[1, 0, 0, 0],[0, math.cos(al), -math.sin(al), 0],[0, math.sin(al), math.cos(al), 0], [0,0,0,1]]
        T_transx = [[1, 0, 0, a], [0, 1, 0, 0], [0, 0, 1, 0] , [0, 0, 0, 1]]
        T_rotz = [[math.cos(th), -math.sin(th), 0, 0], [math.sin(th), math.cos(th), 0, 0], [0, 0, 1, 0] , [0, 0, 0, 1]]
        T_transz = [[1, 0, 0, d], [0, 1, 0, 0], [0, 0, 1, 0] , [0, 0, 0, 1]]
        T = numpy.matmul(numpy.matmul(numpy.matmul(T_rotx, T_transx), T_rotz), T_transz)
        T_list[temp] = T
        temp += 1

    mainMatrix = numpy.matmul(numpy.matmul(T_list[0], T_list[1]), T_list[2])
    print(mainMatrix)

with open('urdf_vectors.yaml', 'w') as yamlFile:
    for k in data.keys():
        # a, d, al, th = data[k]
        # a, d, al, th = float(a), float(d), float(al), float(th)

        # data[k] = [a, d, al, th]



        yamlFile.write(k + ':\n')
        yamlFile.write("  j_xyz: " + str(data[k][0]) + " 0 " + str(data[k][1]) + "\n")
        yamlFile.write("  j_rpy: " + str(data[k][2]) + " 0 " + str(data[k][3]) + "\n")
        yamlFile.write("  l_xyz: " + str(data[k][0]/2) + " 0 0\n")
        yamlFile.write("  l_rpy: 0 0 0\n")
        yamlFile.write("  l_len: " + str(data[k][0]) + "\n")
        yamlFile.write("  slide: " + str(-1*data[k][1]) + "\n")