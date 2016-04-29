#!/usr/bin/python

import os, sys, os.path

weight0 = os.path.isfile('/vagrant/classifier/data/default/net_weight_0') 
weight1 = os.path.isfile('/vagrant/classifier/data/default/net_weight_1') 
if weight0 and weight1:
	print 'Already downloaded weights\nExiting...'
	sys.exit()


print 'Downloading Weights (1.2gb)'
file_dir = os.path.dirname(os.path.abspath(__file__))

weight_url = "http://cilvr.cs.nyu.edu/lib/exe/fetch.php?media=overfeat:overfeat-weights.tgz"

os.system("cd %s && mkdir -p data/default && cd data/default && wget %s -O weights.tgz && tar -xzf weights.tgz && rm weights.tgz"%(os.path.join(file_dir), weight_url))
