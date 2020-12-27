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
                                                              var = var,
                                                              j = self.j-1: self.store_types(onoff,plot_type, subplot, var, j)).pack()
                            self.j = self.j+1
                        elif choice == 'b':
                            self.subtext[self.j] = {subplot:StringVar()}
                            self.sub_checkboxes[self.i] = Checkbutton(self.gui, text = 'contours', variable = self.subtext[self.j][subplot],
                                                              onvalue = 'A', offvalue = 'B',
                                                              command = lambda onoff = self.subtext[self.j][subplot],
                                                              plot_type = 'contours',
                                                              subplot = subplot,
                                                              var = var,
                                                              j = self.j-1: self.store_types(onoff,plot_type,subplot, var, j)).pack()
                            self.j = self.j+1
                        elif choice == 'c':
                            self.subtext[self.j] = {subplot:StringVar()}
                            self.sub_checkboxes[self.i] = Checkbutton(self.gui, text = 'barbs', variable = self.subtext[self.j][subplot],
                                                              onvalue = 'A', offvalue = 'B',
                                                              command = lambda onoff = self.subtext[self.j][subplot],
                                                              plot_type = 'barbs',
                                                              subplot = subplot,
                                                              var = var,
                                                              j = self.j-1: self.store_types(onoff,plot_type,subplot, var, j)).pack()
                            self.j = self.j+1
                        else:
                            pass

                    self.i = self.i+1
        #print('subtext = {}'.format(self.subtext))
        self.i = 1
        self.j = 1
        plot_button = Button(self.gui, text = "Plot", command = lambda: self.multiple_types())
        plot_button.pack()
    def store_types(self, onoff, plot_type, subplot, var, j):
        #If subplot does not match up with the subplot values in self.sub_arr and is new
            #Then store the self.sub_arr into self.temp_sub_arr
            #And reset self.sub_arr to an empty arr and insert the subplot
        #Elif subplot does not match up with the subplot values in self.sub_arr and is old
            #Then go through the different key_arrays in self.types and find the one with values that match the subplot

        onoff = onoff.get()
                    #TODO Have to do something with self.types

        #######################################################################
        #if onoff == "A":
            #for key in self.old_sub_arr:
                #if str(subplot) not in key and str(subplot) in str(self.sub_arr): #'0' not in '[]' and '0' in '[0 0]'
                    #old_key_store = str(self.sub_arr) #'[0 0]'
                    #self.sub_arr = np.append(self.sub_arr, subplot) #[0 0 0]
                    #new_key_store = str(self.sub_arr) #'[0 0 0]'
                    #print("new key: {}".format(new_key_store))
                    #self.types[new_key_store] = self.types.pop(old_key_store) #Replece the key with the updated key and pop the old key
                    #self.type_arr = np.append(self.type_arr, {var:plot_type})
                    #print("type_arr: {}".format(self.type_arr))
                    #self.types[str(new_key_store)] = self.type_arr
                    #print("types: {}".format(self.types))
                #elif str(subplot) not in key and str(subplot) not in str(self.sub_arr): #'1' not in '[]' and '1' not in '[0 0]'
                    #self.old_sub_arr[str(self.sub_arr)] = self.sub_arr #self.old_sub_arr = {'[0 0]': [0 0]}
                    #self.sub_arr = np.array([], dtype = np.int)
                    #self.sub_arr = np.append(self.sub_arr, subplot)
                    #self.old_type_arr[str(self.type_arr)] = self.type_arr
                    #self.type_arr = np.array([])
                    #self.type_arr = np.append(self.type_arr, {var:plot_type})
                    #self.types[str(self.sub_arr)] = self.type_arr
                #else: #'1' in '[1]'
                    #old_key_store = key #old_key = '[0 0]' We can refer to and pop this key in self.types
                    #self.sub_arr = np.append(self.old_sub_arr[key], subplot) #self.sub_arr = [0, 0] + [0] = [0, 0, 0]
                    #new_key_store = str(self.sub_arr)
                    #self.types[new_key_store] = self.types.pop(old_key_store)
                    #new_types_arr = self.types[new_key_store]
                    #new_types_arr = np.append(new_types_arr, {var:plot_type})
                    #self.types[new_key_store] = new_types_arr
        #elif onoff == "B":
            #do
        #######################################################################
        if onoff == "A":
            if str(subplot) in str(self.sub_arr): #if '0' in '[0]'
                #old sub_arrs: {'[]': array([], dtype=int32), '[0 0]': array([0, 0]), '[1 1]': array([1, 1])}
                old_key_store = str(self.sub_arr) #'[0]'
                self.sub_arr = np.append(self.sub_arr, subplot) #[0 0]
                new_key_store = str(self.sub_arr) #'[0 0]'
                print("new key: {}".format(new_key_store))
                self.types[new_key_store] = self.types.pop(old_key_store) #Replece the key with the updated key
                self.type_arr = np.append(self.type_arr, {var:plot_type})
                print("type_arr: {}".format(self.type_arr))
                self.types[str(new_key_store)] = self.type_arr
                print("types: {}".format(self.types))
                            #{np.array([]) : np.array([])}
                            #{[0,0,0,...] : [{u:barbs},{v:barbs},{q:cmap},...]}

            else: # 1 in [0 0]
                #old sub_arrs: {'[]': array([], dtype=int32), '[0 0]': array([0, 0]), '[1 1]': array([1, 1])}

                self.old_sub_arr[str(self.sub_arr)] = self.sub_arr #Store the old subplot array {'[0 0]':[0, 0, 0]}
                self.sub_arr = np.array([], dtype = np.int) #Reset the sub_arr
                self.sub_arr = np.append(self.sub_arr, subplot) #[1]
                print("new sub_arr: {}".format(self.sub_arr))
                self.old_type_arr[str(self.type_arr)] = self.type_arr #Store the old array of type dicts {'[{'u':'cmap'} {'u': 'contours'} {'v':'cmap'}]'}
                self.type_arr = np.array([]) #Reset the type_arr
                self.type_arr = np.append(self.type_arr, {var:plot_type}) # ['u': 'cmap']
                print("new type_arr: {}".format(self.type_arr))
                self.types[str(self.sub_arr)] = self.type_arr
                print("new types before pop: {}".format(self.types))

                for key in self.types.copy(): #Attempt to pop empty key
                    try: #This is for when everything is being initially created
                        if bool(self.types.copy()[key]) == False:
                            self.types.pop(key)
                            print("new types after pop: {}".format(self.types))
                    except: #This is for when self.types already has stuff in it
                        print("new types except: {}".format(self.types))

                print("old sub_arrs: {}".format(self.old_sub_arr))



        elif onoff == 'B': #Everything in commented out is a work in progress
            for sub_arr in self.types.copy():
                #left_bound = 1
                #right_bound = len(sub_arr)
                #elements = np.arange(left_bound, right_bound, 2)
                itervar = 1

                print(sub_arr, itervar)
                itervar = itervar + 1
            '''
            for key in self.types.copy():
                self.type_arr = np.delete(self.types[key], np.where(self.types[key] == {}))
                self.types[new_key] = self.type_arr
            '''


            '''
            for self.sub_arr in self.types.copy():
                for sub in self.sub_arr:
                    try:
                        if sub == subplot:
                            for i in range(len(self.types[self.sub_arr])):
                                try: #sub_arr key no longer exists after passing if key == var:
                                    for key in self.types[self.sub_arr][i]:
                                        if key == var and self.types[self.sub_arr][i][key] == plot_type:
                                            old_key = str(self.sub_arr)
                                            new_key = np.array([], dtype= np.int)
                                            for char in old_key:
                                                if char.isnumeric():
                                                    new_key = np.append(new_key, int(char))
                                        new_key = np.delete(new_key, len(new_key)-1)
                                        self.sub_arr = new_key
                                        print(self.sub_arr)
                                        #Now we have the key ready to put into the dictionary
                                        self.types[str(new_key)] = self.types.pop(old_key)
                                        self.types[str(new_key)][i].pop(var)
                                        if bool(self.types[str(new_key)][i]) == False:
                                            self.type_arr = np.delete(self.type_arr, j)
                                            self.types[str(new_key)] = self.type_arr

                                    #print(var,plot_type, self.type_arr)
                                    print(self.types)


                                except:
                                    break
                    except:
                        pass
            '''
        #Stores choices into arrays
        #self.next = Button(self.gui, text = "Move on to final step", command = lambda : self.multiple_types(self)).pack()

    def multiple_type(self):
        plt.figure(figsize = (12,7))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([np.min(self.xx)+.0001,np.max(self.xx)+.0001, np.min(self.yy), np.max(self.yy)])
        ax.coastlines()
        self.i = 0
        for var in self.vars_to_plot:
            if var in self.cmap:
                ax.pcolormesh(self.xx, self.yy, self.vars_to_plot[var][0])
            elif var in self.contours:
                ax.contour(self.xx, self.yy, self.vars_to_plot[var][0])
            elif var in self.barbs:
                if self.i < 1:
                    RATE = 20
                    for var in self.vars_to_plot:
                        if 'u' in var and var in self.barbs:
                            var1 = self.vars_to_plot[var]
                        if 'v' in var and var in self.barbs:
                            var2 = self.vars_to_plot[var]
                        self.i = self.i + 1
                    ax.barbs(self.xx[::RATE,::RATE], self.yy[::RATE,::RATE], var1[0,::RATE,::RATE], var2[0,::RATE,::RATE], length = 5, linewidth = 0.6,zorder = 4)
                else:
                    pass
        plt.show()
