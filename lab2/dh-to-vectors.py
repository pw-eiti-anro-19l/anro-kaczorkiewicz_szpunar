import json

data = {}
json_file = {}

with open('dh_parameters.json', 'r') as file:
        json_file = json.loads(file.read())

with open('urdf_vectors.yaml', 'w') as yamlFile:
    for k in json_file:
        params = json.loads(json.dumps(k))
        a = params["a"]
        d = params["d"]
        al = params["al"]
        th = params["th"]

        # data[k] = [a, d, al, th]

        yamlFile.write(str(k['name']) + ':\n')
        yamlFile.write("  j_xyz: 0 0 0\n")
        yamlFile.write("  j_rpy: " + str(al) + " 0 " + str(th) + "\n")
        yamlFile.write("  l_xyz: " + str(a/2) + " 0 0\n")
        yamlFile.write("  l_rpy: 0 0 0\n")
        yamlFile.write("  l_len: " + str(d) + "\n")
        yamlFile.write("  slide: " + str(d) + "\n")
        yamlFile.write("  shape_origin: 0 " + str(-1*d/2) + " 0\n")
