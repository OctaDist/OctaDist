###################################################
# Example 1 for running the test on OctaDist PyPI #
###################################################

import octadist as oc

# The first atom must be metal center atom of octahedral structure.
# If not, please see example_2.py for how to handle this issue.

atom = ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']

coord = [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
         [1.885657000, 4.804777000, 6.183726000],
         [1.747515000, 6.960963000, 7.932784000],
         [4.094380000, 5.807257000, 7.588689000],
         [0.539005000, 4.482809000, 8.460004000],
         [2.812425000, 3.266553000, 8.131637000],
         [2.886404000, 5.392925000, 9.848966000]]

dist = oc.CalcDistortion(coord)
zeta = dist.zeta             # Zeta
delta = dist.delta           # Delta
sigma = dist.sigma           # Sigma
theta = dist.theta           # Theta

print("\nAll computed parameters")
print("-----------------------")
print("Zeta  =", zeta)
print("Delta =", delta)
print("Sigma =", sigma)
print("Theta =", theta)

# All computed parameters
# -----------------------
# Zeta  = 0.22807256171728651
# Delta = 0.0004762517834704151
# Sigma = 47.926528379270124
# Theta = 122.688972774546
