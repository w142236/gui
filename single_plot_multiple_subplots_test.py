# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 00:41:40 2020

@author: willk
"""
import numpy as np

def add(iftruths,eliftruths,elsetruths,sub_arr,type_arr, subplot):
    if 1 in iftruths == True: #Only one of these arrays can have a truth at a time
        print("Passing if detected. subplot: {} in current sub_arr: {}".format(subplot, sub_arr))
        print("\n Now appending subplot: {} to current sub_arr and appending var: {} and plot_type: {} to types dictionary".format(subplot,var,plot_type))
        old_key_store = str(sub_arr) #'[0 0]'
        sub_arr = np.append(sub_arr, subplot) #[0 0] -> [0 0 0]
        new_key_store = str(sub_arr) #'[0 0 0]'
        types[new_key_store] = types.pop(old_key_store) #Replece the key with the updated key and pop the old key
        type_arr = np.append(type_arr, {var:plot_type})
        types[str(new_key_store)] = type_arr
        print("\n New Types dictionary: {}".format(types))
    elif 1 in eliftruths == True:
        print("Passing elif detected. subplot: {} is not in sub_arr: {} nor in old_sub_arr:{}".format(subplot, sub_arr, old_sub_arr))
        print("\n Now resetting sub_arr and appending subplot: {} to it. Also resetting type_arr and appending var: {} and plot_type: {} to it".format(subplot,var,plot_type))
        old_sub_arr[str(sub_arr)] = sub_arr #Store the current sub_arr into the old_sub_arr
        old_type_arr[str(sub_arr)] = type_arr #Same for current type_arr
        sub_arr = np.array([],dtype = np.int) #Reset sub_arr
        sub_arr = np.append(sub_arr, subplot) #Append to now empty sub_arr
        type_arr = np.array([]) #Reset type_arr
        type_arr = np.append(type_arr, {var:plot_type}) #Append to now empty type_arr
        types[str(sub_arr)] = type_arr #Create new dictionary key and contents in types dictionary
        print("\n New Types dictionary: {}".format(types))
    elif 1 in elsetruths == True:
        print("Passing else detected. subplot: {} found in current sub_arr: {} and it is a recurring subplot value found in old_sub_arr:{}".format(subplot, sub_arr, old_sub_arr))
        print("\n Now setting sub_arr to array held in old_sub_arr containing the subplot value and appending subplot: {} to it. \nAlso setting type_arr to one found in old_type_arr and appending var: {} and plot_type: {} to it".format(subplot,var,plot_type))
        for key in old_sub_arr:
            if str(subplot) in key:
                sub_arr = old_sub_arr[key]
                sub_arr = np.append(sub_arr,subplot)
                type_arr = old_type_arr[key]
                type_arr = np.append(type_arr, {var:plot_type})
                types[str(sub_arr)] = types.pop(key)
                types[str(sub_arr)] = type_arr
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

plot_type = "cmap"; subplots = np.array([0,0,0],dtype = np.int); var = 'u' #CHANGE THIS!!!
sub_arr = np.array([],dtype = np.int); type_arr = np.array([]); types = {};old_sub_arr = {'':''};old_type_arr={}
i = 0
#j = 0
iftruths = np.array([],dtype = np.int)
eliftruths = np.array([], dtype = np.int)
elsetruths = np.array([],dtype = np.int)
for subplot in subplots:
    for key in old_sub_arr.copy(): #Prevented it from running through if after elif
        print(key, subplot)
        if str(subplot) not in key and str(subplot) in str(sub_arr): #'0' not in '[]' and '0' in '[0 0]'
            print("IF: subplot: {} not in key: {} and subplot: {} in sub_arr: {}".format(subplot, key, subplot, sub_arr))
            sub_arr, type_arr, old_sub_arr,old_type_arr,types = add(iftruths,eliftruths,elsetruths,sub_arr,type_arr,subplot)
        elif str(subplot) not in key and str(subplot) not in str(sub_arr): #This will always run first. After the initial loop, everything goes through setup() function
            print("ELIF: subplot: {} not in key: {} and subplot: {} not in sub_arr: {}".format(subplot, key, subplot, sub_arr))
            if i == 0: #Initially everything is empty and i represents whether or not the the initial loop has been completed or not. After this point, the initial elif will continue to pass and will run into another elif further down
                sub_arr = np.append(sub_arr, subplot) #During first loop, the current subplot is also the new sub_arr so add it on immediately
                type_arr = np.append(type_arr,{var:plot_type})#Same for type_arr
                if len(sub_arr) > 0: #Skips the empty '' key
                    old_sub_arr[str(sub_arr)] = sub_arr # AND during the first loop, the current subplot is not only the new subplot, but the old subplot as well
                else:
                    pass
                if len(type_arr) > 0:
                    old_type_arr[str(sub_arr)] = type_arr
                else:
                    pass
                type_arr = np.array([])
                type_arr = np.append(type_arr, {var:plot_type})
                types[str(sub_arr)] = type_arr
                print(types)
            else: #Here is where we have to force the for loop to pass until it runs into a key where a condition is met
                if len(key) == 0: #Skips empty '' key
                    print("elifif")
                    pass
                else: #Here we assume that it has run into an actual key
                    print("elifelse")
                    #And that the subplot not in key and subplot not in sub_arr so now we have to reset sub_arr and type_arr after putting the current versions of these into there old counterparts
                    eliftruths = np.append(eliftruths,1)
                    sub_arr, type_arr, old_sub_arr,old_type_arr,types = add(iftruths,eliftruths,elsetruths,sub_arr,type_arr,subplot)
        else: #During the initial looping through the for loop, the sub_arr is both the old_sub_arr and current sub_arr
            if str(subplot) in key and str(subplot) in str(sub_arr): #Runs through this until subplot value changes
                print("ELSE IF: subplot: {} found in old_sub_arr: {} and current sub_arr: {}".format(subplot, key,sub_arr))
                old_key_store = str(sub_arr)
                sub_arr = np.append(sub_arr, subplot)#So we just keep appending to the sub_arr and popping and replacing keys in the old_sub_arr until subplot changes
                old_sub_arr[str(sub_arr)] = old_sub_arr.pop(old_key_store)
                old_sub_arr[str(sub_arr)] = sub_arr
                type_arr = np.append(type_arr, {var:plot_type})#And we do the same with the type_arr and old_type_arr
                old_type_arr[str(sub_arr)] = old_type_arr.pop(old_key_store)
                old_type_arr[str(sub_arr)] = type_arr
                types[str(sub_arr)] = types.pop(old_key_store)
                types[str(sub_arr)] = type_arr
                #and the same goes for type_arr and old_type_arr
            elif str(subplot) in key and str(subplot) not in str(sub_arr): #Once subplot value changes then subplot is in old_sub_arr and no longer in current sub_arr
                print("ELSE ELSE: subplot: {} found in old_sub_arr: {} and not in current sub_arr: {}".format(subplot, key,sub_arr))
                elsetruths = np.append(elsetruths, 1)
                sub_arr, type_arr, old_sub_arr,old_type_arr,types = add(iftruths,eliftruths,elsetruths,sub_arr,type_arr,subplot)
            else:
                print("pass")
                pass

        iftruths = np.array([],dtype = np.int)
        eliftruths = np.array([],dtype = np.int)
        elsetruths = np.array([], dtype = np.int)
        i = i+1
