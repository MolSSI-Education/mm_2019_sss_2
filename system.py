import numpy as np
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
		self.box_length = box_length
		self.method = method

		if self.method == 'random':
			self.n_particles = num_particles
			self.coordinates = (0.5 - np.random.rand(num_particles, 3)) * box_length
		elif self.method == 'file':
			if os.path.exists(filename):
				self.coordinates, self.n_particles = self._read_info_from_file_(filename)
			elif:
				print("Please enter the absolute path for your file.")
				print("If you want to use something random, enter 'N'.")
				filename = input("Enter path: ")
				if filename == 'N' or 'n':
					print("Will not use a file. Continuing.")
				else:
					if os.path.exists(filename):
						self.coordinates, self.n_particles = self._read_info_from_file_(filename)
					else:
						print("Continuing without a file.")
						filename = None
		else:
			raise TypeError('You are using a method that is not supported at  this moment.')

	def _read_info_from_file_(filename):
		coordinates = np.loadtxt(filename, skiprows=2, usecols=(1, 2, 3))
		num_particles = len(coordinates)

		return coordinates, num_particles
