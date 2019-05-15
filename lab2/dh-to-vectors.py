import json

from tf.transformations import *

with open('dh_parameters.json', 'r') as file:
    dhJson= json.loads(file.read())

xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)
with open('urdf_vectors.yaml', 'w') as file:
    for instance in dhJson:
        oneInstance= json.loads(json.dumps(instance))
        a = oneInstance["a"]
        d = oneInstance["d"]
        alpha=oneInstance["al"]
        theta = oneInstance["th"]

        matrixD= translation_matrix((0, 0, d))
        matrixTheta = rotation_matrix(theta, zaxis)
        matrixA = translation_matrix((a, 0, 0))
        matrixAlpha = rotation_matrix(alpha, xaxis)

        TransMatrix = concatenate_matrices(matrixA,matrixAlpha,matrixTheta, matrixD)
        rpy = euler_from_matrix(TransMatrix)
        xyz = translation_from_matrix(TransMatrix)


        file.write(oneInstance["name"] + ":\n")
        file.write("  j_xyz: "+str(xyz[0])+" "+str(xyz[1])+" "+str(xyz[2])+"\n")
        file.write("  j_rpy: "+str(rpy[0])+' '+str(rpy[1])+' '+str(rpy[2])+'\n')
        file.write("  l_xyz: "+str(0)+' '+str(0)+' '+str(float(d)*(-0.5))+'\n')
        file.write("  l_rpy: "+str(0)+' '+str(0)+' '+str(0)+'\n')
        file.write("  l_len: "+str(d)+'\n')
            