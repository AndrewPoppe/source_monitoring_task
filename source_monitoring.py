#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
    conditions = ['unmodified', 'pitch - higher', 'pitch - lower']
    for cNum in range(len(conditions)):
        myDlg2.addField(conditions[cNum], choices=[1,2,3], initial=cNum+1)
    myDlg2.show()
    if myDlg2.OK == False: core.quit()  # user pressed cancel
    expInfo['listOrder'] = myDlg2.data
    
from psychopy import visual


# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1440, 900), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "initialize_code"
initialize_codeClock = core.Clock()
from psychopy import gui
from pyo import *
import math, sys, csv, random
from collections import OrderedDict
serv = Server().boot()

## SETTINGS ##

# This is the amount to change the pitch on each block of trials (both higher and lower)
PITCH_DELTA = 0.5

# This is the word list file
WORD_LIST_FILE = "wordlist.csv"

# Colors of the choice buttons
SELF_BOX_FILL_COLOR = '#A6A9FF'
SELF_BOX_BORDER_COLOR = '#3E45FA'
OTHER_BOX_FILL_COLOR = '#FFFCA6'
OTHER_BOX_BORDER_COLOR = '#FAF33E'

## END SETTINGS ##


# this function ends a routine immediately
def endRoutine():
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "status"):
            thisComponent.status = FINISHED
        continueRoutine = False


# initialize this variable - it keeps track of whether 
# the subject is finished speaking during a time stretch trial
finished = True

##########################################################
### read in the original word list file and save word list file for this subject
##########################################################
# container array for file contents
orig_words = []
# read csv file with the original word lists (in same directory as this experiment script)
with open(WORD_LIST_FILE, 'rU') as csvfile:
    test = csv.reader(csvfile)
    for i in test:
        orig_words.append(i)

# depending on experiementer's selection at run time, either randomize word lists or
# use the experimenter's order
def fixList(x):
    return int(x)-1

if expInfo['listMethod']=='set your own':
    assignment_order = map(fixList, expInfo['listOrder'])
else:
    assignment_order = random.sample([0,1,2], 3)

# initialize word containers for the trial types
unmodified_words = []
pitch_higher_words = []
pitch_lower_words = []

# assign words to those containers
for row in orig_words:
    unmodified_words.append(row[assignment_order[0]])
    pitch_higher_words.append(row[assignment_order[1]])
    pitch_lower_words.append(row[assignment_order[2]])

# save word lists for each trial type
unmodified_word_list = unmodified_words.pop(0)
pitch_higher_word_list = pitch_higher_words.pop(0)
pitch_lower_word_list = pitch_lower_words.pop(0)

# randomize words in their lists
random.shuffle(unmodified_words)
random.shuffle(pitch_higher_words)
random.shuffle(pitch_lower_words)

# this will be the name of the wordlist csv file for this subject
wordlist_filename = filename+'_wordlist.csv'
results_filename = filename+'_summarized_results.csv'

# build a big array with all the words and also attach trialtype, block, and amount data,
# like this: [block, word, trialtype, amount, list]
master_list = []

# start pitch change at 0
pitch_amount = 0

# create blocks of 9 words and add them to master list
for block_num in range(10):
    block_words = []
    pitch_amount = pitch_amount + PITCH_DELTA
    for i in range(3):
        word_index = block_num * 3 + i
        subgroup = []
        subgroup.append([block_num+1, unmodified_words[word_index], 'unmodified', 0, unmodified_word_list])
        subgroup.append([block_num+1, pitch_higher_words[word_index], 'pitch higher', pitch_amount, pitch_higher_word_list])
        subgroup.append([block_num+1, pitch_lower_words[word_index], 'pitch lower', -1 * pitch_amount, pitch_lower_word_list])
        random.shuffle(subgroup)
        block_words += subgroup
    master_list += block_words

# save csv file to disk
with open(wordlist_filename,'wb') as w:
    writer=csv.writer(w)
    writer.writerow(['block', 'word', 'trialtype', 'amount', 'list'])
    for row in master_list:
        writer.writerow(row)

# create container for stats
# this keeps track of how many times the subject chooses "other" for
#   each trial type per block
# it gets reset each block
choice_stats = OrderedDict()
choice_stats['unmodified'] = 0 # we shouldn't need this one
choice_stats['pitch higher'] = 0
choice_stats['pitch lower'] = 0
choice_stats['pitch higher block'] = 0
choice_stats['pitch lower block'] = 0
choice_stats['pitch higher amount'] = 0
choice_stats['pitch lower amount'] = 0

# these hold the "done" status for each pitch trial type
pitch_higher_done = False
pitch_lower_done = False

# start with block number = 0
this_block = 0

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
text_4 = visual.TextStim(win=win, ori=0, name='text_4',
    text='Instructions will go here.',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
serv.start()
mic = Input(chnl=0)
text = visual.TextStim(win=win, ori=0, name='text',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "choose_source"
choose_sourceClock = core.Clock()
question = visual.TextStim(win=win, ori=0, name='question',
    text='Whose voice did you hear?',    font='Arial',
    pos=[0, .5], height=0.1, wrapWidth=2,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
self_box = visual.Rect(win=win, name='self_box',
    width=[0.5, 0.5][0], height=[0.5, 0.5][1],
    ori=0, pos=[-.5, -.5],
    lineWidth=5, lineColor=SELF_BOX_BORDER_COLOR, lineColorSpace='rgb',
    fillColor=SELF_BOX_FILL_COLOR, fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
interpolate=True)
self_label = visual.TextStim(win=win, ori=0, name='self_label',
    text='Mine',    font='Arial',
    pos=[-.5, -.5], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
other_box = visual.Rect(win=win, name='other_box',
    width=[0.5, 0.5][0], height=[0.5, 0.5][1],
    ori=0, pos=[.5, -.5],
    lineWidth=5, lineColor=OTHER_BOX_BORDER_COLOR, lineColorSpace='rgb',
    fillColor=OTHER_BOX_FILL_COLOR, fillColorSpace='rgb',
    opacity=1,depth=-3.0, 
interpolate=True)
other_label = visual.TextStim(win=win, ori=0, name='other_label',
    text='Other',    font='Arial',
    pos=[.5, -.5], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-4.0)
mouse = event.Mouse(win=win)
x, y = [None, None]


# Initialize components for Routine "thankyou"
thankyouClock = core.Clock()
text_3 = visual.TextStim(win=win, ori=0, name='text_3',
    text=u'Thank you for participating!',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)


# Initialize components for Routine "display_results"
display_resultsClock = core.Clock()
results_text = visual.TextStim(win=win, ori=0, name='results_text',
    text='default text',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=2,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "initialize_code"-------
t = 0
initialize_codeClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat

# keep track of which components have finished
initialize_codeComponents = []
for thisComponent in initialize_codeComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "initialize_code"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = initialize_codeClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in initialize_codeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "initialize_code"-------
for thisComponent in initialize_codeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "initialize_code" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "instructions"-------
t = 0
instructionsClock.reset()  # clock 
frameN = -1
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
instructionsComponents = []
instructionsComponents.append(text_4)
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instructions"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_4* updates
    if t >= 0.0 and text_4.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_4.tStart = t  # underestimates by a little under one frame
        text_4.frameNStart = frameN  # exact frame index
        text_4.setAutoDraw(True)
    if text_4.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
        text_4.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(wordlist_filename),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    routineTimer.add(11.000000)
    # update component parameters for each repeat
    
    b = Harmonizer(mic, transpo=float(amount))
    c = Gate(b, thresh=-90, falltime=0.02, lookahead=20.0).mix(2).out()
    d = Follower2(b)
    talkThresh = .08
    talkStarted = False
    stoppedTalking = False
    stopTime = 100
    
    text.setText(word)
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(text)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if d.get() > talkThresh:
                talkStarted = True
        
        if talkStarted and not stoppedTalking:
            if d.get() < talkThresh:
                stoppedTalking = True
                stopTime = globalClock.getTime() + 1
        
        if stoppedTalking and globalClock.getTime() >= stopTime:
            b.stop()
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status"):
                    thisComponent.status = FINISHED
                continueRoutine = False
        
        
        # *text* updates
        if t >= 1 and text.status == NOT_STARTED:
            # keep track of start time/frame for later
            text.tStart = t  # underestimates by a little under one frame
            text.frameNStart = frameN  # exact frame index
            text.setAutoDraw(True)
        if text.status == STARTED and t >= (1 + (10-win.monitorFramePeriod*0.75)): #most of one frame period left
            text.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    
    #------Prepare to start Routine "choose_source"-------
    t = 0
    choose_sourceClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    # setup some python lists for storing info about the mouse
    if(pitch_lower_done and pitch_higher_done):
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status"):
                thisComponent.status = FINISHED
            continueRoutine = False
    # keep track of which components have finished
    choose_sourceComponents = []
    choose_sourceComponents.append(question)
    choose_sourceComponents.append(self_box)
    choose_sourceComponents.append(self_label)
    choose_sourceComponents.append(other_box)
    choose_sourceComponents.append(other_label)
    choose_sourceComponents.append(mouse)
    for thisComponent in choose_sourceComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "choose_source"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = choose_sourceClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *question* updates
        if t >= 0.0 and question.status == NOT_STARTED:
            # keep track of start time/frame for later
            question.tStart = t  # underestimates by a little under one frame
            question.frameNStart = frameN  # exact frame index
            question.setAutoDraw(True)
        
        # *self_box* updates
        if t >= 0.0 and self_box.status == NOT_STARTED:
            # keep track of start time/frame for later
            self_box.tStart = t  # underestimates by a little under one frame
            self_box.frameNStart = frameN  # exact frame index
            self_box.setAutoDraw(True)
        
        # *self_label* updates
        if t >= 0.0 and self_label.status == NOT_STARTED:
            # keep track of start time/frame for later
            self_label.tStart = t  # underestimates by a little under one frame
            self_label.frameNStart = frameN  # exact frame index
            self_label.setAutoDraw(True)
        
        # *other_box* updates
        if t >= 0.0 and other_box.status == NOT_STARTED:
            # keep track of start time/frame for later
            other_box.tStart = t  # underestimates by a little under one frame
            other_box.frameNStart = frameN  # exact frame index
            other_box.setAutoDraw(True)
        
        # *other_label* updates
        if t >= 0.0 and other_label.status == NOT_STARTED:
            # keep track of start time/frame for later
            other_label.tStart = t  # underestimates by a little under one frame
            other_label.frameNStart = frameN  # exact frame index
            other_label.setAutoDraw(True)
        if mouse.isPressedIn(self_box, buttons=[0]):
            trials.addData('choice', 'self')
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status"):
                    thisComponent.status = FINISHED
                continueRoutine = False
        elif mouse.isPressedIn(other_box, buttons=[0]):
            trials.addData('choice','other')
            choice_stats[trialtype] += 1
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status"):
                    thisComponent.status = FINISHED
                continueRoutine = False
        
        if self_box.contains(mouse):
            self_box.fillColor = SELF_BOX_BORDER_COLOR
        else:
            self_box.fillColor = SELF_BOX_FILL_COLOR
        
        if other_box.contains(mouse):
            other_box.fillColor = OTHER_BOX_BORDER_COLOR
        else:
            other_box.fillColor = OTHER_BOX_FILL_COLOR
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in choose_sourceComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "choose_source"-------
    for thisComponent in choose_sourceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for trials (TrialHandler)
    # check if next trial is a new block. 
    # if it's a new block, check if current block had 3 "other" votes for either pitch type
    # if so,  1) record appropriate block number for that type
    #  2) set "done" flag to true for that type
    # if both pitch types are done, end the trials loop
    next_block = trials.getFutureTrial(1).block
    this_amount = block * PITCH_DELTA
    if(block != next_block):
        if(choice_stats['pitch higher'] == 3 and not pitch_higher_done):
            expInfo['pitch higher result block'] = block
            expInfo['pitch higher result amount'] = this_amount
            choice_stats['pitch higher block'] = block
            choice_stats['pitch higher amount'] = this_amount
            pitch_higher_done = True
        if(choice_stats['pitch lower'] == 3 and not pitch_lower_done):
            expInfo['pitch lower result block'] = block
            expInfo['pitch lower result amount'] = -1 * this_amount
            choice_stats['pitch lower block'] = block
            choice_stats['pitch lower amount'] = -1 * this_amount
            pitch_lower_done = True
        if(pitch_lower_done and pitch_higher_done):
            trials.finished = True
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status"):
                    thisComponent.status = FINISHED
                continueRoutine = False
        choice_stats['pitch higher'] = 0
        choice_stats['pitch lower'] = 0
    
    
    # the Routine "choose_source" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'trials'


#------Prepare to start Routine "thankyou"-------
t = 0
thankyouClock.reset()  # clock 
frameN = -1
routineTimer.add(5.000000)
# update component parameters for each repeat



# keep track of which components have finished
thankyouComponents = []
thankyouComponents.append(text_3)
for thisComponent in thankyouComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "thankyou"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = thankyouClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_3* updates
    if t >= 0.0 and text_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_3.tStart = t  # underestimates by a little under one frame
        text_3.frameNStart = frameN  # exact frame index
        text_3.setAutoDraw(True)
    if text_3.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
        text_3.setAutoDraw(False)
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in thankyouComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "thankyou"-------
for thisComponent in thankyouComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
results = '\n\r'

results += 'Pitch (higher) block = ' + str(choice_stats['pitch higher block']) + '\n\r'
results += 'Pitch (lower) block = ' + str(choice_stats['pitch lower block']) + '\n\r'
results += '\n\r'
results += 'Pitch (higher) amount = ' + str(choice_stats['pitch higher amount']) + '\n\r'
results += 'Pitch (lower) amount = ' + str(choice_stats['pitch lower amount']) + '\n\r'




#------Prepare to start Routine "display_results"-------
t = 0
display_resultsClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
results_text.setText(results)
key_resp_2 = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_2.status = NOT_STARTED
# keep track of which components have finished
display_resultsComponents = []
display_resultsComponents.append(results_text)
display_resultsComponents.append(key_resp_2)
for thisComponent in display_resultsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "display_results"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = display_resultsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *results_text* updates
    if t >= 0.0 and results_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        results_text.tStart = t  # underestimates by a little under one frame
        results_text.frameNStart = frameN  # exact frame index
        results_text.setAutoDraw(True)
    
    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t  # underestimates by a little under one frame
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['esc'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in display_resultsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "display_results"-------
for thisComponent in display_resultsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "display_results" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

serv.stop()


win.close()
core.quit()
