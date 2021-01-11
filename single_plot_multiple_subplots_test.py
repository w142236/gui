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
                print("\ntype_arr: {} now being set to old_type_arr: {} of key: {} \n".format(type_arr, old_type_arr, key))
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

onoff = np.array(["A","A","A","B","A","A","B","A"]) #A means add, B means removes ["A","A","A","B","A","A","B","A"]
plot_type = np.array(["cmap","cmap","contours","contours","contours","contours","contours","contours"]) #["cmap","cmap","contours","contours","contours","contours","contours","contours"]
subplot = np.array([0,1,0,0,0,1,0,0],dtype = np.int) #[0,1,0,0,0,1,0,0]
var = np.array(['u','u','u','u','u','u','u','u']) #CHANGE THIS!!!Working:['u','u','u','u','u','u','u','u']
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
                print("IF: subplot: {} not in key: {} and subplot[j]: {} in sub_arr: {}".format(subplot[j], key, subplot[j], sub_arr))
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
                else: #Here is where we have to force the for loop to pass until it runs into a key where a condition is met.
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

    else: #Here the user wants to remove a key. When a button is pressed it is GOING TO exist within the sub_arr and old_sub_arr dict
        if len(sub_arr) == 0: #If after deleting from sub_arr we end up with an empty array, we need to set it to something from the old_sub_arr
            print("\nCurrent size of sub_arr is 0. Need to update sub_arr to non zero array from old_sub_arr")
            for arr in old_sub_arr:
                if str(subplot[j]) in arr: #if the subplot to remove from is in this array, then we set sub_arr to that array
                    print("found subplot: {} in array: {}\n Now setting sub_arr to: {}".format(subplot[j], arr, arr))
                    sub_arr = old_sub_arr[arr]
                    #we also assume that type_arr is empty now too
                    type_arr = old_type_arr[str(sub_arr)]
                    print("sub_arr: {}\nold_sub_arr: {}\nold_type_arr:{}".format(sub_arr, old_sub_arr, old_type_arr))
        print("\nRequest to delete key and info from: \ntypes: {} detected. \nWill now remove subplot: {} from sub_arr: {} and old_sub_arr: {}".format(types, subplot[j], sub_arr, old_sub_arr))
        print("will now check if subplot: {} is in sub_arr: {}".format(subplot[j],sub_arr))
        if str(subplot[j]) in str(sub_arr): #First we need to check to see if the subplot is in the current sub_arr
            print("\nUndesired data associated with subplot: {} found in current sub_arr: {}\nWill now delete instance from sub_arr and old_sub_arr keys".format(subplot[j], sub_arr))
            old_key_store = str(sub_arr) #This will be used later
            #Now we search through types and find the exact thing to delete
            #sub_arr = np.delete(sub_arr, 0) #we can just delete any of them, but we cannot just delete without checking to see if the item to delete exists first
            for arr in old_type_arr.copy():#Here we check to see if the exact data to delete exists. In a gui it should, but we're doing this so the test program runs properly
                if str(subplot[j]) in arr: #Is the subplot even in the current arr in the dictionary? If not we skip it
                    print("sub_arr in old_type_arr: {} found!\n Now searching for matching var and plot_type in old_type_arr associated with this sub_arr...".format(old_type_arr))
                    for dic in old_type_arr.copy()[arr]:
                        for key in dic:
                            if var[j] in key and plot_type[j] in dic[key]: #Does the variable match the one dic AND does the plot type match the info attached to that key?
                                #Since it is in the current sub_arr and type_arr, we update these first
                                print("var: {} and plot_type: {} found in old_type_arr: {}\nNow creating new keys and info to replace into types: {}\n".format(var[j], plot_type[j], old_type_arr, types))
                                old_key_store = sub_arr

                                sub_arr = np.delete(sub_arr, 0) #We can just delete wherever
                                print("after sub_arr:{}".format(sub_arr))
                                old_sub_arr[str(sub_arr)] = old_sub_arr.pop(str(old_key_store))
                                old_sub_arr[str(sub_arr)] = sub_arr

                                type_arr = np.delete(type_arr, np.where(type_arr == {var[j]:plot_type[j]}))
                                old_type_arr[str(sub_arr)] = old_type_arr.pop(str(old_key_store))
                                old_type_arr[str(sub_arr)] = type_arr

                                types[str(sub_arr)] = types.pop(str(old_key_store))
                                types[str(sub_arr)] = type_arr
                                break
                else:
                    pass
            if len(sub_arr) > 0:
                print("\nTypes dictionary successfully updated using new keys: {} and info: {}\nTypes:{}\n".format(sub_arr, type_arr, types))
            else:
                print("\nNew key: {} and associated info: {} to replace into types dictionary are empty and will therefore be completely removed".format(sub_arr, type_arr))
                old_sub_arr.pop(str(sub_arr))
                old_type_arr.pop(str(sub_arr))
                types.pop(str(sub_arr))
                print("Types dictionary successfully updated by completely removing empty keys and data\nTypes: {}\n".format(types))
                i = 0

        elif str(subplot[j]) not in str(sub_arr): #Here we can assume that it is referring back to an old point in types and not the most recent one in sub_arr
            print("Undesired data associated with subplot: {} only found in old_sub_arr: {} and not in current sub_arr: {} \nWill now delete instance from old_sub_arr".format(subplot[j], old_sub_arr, sub_arr))

            old_key_store = sub_arr #[1 1] sub_arr will be reset to this after everything is finished
            for key in old_sub_arr: #first We need to replace the current sub_arr with the old_sub_arr array
                if str(subplot[j]) in key:
                    sub_arr = old_sub_arr[key]
                    break
            old_old_key_store = sub_arr #[0 0]
            sub_arr = np.delete(sub_arr, 0) #we can delete any of the elements, position should not matter
            #Now we have to reset the type_arr to the old_type_arr and update both
            itervar = 0
            for arr in old_type_arr.copy(): #This searches through the old_type_arr and updates it
                if str(subplot[j]) in arr:
                    print("\nsubplot: {} found in old_type_arr in key: {}".format(subplot[j],arr))
                    itervar = itervar+1 #break would not work, so this prevents unnecessary looping
                    for dic in old_type_arr[arr]:
                        for key in dic:
                            if var[j] in key and plot_type[j] in dic[key] and itervar==1:
                                type_arr = old_type_arr[arr] #set type_arr to old array of dicts
                                old_type_key = type_arr
                                type_arr = np.delete(type_arr, np.where(type_arr == {var[j]:plot_type[j]}))
                                old_type_arr[str(sub_arr)] = old_type_arr.pop(str(old_old_key_store))
                                old_sub_arr[str(sub_arr)] = old_sub_arr.pop(str(old_old_key_store))
                                old_sub_arr[str(sub_arr)] = sub_arr
                                #Then we take the updated type_arr and sub_arr and remove the keys in types and replace them with these
                                types[str(sub_arr)] = types.pop(str(old_old_key_store))
                                types[str(sub_arr)] = type_arr
                                #Lastly, we reset the the sub_arr and type_arr to their previous versions
                                sub_arr = old_key_store
                                type_arr = old_type_key

                else:
                    pass
            if len(sub_arr) > 0:
                print("\nFinished removing undesired data. \nTypes now in form: {}".format(types))
            else:
                print("\nArray: {} is empty, now popping empty key".format(sub_arr))
                types.pop(str(sub_arr))
                print("Successfully popped empty key from types dict.\nTypes now has form: {}".format(types))
        else:
            print("ERROR! var: {} and plot type: {} not found in {}".format(var[j], plot_type[j], types))
