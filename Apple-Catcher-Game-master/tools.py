from psychopy import visual, event

class Button(object):
	""" Turns an ImageStim or a shape into a button.
	isClicked() checks whether a left mouse click has been pressed *and released* on a stim. To use, it should be called every frame. """

	def __init__(self, stim, mouse):
		self.stim = stim
		self.mouse = mouse
		self.pressStarted = 0

	def isClicked(self):
		stimClicked = 0
		stimContainsMouse =  self.stim.contains(self.mouse)
		mouseIsPressed = self.mouse.getPressed()[0]

		if (not self.pressStarted) and mouseIsPressed and stimContainsMouse: # Press on stim has been started
			self.pressStarted = 1
		elif self.pressStarted and (not mouseIsPressed) and stimContainsMouse: # Mouse press is released inside of stim; button has been clicked
			self.pressStarted = 0
			stimClicked = 1
		elif self.pressStarted and (not mouseIsPressed) and (not stimContainsMouse): # Mouse press is released outside of stim; button not clicked
			self.pressStarted = 0

		return stimClicked

class Scale(object):
	"""docstring for Scale.. units in norm"""
	def __init__(self, win, scaleColor, activeColor, startLevel, width, height, pos, opacity = 1):
		self.win = win
		self.scaleColor = scaleColor
		self.activeColor = activeColor
		self.activeLevel = startLevel # default active level is the starting level
		self.width = width
		self.height = height
		self.posX = pos[0]
		self.posY = pos[1]
		self.opacity = opacity

		# Create scale bar
		barWidth = self.width* 0.8
		barLeftEdge = self.posX - barWidth/2.0
		barRightEdge = self.posX + barWidth/2.0
		self.bar = visual.Line(self.win, lineColor = self.scaleColor, start = (barLeftEdge, self.posY), end = (barRightEdge, self.posY), opacity = self.opacity)

		# Create scale arrows
		arrowWidth = self.width * 0.1
		leftArrowPosX = barLeftEdge - arrowWidth/2.0
		rightArrowPosX = barRightEdge + arrowWidth/2.0
		# Note: Polygon is supposed to create regular polygons, but there is a bug in Psychopy... They didn't account for norm units. So the actual shape will turn out unexpected.
		self.leftArrow = visual.Polygon(win, lineColor = self.scaleColor, fillColor = self.scaleColor, edges = 3, radius = arrowWidth/2.0, pos = (leftArrowPosX, self.posY), ori = -90, opacity = self.opacity)
		self.rightArrow = visual.Polygon(win, lineColor = self.scaleColor, fillColor = self.scaleColor, edges = 3, radius = arrowWidth/2.0, pos = (rightArrowPosX, self.posY), ori = 90, opacity = self.opacity)

		# Make the scale arrows function as buttons
		mouse = event.Mouse()
		self.leftArrowButton = Button(self.leftArrow, mouse)
		self.rightArrowButton = Button(self.rightArrow, mouse)

		# Calculate the space between each tick
		tickIntervalWidth = barWidth/6.0 # 7 ticks => 6 intervals

		# Calculate the end points of the tick bars
		tickYStart = self.posY - self.height/2.0
		tickYEnd = self.posY + self.height/2.0
		tick1PosX = barLeftEdge
		tick2PosX = self.posX - (2*tickIntervalWidth)
		tick3PosX = self.posX - (1*tickIntervalWidth)
		tick4PosX = self.posX
		tick5PosX = self.posX + (1*tickIntervalWidth)
		tick6PosX = self.posX + (2*tickIntervalWidth)
		tick7PosX = barRightEdge

		# Create tick bars
		self.tick1 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick1PosX, tickYStart), end = (tick1PosX, tickYEnd), opacity = self.opacity)
		self.tick2 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick2PosX, tickYStart), end = (tick2PosX, tickYEnd), opacity = self.opacity)
		self.tick3 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick3PosX, tickYStart), end = (tick3PosX, tickYEnd), opacity = self.opacity)
		self.tick4 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick4PosX, tickYStart), end = (tick4PosX, tickYEnd), opacity = self.opacity)
		self.tick5 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick5PosX, tickYStart), end = (tick5PosX, tickYEnd), opacity = self.opacity)
		self.tick6 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick6PosX, tickYStart), end = (tick6PosX, tickYEnd), opacity = self.opacity)
		self.tick7 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick7PosX, tickYStart), end = (tick7PosX, tickYEnd), opacity = self.opacity)

		tickLabelPosY = self.posY - self.height # Prevents scale labels from overlapping the scale

		# Create tick labels
		self.tick1Label = visual.TextStim(self.win, text = '1', height = self.height, color = self.scaleColor, pos = (tick1PosX, tickLabelPosY), opacity = self.opacity)
		self.tick2Label = visual.TextStim(self.win, text = '2', height = self.height, color = self.scaleColor, pos = (tick2PosX, tickLabelPosY), opacity = self.opacity)
		self.tick3Label = visual.TextStim(self.win, text = '3', height = self.height, color = self.scaleColor, pos = (tick3PosX, tickLabelPosY), opacity = self.opacity)
		self.tick4Label = visual.TextStim(self.win, text = '4', height = self.height, color = self.scaleColor, pos = (tick4PosX, tickLabelPosY), opacity = self.opacity)
		self.tick5Label = visual.TextStim(self.win, text = '5', height = self.height, color = self.scaleColor, pos = (tick5PosX, tickLabelPosY), opacity = self.opacity)
		self.tick6Label = visual.TextStim(self.win, text = '6', height = self.height, color = self.scaleColor, pos = (tick6PosX, tickLabelPosY), opacity = self.opacity)
		self.tick7Label = visual.TextStim(self.win, text = '7', height = self.height, color = self.scaleColor, pos = (tick7PosX, tickLabelPosY), opacity = self.opacity)

		# Create tick dictionary
		self.tickDict = {1: {'tick': self.tick1, 'label': self.tick1Label}, 2: {'tick': self.tick2, 'label': self.tick2Label}, 3: {'tick': self.tick3, 'label': self.tick3Label}, 4: {'tick': self.tick4, 'label': self.tick4Label}, 5: {'tick': self.tick5, 'label': self.tick5Label}, 6: {'tick': self.tick6, 'label': self.tick6Label}, 7: {'tick': self.tick7, 'label': self.tick7Label}}
		
		# Set active colors
		self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
		self.tickDict[self.activeLevel]['label'].color = self.activeColor

		# Create clickable (invisible) boxes around the ticks & tick labels so you can skip using the arrow buttons and click directly on the ticks or labels on the scale
		tickBoxPosY = self.posY - self.height/2.0
		tickBoxWidth = tickIntervalWidth * 0.9
		tickBoxHeight = self.height * 2.5
		self.tick1box = visual.Rect(self.win, lineColor = self.scaleColor, width = tickBoxWidth/2.0, height = tickBoxHeight, pos = (tick1PosX + tickBoxWidth/4.0, tickBoxPosY), opacity = self.opacity)
		self.tick2box = visual.Rect(self.win, lineColor = self.scaleColor, width = tickBoxWidth, height = tickBoxHeight, pos = (tick2PosX, tickBoxPosY), opacity = self.opacity)
		self.tick3box = visual.Rect(self.win, lineColor = self.scaleColor, width = tickBoxWidth, height = tickBoxHeight, pos = (tick3PosX, tickBoxPosY), opacity = self.opacity)
		self.tick4box = visual.Rect(self.win, lineColor = self.scaleColor, width = tickBoxWidth, height = tickBoxHeight, pos = (tick4PosX, tickBoxPosY), opacity = self.opacity)
		self.tick5box = visual.Rect(self.win, lineColor = self.scaleColor, width = tickBoxWidth, height = tickBoxHeight, pos = (tick5PosX, tickBoxPosY), opacity = self.opacity)
		self.tick6box = visual.Rect(self.win, lineColor = self.scaleColor, width = tickBoxWidth, height = tickBoxHeight, pos = (tick6PosX, tickBoxPosY), opacity = self.opacity)
		self.tick7box = visual.Rect(self.win, lineColor = self.scaleColor, width = tickBoxWidth/2.0, height = tickBoxHeight, pos = (tick7PosX - tickBoxWidth/4.0, tickBoxPosY), opacity = self.opacity)
		self.tick1button = Button(self.tick1box, mouse)
		self.tick2button = Button(self.tick2box, mouse)
		self.tick3button = Button(self.tick3box, mouse)
		self.tick4button = Button(self.tick4box, mouse)
		self.tick5button = Button(self.tick5box, mouse)
		self.tick6button = Button(self.tick6box, mouse)
		self.tick7button = Button(self.tick7box, mouse)

	def hasLevelChanged(self):
		if self.leftArrowButton.isClicked():
			if self.activeLevel > 1:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel -= 1
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		if self.rightArrowButton.isClicked():
			if self.activeLevel < 7:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel += 1
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		if self.tick1button.isClicked():
			if self.activeLevel != 1:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel = 1
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		if self.tick2button.isClicked():
			if self.activeLevel != 2:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel = 2
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		if self.tick3button.isClicked():
			if self.activeLevel != 3:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel = 3
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		if self.tick4button.isClicked():
			if self.activeLevel != 4:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel = 4
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		if self.tick5button.isClicked():
			if self.activeLevel != 5:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel = 5
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		if self.tick6button.isClicked():
			if self.activeLevel != 6:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel = 6
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		if self.tick7button.isClicked():
			if self.activeLevel != 7:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel = 7
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		return False

	def setLevel(self, newLevel):
		self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
		self.tickDict[self.activeLevel]['label'].color = self.scaleColor
		self.activeLevel = newLevel
		self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
		self.tickDict[self.activeLevel]['label'].color = self.activeColor

	def draw(self):
		self.leftArrow.draw()
		self.rightArrow.draw()
		self.bar.draw()
		self.tick1.draw()
		self.tick2.draw()
		self.tick3.draw()
		self.tick4.draw()
		self.tick5.draw()
		self.tick6.draw()
		self.tick7.draw()
		self.tick1Label.draw()
		self.tick2Label.draw()
		self.tick3Label.draw()
		self.tick4Label.draw()
		self.tick5Label.draw()
		self.tick6Label.draw()
		self.tick7Label.draw()

		# Uncomment the block below to see the tick button boundaries
		# self.tick2box.draw()
		# self.tick3box.draw()
		# self.tick4box.draw()
		# self.tick5box.draw()
		# self.tick6box.draw()
		# self.tick7box.draw()

	def setOpacity(self, newOpacity):
		self.leftArrow.opacity = newOpacity
		self.rightArrow.opacity = newOpacity
		self.bar.opacity = newOpacity
		self.tick1.opacity = newOpacity
		self.tick2.opacity = newOpacity
		self.tick3.opacity = newOpacity
		self.tick4.opacity = newOpacity
		self.tick5.opacity = newOpacity
		self.tick6.opacity = newOpacity
		self.tick7.opacity = newOpacity
		self.setTextOpacity(self.tick1Label, newOpacity)
		self.setTextOpacity(self.tick2Label, newOpacity)
		self.setTextOpacity(self.tick3Label, newOpacity)
		self.setTextOpacity(self.tick4Label, newOpacity)
		self.setTextOpacity(self.tick5Label, newOpacity)
		self.setTextOpacity(self.tick6Label, newOpacity)
		self.setTextOpacity(self.tick7Label, newOpacity)

	def setTextOpacity(self, textStim, newOpacity): # Need this to change text opacity b/c of stupid psychopy bug (see github.com/psychopy/psychopy/issues/1045)
		originalText = textStim.text
		textStim.setOpacity(newOpacity)
		textStim.setText('') # Change the text to force psychopy to update the textstim's properties (opacity) instead of relying on a cached version
		textStim.setText(originalText)

class BoxScale(object):
	"""docstring for BoxScale.. units in norm"""
	def __init__(self, win, boxLineColor, boxFillColor, textColor, activeFillColor, activeTextColor, width, height, pos, defaultRating = 'none', opacity = 1):
		self.win = win
		self.boxLineColor = boxLineColor
		self.boxFillColor = boxFillColor
		self.textColor = textColor
		self.activeFillColor = activeFillColor
		self.activeTextColor = activeTextColor
		self.activeRating = defaultRating # default active rating is the starting rating
		self.width = width
		self.height = height
		self.posX = pos[0]
		self.posY = pos[1]
		self.opacity = opacity

		boxWidth = self.width/7.0 # scale has 7 boxes

		# Calculate the x positions of the rating boxes
		box1PosX = self.posX - (3*boxWidth)
		box2PosX = self.posX - (2*boxWidth)
		box3PosX = self.posX - (1*boxWidth)
		box4PosX = self.posX
		box5PosX = self.posX + (1*boxWidth)
		box6PosX = self.posX + (2*boxWidth)
		box7PosX = self.posX + (3*boxWidth)

		# Create box labels
		textHeight = self.height * 0.5
		self.box1Label = visual.TextStim(self.win, text = '1', height = textHeight, color = self.textColor, pos = (box1PosX, self.posY), opacity = self.opacity)
		self.box2Label = visual.TextStim(self.win, text = '2', height = textHeight, color = self.textColor, pos = (box2PosX, self.posY), opacity = self.opacity)
		self.box3Label = visual.TextStim(self.win, text = '3', height = textHeight, color = self.textColor, pos = (box3PosX, self.posY), opacity = self.opacity)
		self.box4Label = visual.TextStim(self.win, text = '4', height = textHeight, color = self.textColor, pos = (box4PosX, self.posY), opacity = self.opacity)
		self.box5Label = visual.TextStim(self.win, text = '5', height = textHeight, color = self.textColor, pos = (box5PosX, self.posY), opacity = self.opacity)
		self.box6Label = visual.TextStim(self.win, text = '6', height = textHeight, color = self.textColor, pos = (box6PosX, self.posY), opacity = self.opacity)
		self.box7Label = visual.TextStim(self.win, text = '7', height = textHeight, color = self.textColor, pos = (box7PosX, self.posY), opacity = self.opacity)

		# Create clickable boxes
		mouse = event.Mouse()
		self.box1 = visual.Rect(self.win, lineColor = self.boxLineColor, fillColor = self.boxFillColor, width = boxWidth, height = self.height, pos = (box1PosX, self.posY), opacity = self.opacity)
		self.box2 = visual.Rect(self.win, lineColor = self.boxLineColor, fillColor = self.boxFillColor, width = boxWidth, height = self.height, pos = (box2PosX, self.posY), opacity = self.opacity)
		self.box3 = visual.Rect(self.win, lineColor = self.boxLineColor, fillColor = self.boxFillColor, width = boxWidth, height = self.height, pos = (box3PosX, self.posY), opacity = self.opacity)
		self.box4 = visual.Rect(self.win, lineColor = self.boxLineColor, fillColor = self.boxFillColor, width = boxWidth, height = self.height, pos = (box4PosX, self.posY), opacity = self.opacity)
		self.box5 = visual.Rect(self.win, lineColor = self.boxLineColor, fillColor = self.boxFillColor, width = boxWidth, height = self.height, pos = (box5PosX, self.posY), opacity = self.opacity)
		self.box6 = visual.Rect(self.win, lineColor = self.boxLineColor, fillColor = self.boxFillColor, width = boxWidth, height = self.height, pos = (box6PosX, self.posY), opacity = self.opacity)
		self.box7 = visual.Rect(self.win, lineColor = self.boxLineColor, fillColor = self.boxFillColor, width = boxWidth, height = self.height, pos = (box7PosX, self.posY), opacity = self.opacity)
		self.box1button = Button(self.box1, mouse)
		self.box2button = Button(self.box2, mouse)
		self.box3button = Button(self.box3, mouse)
		self.box4button = Button(self.box4, mouse)
		self.box5button = Button(self.box5, mouse)
		self.box6button = Button(self.box6, mouse)
		self.box7button = Button(self.box7, mouse)

		# Create rating dictionary
		self.ratingDict = {1: {'box': self.box1, 'label': self.box1Label}, 2: {'box': self.box2, 'label': self.box2Label}, 3: {'box': self.box3, 'label': self.box3Label}, 4: {'box': self.box4, 'label': self.box4Label}, 5: {'box': self.box5, 'label': self.box5Label}, 6: {'box': self.box6, 'label': self.box6Label}, 7: {'box': self.box7, 'label': self.box7Label}}
		
		# Set active colors
		if defaultRating != 'none':
			self.ratingDict[self.activeRating]['box'].fillColor = self.activeFillColor
			self.ratingDict[self.activeRating]['label'].color = self.activeTextColor

	def hasRatingChanged(self):
		if self.box1button.isClicked():
			if self.activeRating != 1:
				if self.activeRating != "none":
					self.ratingDict[self.activeRating]['box'].fillColor = self.boxFillColor
					self.ratingDict[self.activeRating]['label'].color = self.textColor
				self.activeRating = 1
				self.ratingDict[self.activeRating]['box'].fillColor = self.activeFillColor
				self.ratingDict[self.activeRating]['label'].color = self.activeTextColor
				return True
		if self.box2button.isClicked():
			if self.activeRating != 2:
				if self.activeRating != "none":
					self.ratingDict[self.activeRating]['box'].fillColor = self.boxFillColor
					self.ratingDict[self.activeRating]['label'].color = self.textColor
				self.activeRating = 2
				self.ratingDict[self.activeRating]['box'].fillColor = self.activeFillColor
				self.ratingDict[self.activeRating]['label'].color = self.activeTextColor
				return True
		if self.box3button.isClicked():
			if self.activeRating != 3:
				if self.activeRating != "none":
					self.ratingDict[self.activeRating]['box'].fillColor = self.boxFillColor
					self.ratingDict[self.activeRating]['label'].color = self.textColor
				self.activeRating = 3
				self.ratingDict[self.activeRating]['box'].fillColor = self.activeFillColor
				self.ratingDict[self.activeRating]['label'].color = self.activeTextColor
				return True
		if self.box4button.isClicked():
			if self.activeRating != 4:
				if self.activeRating != "none":
					self.ratingDict[self.activeRating]['box'].fillColor = self.boxFillColor
					self.ratingDict[self.activeRating]['label'].color = self.textColor
				self.activeRating = 4
				self.ratingDict[self.activeRating]['box'].fillColor = self.activeFillColor
				self.ratingDict[self.activeRating]['label'].color = self.activeTextColor
				return True
		if self.box5button.isClicked():
			if self.activeRating != 5:
				if self.activeRating != "none":
					self.ratingDict[self.activeRating]['box'].fillColor = self.boxFillColor
					self.ratingDict[self.activeRating]['label'].color = self.textColor
				self.activeRating = 5
				self.ratingDict[self.activeRating]['box'].fillColor = self.activeFillColor
				self.ratingDict[self.activeRating]['label'].color = self.activeTextColor
				return True
		if self.box6button.isClicked():
			if self.activeRating != 6:
				if self.activeRating != "none":
					self.ratingDict[self.activeRating]['box'].fillColor = self.boxFillColor
					self.ratingDict[self.activeRating]['label'].color = self.textColor
				self.activeRating = 6
				self.ratingDict[self.activeRating]['box'].fillColor = self.activeFillColor
				self.ratingDict[self.activeRating]['label'].color = self.activeTextColor
				return True
		if self.box7button.isClicked():
			if self.activeRating != 7:
				if self.activeRating != "none":
					self.ratingDict[self.activeRating]['box'].fillColor = self.boxFillColor
					self.ratingDict[self.activeRating]['label'].color = self.textColor
				self.activeRating = 7
				self.ratingDict[self.activeRating]['box'].fillColor = self.activeFillColor
				self.ratingDict[self.activeRating]['label'].color = self.activeTextColor
				return True
		return False

	def setRating(self, newRating):
		self.ratingDict[self.activeRating]['box'].fillColor = self.boxFillColor
		self.ratingDict[self.activeRating]['label'].color = self.textColor
		self.activeRating = newRating
		self.ratingDict[self.activeRating]['box'].fillColor = self.activeFillColor
		self.ratingDict[self.activeRating]['label'].color = self.activeTextColor

	def draw(self):
		self.box1.draw()
		self.box2.draw()
		self.box3.draw()
		self.box4.draw()
		self.box5.draw()
		self.box6.draw()
		self.box7.draw()
		self.box1Label.draw()
		self.box2Label.draw()
		self.box3Label.draw()
		self.box4Label.draw()
		self.box5Label.draw()
		self.box6Label.draw()
		self.box7Label.draw()

	def setOpacity(self, newOpacity):
		self.box1.opacity = newOpacity
		self.box2.opacity = newOpacity
		self.box3.opacity = newOpacity
		self.box4.opacity = newOpacity
		self.box5.opacity = newOpacity
		self.box6.opacity = newOpacity
		self.box7.opacity = newOpacity
		self.setTextOpacity(self.box1Label, newOpacity)
		self.setTextOpacity(self.box2Label, newOpacity)
		self.setTextOpacity(self.box3Label, newOpacity)
		self.setTextOpacity(self.box4Label, newOpacity)
		self.setTextOpacity(self.box5Label, newOpacity)
		self.setTextOpacity(self.box6Label, newOpacity)
		self.setTextOpacity(self.box7Label, newOpacity)

	def setTextOpacity(self, textStim, newOpacity): # Need this to change text opacity b/c of stupid psychopy bug (see github.com/psychopy/psychopy/issues/1045)
		originalText = textStim.text
		textStim.setOpacity(newOpacity)
		textStim.setText('') # Change the text to force psychopy to update the textstim's properties (opacity) instead of relying on a cached version
		textStim.setText(originalText)
