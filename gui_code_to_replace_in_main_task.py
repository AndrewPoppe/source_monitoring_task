#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.81.03), Thu Feb  5 12:37:35 2015
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'source_monitoring'  # from the Builder filename that created this script
expInfo = {}

myDlg = gui.Dlg(title=expName, size=gui.wx.Size(-1,-75))
myDlg.addField(u'participant: ', u'')
myDlg.addField('word lists: ', choices=['random','set your own']) 
myDlg.show()
if myDlg.OK == False: core.quit()  # user pressed cancel
expInfo['participant'] = myDlg.data[0]
expInfo['listMethod'] = myDlg.data[1]
print expInfo['listMethod']
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName


if expInfo['listMethod']=='set your own':
    myDlg2 = gui.Dlg(title='Set Word Lists')
    conditions = ['unmodified 1', 'unmodified 2', 'slowed - small', 'slowed - medium', 'slowed - large', 'pitch - higher - small', 'pitch - higher - large', 'pitch - lower - small', 'pitch - lower - large']
    for cNum in range(len(conditions)):
        myDlg2.addField(conditions[cNum], choices=[1,2,3,4,5,6,7,8,9], initial=cNum+1)
    myDlg2.show()
    if myDlg2.OK == False: core.quit()  # user pressed cancel
    expInfo['listOrder'] = myDlg2.data
    
from psychopy import visual
