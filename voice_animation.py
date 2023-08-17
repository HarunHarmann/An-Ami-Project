# Quickly import essential libraries
import queue
import sys
from matplotlib.animation import FuncAnimation
import PyQt6.QtCore
import matplotlib as mlp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
mlp.use("TkAgg") 
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd


class voice_animation:
	def run(self):
		plt.rcParams['toolbar'] = 'None'
		plt.rcParams.update({
			"figure.facecolor":  "black",  # red   with alpha = 30%
			
		}) 

		# Lets define audio variables
		# We will use the default PC or Laptop mic to input the sound

		device = 0 # id of the audio device by default
		window = 1000 # window for the data
		downsample = 1 # how much samples to drop
		channels = [1] # a list of audio channels
		interval = 40 # this is update interval in miliseconds for plot

		# lets make a queue
		q = queue.Queue()
		# Please note that this sd.query_devices has an s in the end.
		device_info =  sd.query_devices(device, 'input')
		samplerate = device_info['default_samplerate']
		length  = int(window*samplerate/(1000*downsample))

		plotdata =  np.zeros((length,len(channels)))

		# next is to make fig and axis of matplotlib plt
		fig,ax = plt.subplots(figsize=(2,1))
		fig.subplots_adjust(0,0,1,1)
		ax.axis("off")
		fig.canvas.manager.window.overrideredirect(1)

		# lets set the title
		ax.set_title("On Action")

		# Make a matplotlib.lines.Line2D plot item of color green
		# R,G,B = 0,1,0.29

		lines = ax.plot(plotdata,color = "purple")

		# We will use an audio call back function to put the data in queue

		def audio_callback(indata,frames,time,status):
			q.put(indata[::downsample,[0]])

		# now we will use an another function 
		# It will take frame of audio samples from the queue and update
		# to the lines

		def update_plot(frame):
			global plotdata
			while True:
				try: 
					data = q.get_nowait()
				except queue.Empty:
					break
				shift = len(data)
				plotdata = np.roll(plotdata, -shift,axis = 0)
				# Elements that roll beyond the last position are 
				# re-introduced 
				plotdata[-shift:,:] = data
			for column, line in enumerate(lines):
				line.set_ydata(plotdata[:,column])
			return lines
		# Lets add the grid
		ax.set_yticks([0])
		# ax.yaxis.grid(True)

		""" INPUT FROM MIC """

		stream  = sd.InputStream(device = device, channels = max(channels), samplerate = samplerate, callback  = audio_callback)


		""" OUTPUT """		


		ani  = FuncAnimation(fig,update_plot, interval=interval,blit=True, )
		plt.get_current_fig_manager().window.wm_geometry("200x100+850+450") 

		# win = plt.gcf().canvas.manager.window
		# win.setStyleSheet("background:transparent")

		with stream: 
			plt.show()

# import queue
# import sys
# from matplotlib.animation import FuncAnimation
# import matplotlib.pyplot as plt
# import numpy as np
# import sounddevice as sd
# from pyqtgraph import PlotWidget, plot
# import pyqtgraph as pg
# import sys  # We need sys so that we can pass argv to QApplication
# import os

# class voice_animation:
# 	def run(self):
# 		device = 0 # id of the audio device by default
# 		window = 1000 # window for the data
# 		downsample = 1 # how much samples to drop
# 		channels = [1] # a list of audio channels
# 		interval = 30 # this is update interval in miliseconds for plot

# 		q = queue.Queue()
# 		# Please note that this sd.query_devices has an s in the end.
# 		device_info =  sd.query_devices(device, 'input')
# 		samplerate = device_info['default_samplerate']
# 		length  = int(window*samplerate/(1000*downsample))

# 		plt.rcParams['interactive'] = False
# 		plt.rcParams['toolbar'] = 'None'
# 		plotdata =  np.zeros((length,len(channels)))
# 		# Lets look at the shape of this plotdata 
# 		# So its vector of length 44100
# 		# Or we can also say that its a matrix of rows 44100 and cols 1

# 		# next is to make fig and axis of matplotlib plt
# 		fig,ax = plt.subplots(figsize=(2,1))
# 		ax.axis("off")

# 		# Make a matplotlib.lines.Line2D plot item of color green
# 		# R,G,B = 0,1,0.29

# 		lines = ax.plot(plotdata,color = (0,1,0.29))

# 		# We will use an audio call back function to put the data in queue

# 		def audio_callback(indata,frames,time,status):
# 			q.put(indata[::downsample,[0]])

# 		def update_plot(frame):
# 			nonlocal plotdata
# 			while True:
# 				try: 
# 					data = q.get_nowait()
# 				except queue.Empty:
# 					break
# 				shift = len(data)
# 				plotdata = np.roll(plotdata, -shift,axis = 0)
# 				# Elements that roll beyond the last position are 
# 				# re-introduced 
# 				plotdata[-shift:,:] = data
# 			for column, line in enumerate(lines):
# 				line.set_ydata(plotdata[:,column])
# 			return lines
# 		ax.set_facecolor((0,0,0))
# 		# Lets add the grid
# 		ax.set_yticks([0])
# 		ax.yaxis.grid(True)

# 		""" INPUT FROM MIC """

# 		stream  = sd.InputStream( device = device, channels = max(channels), samplerate = samplerate, callback  = audio_callback)

# 		""" OUTPUT """		

# 		ani  = FuncAnimation(fig,update_plot, interval=interval,blit=True)
# 		with stream:
# 			plt.show()
	

