# import numpy as np
#
#
# def angle_btw_2vec(v1, v2):
#     """Compute angle between two vectors and return value in degree
#
#     :param v1: vector 1 in 3D space
#     :param v2: vector 2 in 3D space
#     :type v1: list, array
#     :type v2: list, array
#     :return angle: angle between two vectors
#     :rtype angle: int, float
#     """
#     ab_v1 = np.sqrt((pow(v1[0], 2) + pow(v1[1], 2) + pow(v1[2], 2)))
#     ab_v2 = np.sqrt((pow(v2[0], 2) + pow(v2[1], 2) + pow(v2[2], 2)))
#
#     scalar = (v1[0] * v2[0]) + (v1[1] * v2[1]) + (v1[2] * v2[2])
#
#     dotVec = scalar / (ab_v1 * ab_v2)
#
#     if -1 <= dotVec <= 1:
#         angle = ((np.arccos(dotVec)) / np.pi) * 180
#     else:
#         angle = 0
#
#     return float(angle)
#
#
# def angles(V1, V2):
#     ## vectors moduli
#     Mod1 = np.sqrt((pow(V1[0], 2) + pow(V1[1], 2) + pow(V1[2], 2)))
#     Mod2 = np.sqrt((pow(V2[0], 2) + pow(V2[1], 2) + pow(V2[2], 2)))
#     ## scalar product
#     Sca1 = V1[0] * V2[0] + V1[1] * V2[1] + V1[2] * V2[2]
#     ## Angle calculation in degrees
#     leCos = Sca1 / (Mod1 * Mod2)
#     if -1 <= leCos <= 1:
#         resultat = ((np.arccos(leCos)) / np.pi) * 180
#     else:
#         resultat = 0
#     return float(resultat)
#
#
# a = [[0.6179, -1.2477, -1.3562],
#      [-0.6573, 1.2028, -1.3837],
#      [-1.7201, -0.9335, 0.1971],
#      [1.7313, 0.9551, 0.0387],
#      [0.4774, -1.2687, 1.442],
#      [-0.3766, 1.2957, 1.4612]]
#
# b = [[-1.7201, -0.9335, 0.19709999999999983],
#      [-0.3765999999999998, 1.2957, 1.4612],
#      [0.47740000000000027, -1.2687, 1.442],
#      [1.7313, 0.9550999999999998, 0.03869999999999996],
#      [0.6178999999999997, -1.2477, -1.3562],
#      [-0.6573000000000002, 1.2027999999999999, -1.3837000000000002]]
#
# for i in range(6):
#     angle = angle_btw_2vec(a[0], a[i])
#     print(angle)
#
# print("=====")
#
# for i in range(6):
#     angle = angles(a[0], a[i])
#     print(angle)
#
# print("^^^^^^^")
#
# for i in range(6):
#     angle = angle_btw_2vec(b[0], b[i])
#     print(angle)
#
# print("=====")
#
# for i in range(6):
#     angle = angles(b[0], b[i])
#     print(angle)

# ------
#
# from octadist_gui import calc_d_mean
#
# a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# b = [[0.6179, -1.2477, -1.3562],
#          [-0.6573, 1.2028, -1.3837],
#          [-1.7201, -0.9335, 0.1971],
#          [1.7313, 0.9551, 0.0387],
#          [0.4774, -1.2687, 1.442],
#          [-0.3766, 1.2957, 1.4612],
#          [5.6545, 1.1234, -4.5344]]
#
#
# x, y = calc_d_mean_(a, b)
# print(x)

import octadist_gui

print(octadist_gui.__version__)
print(octadist_gui.__src__)
