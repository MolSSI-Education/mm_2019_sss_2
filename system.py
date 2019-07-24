import numpy as np
import sys
import os

class System:
	"""This is a class object that initializes a system for your Monte Carlo calculation.

	Parameters
	----------
	method : str
		The method is either 'random' or 'file'. By default the method is set to 'random'.
	num_particles : int
		The number of particles should be defined as an integer value. By default the value is 20.
	box_length : float
		The box is assumed to be cubic. By default the value is set to 3.0 Angstroms.
	filename : str
		The file name if the method is set to file.
	"""

	def __init__(self, method='random', num_particles=20, box_length=3.0, filename=None):
		self.method = method

		if self.method == 'random':
			self.nparticles = num_particles
			self.coordinates = (0.5 - np.random.rand(num_particles, 3)) * box_length
		elif self.method == 'file':
			self.coordinates = np.loadtxt(filename, skiprows=2, usecols(1,2,3))
			self.nparticles = len(self.coordinates)
		else:
			raise TypeError('You are using a method that is not supported at this moment.')

		
		
