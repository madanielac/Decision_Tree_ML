#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 00:32:55 2020

@author: danielacamacho
"""

import math

def choosing_root_3rd(node, root_chosen): 
    info_gain = []
    node_len = node.data
    
    for i in range(1,len(node_len[0])):
        if i != root_chosen:
            node_temp = node
            node_temp.create_layer(i)

            info_gain.append((I(node_temp),i))
    
    return max(info_gain)
    
def H(S):
    out_of = len(S.data)
    ones = 0
    zeros = 0
    
    for n in S.data:
        if n[0] == 1:
            ones += 1
        else:
            zeros += 1
    
    ones = ones/out_of 
    zeros = zeros/out_of
    
    prob = [ones, zeros]
    h = 0
    
    for x in prob:
        if x == 0:
            h -= 0
        else:
            h -= (x * math.log2(x))
    return h

def I(A):
    out_of = len(A.data)
    probL = len(A.left.data)/out_of
    probR = len(A.right.data)/out_of
    
    i = H(A) - (probL * H(A.left)) - (probR * H(A.right))
    
    return i

def err_perc(S):
    
    error = 0
    out_of = len(S.data)
      
    def leaf_err(S):
        leaf_l = 0
        leaf_r = 0
        error = 0
        
        if S.left != None:
            leaf_l = leaf_err(S.left)
        if S.right != None:
            leaf_r = leaf_err(S.right)
        
        if S.label != None: 
            for n in S.data:
                if n[0] != S.label:
                    error += 1
            return error
        else:
            return leaf_l + leaf_r
        
    error += leaf_err(S)
    error = (error/out_of) *100
    return error

def change_labels(tree_train, tree_test):
    
    if tree_train.left != None:
        change_labels(tree_train.left, tree_test.left)
    if tree_train.right != None:
        change_labels(tree_train.right, tree_test.right)
    
    if tree_train.label != tree_test.label:
            tree_test.label = tree_train.label
    


#-----------------------------------------------
class Node:
    def __init__(self, data_list):
        
        self.left = None
        self.right = None
        self.label = None
        self.data = data_list
        self.split_on = None
        self.label_node()


    def create_layer(self, chosen_feat):
        left = []
        right = []
        for n in self.data:
            if n[chosen_feat] == 0:
                left.append(n)
            else:
                right.append(n)

        self.left = Node(left) 
        self.right = Node(right)
        self.label = None
        self.split_on = chosen_feat
        
    def label_node(self):
        win0 = 0
        win1 = 0
        for n in self.data:
            if n[0] == 0:
                win0 += 1
            else:
                win1 += 1
                
        if win0 > win1:
            self.label = 0
        else:
            self.label = 1

#--------------------------------------------   
        
        

file = open('specttrain.txt', 'r')
data = file.readlines()
data = data[:-1]
file.close()

data_list = [[int(x) for x in xs.strip().split(",")] for xs in data]


i_gain = []

for i in range(1,len(data_list[0])):
    node = Node(data_list)
    node.create_layer(i)

    i_gain.append((I(node),i))
    
root_chosen = max(i_gain)[1]
info_gain_chosen = max(i_gain)[0]

node_chosen_feat = Node(data_list)
node_chosen_feat.create_layer(root_chosen)

error_feat = err_perc(node_chosen_feat)

print('\n-------------------------------\n')
print('For the Training Set:')
print("The chosen feature as the root of the stump is #", 
      root_chosen)
print('Its information gain value is:', info_gain_chosen)
print('Error on training data is', error_feat, '%')




left_branch_3 = choosing_root_3rd(node_chosen_feat.left, root_chosen)
right_branch_3 = choosing_root_3rd(node_chosen_feat.right, root_chosen)

        
root_3_l = left_branch_3[1]
info_gain_l = left_branch_3[0]

root_3_r = right_branch_3[1]
info_gain_r = right_branch_3[0]



node_chosen_feat.left.create_layer(root_3_l)
node_chosen_feat.right.create_layer(root_3_r)
error_feat_3 = err_perc(node_chosen_feat)



print('\n-------------------------------\n')
print("The chosen feature for 3rd layer on the left side #", 
      root_3_l)
print('Its information gain value is:', info_gain_l)
#print('Error: ', error_left_3, '%')

print("\n")
print("The chosen feature for 3rd layer on the right side #", 
      root_3_r)
print('Its information gain value is:', info_gain_r)

print('\nError:', error_feat_3, '%')


#------------testing data-------------

file = open('specttest.txt', 'r')
data = file.readlines()
data = data
file.close()

data_list_test = [[int(x) for x in xs.strip().split(",")] for xs in data]


node_test = Node(data_list_test)
node_test.create_layer(root_chosen)
node_train_1st = Node(data_list)
node_train_1st.create_layer(root_chosen)

change_labels(node_train_1st,node_test)
error_layer1 = err_perc(node_test)
info_gain_1 = I(node_test)

node_test.left.create_layer(root_3_l)
node_test.right.create_layer(root_3_r)

change_labels(node_chosen_feat,node_test)
error_test = err_perc(node_test)


print('\n-------------------------------\n')
print("Testing Data:")
print("\nInfo Value for Testing Data:", info_gain_1)
print('\nError on 2 layers:', error_layer1, '%')
print('\nError on 3 layers:', error_test, '%')






