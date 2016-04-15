import os, sys, shutil, subprocess, getopt, math, copy
import numpy as np
from cStringIO import StringIO
import scipy
import scipy.linalg
import scipy.optimize

# file_path_c='test_c.csv'
# file_path_r='test_r.csv'
# file_path_output='out_Z.csv'


def main(argv):
	file_path_c = None
	file_path_r = None
	file_path_output = None
	try:
		opts, args = getopt.getopt(argv, "c:r:o:", ["ColumnDegrees=", "RowDegrees=", "Output="])
	except getopt.GetoptError:
		print 'Call using: python MaxEntMatrix.py -c <ColumnDegrees.csv> -r <RowDegrees.csv> -o <Output.csv>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Call using: python MaxEntMatrix.py -c <ColumnDegrees.csv> -r <RowDegrees.csv> -o <Output.csv>'
			sys.exit(2)
		elif opt in ("-c", "--ColumnDegrees"):
			file_path_c = arg
		elif opt in ("-r", "--RowDegrees"):
			file_path_r = arg
		elif opt in ("-o", "--Output"):
			file_path_output = arg
	#Run the main program
	calc_max_ent(file_path_c, file_path_r, file_path_output)

def G(x,r,c): #This is the G function on page 3 of Barvinok 2009
	m = len(r)
	n = len(c)
	s = x[0:m]
	t = x[m:]
	res = -np.sum(r*s) - np.sum(c*t) + np.sum(np.log(1+np.exp(t[:,np.newaxis]+s))) #-\sum_i r_i*s_i - \sum_i c_i*t_i + sum_{i,j} \log(1+e^{s_i+t_j})
	return res

def JacG(x,r,c):  # This is the Jacobian of the G function
	res = list()
	m = len(r)
	n = len(c)
	s = np.array(x[0:m])
	t = np.array(x[m:])
	for i in range(len(s)):
		res.append(-r[i] + np.sum(np.exp(s[i]+t)/(1+np.exp(s[i]+t))))
	for j in range(len(t)):
		res.append(-c[j] + np.sum(np.exp(s+t[j])/(1+np.exp(s+t[j]))))
	return np.array(res)

def HessG(x, r, c):  # This is the Hessian of the G function
	res = np.zeros((len(x),len(x)))
	m = len(r)
	n = len(c)
	s = np.array(x[0:m])
	t = np.array(x[m:])
#	for i in range(m):
#		for j in range(n):
#			res[i,j+m] = np.exp(s[i]+t[j])/(1+np.exp(s[i]+t[j]))**2
#	for i in range(m):
#		for j in range(n):
#			res[m+j,i] = np.exp(s[i]+t[j])/(1+np.exp(s[i]+t[j]))**2
#	return res
	temp = np.exp(s+t[:,np.newaxis])/(1+np.exp(s+t[:,np.newaxis]))**2  # Faster, but not 100% about the indicies
	res[n:m+n,0:n] = temp.transpose()
	res[0:n,n:m+n]=temp
	return res


def calc_max_ent(file_path_c, file_path_r, file_path_output):
	assert isinstance(file_path_c,basestring), file_path_c
	assert isinstance(file_path_r,basestring), file_path_r
	assert isinstance(file_path_output,basestring), file_path_output
	
	#Read in files
	c_degrees = np.genfromtxt(file_path_c,delimiter=',')
	r_degrees = np.genfromtxt(file_path_r,delimiter=',')
	
	m = len(r_degrees)
	n = len(c_degrees)
	x0 = np.concatenate((r_degrees/np.sum(r_degrees), c_degrees/np.sum(c_degrees)))

	#BFGS quasi-Newton method of Broyden, Fletcher, Goldfarb, and Shannon.
	#res = scipy.optimize.minimize(G, x0, args=(r_degrees,c_degrees))
	#Newton-CG algorithm, using the Jacobian
	res = scipy.optimize.minimize(G, x0, args=(r_degrees,c_degrees), jac=JacG, method='Newton-CG')  
	res = res.x
	
	x = np.exp(res[0:m])
	y = np.exp(res[m:])
	Z = np.zeros((m,n))
	for i in range(m):
		for j in range(n):
			Z[i,j] = x[i]*y[j]/(1+x[i]*y[j])
	
	
	np.savetxt(file_path_output, Z, delimiter=',')


	


if __name__ == "__main__":
	main(sys.argv[1:])
