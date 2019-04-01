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
		a, d, al, th = params[key]
		al, a, d, th = float(al), float(a), float(d), float(th)

		switch(k):
			case


	file.write(k + '\n')
	file.write("")