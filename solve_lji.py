from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle


# The dataset used for this case study are confidential, instead we share a template of the csv file (see lji_template.csv)
dat = pd.read_csv('*.csv', sep=';')

sol, obj_vals, k_vals, l_vals = {}, {}, {}, {}

V = dat.shape[0]
Q = np.log2(dat.iloc[:,12]*dat.iloc[:,10])
Cq = np.ones(V)
num_samples = 1000
# define proportion of trafficking as a random variable
s_mean = dat.iloc[:,3]/dat.iloc[:,2]
s_mean[10]=.31
s_mean[s_mean==0]=.05
mar = .1
s=np.minimum(np.maximum(np.random.triangular(left=s_mean-mar, mode=s_mean, right=s_mean+mar, size=(num_samples, len(s_mean))),0),1)

S1 = [Q*(1-s[j]) for j in range(num_samples)]
S2 = [Q*s[j] for j in range(num_samples)]

num_devices = V
ytpr = (dat.iloc[:,5:10] * [.1,.3,.5,.7,.9]).sum(axis=1)/dat.iloc[:,2]

for  tnr in [0.5, 0.55, 0.6, 0.65, 0.7]:
	ytnr = tnr * np.ones(V)

	coeff2 = [[a*b for a,b in zip(S2[j],ytpr)] for j in range(num_samples)]
	coeff3 = [[a*b for a,b in zip(S1[j],ytnr)] for j in range(num_samples)]
	coq = [S1[j]*(1-ytnr)+S2[j]*(1-ytpr) for j in range(num_samples)]

	alloc_lji = dat.iloc[:,11]
	B = sum(dat.iloc[:,11])
	K = 60
	L = 6*K
	m = Model()
	m.ModelSense = 1  # minimize
	# Add variables
	x = m.addVars(V, vtype='I', name='x', lb=[1]*V, ub=[10]*V)
	error = m.addVars(num_samples, obj=1.0/num_samples, name='error')
	# Set constraints
	m.addConstr(quicksum(Cq[i]*x[i] for i in range(V)) == B, name="resources")
	m.addConstrs((quicksum(coeff2[j][i]*x[i] for i in range(V)) >= K for j in range(num_samples)), name="HT")
	m.addConstrs((quicksum(coeff3[j][i]*x[i] for i in range(V)) <= L for j in range(num_samples)), name="NHT")
	m.addConstrs((error[j] == quicksum(coq[j][i]*x[i] for i in range(V)) for j in range(num_samples)), name='error')
	m.update()

	m.optimize()

	sol[tnr] = [v.X for k,v in x.items()]
	obj_vals[tnr] = [v.X for k,v in error.items()]
	k_vals[tnr] = [quicksum(coeff2[j][i]*x[i] for i in range(V)).getValue() for j in range(num_samples)]
	l_vals[tnr] = [quicksum(coeff3[j][i]*x[i] for i in range(V)).getValue() for j in range(num_samples)]

with open('lji_tnr.pkl', 'wb') as f:
    pickle.dump([obj_vals, k_vals, l_vals, sol], f)