# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 23:42:02 2020

@author: willk
"""
# If multiple files are passed in, run this class file

#Check to see if use wants 1 plot or multiple subplots
import netCDF4 as nc
from netCDF4 import Dataset
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from tkinter.filedialog import askopenfile
import PIL.Image
import PIL.ImageTk

#User-defined imports##########################################################
import single_plot_single_subplot as onepones
import single_plot_multiple_subplots as onepms
import multiple_plot_single_subplot as mpss
import multiple_plot_multiple_subplots as mpms
###############################################################################

class multiple:
    def __init__(self, files):
        self.gui = Toplevel()
        self.files = files
        self.fh = {}
        self.vars_to_plot = {}
        #TODO Ask user for variables they want to load in (otherwise program will crash)
        self.checkboxes = {}
        self.text_dict = {}

        sample_fh = Dataset(self.files[0])
        for name in sample_fh.variables:
            self.text_dict[name] = StringVar()
            self.checkboxes[name] = Checkbutton(self.gui, text = name, variable = self.text_dict[name], onvalue = 'A', offvalue = 'B',
                                                command = lambda var = name: self.choose_vars(var))

        for check in self.checkboxes:
            self.checkboxes[check].pack()

    def choose_vars(self, variable):
        for file in self.files:
            self.vars_to_plot[file] = {variable: Dataset(file).variables[variable][:]}
        for key in self.vars_to_plot:
            print(key, self.vars_to_plot[key])
