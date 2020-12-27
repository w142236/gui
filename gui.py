#Package imports###############################################################
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from tkinter.filedialog import askopenfile
import PIL.Image
import PIL.ImageTk
#from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import numpy as np
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from metpy.plots import ctables
cmap = ctables.registry.get_colortable('NWSReflectivity')
from netCDF4 import Dataset
###############################################################################

#User-defined imports##########################################################
import single_file as single
import multiple_files as multiple
###############################################################################
class aclass:
    def __init__(self,lons,lats, ax, subplots, files, string):
        self.files = files
        self.amount = string
        #MOVE THESE############################################################
        #self.root = Tk()
        self.lons = lons
        self.lats = lats
        #######################################################################

        if self.lons.ndim == 1 and self.lats.ndim ==1:
            self.xx, self.yy = np.meshgrid(self.lons, self.lats)
        else:
            self.xx, self.yy = self.lons, self.lats
        self.subplots = int(subplots)
        self.checkbuttons = {}
        self.dict = {} #Dictionary of Variables
        if len(self.files) == 1:
            self.fh = Dataset(self.files[0])
            #CALL##############################################################
            self.single_object = single.single(self.fh, self.xx, self.yy, self.subplots, self.amount)
            ###################################################################
        elif len(self.files) > 1:
            self.fh_sample = Dataset(self.files[0])
            #CALL##############################################################
            self.multi_object = multiple.multiple(self.fh_sample, self.xx, self.yy, self.subplots, self.amount)
            ###################################################################
    def clear_all(self):
        #self.mt_plot_button.destroy()
        self.plot_button.pack()#Repack the begin plotting button
        self.clear_button.destroy()
        self.cmap = np.array([])
        self.contours = np.array([])
        self.barbs = np.array([])
        self.mt_plot_button.destroy()
        for var in self.type_buttons:
            self.T[var].destroy()
            for button in self.type_buttons[var]:
                self.type_buttons[var][button].destroy()

#########################################################
def display_button():
	canvas = Canvas(gui, width = 300, height = 200)
	canvas.pack(expand = YES, fill = BOTH)
	fig1 = PhotoImage(file = '/home/quit/test.png')
	canvas.create_image(50, 10, image = fig1, anchor = NW)
	canvas.fig1 = fig1
def reference_plot_class(lons, lats, ax, number, files, string): #This function will point to type
    aclass(lons,lats, ax, number.get(), files, string)
	#object.select_vars()

def single_or_multi(button, root, lons, lats, new_ax, number, files):
    if str(button) == ".!radiobutton":
        string = "single"
    elif str(button) == ".!radiobutton2":
        string = "multi"
    build_button = Button(root, text = "Build plots", command = lambda: reference_plot_class(lons, lats, new_ax, number, files, string))
    build_button.pack()
def buildmap_and_subplots(projection,urcrnrlat,llcrnrlat,urcrnrlon,llcrnrlon,r,lons,lats,files):
	root = Tk()
	fh_test = Dataset(files[0])
	for var in fh_test.variables:
		if 'T' in var.upper() and var.upper() != 'TIME':
			test_var = fh_test.variables[var][:]
	if test_var.ndim == 4: #We assume the time axis is first
		slice_var = test_var[0][0]
	elif test_var.ndim == 3: #We assume height axis is first
		slice_var = test_var[0]
	elif test_var.ndim ==2:
		slice_var = test_var
	#TODO put string in projection

	ax = plt.axes(projection = ccrs.PlateCarree())
	ax.set_global()
	ax.coastlines()
	plt.contour(lons, lats, slice_var,latlon= True)
	plt.show()
	#TODO ask if data is projected correctly. If it isn't: ax.set_extent(same,same, same + deviation, same + deviation)
	new_ax = plt.axes(projection = ccrs.PlateCarree())
	new_ax.set_extent([llcrnrlon+.0001, urcrnrlon+.0001, llcrnrlat, urcrnrlat])
	subplots = IntVar()
	number = Entry(root, width = 15, textvariable = subplots)
	number.pack()

	single_mult = IntVar()
	single_button = tk.Radiobutton(root,text = "One plot (Used for testing)",padx = 20, variable = single_mult, value = 1, command = lambda: single_or_multi(single_button,root, lons, lats, new_ax, number, files))
	multi_button = tk.Radiobutton(root, text = "More than one plot (Make plots between date range)", variable = single_mult, value = 2, command = lambda: single_or_multi(multi_button,root, lons, lats, new_ax, number, files))
	single_button.pack()
	multi_button.pack()


def pick_resolution(projection,files):
	root = Tk()
	fh = Dataset(files[0])
	if 'lon' in fh.variables:
		lons = fh.variables['lon'][:]
		lats = fh.variables['lat'][:]
		#TODO: centerlon =
		#TODO: centerlat =
		urcrnrlat, llcrnrlat = np.max(lats), np.min(lats)
		urcrnrlon, llcrnrlon = np.max(lons), np.min(lons)
		v = IntVar()
		resolution1 = tk.Radiobutton(root,text = "high",padx = 20, variable = v, value = 1, command = lambda: buildmap_and_subplots(projection,urcrnrlat,llcrnrlat,urcrnrlon,llcrnrlon,"h",lons,lats,files))
		resolution2 = tk.Radiobutton(root,text = "med",padx = 20, variable = v, value = 2, command = lambda: buildmap_and_subplots(projection,urcrnrlat,llcrnrlat,urcrnrlon,llcrnrlon,"m",lons,lats,files))
		resolution3 = tk.Radiobutton(root,text = "low (recommended)",padx = 20, variable = v, value = 3, command = lambda: buildmap_and_subplots(projection,urcrnrlat,llcrnrlat,urcrnrlon,llcrnrlon,"l",lons,lats,files))
		resolution4 = tk.Radiobutton(root,text = "crude",padx = 20, variable = v, value = 4, command = lambda: buildmap_and_subplots(projection,urcrnrlat,llcrnrlat,urcrnrlon,llcrnrlon,"c",lons,lats,files))
		resolution1.pack()
		resolution2.pack()
		resolution3.pack()
		resolution4.pack()


def pick_projection():

    v = IntVar()
    files = tk.filedialog.askopenfilenames(parent=gui,title='Choose file(s)')
    #print (root.splitlist(files))
    Label(gui,text = "choose projection")
    Radiobutton(gui,text = "cyl", variable = v, value = 1, command = lambda: pick_resolution("PlateCarree",files)).pack()


gui = Tk()

display_button = tk.Button(gui, text = "display test", command = display_button)
make_plot_button = tk.Button(gui, text = 'Open', command = lambda:pick_projection())
display_button.pack()
make_plot_button.pack()
gui.mainloop()
###END/###
