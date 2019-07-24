import numpy as np
import sys
import os

class System:

	def __init__(self, method='random', num_particles=None, box_length=None, filename=None):
		self.method = method

		if self.method == 'random':
			self.nparticles = num_particles
			self.coordinates = (0.5 - np.random.rand(num_particles, 3)) * box_length
		elif self.method == 'file':
			self.coordinates = np.loadtxt(filename, skiprows=2, usecols(1,2,3))
			self.nparticles = len(self.coordinates)
		else:
			raise TypeError('You are using a method that is not supported at this moment.')

		
		
