# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 04:48:25 2022

@author: 
"""
#%%

import os
import tkinter as tk # Import the module to load the paths of the files
import tkinter.filedialog # The function that opens the file dialog to select the file/files/directory
import numpy as np
from natsort import natsorted


#%%

class pth:
    "Class that contains the functions to import and manipulate paths"


    @classmethod
    def file(self):
        """
        Function that loads a single file path.
        
        Returns
        -------
        path: str
            Path of the file
        file: str
            Name of the file
        directory: str 
            Directory of the file
        """
 
        
        try:
            root=tk.Tk() # It helps to display the root window
            root.withdraw() # Hide a small window openned by tkinter
            root.attributes("-topmost", True)
            path = tk.filedialog.askopenfilename(parent=root) # Shows dialog box and return the path of the file
            root.destroy()
            file = os.path.basename(path) # Get the name of the file
            dirpath = os.path.dirname(path) # Get the directory path of the file
            
            return path, file, dirpath

        except:
            raise Exception('the path cannot be imported')
            return None    

    @classmethod
    def folder(self):
        """
        Function that loads a single folder path.
        
        Returns
        -------
        path: str
            Path of the folder
        """
 
        
        try:
            root=tk.Tk() # It helps to display the root window
            root.withdraw() # Hide a small window openned by tkinter
            root.attributes("-topmost", True)
            path = tk.filedialog.askdirectory(parent=root) # Shows dialog box and return the path of the file
            root.destroy()
            
            return path

        except:
            raise Exception('the path cannot be imported')
            return None
        

    @classmethod
    def files(self):
        """
        Function that loads several selected file paths.
        
        Returns
        -------
        path: string
            Path of the files
        file: string
            Name of the files
        directory: string
            Directory of the files
        """

        try:        
            root=tk.Tk() # It helps to display the root window
            root.withdraw() # Hide a small window openned by tkinter
            root.attributes("-topmost", True)
            path = tk.filedialog.askopenfilenames(title='Select multiple files') # Shows dialog box and return the path of the file
            files = [os.path.basename(f) for f in path if '.ini' not in f] # Get a list of the name of the files
            files = natsorted(files) # Sorted the files naturally (in case it contains numbers)
            dirpath = os.path.dirname(path[0]) # Get the directoy path of the files
            
            return list(path), list(files), dirpath

        except:
            raise Exception('the paths cannot be imported')
            return None    
    
    
    
    @classmethod  
    def dirfiles(self, name=None, ext = None):
        """Function that reads all the files in the selected folder, files can be filtered by name and extension.
        
        Parameters
        ----------
        
        name: string, default None
            Name of the file to be filtered
        ext: string, default None
            Extension of the file to be filtered
            
        Returns
        -------
        path: str
            Path of the file
        file: str
            Name of the file
        directory: str 
            Directory of the file
        """
        
        try:
            root=tk.Tk() # It helps to display the root window
            root.withdraw() # Hide a small window openned by tkinter
            dirpath = tk.filedialog.askdirectory(title='Select directory') # Shows dialog box and return the path of the file   
            
            if name == None and ext == None: # If name and extension not used, import every file
                files = [f for f in os.listdir(dirpath) if '.ini' not in f]
                files = natsorted(files)   
                
            elif name == None and ext != None: # Import files with the extension used
                files = [f for f in os.listdir(dirpath) if '.ini' not in f and ext in f]
                files = natsorted(files)
                
            elif name != None and ext == None:# Import files with the name used
                files = [f for f in os.listdir(dirpath) if name in f and '.ini' not in f]
                files = natsorted(files)
                
            else: # Import files with the extension and name
                files = [f for f in os.listdir(dirpath) if name in f and '.ini' not in f and ext in f]
                files = natsorted(files) 
                   
            path = []
            for i in files: # Append every file path
                path.append(os.path.join(dirpath, i))
        
    
            return path, files, dirpath 
    
        except:
            raise Exception('the files from the directory cannot be imported')
            return None



    @classmethod 
    def resultsfolder(self, dirpath, name = None): 
        """
        Function that checks if a the folder exists, if not, creates a folder called 'Output'.
        
        Parameters
        ----------
        
        dirpath: string
            Full path where the folder will be created
        name: string, default None
            Name of the created folder, if None, name = Output
            
        Returns
        -------
        fdir: string
            Full path of the folder
        """
        
        try:
            if name == None:
                fdir = os.path.join(dirpath,'Output') # Get the path with the name of the file without the extension
            
            else:
                fdir = os.path.join(dirpath, name) # Get the path with the name of the file without the extension        
            
            if os.path.exists(fdir): # Check if the folder already exists
                None
            else: # If not, then creates the folder
                os.mkdir(fdir) # Creates the new folder in the specified path     
            return fdir
    
        except:
            raise Exception('not possible to create the results folder')
            return None



    @classmethod 
    def renamefiles(self, original, replace): # Useful to replace a lot of file names
        """
        Function that renames the selected files.
        
        Parameters
        ----------
        
        original: string
            Part of the name to change
        replace: string
            New name part replacing the original
            
        Returns
        -------
        None
        """
        
        path, files, dirpath = self.files() # Uses the file function
        try:
            for index, file in enumerate(files): # Loop for rename each file with the new name
                os.rename(os.path.join(dirpath,file), os.path.join(dirpath, file.replace(original, replace)))
        except:
            raise Exception('file names cannot be replaced')
            
    @classmethod     
    def getparam(self, name, left = None, right = None):
        """
        Function that gets the parameter from the filename , a left and right separator are necessary to identify the desired parameter
        if the separators are unkown, look at the filename to write the separators.
        
        Parameters
        ----------
        
        name: string or list
            Name of the file you want to get the paremeter
        left: string, default None
            The left separator to identify the parameter
        right: string, default None
            The right separator to identify the parameter

        Returns
        -------
        Param: array
            Array containing the parameters
        """    

        Param = []
        try:
            if type(name) == list:
                for i in name: # Loop for get each name
                    Param.append(i.split('_')[-1])
                  
            else:
                tempt = name.split(left)[1] # Same as before but for a single name
                tempt = tempt.split(right)[0]
                Param.append(str(tempt))
                
            Param = np.asarray(Param) # Transforms the parameter into an array
            return Param
       
        except:
            raise Exception('check the separators of the parameter you want')
            return None
            
###############################################################################