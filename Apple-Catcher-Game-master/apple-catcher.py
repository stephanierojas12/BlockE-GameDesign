from psychopy import core, event, gui, visual
from time import strftime
import os, csv, random
import pylab
import tools

# Condition 1: Can pause to change difficulty levels at any time
# Condition 2: Can set difficulty level once at the beginning
# Condition 3: Difficulty level changes are yoked to condition 1
# Condition 4: Difficulty level is yoked to condition 2.

# Get participant's Sona ID, participant #, and handedness via a dialog box
participantDlg = gui.Dlg()
participantDlg.addField('SONA ID:')
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Participant #')
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Handedness:', choices = ['Right', 'Left'])
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Condition:')
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Version:')
participantDlg.addText('                                                                                                               ')
participantDlg.show()

sonaID = participantDlg.data[0]
participantNum = participantDlg.data[1]
handedness = participantDlg.data[2]
condition = int(participantDlg.data[3])
yokeID = participantDlg.data[4] # The participant # that the game is yoked to (relevant only for condition 3 & 4)
participantDataDict = {'SONA ID': sonaID, 'Participant #': participantNum, 'Handedness': handedness, 'Condition': condition}
if condition == 3 or condition == 4:
	participantDataDict.update({'Yoke ID': yokeID})

# Generate window
win = visual.Window(fullscr = True, color = 'white', units = 'norm')

# Set frame rate
frameRate = 60

# Window edges (units = norm)
topWinEdge = 1.0
bottomWinEdge = -1.0
leftWinEdge = -1.0
rightWinEdge = 1.0
windowWidth = 2.0
windowHeight = 2.0

# Get mouse
mouse = event.Mouse()

# Initialize Overshoot Data Log & relevant variables
overshootDataLog = []
startBasketPosX = -1000 # the basket position the moment the apple's position has been reset to the top of the screen (the random initialization value here will be overwritten)
endBasketPosX = -1000 # the basket position the moment the apple hits the ground/basket (the random initialization value here will be overwritten)

# Initialize Frame Data Log
frameDataLog = []
frameNum = 0

# Initialize Level Data Log
# The level data log is an array of dictionaries that will collect data (i.e. gamer timer, level, apple drop time, drop interval length, apples dropped, hits, misses, near misses, % hits, % misses, % near misses) for each level that the participant plays
levelDataLog = []
i = 0 # Index for level data log

# Initialize game variables
gamePaused = 0
score = 0 # +1 point for every apple caught (counts for whole game, not per level)
hits = 0 # Number of apples caught per level
nearMisses = 0 # A 'near miss' is when an apple falls within a 3 basket width range (1 basket width from the actual basket on each side)
misses = 0 # A (complete) 'miss' is when an apple falls outside of the near miss range
appleNum = 0 # The number of apples dropped so far
catchStatus = 0 # 1 = hit, 2 = near miss, 3 = miss
levelChangeTime = 0 # The game time when the level is changed
prevLevelChangeTime = 0 # Keeps track of the previous level change time
totalTimePlayed = 0

# Time variables (Unit = seconds)
practisePlayLength = 1 # Practise play time (excluding pauses)
gamePlayLength = 7 # Play time (excluding pauses) should max out at 10 minutes
dropIntervalClock = core.Clock()
pauseClock = core.Clock()

#################################### Instruction / Text Display Screens #################################### 
# Pre-Study (ps) Probe Instruction Screen
psProbeInstructions = visual.TextStim(win, wrapWidth = 1.8, text = 'Please answer the questions on the following screen.', color = 'black', height = 0.08, pos = (0, 0.5))
psProbeStartButtonBoxPosX = 0
psProbeStartButtonBoxPosY = 0
psProbeStartButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (psProbeStartButtonBoxPosX, psProbeStartButtonBoxPosY))
psProbeStartButtonText = visual.TextStim(win, text = 'Next', color = 'black', height = 0.08, pos = (psProbeStartButtonBoxPosX, psProbeStartButtonBoxPosY))
psProbeStartButton = tools.Button(psProbeStartButtonBox, mouse)

# Pre-Study Probe Screen
psQ1 = visual.TextStim(win, alignHoriz = 'left', text = 'How bored are you right now?', color = 'black', height = 0.08, pos = (-0.9, 0.7))
psQ2 = visual.TextStim(win, alignHoriz = 'left', text = 'How motivated are you for this task?', color = 'black', height = 0.08, pos = (-0.9, 0.4))
psQ1Scale = tools.BoxScale(win, boxLineColor = 'black', boxFillColor = 'lightgrey', textColor = 'black', activeFillColor = 'white', activeTextColor = 'red', width = 0.7, height = 0.15, pos = (0.5, 0.7))
psQ2Scale = tools.BoxScale(win, boxLineColor = 'black', boxFillColor = 'lightgrey', textColor = 'black', activeFillColor = 'white', activeTextColor = 'red', width = 0.7, height = 0.15, pos = (0.5, 0.4))
psLikertLabel1 = visual.TextStim(win, text = 'Not at all', color = 'black', height = 0.07, pos = (0.2, 0.9))
psLikertLabel2 = visual.TextStim(win, text = 'Neutral', color = 'black', height = 0.07, pos = (0.5, 0.9))
psLikertLabel3 = visual.TextStim(win, text = 'Extremely', color = 'black', height = 0.07, pos = (0.8, 0.9))
psQ1Answer = 'none' # Default answer (before participant chooses an answer) is none 
psQ2Answer = 'none'
psProbeSubmitButtonBoxPosX = 0
psProbeSubmitButtonBoxPosY = -0.8
psProbeSubmitButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (psProbeSubmitButtonBoxPosX, psProbeSubmitButtonBoxPosY))
psProbeSubmitButtonText = visual.TextStim(win, text = 'Submit', color = 'black', height = 0.08, pos = (psProbeSubmitButtonBoxPosX, psProbeSubmitButtonBoxPosY))
psProbeSubmitButton = tools.Button(psProbeSubmitButtonBox, mouse)
psProbeSubmitButtonClicked = False
psProbeSubmitError = False
psProbeSubmitErrorMsg = visual.TextStim(win, wrapWidth = 1.6, text = 'Please select an answer for all the questions.', color = 'red', height = 0.08, pos = (0, -0.2))

# Practise Trial Instruction Screen
practiseInstructions = visual.TextStim(win, wrapWidth = 1.6, text = "Before you start the game, you will have about a minute to practise. Catch as many apples as you can by dragging the basket. Try changing the difficulty of the game by pressing pause to adjust the difficulty level using the scale in the bottom right corner of the screen. Level 1 is the easiest and level 7 is the hardest. Press next to start the practise round.", color = 'black', height = 0.08, pos = (0, 0.3))
practiseButtonBoxPosX = 0
practiseButtonBoxPosY = -0.5
practiseButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (practiseButtonBoxPosX, practiseButtonBoxPosY))
practiseButtonText = visual.TextStim(win, text = 'Next', color = 'black', height = 0.08, pos = (practiseButtonBoxPosX, practiseButtonBoxPosY))
practiseButton = tools.Button(practiseButtonBox, mouse)

# Game Instruction screen
if condition == 1:
	gameInstructionsText = 'You have finished the practise round. Like in the practise round, you will be able to change the difficulty level at any time to suit your preference by pressing the pause button to activate the difficulty scale in the bottom right corner. Level 1 is the easiest and level 7 is the hardest. Press start when you are ready to play.'
	startButtonBoxPosY = -0.5
elif condition == 2:
	gameInstructionsText = 'You have finished the practise round. Before you start the game, choose how difficult you want the game to be using the scale below. Level 1 is the easiest and level 7 is the hardest. Unlike the practise round, you will *not* be able to change the difficulty of the game once you start. Press start when you are ready to play.'
	startButtonBoxPosY = -0.75
elif condition == 3:
	gameInstructionsText = 'You have finished the practise round. Unlike the practise round, you will *not* be able to change the difficulty level of the game. The difficulty of the game may or may not change as you play, but you will not be able to choose when these changes happen. Press start when you are ready to play.'
	startButtonBoxPosY = -0.5
elif condition == 4:
	gameInstructionsText = 'You have finished the practise round. Unlike the practise round, you will *not* be able to change the difficulty level of the game. The difficulty of the game may or may not change as you play, but you will not be able to choose when these changes happen. Press start when you are ready to play.'
	startButtonBoxPosY = -0.5
gameInstructions = visual.TextStim(win, wrapWidth = 1.6, text = gameInstructionsText, color = 'black', height = 0.08, pos = (0, 0.3))
difficultyScaleCond2 = tools.Scale(win, scaleColor = 'black', activeColor = 'red', startLevel = 4, width = 0.5, height = 0.05, pos = (0, -0.5)) # Difficulty scale for condition 2 where participants set their difficulty level for the game
startButtonBoxPosX = 0
startButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButtonText = visual.TextStim(win, text = 'start', color = 'black', height = 0.08, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButton = tools.Button(startButtonBox, mouse)

# Probe Instruction Screen
probeInstructions = visual.TextStim(win, wrapWidth = 1.6, text = 'We now have a couple questions about your experience of the game. On the following screen, you will see the questions with rating scales next to them.', color = 'black', height = 0.08, pos = (0, 0.5))
probeStartButtonBoxPosX = 0
probeStartButtonBoxPosY = 0
probeStartButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (probeStartButtonBoxPosX, probeStartButtonBoxPosY))
probeStartButtonText = visual.TextStim(win, text = 'Next', color = 'black', height = 0.08, pos = (probeStartButtonBoxPosX, probeStartButtonBoxPosY))
probeStartButton = tools.Button(probeStartButtonBox, mouse)

# Probe Screen
q1 = visual.TextStim(win, alignHoriz = 'left', text = 'How bored were you during the game?', color = 'black', height = 0.08, pos = (-0.9, 0.7))
q2 = visual.TextStim(win, alignHoriz = 'left', text = 'How frustrated were you during the game?', color = 'black', height = 0.08, pos = (-0.9, 0.4))
q3 = visual.TextStim(win, alignHoriz = 'left', text = 'How motivated were you during the game?', color = 'black', height = 0.08, pos = (-0.9, 0.1))
q4 = visual.TextStim(win, alignHoriz = 'left', text = 'How difficult did you find the game?', color = 'black', height = 0.08, pos = (-0.9, -0.2))
q5 = visual.TextStim(win, alignHoriz = 'left', text = 'How in control did you feel during the game?', color = 'black', height = 0.08, pos = (-0.9, -0.5))
q1Scale = tools.BoxScale(win, boxLineColor = 'black', boxFillColor = 'lightgrey', textColor = 'black', activeFillColor = 'white', activeTextColor = 'red', width = 0.7, height = 0.15, pos = (0.5, 0.7))
q2Scale = tools.BoxScale(win, boxLineColor = 'black', boxFillColor = 'lightgrey', textColor = 'black', activeFillColor = 'white', activeTextColor = 'red', width = 0.7, height = 0.15, pos = (0.5, 0.4))
q3Scale = tools.BoxScale(win, boxLineColor = 'black', boxFillColor = 'lightgrey', textColor = 'black', activeFillColor = 'white', activeTextColor = 'red', width = 0.7, height = 0.15, pos = (0.5, 0.1))
q4Scale = tools.BoxScale(win, boxLineColor = 'black', boxFillColor = 'lightgrey', textColor = 'black', activeFillColor = 'white', activeTextColor = 'red', width = 0.7, height = 0.15, pos = (0.5, -0.2))
q5Scale = tools.BoxScale(win, boxLineColor = 'black', boxFillColor = 'lightgrey', textColor = 'black', activeFillColor = 'white', activeTextColor = 'red', width = 0.7, height = 0.15, pos = (0.5, -0.5))
likertLabel1 = visual.TextStim(win, text = 'Not at all', color = 'black', height = 0.07, pos = (0.2, 0.9))
likertLabel2 = visual.TextStim(win, text = 'Neutral', color = 'black', height = 0.07, pos = (0.5, 0.9))
likertLabel3 = visual.TextStim(win, text = 'Extremely', color = 'black', height = 0.07, pos = (0.8, 0.9))
q1Answer = 'none' # Default answer (before participant chooses an answer) is none 
q2Answer = 'none'
q3Answer = 'none'
q4Answer = 'none'
q5Answer = 'none'
probeSubmitButtonBoxPosX = 0
probeSubmitButtonBoxPosY = -0.8
probeSubmitButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (probeSubmitButtonBoxPosX, probeSubmitButtonBoxPosY))
probeSubmitButtonText = visual.TextStim(win, text = 'Submit', color = 'black', height = 0.08, pos = (probeSubmitButtonBoxPosX, probeSubmitButtonBoxPosY))
probeSubmitButton = tools.Button(probeSubmitButtonBox, mouse)
probeSubmitButtonClicked = False
probeSubmitError = False
probeSubmitErrorMsg = visual.TextStim(win, wrapWidth = 0.5, text = 'Please select an answer for all the questions.', color = 'red', height = 0.08, pos = (0.5, probeSubmitButtonBoxPosY))


# End Screen
endText = visual.TextStim(win, wrapWidth = 2, text = 'This is the end of the study. Please get the experimenter.', color = 'black', height = 0.08)
#################################### #################################### #################################### 

# Specify game play area (units = norm)
gameAreaWidth = windowWidth
gameAreaHeight = windowHeight * (9.0/10.0) # The game play area is 9/10th the size of the window
gameAreaPosX = 0 
gameAreaPosY = (windowHeight - gameAreaHeight)/2.0
topGameAreaEdge = gameAreaPosY + gameAreaHeight/2.0
bottomGameAreaEdge = gameAreaPosY - gameAreaHeight/2.0
leftGameAreaEdge = gameAreaPosX - gameAreaWidth/2.0
rightGameAreaEdge = gameAreaPosX + gameAreaWidth/2.0

# Background image parameters environment
bkgimg = 'tree-bkg.png'
bkgPosX = leftGameAreaEdge + gameAreaWidth/2.0
bkgPosY = topGameAreaEdge - gameAreaHeight/2.0
bkg = visual.ImageStim(win, image = bkgimg, size = (gameAreaWidth, gameAreaHeight), pos = (bkgPosX, bkgPosY), opacity = 1)
bkgPauseOverlay = visual.Rect(win, fillColor = 'white', width = gameAreaWidth, height = gameAreaHeight, pos = (bkgPosX, bkgPosY), opacity = 0)

# Basket parameters (norm units)
basketWidth = 0.1
basketHeight = 0.08
basketImg = 'basket.png'
basket = visual.ImageStim(win, image = basketImg, size = (basketWidth, basketHeight))
basketPosX = gameAreaPosX # Basket starts at the center of the game area
basketPosY = bottomGameAreaEdge + basketHeight/2.0 # The vertical position of the basket is fixed

# Apple image parameters (norm units)
appleWidth = 0.05
appleHeight = 0.1
appleImg = 'apple.png'
apple = visual.ImageStim(win, image = appleImg, size = (appleWidth, appleHeight))

# Apple animation settings 
difficultyLevel = 4 # Initial setting
difficultyDict = { # difficultyDict is a dictionary containing a dictionary of 'interval' & 'drop time' settings associated with each difficulty level
	1: {'interval': 0.6, 'drop time': 1.4}, 
	2: {'interval': 0.5, 'drop time': 1.25}, 
	3: {'interval': 0.4, 'drop time': 1.1}, 
	4: {'interval': 0.3, 'drop time': 0.95},  
	5: {'interval': 0.2, 'drop time': 0.8}, 
	6: {'interval': 0.1, 'drop time': 0.65}, 
	7: {'interval': 0, 'drop time': 0.5}}
dropIntervalLength = difficultyDict[difficultyLevel]['interval'] # Unit = seconds. Time (excluding pauses) between apple drops from when last apple hit the ground to when the next apple drops
appleDropTime = difficultyDict[difficultyLevel]['drop time'] # Unit = seconds. The time it takes for an apple to hit the ground.
appleDecrement = gameAreaHeight/(frameRate*appleDropTime) # The decrement is how much down the screen the apple should drop per frame
appleStartPosX = random.uniform(leftGameAreaEdge + appleWidth/2.0, rightGameAreaEdge - appleWidth/2.0)
appleStartPosY = topGameAreaEdge + appleHeight/2
applePosX = appleStartPosX
applePosY = appleStartPosY

# Game options box (the area containing pause button, score, difficulty level scale)
optionsBoxWidth = windowWidth
optionsBoxHeight = windowHeight - gameAreaHeight
optionsBoxPosX = 0
optionsBoxPosY = bottomGameAreaEdge - optionsBoxHeight/2.0
optionsBox = visual.Rect(win, fillColor = 'grey', width = optionsBoxWidth, height = optionsBoxHeight, pos = (optionsBoxPosX, optionsBoxPosY))

# Difficulty Scale
difficultyScale = tools.Scale(win, scaleColor = 'white', activeColor = 'red', startLevel = 4, width = 0.5, height = 0.05, pos = (0.6, optionsBoxPosY), opacity = 0.3)

# Score display
scoreDisplay = visual.TextStim(win, text = 'Score: 0', color = 'white', height = 0.08, pos = (0, optionsBoxPosY + 0.04))

# Fake high score
highScore = 1749
highScoreDisplay =  visual.TextStim(win, text = 'High score: ' + str(highScore), color = 'red', height = 0.05, pos = (0, optionsBoxPosY - 0.04))

# Game Timer Visual
timerStim = visual.TextStim(win, text = "", color = 'white', height = 0.1, pos = (0, 0.9))

# Pause button
pauseButtonBoxPosX = -0.75
pauseButtonBoxPosY = optionsBoxPosY
pauseButtonBox = visual.Rect(win, fillColor ='darkgrey', width = 0.3, height = 0.15, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
pauseButtonText = visual.TextStim(win, text = 'Pause', color = 'white', height = 0.08, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
pauseButton = tools.Button(pauseButtonBox, mouse)

def displayPSProbeInstructions(): # display pre-study probe instructions
	psProbeInstructions.draw()
	psProbeStartButtonBox.draw()
	psProbeStartButtonText.draw()

def displayPSProbe(): # display pre-study probe screen
	global psQ1Answer
	global psQ2Answer
	global psProbeSubmitError
	global psProbeSubmitButtonClicked

	psQ1.draw()
	psQ2.draw()
	psLikertLabel1.draw()
	psLikertLabel2.draw()
	psLikertLabel3.draw()
	if psQ1Scale.hasRatingChanged():
		psQ1Answer = psQ1Scale.activeRating
	if psQ2Scale.hasRatingChanged():
		psQ2Answer = psQ2Scale.activeRating
	psQ1Scale.draw()
	psQ2Scale.draw()
	psProbeSubmitButtonBox.draw()
	psProbeSubmitButtonText.draw()

	psProbeSubmitButtonClicked = psProbeSubmitButton.isClicked() # Track whether the submit button has been clicked

	# Display error message to participant if the participant tries to click the submit button without selecting an answer for all the questions
	if psProbeSubmitButtonClicked and (psQ1Answer == 'none' or psQ2Answer == 'none'):
		psProbeSubmitError = True
	if psProbeSubmitError:
		psProbeSubmitErrorMsg.draw()

def displayGameInstructions():
	gameInstructions.draw()
	if condition == 2:
		if difficultyScaleCond2.hasLevelChanged():
			changeDifficulty(difficultyScaleCond2.activeLevel)
		difficultyScaleCond2.draw()
	startButtonBox.draw()
	startButtonText.draw()

def displayPractiseScreen():
	practiseInstructions.draw()
	practiseButtonBox.draw()
	practiseButtonText.draw()

def displayEndScreen():
	while True:
		if event.getKeys(keyList = ['q','escape']):
			core.quit()
		endText.draw()
		win.flip()

def updateTimerText():
	global timerStim
	time = gamePlayClock.getTime()
	minutes = int(time/60)
	seconds = int(time)%60
	timerText = str(minutes).zfill(2) + ':' + str(seconds).zfill(2) # create a string of characters representing the time
	timerStim.text = timerText

def getBasketEdges():
	basketTopEdge = basketPosY + basketHeight/2.0
	basketBottomEdge = basketPosY - basketHeight/2.0
	basketLeftEdge = basketPosX - basketWidth/2.0
	basketRightEdge = basketPosX + basketWidth/2.0
	return {'top': basketTopEdge, 'bottom': basketBottomEdge, 'left': basketLeftEdge, 'right': basketRightEdge}

def getAppleEdges():
	appleTopEdge = applePosY + appleHeight/2.0
	appleBottomEdge = applePosY - appleHeight/2.0
	appleLeftEdge = applePosX - appleWidth/2.0
	appleRightEdge = applePosX + appleWidth/2.0
	return {'top': appleTopEdge, 'bottom': appleBottomEdge, 'left': appleLeftEdge, 'right': appleRightEdge}

# Move basket to track the mouse 
def moveBasket():
	mousePos = mouse.getPos()
	global basketPosX
	basketPosX = mousePos[0] # Set basket's x position to the mouse's x position
	basketEdges = getBasketEdges()
	# Restrict basket within the game area
	if basketEdges['left'] <= leftGameAreaEdge:
		basketPosX = leftGameAreaEdge + basketWidth/2.0
	elif basketEdges['right'] >= rightGameAreaEdge:
		basketPosX = rightGameAreaEdge - basketWidth/2.0
	basket.setPos([basketPosX, basketPosY])

def isAppleCaught():
	basketEdges = getBasketEdges()
	appleEdges = getAppleEdges()
	if (appleEdges['left'] <= basketEdges['right']) & (appleEdges['right'] >= basketEdges['left']) & (appleEdges['bottom'] <= basketEdges['top']): # If the apple is overlapping the same horizontal space (column) as the basket... & If the apple's bottom is touching or is below the top of the basket...  if the apple's decrement is larger than the basket, then it could skip over the basket and end up under the basket
		return True
	else:
		return False

def isAppleTouchingGround():
	appleEdges = getAppleEdges()
	if appleEdges['bottom'] <= bottomGameAreaEdge:
		return True
	else:
		return False

# Checks for near misses & misses. Update these counts.
def updateMisses():
	global nearMisses
	global misses
	global catchStatus
	basketEdges = getBasketEdges()
	appleEdges = getAppleEdges()
	if isAppleCaught() == False & isAppleTouchingGround(): # If the apple hit the ground not in the basket, then check whether it is a near miss or a (complete) miss
		if (appleEdges['left'] <= basketEdges['right'] + basketWidth) & (appleEdges['right'] >= basketEdges['left'] - basketWidth):
			nearMisses += 1
			catchStatus = 2
		else:
			misses +=1
			catchStatus = 3

# Update score & hit counts if apple has been caught.
def updateScoreAndHits():
	global score
	global hits
	global catchStatus
	if isAppleCaught():
		score += 1
		hits +=1
		catchStatus = 1
		scoreDisplay.setText('Score: ' + str(score))

# Reset apple position to top of screen. Also reset the drop interval clock.
def resetApple():
	global applePosX
	global applePosY
	global appleNum
	global startBasketPosX
	dropIntervalClock.reset()
	applePosY = appleStartPosY
	applePosX = random.uniform(leftGameAreaEdge + appleWidth/2.0, rightGameAreaEdge - appleWidth/2.0)
	while abs(applePosX - basketPosX) < (basketWidth/2.0 + basketWidth + appleWidth/2.0): # Make sure the new apple drops at least a certain distance from the basket to prevent any default hits or default near misses (new apple should fall greater than half a basket width + basket width + half the apple's width from the participant's basket to force the participant to move their basket to get a hit/near miss)
		applePosX = random.uniform(leftGameAreaEdge + appleWidth/2.0, rightGameAreaEdge - appleWidth/2.0)
	apple.setPos([applePosX, applePosY])
	appleNum += 1
	startBasketPosX = basket.pos[0] # Get the basket's x position when the apple has been reset (this is used to calculate overshoot)

# Move the apple's position down
def decrementApple():
	global applePosY
	applePosY -= appleDecrement
	apple.setPos([applePosX, applePosY])

# Checks for and updates hits/misses. Update apple position.
def updateApple():
	global endBasketPosX
	if isAppleCaught() or isAppleTouchingGround():
		endBasketPosX = basket.pos[0] # Get the basket's x position when the apple hits the basket/ground (this is used to calculate overshoot)
		updateMisses() # Check for & update misses & near misses
		updateScoreAndHits() # Check for & update hits & the score
		logOvershootData()
		resetApple()
	else:
		decrementApple()

# Change difficulty level of game (including how fast the apple falls and interval between apple drops)
def changeDifficulty(newDifficultyLevel):
	global difficultyLevel
	global dropIntervalLength
	global appleDropTime
	global appleDecrement
	difficultyLevel = newDifficultyLevel
	dropIntervalLength = difficultyDict[difficultyLevel]['interval']
	appleDropTime = difficultyDict[difficultyLevel]['drop time']
	appleDecrement = gameAreaHeight/(frameRate*appleDropTime)

def pauseGame():
	bkgPauseOverlay.opacity = 0.5
	difficultyScale.setOpacity(1)
	pauseButtonText.text = 'Resume'
	pauseClock.reset()

def resumeGame():
	gamePlayClock.add(pauseClock.getTime()) # This effectively subtracts the pause time from the game play time
	dropIntervalClock.add(pauseClock.getTime())
	bkgPauseOverlay.opacity = 0
	difficultyScale.setOpacity(0.5)
	pauseButtonText.text = 'Pause'

# Update the levelDataLog with the number of apples dropped, caught (hit), missed, and near-missed during the level. Then reset the apple catch data variables.
def logAppleCatchData():
	global hits
	global misses
	global nearMisses
	global levelChangeTime
	global prevLevelChangeTime

	applesDropped = hits + misses + nearMisses
	if applesDropped > 0:
		percentHits = (hits/float(applesDropped))*100
		percentMisses = (misses/float(applesDropped))*100
		percentNearMisses = (nearMisses/float(applesDropped))*100
	else:
		percentHits = 0
		percentMisses = 0
		percentNearMisses = 0

	# Calculate the time spent in level and update the previous level change time
	levelChangeTime = gamePlayClock.getTime()
	timeSpentInLevel = levelChangeTime - prevLevelChangeTime
	prevLevelChangeTime = levelChangeTime

	levelDataLog[i].update({'Time Spent In Level': timeSpentInLevel, 'Apples Dropped': applesDropped, 'Hits': hits, 'Misses': misses, 'Near Misses': nearMisses, '% Hits': percentHits, '% Misses': percentMisses, '% Near Misses': percentNearMisses})
	hits = 0
	misses = 0
	nearMisses = 0

# For every apple drop, log the following data: Level, Apple #, Catch status (1=hit/2=near miss/3=miss), Overshoot (distance b/t apple center & basket center when the apple hits the ground/basket in norm units), Start basket x-pos (when apple is at reset position), End basket x-pos (when apple hits ground/basket), Apple x-pos
def logOvershootData():
	applePosX = apple.pos[0]
	appleBasketDist = abs(applePosX - endBasketPosX) # Distance between the apple and the end basket

	# Determine overshoot status: perfect, undershoot, or overshoot
	# Perfect catch = Center of the basket exactly matches the center of the apple, Undershoot = end basket is on the same side of the apple as the start basket, Overshoot = end basket has passed the apple and is now on the other side of the apple compared to where it started
	if endBasketPosX == applePosX:
		shootStatus = 'Perfect'
	elif (startBasketPosX < applePosX and endBasketPosX < applePosX) or (startBasketPosX > applePosX and endBasketPosX > applePosX):
		shootStatus = 'Undershoot'
	elif (startBasketPosX < applePosX and endBasketPosX > applePosX) or (startBasketPosX > applePosX and endBasketPosX < applePosX):
		shootStatus = 'Overshoot'
	overshootDataLog.append({'Level': difficultyLevel, 'Apple #': appleNum, 'Catch Status (1 = hit, 2 = near miss, 3 = miss)': catchStatus, 'End Distance From Apple': appleBasketDist, 'Shoot Status': shootStatus, 'Start Basket Pos X': startBasketPosX, 'End Basket Pos X': endBasketPosX, 'Apple Pos X': applePosX})

# For every frame, log the following game data: Time (actual time, not game timer), Frame, Level, Game Paused (1 = game is paused), Apple #, Basket Pos X, Basket Pos Y, Apple Pos X, Apple Pos Y
def logFrameData():
	time = strftime("%H:%M:%S") 
	basketPosX = basket.pos[0]
	basketPosY = basket.pos[1]
	applePosX = apple.pos[0]
	applePosY = apple.pos[1]
	frameDataLog.append({'SONA ID': sonaID, 'Time': time, 'Frame': frameNum, 'Game Paused': gamePaused, 'Level': difficultyLevel, 'Apple #': appleNum, 'Basket Pos X': basketPosX, 'Basket Pos Y': basketPosY, 'Apple Pos X': applePosX, 'Apple Pos Y': applePosY})

# Draw game graphics common to practise trial and all conditions
def drawCommonGameGraphics():
	bkg.draw()
	apple.draw()
	basket.draw()
	optionsBox.draw()
	scoreDisplay.draw()
	highScoreDisplay.draw()

# Play practise trial for participant
def playPractise():
	global gamePaused

	if (not gamePaused):
		moveBasket()
		if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
			updateApple()
	elif difficultyScale.hasLevelChanged():
		changeDifficulty(difficultyScale.activeLevel)

	if pauseButton.isClicked():
		gamePaused = 1 - gamePaused # Flip pause status of game from 0 to 1 or vice versa
		if gamePaused:
			pauseGame()
		else:
			resumeGame()

	drawCommonGameGraphics()
	difficultyScale.draw()
	pauseButtonBox.draw()
	pauseButtonText.draw()
	bkgPauseOverlay.draw()

def playCond1():
	global gamePaused
	global i

	if (not gamePaused):
		moveBasket()
		if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
			updateApple()
		updateTimerText()
	elif difficultyScale.hasLevelChanged():
		changeDifficulty(difficultyScale.activeLevel)

	if pauseButton.isClicked():
		gamePaused = 1 - gamePaused # Flip pause status of game from 0 to 1 or vice versa
		if gamePaused:
			pauseGame()
		else:
			resumeGame()
			if levelDataLog[i]['Level'] != difficultyLevel: # Relevant only to Condition 1: If the difficulty level has changed upon resume, update the level data log.
				logAppleCatchData()
				levelDataLog.append({'Level Change Time': levelChangeTime, 'Level': difficultyLevel, 'Apple Drop Time': appleDropTime, 'Drop Interval Length': dropIntervalLength})
				i += 1

	drawCommonGameGraphics()
	difficultyScale.draw()
	timerStim.draw()
	pauseButtonBox.draw()
	pauseButtonText.draw()
	bkgPauseOverlay.draw()

def playCond2():
	moveBasket()
	if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
		updateApple()

	updateTimerText()
	drawCommonGameGraphics()
	timerStim.draw()

def playCond3():
	global i
	global nextLevelChangeTime

	moveBasket()
	if gamePlayClock.getTime() >= nextLevelChangeTime: 
		logAppleCatchData()
		i += 1
		changeDifficulty(levelDataLog[i]['Level']) # Yoke difficulty level to that of condition 1
		levelDataLog[i].update({'Apple Drop Time': appleDropTime, 'Drop Interval Length': dropIntervalLength})
		if i+1 < len(levelDataLog):
			nextLevelChangeTime = levelDataLog[i+1]['Level Change Time']
		else:
			nextLevelChangeTime = gamePlayLength + 100 # If there are no more level changes, make the next level change time unreachable

	if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
		updateApple()

	updateTimerText()
	drawCommonGameGraphics()
	timerStim.draw()

def playCond4():
	moveBasket()
	if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
		updateApple()

	updateTimerText()
	drawCommonGameGraphics()
	timerStim.draw()

# Create a csv file from overshootDataLog 
def createOvershootLogCsv():
	if condition == 1:
		outputFolderName = 'Overshoot-Data-Logs_Condition-1'
	elif condition == 2:
		outputFolderName = 'Overshoot-Data-Logs_Condition-2'
	elif condition == 3:
		outputFolderName = 'Overshoot-Data-Logs_Condition-3'
	elif condition == 4:
		outputFolderName = 'Overshoot-Data-Logs_Condition-4'

	outputFileName = sonaID + '.csv'
	outputFilePath = os.path.join(os.getcwd(), outputFolderName, outputFileName)

	# If the output folder does not exist, create it
	if not os.path.exists(outputFolderName):
		os.makedirs(outputFolderName)

	column_labels = ['Level', 'Apple #', 'Catch Status (1 = hit, 2 = near miss, 3 = miss)', 'End Distance From Apple', 'Shoot Status', 'Start Basket Pos X', 'End Basket Pos X', 'Apple Pos X']
	with open(outputFilePath, 'wb') as new_csvfile:
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		writer.writeheader()
		for entry in overshootDataLog:
			writer.writerow(entry)

# Create a csv file from frameDataLog with the frame by frame game data
def createFrameLogCsv():
	if condition == 1:
		outputFolderName = 'Frame-Data-Logs_Condition-1'
	elif condition == 2:
		outputFolderName = 'Frame-Data-Logs_Condition-2'
	elif condition == 3:
		outputFolderName = 'Frame-Data-Logs_Condition-3'
	elif condition == 4:
		outputFolderName = 'Frame-Data-Logs_Condition-4'

	outputFileName = sonaID + '.csv'
	outputFilePath = os.path.join(os.getcwd(), outputFolderName, outputFileName)

	# If the output folder does not exist, create it
	if not os.path.exists(outputFolderName):
		os.makedirs(outputFolderName)

	column_labels = ['SONA ID', 'Time', 'Frame', 'Game Paused', 'Level', 'Apple #', 'Basket Pos X', 'Basket Pos Y', 'Apple Pos X', 'Apple Pos Y']
	with open(outputFilePath, 'wb') as new_csvfile:
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		writer.writeheader()
		for entry in frameDataLog:
			writer.writerow(entry)

# Create a csv file containing level change data. Used only in Condition 1 to save the participant's level changes to a csv (which will later be used for yoking in Condition 3).
def createChangeLogCsv():
	outputFileName = participantNum + '.csv'
	outputFolderName = 'Condition-1_Level-Change-Logs'
	outputFilePath = os.path.join(os.getcwd(), outputFolderName, outputFileName)

	# If the output folder does not exist, create it
	if not os.path.exists(outputFolderName):
		os.makedirs(outputFolderName)

	column_labels = ['Level Change Time', 'Level']
	with open(outputFilePath, 'wb') as new_csvfile:
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		writer.writeheader()
		for entry in levelDataLog:
			levelChangeDict = {'Level Change Time': entry['Level Change Time'], 'Level': entry['Level']} # Extract just the 'Level Change Time' and 'Level' data from levelDataLog (these are the data needed for yoking)
			writer.writerow(levelChangeDict)

# Converts csv containing level changes (from participant in Condition 1) to an array of dictionaries. Used only in Condition 3 for yoking.
def changeLogCsvToDict():
	inputFileName = yokeID + '.csv'
	inputFolderName = 'Condition-1_Level-Change-Logs'
	inputFilePath = os.path.join(os.getcwd(), inputFolderName, inputFileName)
	with open(inputFilePath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			levelDataLog.append({'Level Change Time': float(row['Level Change Time']), 'Level': int(row['Level'])})

# Create a csv file containing the difficulty level that the participant in Condition 2 chose. Used only in Condition 2 to save the participant's level choice to a csv (which will later be used for yoking in Condition 4).
def createCond2LevelCsv():
	outputFileName = participantNum + '.csv'
	outputFolderName = 'Condition-2_Level-Logs'
	outputFilePath = os.path.join(os.getcwd(), outputFolderName, outputFileName)

	# If the output folder does not exist, create it
	if not os.path.exists(outputFolderName):
		os.makedirs(outputFolderName)

	column_labels = ['Level']
	with open(outputFilePath, 'wb') as new_csvfile:
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		writer.writeheader()
		writer.writerow({'Level': difficultyLevel})

# Gets the level choice of the participant in Condition 2 that the current participant in Condition 4 is yoked to. Used only in Condition 4 for yoking.
def getYokedLevel():
	inputFileName = yokeID + '.csv'
	inputFolderName = 'Condition-2_Level-Logs'
	inputFilePath = os.path.join(os.getcwd(), inputFolderName, inputFileName)
	with open(inputFilePath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			yokedLevel = int(row['Level'])
		return yokedLevel

# Write participant data to two csv files (individual participant file and master file with data of all participants of the same condition)
def participantDataToCsv():
	if condition == 1:
		outputFolderName = 'Individual-Participant-Data_Condition-1' # folder name for individual participant data files
		masterFileName = 'Master-Participant-Data_Condition-1.csv'  # filepath for the master participant data file
	elif condition == 2:
		outputFolderName = 'Individual-Participant-Data_Condition-2'
		masterFileName = 'Master-Participant-Data_Condition-2.csv'
	elif condition == 3:
		outputFolderName = 'Individual-Participant-Data_Condition-3'
		masterFileName = 'Master-Participant-Data_Condition-3.csv'
	elif condition == 4:
		outputFolderName = 'Individual-Participant-Data_Condition-4'
		masterFileName = 'Master-Participant-Data_Condition-4.csv'

	outputFileName = 'PID' + '-'+ participantNum + '_' + date + '_' + strftime('%H%M%S') + '.csv' # file name format for individual participant data files
	outputFilePath = os.path.join(os.getcwd(), outputFolderName, outputFileName) # filepath for individual participant data files

	# If the output folder does not exist, create it
	if not os.path.exists(outputFolderName):
		os.makedirs(outputFolderName)

	if condition == 1 or condition == 2:
		column_labels = ['Date', 'Time', 'SONA ID', 'Participant #', 'Handedness', 'Condition', 'Pre Q1', 'Pre Q2', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Total Time Played', 'Level Change Time', 'Time Spent In Level', 'Level', 'Apple Drop Time', 'Drop Interval Length', 'Apples Dropped', 'Hits', 'Misses', 'Near Misses', '% Hits', '% Misses', '% Near Misses']
	elif condition == 3 or condition == 4:
		column_labels = ['Date', 'Time', 'SONA ID', 'Participant #', 'Handedness', 'Condition', 'Yoke ID', 'Pre Q1', 'Pre Q2', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Total Time Played', 'Level Change Time', 'Time Spent In Level', 'Level', 'Apple Drop Time', 'Drop Interval Length', 'Apples Dropped', 'Hits', 'Misses', 'Near Misses', '% Hits', '% Misses', '% Near Misses']

	with open(outputFilePath, 'wb') as new_csvfile: # writes to new file (individual participant data file)
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		writer.writeheader()
		for entry in levelDataLog:
			participantDataDict.update(entry)
			writer.writerow(participantDataDict)

	masterFilePath = os.path.join(os.getcwd(), masterFileName) # filepath for the master participant data file (holds data of all participants in 1 file)
	masterFileExists = os.path.isfile(masterFilePath) # Boolean variable for whether the master file already exists
	with open(masterFilePath, 'ab') as new_csvfile: # appends the same data as above to master participant data file
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		if not masterFileExists: # if master participant file does not already exist, create a new file with headers (otherwise, do nothing & just append data to existing file)
			writer.writeheader()
		for entry in levelDataLog:
			participantDataDict.update(entry)
			writer.writerow(participantDataDict)

def displayProbeInstructions():
	probeInstructions.draw()
	probeStartButtonBox.draw()
	probeStartButtonText.draw()

def displayProbe():
	global q1Answer
	global q2Answer
	global q3Answer
	global q4Answer
	global q5Answer
	global probeSubmitButtonClicked
	global probeSubmitError

	q1.draw()
	q2.draw()
	q3.draw()
	q4.draw()
	q5.draw()
	likertLabel1.draw()
	likertLabel2.draw()
	likertLabel3.draw()
	if q1Scale.hasRatingChanged():
		q1Answer = q1Scale.activeRating
	if q2Scale.hasRatingChanged():
		q2Answer = q2Scale.activeRating
	if q3Scale.hasRatingChanged():
		q3Answer = q3Scale.activeRating
	if q4Scale.hasRatingChanged():
		q4Answer = q4Scale.activeRating
	if q5Scale.hasRatingChanged():
		q5Answer = q5Scale.activeRating
	q1Scale.draw()
	q2Scale.draw()
	q3Scale.draw()
	q4Scale.draw()
	q5Scale.draw()
	probeSubmitButtonBox.draw()
	probeSubmitButtonText.draw()

	probeSubmitButtonClicked = probeSubmitButton.isClicked() # Track whether the submit button has been clicked

	# Display error message to participant if the participant tries to click the submit button without selecting an answer for all the questions
	if probeSubmitButtonClicked and (q1Answer == 'none' or q2Answer == 'none' or q3Answer == 'none' or q4Answer == 'none' or q5Answer == 'none'):
		probeSubmitError = True
	if probeSubmitError:
		probeSubmitErrorMsg.draw()

def writeData():
	participantDataDict.update({'Date': date, 'Time': time, 'Pre Q1': psQ1Answer, 'Pre Q2': psQ2Answer,'Q1': q1Answer, 'Q2': q2Answer, 'Q3': q3Answer, 'Q4':q4Answer, 'Q5': q5Answer, 'Total Time Played': totalTimePlayed})
	participantDataToCsv()
	createOvershootLogCsv()
	createFrameLogCsv()

#################################### START EXPERIMENT ####################################
#win.setRecordFrameIntervals(True)

# Get date & time
date = strftime("%Y-%m-%d") # Get current date
time = strftime("%H:%M") # Get current time (the time when the data in the dialog box is submitted)

# Display instruction screen for the pre-study probe
while not psProbeStartButton.isClicked():
	displayPSProbeInstructions()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

# Display pre-study probe screen
while not psProbeSubmitButtonClicked or psQ1Answer == 'none' or psQ2Answer == 'none':
	displayPSProbe()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

# Display instruction screen for the practise trial
while not practiseButton.isClicked():
	displayPractiseScreen()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

# Initializations for practise trial
resetApple() # Initialize apple (drop interval timer is also reset here)
gamePlayClock = core.Clock() # Effectively starts the game play timer

# Run practise trial
while gamePlayClock.getTime() <= practisePlayLength or gamePaused: 
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	playPractise()
	mouse.clickReset()
	win.flip()

# Display instruction screen for the actual game
while not startButton.isClicked():
	displayGameInstructions()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

# If Condition 1 or 3, reset difficulty level of game back to 4 (in Condition 2, participant chooses the difficulty level via a scale in the game instructions screen)
if condition == 1 or condition == 3:
	changeDifficulty(4)
elif condition == 4:
	changeDifficulty(getYokedLevel()) # If Condition 4, yoke the difficulty level 

# If Condition 3, get the time that the next level change should occur
if condition == 3:
	changeLogCsvToDict()
	if i+1 < len(levelDataLog):
		nextLevelChangeTime = levelDataLog[i+1]['Level Change Time']
	else:
		nextLevelChangeTime = gamePlayLength + 100 # If there are no more level changes, make the next level change time unreachable

# Reset game variables (since the trial round has finished and the real game will be starting)
score = 0
hits = 0
misses = 0
nearMisses = 0
appleNum = 0
levelChangeTime = 0
prevLevelChangeTime = 0
scoreDisplay.setText('Score: ' + str(score))
difficultyScale.setLevel(difficultyLevel) # Visually set active level of difficulty scale to proper difficulty level
overshootDataLog = []
resetApple() # Initialize apple (drop interval timer is also reset here)
gamePlayClock = core.Clock() # Effectively starts the game play timer

# Run the appropriate game for the condition
if condition == 1:
	levelDataLog.append({'Level Change Time': 0, 'Level': difficultyLevel, 'Apple Drop Time': appleDropTime, 'Drop Interval Length': dropIntervalLength})
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused:
		if event.getKeys(keyList = ['q','escape']):
			totalTimePlayed = gamePlayClock.getTime()
			logAppleCatchData()
			writeData()
			createChangeLogCsv()
			core.quit()
		playCond1()
		logFrameData()
		frameNum += 1
		mouse.clickReset()
		win.flip()
	createChangeLogCsv()
elif condition == 2:
	levelDataLog.append({'Level Change Time': 0, 'Level': difficultyLevel, 'Apple Drop Time': appleDropTime, 'Drop Interval Length': dropIntervalLength})
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
		if event.getKeys(keyList = ['q','escape']):
			totalTimePlayed = gamePlayClock.getTime()
			logAppleCatchData()
			writeData()
			createCond2LevelCsv() 
			core.quit()
		playCond2()
		logFrameData()
		frameNum += 1
		mouse.clickReset()
		win.flip()
	createCond2LevelCsv() # Write participant's level choice into a csv
elif condition == 3:
	levelDataLog[i].update({'Apple Drop Time': appleDropTime, 'Drop Interval Length': dropIntervalLength})
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
		if event.getKeys(keyList = ['q','escape']):
			totalTimePlayed = gamePlayClock.getTime()
			logAppleCatchData()
			writeData()
			core.quit()
		playCond3()
		logFrameData()
		frameNum += 1
		mouse.clickReset()
		win.flip()
elif condition == 4:
	levelDataLog.append({'Level Change Time': 0, 'Level': difficultyLevel, 'Apple Drop Time': appleDropTime, 'Drop Interval Length': dropIntervalLength})
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
		if event.getKeys(keyList = ['q','escape']):
			totalTimePlayed = gamePlayClock.getTime()
			logAppleCatchData()
			writeData()
			core.quit()
		playCond4()
		logFrameData()
		frameNum += 1
		mouse.clickReset()
		win.flip()

totalTimePlayed = gamePlayClock.getTime()
logAppleCatchData()

# Display instruction screen for the probe
while not probeStartButton.isClicked():
	displayProbeInstructions()
	if event.getKeys(keyList = ['q','escape']):
		writeData()
		core.quit()
	mouse.clickReset()
	win.flip()

# Display screen containing the probes
while not probeSubmitButtonClicked or q1Answer == 'none' or q2Answer == 'none' or q3Answer == 'none' or q4Answer == 'none' or q5Answer == 'none':
	displayProbe()
	if event.getKeys(keyList = ['q','escape']):
		writeData()
		core.quit()
	mouse.clickReset()
	win.flip()

participantDataDict.update({'Date': date, 'Time': time, 'Pre Q1': psQ1Answer, 'Pre Q2': psQ2Answer,'Q1': q1Answer, 'Q2': q2Answer, 'Q3': q3Answer, 'Q4':q4Answer, 'Q5': q5Answer, 'Total Time Played': totalTimePlayed})

# Write all participant data collected over the duration of the experiment to csv files
participantDataToCsv()

# Write the overshoot log to a csv file
createOvershootLogCsv()

# Write the frame log to a csv file
createFrameLogCsv()

# Display end screen
displayEndScreen()

win.close()
# pylab.plot(win.frameIntervals)
# pylab.show()
