# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 23:41:09 2020

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

class single_single:
    def __init__(self, fh,  xx, yy, choices, vars_to_plot):
        self.gui = Toplevel()
        self.fh = fh
        self.xx = xx
        self.yy = yy
        self.choices = choices
        self.vars_to_plot = vars_to_plot
        self.type1 = StringVar()
        self.type2 = StringVar()
        self.type3 = StringVar()
        self.cmap = np.array([])
        self.contours = np.array([])
        self.barbs = np.array([])
        self.i = 0

    def class_plot(self):
        plt.figure(figsize = (12,7))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([np.min(self.xx)+.0001,np.max(self.xx)+.0001, np.min(self.yy), np.max(self.yy)])
        self.types = np.array([])
        for choice in self.choices:
            if choice != '':
                self.types = np.append(self.types, choice)
            else:
                pass
        self.type_buttons = {}
        if len(self.types) == 1 and len(self.vars_to_plot) == 1:
            for key in self.vars_to_plot:
                var_name = key
            if 'a' in self.types:
                print(var_name)
                ax.coastlines()
                ###TODO: if shape is 4-D: time and height dropdown or Radiobutton
                #     if shape is 3-D: height dropdown or Radiobutton
                ###TODO: cmap_name = Entry()
                ax.pcolormesh(self.xx, self.yy, self.vars_to_plot[var_name][0])
                ###TODO title = Entry()
                #
                #plt.savefig("cmap.png")
                plt.title("{} cmap".format(var_name))
                plt.show()
                #TODO display map on same GUI
            elif 'b' in self.types:
                print(var_name)
                ax.coastlines()
                                ###TODO: if shape is 4-D: time and height dropdown
                                #        if shape is 3-D: height dropdown
                                ###TODO: cmap_name = Entry()
                ###TODO contour_to_highlight = Entry()
                try:
                    ax.contour(self.xx, self.yy, self.vars_to_plot[var_name][0])
                except:
                    print("cmap name either spelled incorrectly or does not exist.\n Please enter name again")
                    #cmap_name = Entry()
                    ax.contour(self.xx, self.yy, self.vars_to_plot[var_name][0])
                ###TODO title = Entry()
                #
                plt.title("{} contours".format(var_name))
                plt.savefig("contour.png")
                plt.show()
                #TODO display map on same GUI
                print("Done!")
            elif 'c' in self.types:
                print("ERROR! Not enough variables for barbs plot. Need two variables (u_wind and v_wind)")
                print("Choose another variable(s) from checkboxes and try plotting again!")
        elif len(self.types) == 1: #In this case they must be plotting wind
            for var_name in self.vars_to_plot:
                if 'u' in var_name or 'zon' in var_name or 'x' in var_name and (self.fh.variables[var_name].units == 'm/s' or 'knot' in self.fh.variables[var_name].units): #u or zonal or x
                    var1 = self.vars_to_plot[var_name]
                elif 'v' in var_name or 'mer' in var_name or 'y' in var_name and (self.fh.variables[var_name].units == 'm/s' or 'knot' in self.fh.variables[var_name].units): #v or meridional or y
                    var2 = self.vars_to_plot[var_name]
                else:
                    print("Too many variables that are not u_wind and v_wind for 1 subplot and 1 plot type!/n Close window, re-enter number of subplots and try again!")
            if 'c' in self.types:
                RATE = 20
                ax.coastlines()
                ax.barbs(self.xx[::RATE,::RATE], self.yy[::RATE,::RATE], var1[0,::RATE,::RATE], var2[0,::RATE,::RATE], length = 5, linewidth = 0.6, zorder = 1)
                ###TODO title = Entry()
                plt.title("wind barbs")
                plt.savefig("barbs.png")
                plt.show()
                print("Done!")
        elif len(self.types) > 1:
            #TODO They want multiple types of plots for one variable
            ax.coastlines()
            if len(self.vars_to_plot) == 1:
                for key in self.vars_to_plot:
                    var_name = key
                if 'c' in self.types:
                    print("Not enough wind components to plot barbs")
                elif 'a' in self.types and 'b' in self.types:
                ###TODO: if shape is 4-D: time and height dropdown
                                #        if shape is 3-D: height dropdown
                                ###TODO: cmap_name = Entry()
                    ax.pcolormesh(self.xx,self.yy, self.vars_to_plot[var_name][0])
                    ax.contour(self.xx, self.yy, self.vars_to_plot[var_name][1])
                    #TODO display image on same GUI
                plt.show()
            #TODO OR they want a different type of plot for each variable onto one single plot
            else:
                self.mt_plot_button = Button(self.gui, text = 'Plot', command = lambda: self.multiple_type())
                self.T = {}
                for var in self.vars_to_plot:
                    T = Text(self.gui, height = 2, width = 40)
                    self.T[var] = T
                    self.T[var].pack()
                    T.insert(END, "Pick desired plot type(s) for variable: {}".format(var))
                    self.type_buttons[var] = {}
                    for types in self.types:
                        if types == 'a':
                            self.type_buttons[var][types] = Checkbutton(self.gui, text = 'cmap', variable = self.type1, onvalue = 'A', offvalue = 'B', command  = lambda bool = self.type1, var_name = var, type = 'cmap' : self.multiple_types(type, var_name, bool))
                            self.type_buttons[var][types].pack()
                        elif types == 'b':
                            self.type_buttons[var][types] = Checkbutton(self.gui, text = 'contours', variable = self.type2, onvalue = 'A', offvalue = 'B', command  = lambda bool = self.type2, var_name = var, type = 'contours' : self.multiple_types(type, var_name, bool))
                            self.type_buttons[var][types].pack()
                            print(self.type_buttons)
                        elif types == 'c':
                            self.type_buttons[var][types] = Checkbutton(self.gui, text = 'barbs', variable = self.type3, onvalue = 'A', offvalue = 'B', command  = lambda bool = self.type3, var_name = var, type = 'barbs' : self.multiple_types(type, var_name, bool))
                            self.type_buttons[var][types].pack()
                        else:
                            pass
                    print(self.type_buttons)
                    self.type1 = StringVar()
                    self.type2 = StringVar()
                    self.type3 = StringVar()
                    #TODO Add textfield to explain

    def multiple_types(self, type, var_name, bool):
        #For each variable, check off which type to attribute it to
        print(bool.get(), var_name, type)
        if type == 'cmap' and bool.get() == 'A':
            self.cmap = np.append(self.cmap,var_name)
        elif type == 'cmap' and bool.get() == 'B':
            self.cmap = np.delete(self.cmap, np.where(self.cmap == var_name))
        elif type == 'contours' and bool.get() == 'A':
            self.contours = np.append(self.contours, var_name)
        elif type == 'contours' and bool.get() == 'B':
            self.contours = np.delete(self.contours, np.where(self.contours == var_name))
        elif type == 'barbs' and bool.get() == 'A':
            self.barbs = np.append(self.barbs, var_name)
        else:
            self.barbs = np.delete(self.barbs, np.where(self.barbs == var_name))
        print('{}{}{}'.format(self.cmap, self.contours, self.barbs))
        self.mt_plot_button.pack()

    def multiple_type(self):
        plt.figure(figsize = (12,7))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([np.min(self.xx)+.0001,np.max(self.xx)+.0001, np.min(self.yy), np.max(self.yy)])
        ax.coastlines()
        self.i = 0
        #print(self.vars_to_plot)
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
