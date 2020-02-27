#!/usr/bin/python

from numpy import loadtxt, asarray
from numpy.random import normal as gaussian_noise
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings

"""
Here you register new characters in format:
'<char>' : (<width>, <height>, '<filename>'),
"""
charlist = {
	'a' : (0.7, 1.0, 'a'),
	'b' : (0.7, 1.0, 'b'),
	'c' : (0.7, 1.0, 'c'),
	'd' : (0.7, 1.0, 'd'),
	'e' : (0.7, 1.0, 'e'),
	'f' : (0.7, 1.0, 'f'),
	'g' : (0.7, 1.0, 'g'),
	'h' : (0.7, 1.0, 'h'),
	'i' : (0.4, 1.0, 'i'),
	'j' : (0.4, 1.0, 'j'),
	'k' : (0.7, 1.0, 'k'),
	'l' : (0.7, 1.0, 'l'),
	'm' : (0.7, 1.0, 'm'),
	'n' : (0.7, 1.0, 'n'),
	'o' : (0.7, 1.0, 'o'),
	'p' : (0.7, 1.0, 'p'),
	'q' : (0.7, 1.0, 'q'),
	'r' : (0.7, 1.0, 'r'),
	's' : (0.7, 1.0, 's'),
	't' : (0.7, 1.0, 't'),
	'u' : (0.7, 1.0, 'u'),
	'v' : (0.7, 1.0, 'v'),
	'w' : (0.7, 1.0, 'w'),
	'x' : (0.7, 1.0, 'x'),
	'y' : (0.7, 1.0, 'y'),
	'z' : (0.7, 1.0, 'z'),

	'0' : (0.7, 1.0, '0'),
	'1' : (0.5, 1.0, '1'),
	'2' : (0.7, 1.0, '2'),
	'3' : (0.7, 1.0, '3'),
	'4' : (0.7, 1.0, '4'),
	'5' : (0.7, 1.0, '5'),
	'6' : (0.7, 1.0, '6'),
	'7' : (0.7, 1.0, '7'),
	'8' : (0.7, 1.0, '8'),
	'9' : (0.7, 1.0, '9'),

	' ' : (0.7, 0.0, 'space'),
	'?' : (0.7, 1.0, 'questionmark'),
	'!' : (0.2, 1.0, 'exclamationmark'),
	',' : (0.1, 0.1, 'comma'),
	'.' : (0.2, 0.1, 'fullstop'),
	'&' : (0.6, 1.0, 'ampersand'),
	'$' : (0.5, 1.0, 'dollar'),
	'@' : (0.7, 1.0, 'at'),
	'(' : (0.3, 1.0, 'brackets_open'),
	')' : (0.3, 1.0, 'brackets_close'),
	'#' : (0.7, 1.0, 'hash'),
	'%' : (0.7, 1.0, 'percent'),
}


class Character(object):
	"""
	ARGUMENTS
	char	- single character (first one is chosen)
	size	- size of the letter (width, height)

	self.xs, self.ys - arrays with letter points
	"""
	def __init__(self, char, filename='', size=(1.0, 1.0), jitter=0.0):
		if len(char) < 1:
			raise Exception('Empty string is passed to Character() constructor.')

		self.char = char[0]
		if len(filename) > 0:
			self.filename = filename
		else:
			'chars/' + self.char + '.dat'

		self._getPoints()
		self.resize(size=size)

	def _getPoints(self):
		xs, ys = loadtxt('chars/' + self.filename + '.dat', unpack=True)
		self.xs = asarray(xs)
		self.ys = asarray(ys)

		self._sort()

	def _sort(self):
		points = zip(self.xs, self.ys)
		sorted_points = sorted(points)

		self.xs = asarray([point[0] for point in sorted_points])
		self.ys = asarray([point[1] for point in sorted_points])

	def resize(self, size=(1.0, 1.0)):
		self.size = size

		if len(self.xs) < 1:
			self._getPoints()

		xmin = min(self.xs)
		xmax = max(self.xs)
		ymin = min(self.ys)
		ymax = max(self.ys)

		for i in range(0, len(self.xs)):
			self.xs[i] = self.size[0] * (self.xs[i] - xmin) / (xmax - xmin)
			self.ys[i] = self.size[1] * (self.ys[i] - ymin) / (ymax - ymin)



class TextyPloty(object):
	"""
	ARGUMENTS
	jitter	- to randomize points locations, represents sigma for gaussian noise
	spacing	- distance between letters
	offset	- offset from zero point if format (x, y)
	scale	- scale/size of the letters
	func	- function to add text to 
	"""
	def __init__(self, jitter=0.0, spacing=0.1, offset=(0.0, 0.0), scale=(1.0, 1.0), func=None):
		self.jitter = jitter
		self.spacing = spacing
		self.offset = offset
		self.scale = scale
		self.func = func

		self.charlist = charlist

	"""
	ARGUMENTS
	text	- string to plot

	RETURNS
	xs, ys	- points coordinates
	"""
	def get(self, text):
		xs, ys = [], []

		xoffset = self.offset[0]
		for char in text:
			if char == ' ':
				xoffset += self.charlist[char][0] * self.scale[0]
			elif char == '\t':
				xoffset += self.charlist[char][0] * self.scale[0] * 4
			elif char in self.charlist:
				charobj = Character(char=char, filename=self.charlist[char][2], size=self.charlist[char])
				xs.extend(self.scale[0] * charobj.xs + xoffset)
				ys.extend(self.scale[1] * charobj.ys + self.offset[1])
				xoffset += self.charlist[char][0] * self.scale[0]
			else:
				warnings.warn('Could not find file with "' + char + '" character. Skipping...', Warning)

			xoffset += self.spacing * self.scale[0]

		if self.func != None:
			for i in range(0,len(xs)):
				ys[i] += self.func(xs[i])

		if self.jitter > 0:			
			noise = gaussian_noise(0.0, self.jitter*self.scale[1], (len(ys)))
			ys = [x+y for x, y in zip(ys, noise)]

		return asarray(xs), asarray(ys)


class ResidualsPlot(object):
	"""

	"""
	def __init__(self, data=([],[]), datastyle='k.', xs_fit=[], func=None, fitstyle='r-', \
		xlabel='', ylabel='', reslabel='', ratio=[4, 1], figsize=(10,6), axis=None, res_axis=None, \
		fitlabel='fit', datalabel='points'):
		self.plt_instance = plt
		self.xs = data[0]
		self.ys = data[1]
		self.datastyle = datastyle
		self.xs_fit = xs_fit
		self.func = func
		self.ys_fit = self.func(self.xs_fit)
		self.fitstyle = fitstyle
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.reslabel = reslabel
		self.ratio = ratio
		self.figsize = figsize
		self.axis = axis
		self.res_axis = res_axis

		self.fitlabel = fitlabel
		self.datalabel = datalabel

	def draw(self):
		self.redraw()

	def redraw(self):
		self.plt_instance = plt

		self.plt_instance.figure(figsize=self.figsize)
		self.gridspec_instance = gridspec.GridSpec(2, 1, height_ratios=self.ratio)
		self.gridspec_instance.update(hspace=0.00)
		self.ax0 = self.plt_instance.subplot(self.gridspec_instance[0])
		self.ax1 = self.plt_instance.subplot(self.gridspec_instance[1])
		self.ys_res = self.ys - self.func(self.xs)

		# set axis ranges
		if self.axis == None:
			self.ax0.axis([min(self.xs_fit) * 1.1, max(self.xs_fit)*1.1, min(self.ys_fit) * 1.1, max(self.ys_fit) * 1.1])
		elif len(self.axis) != 4:
			raise Exception('ResidualsPlot: axis should contain 4 numbers: (x1, x2, y1, y2)')
		else:
			self.ax0.axis(self.axis)

		if self.res_axis == None:
			self.ax1.axis([min(self.xs_fit) * 1.1, max(self.xs_fit)*1.1, min(self.ys_res) * 1.1, max(self.ys_res)*1.1])
		elif len(self.res_axis) != 4:
			raise Exception('ResidualsPlot: res_axis should contain 4 numbers: (x1, x2, y1, y2)')
		else:
			self.ax1.axis(self.res_axis)

		# set axis labels
		self.ax0.set_ylabel(self.ylabel)
		self.ax1.set_ylabel(self.reslabel)
		self.ax1.set_xlabel(self.xlabel)

		# first subplot: datapoints and fit
		self.ax0.plot(self.xs_fit, self.ys_fit, self.fitstyle, label=self.fitlabel)
		self.ax0.plot(self.xs, self.ys, self.datastyle, label=self.datalabel)

		# second subplot: residuals
		self.ax1.plot([min(self.xs), max(self.xs)], [0,0], self.fitstyle)
		self.ax1.plot(self.xs, self.ys_res, self.datastyle)

		self.ax0.legend(loc="upper right")


	def show(self):
		self.plt_instance.show()

	def savefig(self, name='plot.pdf'):
		self.plt_instance.savefig(name)
