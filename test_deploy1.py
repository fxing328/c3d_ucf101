import sys
#sys.path.insert(0,'/scratch/ys1297/caffe-installation/video-caffe/python')
import caffe
import numpy as np
import pdb
import cPickle as pkl
from sklearn import preprocessing
import h5py
import copy
import math
#import matplotlib
import h5py
import scipy.io as scipy_io
from pylab import *
from numpy import linalg as LA

def net(hdf5, batch_size):
    n = caffe.NetSpec()
    n.data, n.label = L.HDF5Data(batch_size=batch_size, source=hdf5, ntop=2)
    n.ip1 = L.InnerProduct(n.data, num_output=1024, weight_filler=dict(type='xavier'))
    n.relu1 = L.ReLU(n.ip1, in_place=True)
    n.ip2 = L.InnerProduct(n.relu1, num_output=1024, weight_filler=dict(type='xavier'))
    n.relu2 = L.ReLU(n.ip2, in_place=True)
    n.ip3 = L.InnerProduct(n.relu2, num_output=2, weight_filler=dict(type='xavier'))
    n.loss = L.SigmoidCrossEntropyLoss(n.ip3, n.label)
    return n.to_proto()

def vis_square(data,image_name):
    """Take an array of shape (n, height, width) or (n, height, width, 3)
       and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)"""

    # normalize data for display
    data = (data - data.min()) / (data.max() - data.min())

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = (((0, n ** 2 - data.shape[0]),
               (0, 1), (0, 1))                 # add some space between filters
               + ((0, 0),) * (data.ndim - 3))  # don't pad the last dimension (if there is one)
    data = np.pad(data, padding, mode='constant', constant_values=1)  # pad with ones (white)

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    plt.imshow(data)
    plt.axis('off')
    plt.savefig(image_name)


if __name__ =='__main__':
    caffe.set_mode_gpu()
    net = caffe.Net('./c3d_ucf101_my_train_test.prototxt','/scratch/xf362/c3d_ucf101/model1/test_new_57000.000000',caffe.TEST)
    iteration = 7150 
#    pos = []
 #   neg = []
    data_fc6 = np.zeros((2048,iteration*15))
    data_fc7 = np.zeros((2048,iteration*15))
    data_fc8 = np.zeros((101,iteration*15))
    label = np.zeros(iteration*15)
    testRes_fc6 = {}
    testRes_fc7 = {}
    testRes_fc8 = {}

    j = 0
    for i in range(iteration):
      data = net.forward()
      #pdb.set_trace()
      for m in range(15):
        data_fc6[:,j] = net.blobs['fc6'].data[m,:]
        data_fc7[:,j] = net.blobs['fc7'].data[m,:]
        data_fc8[:,j] = net.blobs['fc8'].data[m,:]
        label[j] = net.blobs['label'].data[m]
        j = j+1
      #data2 = net.blobs['fc8_p'].data
      #for j in range(5):	
      #  if data['label'][j,:] == 1:
      #     dis_pos = LA.norm(data1[j,:]-data2[j,:])
      #     pos.append(dis_pos)
      #  else:
      #     dis_neg = LA.norm(data1[j,:]-data2[j,:])
      #     neg.append(dis_neg)
      print i 
    testRes_fc6['data'] = data_fc6
    testRes_fc6['label'] = label
    pkl.dump(testRes_fc6,open("feature_c3d_train_fc6","wb"))
    testRes_fc7['data'] = data_fc7
    testRes_fc7['label'] = label
    pkl.dump(testRes_fc7,open("feature_c3d_train_fc7","wb"))
    testRes_fc8['data'] = data_fc8
    testRes_fc8['label'] = label
    pkl.dump(testRes_fc8,open("feature_c3d_train_fc8","wb"))
    
    
    #scipy_io.savemat(open('testResult.mat','wb'), testRes)
     

