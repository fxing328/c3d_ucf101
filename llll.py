import cPickle as pkl 
import pdb
file1 = pkl.load(open('feature_c3d_train_fc6','rb'))
#   # # construction training set for triplet loss
pdb.set_trace()
X = np.matrix(file1['data'])
Y = np.array(file1['label'])

