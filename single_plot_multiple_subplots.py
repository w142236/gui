# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 23:45:23 2020

@author: willk
"""
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from tkinter.filedialog import askopenfile
import PIL.Image
import PIL.ImageTk
import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

class single_multiple:
    def __init__(self, fh,  xx, yy, choices, vars_to_plot, subplots):
        self.gui = Toplevel()
        self.fh = fh
        self.xx = xx
        self.yy = yy
        self.choices = choices
        self.vars_to_plot = vars_to_plot
        self.type1 = StringVar()
        self.type2 = StringVar()
        self.type3 = StringVar()
        self.cmap = {} #Need to change into a dictionary of arrays for each subplot
        self.contours = {} #Need to change into a dictionary of arrays for each subplot
        self.barbs = {} #Need to change into a dictionary of arrays for each subplot
        self.i = 0
        self.iter = 0
        self.subplots = subplots

        self.axes = {}
        self.vars_to_subplot = {}
        self.sub_choices = {}
        for i in range(self.subplots):
            self.vars_to_subplot[i] = np.array([])
            self.sub_choices[i] = np.array([])

        self.types = {}
        self.sub_arr = np.array([], dtype=np.int)
        self.old_sub_arr = {'':''}
        self.type_arr = np.array([], dtype=np.int)
        self.old_type_arr = {}
        self.temp_type_arr = np.array([])
        self.types[str(self.sub_arr)] = self.type_arr
    def choose_vars(self):
        self.subplot_checkboxes = {}
        self.text = {}
        for i in range(self.subplots):
            T = Text(self.gui, height = 2, width = 40)
            T.pack()
            T.insert(END, "Pick variable(s) to use in subplot {}".format(i+1))
            for var in self.vars_to_plot:
                self.text[i] = {var : StringVar()}
                                                   #0: {u : StringVar()}
                                                   #0: {v: StringVar()}
                                                   #1: {u: StringVar()}
                                                   #1: {v: StringVar()}
                self.subplot_checkboxes[i] = Checkbutton(self.gui, text = var, variable = self.text[i][var],onvalue = 'A', offvalue = 'B',
                                                         command = lambda var = var,
                                                         subplot = i,
                                                         onoff = self.text[i][var]: self.store_vars(subplot,var,onoff)).pack()

        pick_types_button = Button(self.gui, text = "Pick plot types for each variable", command = lambda : self.pick_types()).pack()





    def store_vars(self, subplot, var, onoff):
        #print(subplot, var, onoff.get())
        if onoff.get() == 'A':
            self.vars_to_subplot[subplot] = np.append(self.vars_to_subplot[subplot], {var: var}) #vars_to_subplot = {0 : [{'u':values}]}
        elif onoff.get() == 'B':
            print(len(self.vars_to_subplot[subplot]))
            for i in range(len(self.vars_to_subplot[subplot])):
                try:
                    for key in self.vars_to_subplot[subplot][i]:
                        if key == var:
                            self.vars_to_subplot[subplot] = np.delete(self.vars_to_subplot[subplot],
                                                                      np.where(self.vars_to_subplot[subplot] == {var:var}))#TODO replace with var values
                except:
                    pass #Gets past the i out of range issue
        print(self.vars_to_subplot)

    def pick_types(self):
        self.sub_checkboxes = {}
        self.subtext = {}
        self.i = 1
        self.j = 1
        for subplot in self.vars_to_subplot:
            T = Text(self.gui, height = 2, width = 40)
            T.pack()
            T.insert(END, "Pick plot type(s) to use for variables corresponding to subplot: {}".format(subplot+1))
            for element in self.vars_to_subplot[subplot]:
                for var in element:
                    T = Text(self.gui, height = 2, width = 40)
                    T.pack()
                    T.insert(END, "Pick plot type(s) to use for {}".format(var))

                    for choice in self.choices:

                        if choice == 'a':
                            self.subtext[self.j] = {subplot:StringVar()}
                            self.sub_checkboxes[self.i] = Checkbutton(self.gui, text = 'cmap', variable = self.subtext[self.j][subplot],
                                                              onvalue = 'A', offvalue = 'B',
                                                              command = lambda onoff = self.subtext[self.j][subplot],
                                                              plot_type = 'cmap',
                                                              subplot = subplot,
                                                              var = var: self.store_types(onoff,plot_type, subplot, var))
                            self.sub_checkboxes[self.i].pack()
                            self.j = self.j+1
                        elif choice == 'b':
                            self.subtext[self.j] = {subplot:StringVar()}
                            self.sub_checkboxes[self.i] = Checkbutton(self.gui, text = 'contours', variable = self.subtext[self.j][subplot],
                                                              onvalue = 'A', offvalue = 'B',
                                                              command = lambda onoff = self.subtext[self.j][subplot],
                                                              plot_type = 'contours',
                                                              subplot = subplot,
                                                              var = var: self.store_types(onoff,plot_type,subplot, var))
                            self.sub_checkboxes[self.i].pack()
                            self.j = self.j+1
                        elif choice == 'c':
                            self.subtext[self.j] = {subplot:StringVar()}
                            self.sub_checkboxes[self.i] = Checkbutton(self.gui, text = 'barbs', variable = self.subtext[self.j][subplot],
                                                              onvalue = 'A', offvalue = 'B',
                                                              command = lambda onoff = self.subtext[self.j][subplot],
                                                              plot_type = 'barbs',
                                                              subplot = subplot,
                                                              var = var: self.store_types(onoff,plot_type,subplot, var))
                            self.sub_checkboxes[self.i].pack()
                            self.j = self.j+1
                        else:
                            pass

                    self.i = self.i+1
        #print('subtext = {}'.format(self.subtext))
        self.i = 1
        self.j = 1
        plot_button = Button(self.gui, text = "Plot", command = lambda: self.plot())
        plot_button.pack()

    def add(self,iftruths,eliftruths,elsetruths, subplot, var, plot_type):
        if 1 in iftruths == True: #Only one of these arrays can have a truth at a time
            print("Passing if detected. subplot[j]: {} in current sub_arr: {}".format(subplot, self.sub_arr))
            print("\n Now appending subplot[j]: {} to current sub_arr and appending var: {} and plot_type: {} to types dictionary".format(subplot,var,plot_type))
            old_key_store = str(self.sub_arr) #'[0 0]'
            self.sub_arr = np.append(self.sub_arr, subplot) #[0 0] -> [0 0 0]
            new_key_store = str(self.sub_arr) #'[0 0 0]'

            self.old_sub_arr[new_key_store] = self.old_sub_arr.pop(old_key_store) #pop and replace old key with new key
            self.old_sub_arr[new_key_store] = self.sub_arr #overwrite old content with new content

            self.type_arr = np.append(self.type_arr, {var:plot_type})
            self.old_type_arr[new_key_store] = self.old_type_arr.pop(old_key_store)
            self.old_type_arr[new_key_store] = self.type_arr

            self.types[new_key_store] = self.types.pop(old_key_store)
            self.types[new_key_store] = self.type_arr
            print("\n New Types dictionary: {}".format(self.types))
        elif 1 in eliftruths == True: #Since we are dealing with a brand new subplot, no popping and replacing needed. We just have to create a new key and content
            print("Passing elif detected. subplot[j]: {} is not in sub_arr: {} nor in old_sub_arr:{}".format(subplot, self.sub_arr, self.old_sub_arr))
            print("\n Now resetting sub_arr and appending subplot[j]: {} to it. Also resetting type_arr and appending var: {} and plot_type: {} to it".format(subplot,var,plot_type))

            self.sub_arr = np.array([],dtype = np.int) #Reset sub_arr
            self.sub_arr = np.append(self.sub_arr, subplot) #Append to now empty sub_arr
            self.type_arr = np.array([]) #Reset type_arr
            self.type_arr = np.append(self.type_arr, {var:plot_type}) #Append to now empty type_arr
            self.types[str(self.sub_arr)] = self.type_arr #Create new dictionary key and contents in types dictionary

            self.old_sub_arr[str(self.sub_arr)] = self.sub_arr#Lastly we have to add this instance as a new entry into the dicts of old arrays
            self.old_type_arr[str(self.sub_arr)] = self.type_arr

            print("\n New Types dictionary: {}".format(self.types))
        elif 1 in elsetruths == True: #Here we have run into an old key, so we have to do popping and replacing
            print("Passing else detected. subplot: {} not found in current sub_arr: {}, but it is a recurring subplot value found in old_sub_arr:{}".format(subplot, self.sub_arr, self.old_sub_arr))
            print("\n Now setting sub_arr to array held in old_sub_arr containing the subplot value and appending subplot: {} to it. \nAlso setting type_arr to one found in old_type_arr and appending var: {} and plot_type: {} to it".format(subplot,var,plot_type))
            for key in self.old_sub_arr:
                if str(subplot) in key:
                    self.sub_arr = self.old_sub_arr[key]
                    old_key_store = str(self.sub_arr)
                    self.sub_arr = np.append(self.sub_arr,subplot)
                    new_key_store = str(self.sub_arr)

                    self.old_sub_arr[new_key_store] = self.old_sub_arr.pop(old_key_store)
                    self.old_sub_arr[new_key_store] = self.sub_arr
                    print("\ntype_arr: {} now being set to old_type_arr: {} of key: {} \n".format(self.type_arr, self.old_type_arr, key))
                    self.type_arr = self.old_type_arr[key]

                    self.type_arr = np.append(self.type_arr, {var:plot_type})
                    self.old_type_arr[new_key_store] = self.old_type_arr.pop(old_key_store)
                    self.old_type_arr[new_key_store] = self.type_arr

                    self.types[new_key_store] = self.types.pop(old_key_store)
                    self.types[new_key_store] = self.type_arr
                    break
                else:
                    pass

            print("\n New Types dictionary: {}".format(self.types))
        else:
            pass

    #iftruths = np.array([],dtype = np.int) #CANNOT reset locally created arrays from inside of a function created before the declaration
    #eliftruths = np.array([],dtype = np.int)
    #elsetruths = np.array([], dtype = np.int)


    def store_types(self, onoff, plot_type, subplot, var):
        onoff = onoff.get()
        iftruths = np.array([],dtype = np.int)
        eliftruths = np.array([], dtype = np.int)
        elsetruths = np.array([],dtype = np.int)
                    #TODO Have to do something with self.types
        if onoff == "A":
            for key in self.old_sub_arr.copy(): #Prevented it from running through if after elif
                print(key, subplot)
                if str(subplot) not in key and str(subplot) in str(self.sub_arr): #'0' not in '[]' and '0' in '[0 0]'
                    print("IF: subplot: {} not in key: {} and subplot[j]: {} in sub_arr: {}".format(subplot, key, subplot, self.sub_arr))
                    self.add(iftruths, eliftruths, elsetruths, subplot, var, plot_type)
                elif str(subplot) not in key and str(subplot) not in str(self.sub_arr): #This will always run first. After the initial loop
                    print("ELIF: subplot: {} not in key: {} and subplot[j]: {} not in sub_arr: {}".format(subplot, key, subplot, self.sub_arr))
                    if self.iter == 0: #Initially everything is empty and i represents whether or not the the initial loop has been completed or not. After this point, the initial elif will continue to pass and will run into another elif further down
                        self.sub_arr = np.append(self.sub_arr, subplot) #During first loop, the current subplot[j] is also the new sub_arr so add it on immediately
                        self.type_arr = np.append(self.type_arr,{var:plot_type})#Same for type_arr
                        if len(self.sub_arr) > 0: #Skips the empty '' key
                            self.old_sub_arr[str(self.sub_arr)] = self.sub_arr # AND during the first loop, the current subplot[j] is not only the new subplot[j], but the old subplot[j] as well. No need for popping
                        else:
                            pass
                        if len(self.type_arr) > 0:
                            self.old_type_arr[str(self.sub_arr)] = self.type_arr #No need for popping yet
                        else:
                            pass
                        self.type_arr = np.array([])
                        self.type_arr = np.append(self.type_arr, {var:plot_type})
                        self.types[str(self.sub_arr)] = self.type_arr #No need for popping yet
                        print(self.types)
                    else: #Here is where we have to force the for loop to pass until it runs into a key where a condition is met
                        if len(key) == 0: #Skips empty '' key
                            print("elifif")
                            pass
                        else: #Here we assume that it has run into an actual key
                            print("elifelse")
                            #And that the subplot not in key and subplot not in sub_arr so now we have to reset sub_arr and type_arr after putting the current versions of these into there old counterparts
                            eliftruths = np.append(eliftruths,1)
                            self.add(iftruths, eliftruths,elsetruths,subplot,var,plot_type)
                else: #During the initial looping through the for loop, the sub_arr is both the old_sub_arr and current sub_arr
                    if str(subplot) in key and str(subplot) in str(self.sub_arr): #Runs through this until subplot[j] value changes
                        print("ELSE IF: subplot[j]: {} found in old_sub_arr: {} and current sub_arr: {}".format(subplot, key,self.sub_arr))
                        old_key_store = str(self.sub_arr)
                        self.sub_arr = np.append(self.sub_arr, subplot)#So we just keep appending to the sub_arr and popping and replacing keys in the old_sub_arr until subplot[j] changes
                        self.old_sub_arr[str(self.sub_arr)] = self.old_sub_arr.pop(old_key_store)
                        self.old_sub_arr[str(self.sub_arr)] = self.sub_arr
                        self.type_arr = np.append(self.type_arr, {var:plot_type})#And we do the same with the type_arr and old_type_arr
                        self.old_type_arr[str(self.sub_arr)] = self.old_type_arr.pop(old_key_store)
                        self.old_type_arr[str(self.sub_arr)] = self.type_arr
                        self.types[str(self.sub_arr)] = self.types.pop(old_key_store)
                        self.types[str(self.sub_arr)] = self.type_arr
                        #and the same goes for type_arr and old_type_arr
                    elif str(subplot) in key and str(subplot) not in str(self.sub_arr): #Once subplot[j] value changes then subplot[j] is in old_sub_arr and no longer in current sub_arr
                        print("ELSE ELSE: subplot[j]: {} found in old_sub_arr: {} and not in current sub_arr: {}".format(subplot, key, self.sub_arr))
                        elsetruths = np.append(elsetruths, 1)
                        self.add(iftruths,eliftruths,elsetruths,subplot, var, plot_type)
                    else:
                        print("pass")
                        pass
                iftruths = np.array([],dtype = np.int)
                eliftruths = np.array([],dtype = np.int)
                elsetruths = np.array([], dtype = np.int)
                self.iter = self.iter+1



        elif onoff == 'B': #Everything in commented out is a work in progress
            if len(self.sub_arr) == 0: #If after deleting from sub_arr we end up with an empty array, we need to set it to something from the old_sub_arr
                print("\nCurrent size of sub_arr is 0. Need to update sub_arr to non zero array from old_sub_arr")
                for arr in self.old_sub_arr:
                    if str(subplot) in arr: #if the subplot to remove from is in this array, then we set sub_arr to that array
                        print("found subplot: {} in array: {}\n Now setting sub_arr to: {}".format(subplot, arr, arr))
                        self.sub_arr = self.old_sub_arr[arr]
                        #we also assume that type_arr is empty now too
                        self.type_arr = self.old_type_arr[str(self.sub_arr)]
                        print("sub_arr: {}\nold_sub_arr: {}\nold_type_arr:{}".format(self.sub_arr, self.old_sub_arr, self.old_type_arr))
            print("\nRequest to delete key and info from: \ntypes: {} detected. \nWill now remove subplot: {} from sub_arr: {} and old_sub_arr: {}".format(self.types, subplot, self.sub_arr, self.old_sub_arr))
            print("will now check if subplot: {} is in sub_arr: {}".format(subplot,self.sub_arr))
            if str(subplot) in str(self.sub_arr): #First we need to check to see if the subplot is in the current sub_arr
                print("\nUndesired data associated with subplot: {} found in current sub_arr: {}\nWill now delete instance from sub_arr and old_sub_arr keys".format(subplot, self.sub_arr))
                old_key_store = str(self.sub_arr) #This will be used later
                #Now we search through types and find the exact thing to delete
                #sub_arr = np.delete(sub_arr, 0) #we can just delete any of them, but we cannot just delete without checking to see if the item to delete exists first
                for arr in self.old_type_arr.copy():#Here we check to see if the exact data to delete exists. In a gui it should, but we're doing this so the test program runs properly
                    if str(subplot) in arr: #Is the subplot even in the current arr in the dictionary? If not we skip it
                        print("sub_arr in old_type_arr: {} found!\n Now searching for matching var and plot_type in old_type_arr associated with this sub_arr...".format(self.old_type_arr))
                        for dic in self.old_type_arr.copy()[arr]:
                            print(type(dic))
                            for key in dic:
                                if var in key and plot_type in dic[key]: #Does the variable match the one dic AND does the plot type match the info attached to that key?
                                    #Since it is in the current sub_arr and type_arr, we update these first
                                    print("var: {} and plot_type: {} found in old_type_arr: {}\nNow creating new keys and info to replace into types: {}\n".format(var, plot_type, self.old_type_arr, self.types))
                                    old_key_store = self.sub_arr

                                    self.sub_arr = np.delete(self.sub_arr, 0) #We can just delete wherever
                                    print("after sub_arr:{}".format(self.sub_arr))
                                    self.old_sub_arr[str(self.sub_arr)] = self.old_sub_arr.pop(str(old_key_store))
                                    self.old_sub_arr[str(self.sub_arr)] = self.sub_arr

                                    self.type_arr = np.delete(self.type_arr, np.where(self.type_arr == {var:plot_type}))
                                    self.old_type_arr[str(self.sub_arr)] = self.old_type_arr.pop(str(old_key_store))
                                    self.old_type_arr[str(self.sub_arr)] = self.type_arr

                                    self.types[str(self.sub_arr)] = self.types.pop(str(old_key_store))
                                    self.types[str(self.sub_arr)] = self.type_arr
                                    break
                    else:
                        pass
                if len(self.sub_arr) > 0:
                    print("\nTypes dictionary successfully updated using new keys: {} and info: {}\nTypes:{}\n".format(self.sub_arr, self.type_arr, self.types))
                else:
                    print("\nNew key: {} and associated info: {} to replace into types dictionary are empty and will therefore be completely removed".format(self.sub_arr, self.type_arr))
                    self.old_sub_arr.pop(str(self.sub_arr))
                    self.old_type_arr.pop(str(self.sub_arr))
                    self.types.pop(str(self.sub_arr))
                    print("Types dictionary successfully updated by completely removing empty keys and data\nTypes: {}\n".format(self.types))
                    self.iter = 0
            elif str(subplot) not in str(self.sub_arr): #Here we can assume that it is referring back to an old point in types and not the most recent one in sub_arr
                print("Undesired data associated with subplot: {} only found in old_sub_arr: {} and not in current sub_arr: {} \nWill now delete instance from old_sub_arr".format(subplot, self.old_sub_arr, self.sub_arr))

                old_key_store = self.sub_arr #[1 1] sub_arr will be reset to this after everything is finished
                for key in self.old_sub_arr: #first We need to replace the current sub_arr with the old_sub_arr array
                    if str(subplot) in key:
                        self.sub_arr = self.old_sub_arr[key]
                        break
                old_old_key_store = self.sub_arr #[0 0]
                self.sub_arr = np.delete(self.sub_arr, 0) #we can delete any of the elements, position should not matter
                #Now we have to reset the type_arr to the old_type_arr and update both
                itervar = 0
                for arr in self.old_type_arr.copy(): #This searches through the old_type_arr and updates it
                    if str(subplot) in arr:
                        itervar = itervar+1 #break would not work, so this prevents unnecessary looping
                        for dic in self.old_type_arr[arr]:
                            for key in dic:
                                if var in key and plot_type in dic[key] and itervar==1:
                                    self.type_arr = self.old_type_arr[arr] #set type_arr to old array of dicts
                                    old_type_key = self.type_arr
                                    self.type_arr = np.delete(self.type_arr, np.where(self.type_arr == {var:plot_type}))
                                    self.old_type_arr[str(self.sub_arr)] = self.old_type_arr.pop(str(old_old_key_store))
                                    self.old_sub_arr[str(self.sub_arr)] = self.old_sub_arr.pop(str(old_old_key_store))
                                    self.old_sub_arr[str(self.sub_arr)] = self.sub_arr
                                    #Then we take the updated type_arr and sub_arr and remove the keys in types and replace them with these
                                    self.types[str(self.sub_arr)] = self.types.pop(str(old_old_key_store))
                                    self.types[str(self.sub_arr)] = self.type_arr
                                    #Lastly, we reset the the sub_arr and type_arr to their previous versions
                                    self.sub_arr = old_key_store
                                    self.type_arr = old_type_key
                    else:
                        pass
                if len(self.sub_arr) > 0:
                    print("\nFinished removing undesired data. \nTypes now in form: {}".format(self.types))
                else:
                    print("\nArray: {} is empty, now popping empty key".format(self.sub_arr))
                    self.types.pop(str(self.sub_arr))
                    print("Successfully popped empty key from types dict.\nTypes now has form: {}".format(self.types))
            else:
                print("ERROR! var: {} and plot type: {} not found in {}".format(var, plot_type, self.types))
    def plot(self):
        ax = {}
        fig = plt.figure(figsize = (16,9))
        for key in self.types.copy(): #First we delete any empty keys
            if len(self.types[key]) == 0:
                self.types.pop(key)
        i = 0
        for key in sorted(self.types.keys()):
            if i == len(self.types) - 1:
                nrows = int(key[1]) + 1
            i = i+1
        #axs = fig.subplots(nrows, subplot_kw = {'projection':ccrs.PlateCarree()})
        i = 0
        j = 0 #this is only used for barbs
        for key in sorted(self.types.keys()):#Then we go in order of the numeric values in the keys
            print(key[1], nrows)
            ax['ax{}'.format(i+1)] = fig.add_subplot('{}1{}'.format(nrows,i+1), projection=ccrs.PlateCarree())
            ax['ax{}'.format(i+1)].coastlines()
            ax['ax{}'.format(i+1)].axis(xmin = np.min(self.xx) - 359, xmax = np.max(self.xx)-359, ymin = np.min(self.yy), ymax = np.max(self.yy))

            #And lastly, we go through the self.types dictionary and plot using the plot_type and variable

            for dic in self.types[key]:
                for key in dic:
                    var_to_plot = key
                    plot_type = dic[key]
                    if plot_type == 'cmap':
                        var_to_plot = self.fh.variables[var_to_plot][:]
                        cmap = ax['ax{}'.format(i+1)].pcolormesh(self.xx,self.yy, var_to_plot[0])
                    elif plot_type == 'contours':
                        var_to_plot = self.fh.variables[var_to_plot][:]
                        contours = ax['ax{}'.format(i+1)].contour(self.xx, self.yy, var_to_plot[0])
                    elif plot_type == 'barbs':
                        if 'u' in var_to_plot:
                            u = self.fh.variables[var_to_plot][:]
                        elif 'v' in var_to_plot:
                            v = self.fh.variables[var_to_plot][:]
                        else:
                            print("ERROR! Cannot use this variable to plot barbs")
                            break
                        if j == 0: #then we only have 1 of two vars needed
                            pass
                        else:
                            #Here we plot
                            barbs = ax['ax{}'.format(i+1)].barbs(self.xx[::20,::20], self.yy[::20,::20], u[::20,::20][0], v[::20,::20][0])
                        j = j+1

            j = 0
            i= i + 1
        plt.show()
