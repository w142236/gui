# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 00:41:40 2020

@author: willk
"""
import numpy as np

plot_type = "cmap"; subplot = 0; var = 'u' #CHANGE THIS!!!
sub_arr = np.array([],dtype = np.int); type_arr = np.array([]); types = {};old_sub_arr = {'':''};old_type_arr={}

for key in old_sub_arr.copy():
    if str(subplot) not in key and str(subplot) in str(sub_arr): #'0' not in '[]' and '0' in '[0 0]'
        print("if")
        old_key_store = str(sub_arr) #'[0 0]'
        sub_arr = np.append(sub_arr, subplot) #[0 0 0]
        new_key_store = str(sub_arr) #'[0 0 0]'
        print("new key: {}".format(new_key_store))
        types[new_key_store] = types.pop(old_key_store) #Replece the key with the updated key and pop the old key
        type_arr = np.append(type_arr, {var:plot_type})
        print("type_arr: {}".format(type_arr))
        types[str(new_key_store)] = type_arr
        print("types: {}".format(types))
    elif str(subplot) not in key and str(subplot) not in str(sub_arr): #'1' not in '[]' and '1' not in '[0 0]'
        print("elif")
        old_sub_arr[str(sub_arr)] = sub_arr #self.old_sub_arr = {'[0 0]': [0 0]}
        sub_arr = np.array([], dtype = np.int)
        sub_arr = np.append(sub_arr, subplot)
        old_type_arr[str(type_arr)] = type_arr
        type_arr = np.array([])
        type_arr = np.append(type_arr, {var:plot_type})
        types[str(sub_arr)] = type_arr
    else: #HAS TO RUN THROUGH THIS IF we go back from subplot = 1 to subplot = 0
        print("else")
        old_key_store = key #old_key = '[0 0]' We can refer to and pop this key in self.types
        sub_arr = np.append(old_sub_arr[key], subplot) #self.sub_arr = [0, 0] + [0] = [0, 0, 0]
        new_key_store = str(sub_arr)
        types[new_key_store] = types.pop(old_key_store)
        new_types_arr = types[new_key_store]
        new_types_arr = np.append(new_types_arr, {var:plot_type})
        types[new_key_store] = new_types_arr

print("old_sub_arr: {}".format(old_sub_arr))
print("old_type_arr: {}".format(old_type_arr))
print("types: {}".format(types))