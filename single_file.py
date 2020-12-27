# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 23:41:56 2020

@author: willk
"""
#If a single file is passed in run through this file
#Once the user enters the number of subplots, check to see if it is >  1 or = 1
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

#User-defined imports##########################################################
import single_plot_single_subplot as onepones
import single_plot_multiple_subplots as onepms
import multiple_plot_single_subplot as mpss
import multiple_plot_multiple_subplots as mpms
###############################################################################

class single:
    def __init__(self,fh, lons, lats, subplots, amount):
        #Going to construct a numpy array of IVT values
        self.gui = Toplevel()
        self.vars = fh.variables
        self.fh = fh
        self.dict = {}
        self.lons = lons
        self.lats = lats
        self.amount = amount
        self.subplots = subplots

        for var in self.vars:
            if self.fh.variables[var].ndim == 1 or self.fh.variables[var].units == 's' or self.fh.variables[var].units == 'hPa' or self.fh.variables[var].units == 'Pa':
                pass
            else:
                self.dict[var] = self.fh.variables[var]

        self.text_dict = {} #Dictionary of StringVars()
        for key in self.dict:
            self.text_dict[key] = StringVar()
        self.checkbuttons = {} #Dictionary of variable checkboxes
        for key in self.text_dict:
            self.checkbuttons[key] = Checkbutton(self.gui, text = key, variable = self.text_dict[key], onvalue = 'A', offvalue = 'B',
                                                 command = lambda var1 = self.text_dict[key],
                                                 var2 = self.dict[key],
                                                 var3 = key: self.select_vars(var1,var2, var3)) #Needed to use lambda var = key
        for key in self.checkbuttons:
            self.checkbuttons[key].pack()

        self.vars_to_plot = {}

        T = Text(self.gui, height = 2, width = 40)
        T.pack()
        T.insert(END, "Pick one or more variable(s) to plot")

        self.choices = np.array(['','',''])
        self.text1 = StringVar()
        self.text2 = StringVar()
        self.text3 = StringVar()
        self.text1.set('')
        self.text2.set('')
        self.text3.set('')
        self.c1 = Checkbutton(self.gui, text = 'cmap', variable = self.text1, onvalue='A', offvalue='B', command = lambda: self.addchoice(self.text1,self.c1.cget("text")))
        self.c2 = Checkbutton(self.gui, text = 'contour', variable = self.text2, onvalue='A', offvalue='B', command = lambda: self.addchoice(self.text2,self.c2.cget("text")))
        self.c3 = Checkbutton(self.gui, text = 'barbs', variable = self.text3, onvalue='A', offvalue='B', command = lambda: self.addchoice(self.text3,self.c3.cget("text")))
        self.plot_button = Button(self.gui, text = "Begin Plotting", command = lambda: self.determine_class())



    def select_vars(self, bool, var, var_name): #Stores checked off variables into dictionary
        if bool.get() == 'A':
            self.vars_to_plot[var_name] = var
        elif bool.get() =='B':
            self.vars_to_plot.pop(var_name)

        self.c1.pack()
        self.c2.pack()
        self.c3.pack()
        self.plot_button.pack()



    def addchoice(self, bool, text):
        if text == 'cmap':
            if bool.get() == 'A':
                self.choices[0] = 'a'
            else:
                self.choices[0] = ''
        elif text == 'contour':
            if bool.get() == 'A':
                self.choices[1] = 'b'
            else:
                self.choices[1] = ''
        elif text == 'barbs':
            if bool.get() == 'A':
                self.choices[2] = 'c'
            else:
                self.choices[2] = ''

    def determine_class(self):
        self.plot_button.forget()
        if self.amount == "single" and self.subplots == 1:#TODO and number or plots ==1
            self.obj = onepones.single_single(self.fh, self.lons, self.lats, self.choices, self.vars_to_plot)
            self.obj.class_plot()
        elif self.amount == "single" and self.subplots > 1:
            self.obj = onepms.single_multiple(self.fh, self.lons, self.lats, self.choices, self.vars_to_plot, self.subplots)
            self.obj.choose_vars()
        elif self.amount == "multi" and self.subplots == 1:
            self.obj = mpss.multiple_single(self.fh, self.lons, self.lats, self.choices, self.vars_to_plot)
        elif self.amount == "multi" and self.subplots > 1:
            self.obj = mpms.multiple_multiple(self.fh, self.lons, self.lats, self.choices, self.vars_to_plot, self.subplots)

