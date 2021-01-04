# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 00:41:40 2020

@author: willk
"""
import numpy as np

def add(iftruths,eliftruths,elsetruths,sub_arr,type_arr, subplot, var, plot_type):
    if 1 in iftruths == True: #Only one of these arrays can have a truth at a time
        print("Passing if detected. subplot[j]: {} in current sub_arr: {}".format(subplot[j], sub_arr))
        print("\n Now appending subplot[j]: {} to current sub_arr and appending var: {} and plot_type: {} to types dictionary".format(subplot[j],var,plot_type))
        old_key_store = str(sub_arr) #'[0 0]'
        sub_arr = np.append(sub_arr, subplot) #[0 0] -> [0 0 0]
        new_key_store = str(sub_arr) #'[0 0 0]'

        old_sub_arr[new_key_store] = old_sub_arr.pop(old_key_store) #pop and replace old key with new key
        old_sub_arr[new_key_store] = sub_arr #overwrite old content with new content

        type_arr = np.append(type_arr, {var:plot_type})
        old_type_arr[new_key_store] = old_type_arr.pop(old_key_store)
        old_type_arr[new_key_store] = type_arr

        types[new_key_store] = types.pop(old_key_store)
        types[new_key_store] = type_arr
        print("\n New Types dictionary: {}".format(types))
    elif 1 in eliftruths == True: #Since we are dealing with a brand new subplot[j], no popping and replacing needed. We just have to create a new key and content
        print("Passing elif detected. subplot[j]: {} is not in sub_arr: {} nor in old_sub_arr:{}".format(subplot, sub_arr, old_sub_arr))
        print("\n Now resetting sub_arr and appending subplot[j]: {} to it. Also resetting type_arr and appending var: {} and plot_type: {} to it".format(subplot,var,plot_type))

        sub_arr = np.array([],dtype = np.int) #Reset sub_arr
        sub_arr = np.append(sub_arr, subplot) #Append to now empty sub_arr
        type_arr = np.array([]) #Reset type_arr
        type_arr = np.append(type_arr, {var:plot_type}) #Append to now empty type_arr
        types[str(sub_arr)] = type_arr #Create new dictionary key and contents in types dictionary

        old_sub_arr[str(sub_arr)] = sub_arr#Lastly we have to add this instance as a new entry into the dicts of old arrays
        old_type_arr[str(sub_arr)] = type_arr

        print("\n New Types dictionary: {}".format(types))
    elif 1 in elsetruths == True: #Here we have run into an old key, so we have to do popping and replacing
        print("Passing else detected. subplot[j]: {} not found in current sub_arr: {}, but it is a recurring subplot[j] value found in old_sub_arr:{}".format(subplot, sub_arr, old_sub_arr))
        print("\n Now setting sub_arr to array held in old_sub_arr containing the subplot[j] value and appending subplot[j]: {} to it. \nAlso setting type_arr to one found in old_type_arr and appending var: {} and plot_type: {} to it".format(subplot,var,plot_type))
        for key in old_sub_arr:
            if str(subplot) in key:
                sub_arr = old_sub_arr[key]
                old_key_store = str(sub_arr)
                sub_arr = np.append(sub_arr,subplot)
                new_key_store = str(sub_arr)

                old_sub_arr[new_key_store] = old_sub_arr.pop(old_key_store)
                old_sub_arr[new_key_store] = sub_arr

                type_arr = old_type_arr[key]
                type_arr = np.append(type_arr, {var:plot_type})
                old_type_arr[new_key_store] = old_type_arr.pop(old_key_store)
                old_type_arr[new_key_store] = type_arr

                types[new_key_store] = types.pop(old_key_store)
                types[new_key_store] = type_arr
                break
            else:
                pass

        print("\n New Types dictionary: {}".format(types))
    else:
        pass

    #iftruths = np.array([],dtype = np.int) #CANNOT reset locally created arrays from inside of a function created before the declaration
    #eliftruths = np.array([],dtype = np.int)
    #elsetruths = np.array([], dtype = np.int)

    return sub_arr,type_arr,old_sub_arr,old_type_arr,types

def remove():
    return sub_arr, type_arr, old_sub_arr, old_type_arr, types

onoff = np.array(["A", "A","A","A","A","A"]) #A means add, B means removes
plot_type = np.array(["cmap","contours", "cmap", "contours", "cmap", "contours"]); subplot = np.array([0,0,0,1,0,1],dtype = np.int); var = np.array(['u','v','u','v','u','v']) #CHANGE THIS!!!Working:[0],[0 0],[0 1], [0 1 0], [0 0 1], [0 0 1 0], [0 0 1 0 0], [0 0 1 0 1]
sub_arr = np.array([],dtype = np.int); type_arr = np.array([]); types = {};old_sub_arr = {'':''};old_type_arr={}
i = 0
#j = 0
iftruths = np.array([],dtype = np.int)
eliftruths = np.array([], dtype = np.int)
elsetruths = np.array([],dtype = np.int)

for j in range(len(subplot)):
    if onoff[j] == "A":
        for key in old_sub_arr.copy(): #Prevented it from running through if after elif
            print(key, subplot[j])
            if str(subplot[j]) not in key and str(subplot[j]) in str(sub_arr): #'0' not in '[]' and '0' in '[0 0]'
                print("IF: subplot[j]: {} not in key: {} and subplot[j]: {} in sub_arr: {}".format(subplot[j], key, subplot[j], sub_arr))
                sub_arr, type_arr, old_sub_arr,old_type_arr,types = add(iftruths,eliftruths,elsetruths,sub_arr,type_arr,subplot[j], var[j], plot_type[j])
            elif str(subplot[j]) not in key and str(subplot[j]) not in str(sub_arr): #This will always run first. After the initial loop
                print("ELIF: subplot[j]: {} not in key: {} and subplot[j]: {} not in sub_arr: {}".format(subplot[j], key, subplot[j], sub_arr))
                if i == 0: #Initially everything is empty and i represents whether or not the the initial loop has been completed or not. After this point, the initial elif will continue to pass and will run into another elif further down
                    sub_arr = np.append(sub_arr, subplot[j]) #During first loop, the current subplot[j] is also the new sub_arr so add it on immediately
                    type_arr = np.append(type_arr,{var[j]:plot_type[j]})#Same for type_arr
                    if len(sub_arr) > 0: #Skips the empty '' key
                        old_sub_arr[str(sub_arr)] = sub_arr # AND during the first loop, the current subplot[j] is not only the new subplot[j], but the old subplot[j] as well. No need for popping
                    else:
                        pass
                    if len(type_arr) > 0:
                        old_type_arr[str(sub_arr)] = type_arr #No need for popping yet
                    else:
                        pass
                    type_arr = np.array([])
                    type_arr = np.append(type_arr, {var[j]:plot_type[j]})
                    types[str(sub_arr)] = type_arr #No need for popping yet
                    print(types)
                else: #Here is where we have to force the for loop to pass until it runs into a key where a condition is met
                    if len(key) == 0: #Skips empty '' key
                        print("elifif")
                        pass
                    else: #Here we assume that it has run into an actual key
                        print("elifelse")
                        #And that the subplot[j] not in key and subplot[j] not in sub_arr so now we have to reset sub_arr and type_arr after putting the current versions of these into there old counterparts
                        eliftruths = np.append(eliftruths,1)
                        sub_arr, type_arr, old_sub_arr,old_type_arr,types = add(iftruths,eliftruths,elsetruths,sub_arr,type_arr,subplot[j], var[j], plot_type[j])
            else: #During the initial looping through the for loop, the sub_arr is both the old_sub_arr and current sub_arr
                if str(subplot[j]) in key and str(subplot[j]) in str(sub_arr): #Runs through this until subplot[j] value changes
                    print("ELSE IF: subplot[j]: {} found in old_sub_arr: {} and current sub_arr: {}".format(subplot[j], key,sub_arr))
                    old_key_store = str(sub_arr)
                    sub_arr = np.append(sub_arr, subplot[j])#So we just keep appending to the sub_arr and popping and replacing keys in the old_sub_arr until subplot[j] changes
                    old_sub_arr[str(sub_arr)] = old_sub_arr.pop(old_key_store)
                    old_sub_arr[str(sub_arr)] = sub_arr
                    type_arr = np.append(type_arr, {var[j]:plot_type[j]})#And we do the same with the type_arr and old_type_arr
                    old_type_arr[str(sub_arr)] = old_type_arr.pop(old_key_store)
                    old_type_arr[str(sub_arr)] = type_arr
                    types[str(sub_arr)] = types.pop(old_key_store)
                    types[str(sub_arr)] = type_arr
                    #and the same goes for type_arr and old_type_arr
                elif str(subplot[j]) in key and str(subplot[j]) not in str(sub_arr): #Once subplot[j] value changes then subplot[j] is in old_sub_arr and no longer in current sub_arr
                    print("ELSE ELSE: subplot[j]: {} found in old_sub_arr: {} and not in current sub_arr: {}".format(subplot[j], key,sub_arr))
                    elsetruths = np.append(elsetruths, 1)
                    sub_arr, type_arr, old_sub_arr,old_type_arr,types = add(iftruths,eliftruths,elsetruths,sub_arr,type_arr,subplot[j], var[j], plot_type[j])
                else:
                    print("pass")
                    pass

            iftruths = np.array([],dtype = np.int)
            eliftruths = np.array([],dtype = np.int)
            elsetruths = np.array([], dtype = np.int)
            i = i+1
    else:
        pass
