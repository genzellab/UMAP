import sys
#sys.path.append('/media/enrique/Disk1/Proyectos/UnsupervisedRippleClassification/Code/Python')
from sklearn.manifold import Isomap
from sklearn.metrics.pairwise import euclidean_distances
from scipy.stats import pearsonr
from kneed import KneeLocator


def isomapFindKnee(res_var):
	kn = KneeLocator(range(1,len(res_var)+1), res_var, curve='convex', direction='decreasing')
	if bool(kn.knee):
		dimEst = kn.knee
	else:	
		m = np.abs(np.diff(res_var))
		try:
			dimEst = np.where(m <= 0.01)[0][0] + 1
		except IndexError:
			dimEst = float('nan')
	return dimEst


def isomapDimEst(data):
	#Insert data in rows
	print("isomapDimEst", end="\r")
	if data.shape[1] >= 15:
		n_dim = 15
	else:
		n_dim =  data.shape[1]
	embedding = Isomap(n_components=n_dim)
	emb = embedding.fit(data)
	G = emb.dist_matrix_
	res_var = []
	for dim in range(1,n_dim+1):
		D = euclidean_distances(emb.embedding_[:,:dim])
		res_var.append(1 - pearsonr(G.flatten(),D.flatten())[0])
	dimEst = isomapFindKnee(res_var)
	return dimEst, res_var