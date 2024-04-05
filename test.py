import octadist as oc

# Prepare list of atomic coordinates of octahedral structure:

atom = ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']

coord = [
    [2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
    [1.885657000, 4.804777000, 6.183726000],
    [1.747515000, 6.960963000, 7.932784000],
    [4.094380000, 5.807257000, 7.588689000],
    [0.539005000, 4.482809000, 8.460004000],
    [2.812425000, 3.266553000, 8.131637000],
    [2.886404000, 5.392925000, 9.848966000],
]

dist = oc.CalcDistortion(coord)
zeta = dist.zeta
delta = dist.delta
sigma = dist.sigma
theta = dist.theta

zeta_ref = 0.228072561
delta_ref = 0.000476251
sigma_ref = 47.926528379
theta_ref = 122.688972774

cutoff = 0.00000001

def test_results():
	assert zeta - zeta_ref < cutoff
	assert delta - delta_ref < cutoff
	assert sigma - sigma_ref < cutoff
	assert theta - theta_ref < cutoff

