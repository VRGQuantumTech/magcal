# -*- coding: utf-8 -*-
#%% Importing modules
## import qutip as qt
from IPython import get_ipython # These two lines clear all the variables
get_ipython().magic('reset -sf')


import numpy as np
import os
import scipy.io as sio
import magcal as qf
from loadpath import pth

#format to save plots
fmt = 'png'

#%% Loading current matrices and geometric data

path,file,_ = pth.file()

dirpath = os.path.dirname(path)

current = qf.loadcurrent(path)

#%% Plotting current matrices before B calculation

# Creating folder to save data
fdir = pth.resultsfolder(dirpath, 'Currents and Fields')

#%%

current.vec_plot()
current.mod_plot()


#%% GPU calculation of magnetic field matrices from current matrices. 
"""CALCULATION OF THE MAGNETIC FIELD"""
#!!! NVIDIA graphics card is needed

Z = np.linspace(1*1e-6, 150*1e-6, 150)

Field = qf.gpu_field(current.Ixrs, current.Iyrs, current.posx, current.posy, Z)

#%%

print('Saving field . . .')

field = {'field': 'fieldout', 'H2DX':Field.Brfx[:,:,:], 'H2DY':Field.Brfy[:,:,:],
         'H2DZ':Field.Brfz[:,:,:], 'H2DM':Field.Brf[:,:,:], 'posx':Field.posx,
         'posy':Field.posy, 'posz':Field.posz}

sio.savemat(dirpath + '/field.mat' , {'field': field} , format = '5' , do_compression = True)


#%% Loading Brf field matrices for coupling calculation

# (If Field Matrices are provided) load field matrices data with the molecule orientation selected in axis
# The variable axis states the resonator axis (X parallel to long direction of the inductor and Y parallel to the
# short direction of the inductor, Z is perpendicular to the chip) which is parallel to the C3 axis (Yb: Z axis of the Hamiltonian=> axis: X; Mn1: C3 is Z molecule ==> axis Z resonator parallel to C3)

#sample = 'MnMe6trenCl_Cl04'
# angles = {'angle': 0., 'fi': 0., 'theta': 0} #deg. theta = 0. if Anysotropy axis is // to Bdc (Z) 


path,file,dirpath = pth.file()

field = qf.loadfield(path)

#%%

field.mod_plot(linthresh=0.01)

#%%
field.vec_plot(linthresh=0.01, subplot=True, save=True, figsize=(19.0,4.8), clabel_pos=[0.15, -0.05, 0.7, 0.05])

#%%

field.xz_cut(yc = 300)

#%%

field.yz_cut(xc = 438)