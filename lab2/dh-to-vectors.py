import json

data = {}

# data['i1_xyz'] = []
i1_rpy = []

i2_xyz = []
i2_rpy = []

i3_xyz = []
i3_rpy = []

with open('dh_parameters.json', 'r') as jsonFile:
    data = json.loads(jsonFile.read())

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
