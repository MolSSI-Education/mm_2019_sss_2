import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_initial_state(method='random', file_name=None, num_particles=None, box_length=None):
    """
    Function generates initial coordinates for a LJ fluid simulation

    This function can generate coordintes either from a file (NIST LJ Fluid Configurations) or from
    a random configuration

    Parameters
    ----------

    method : str
        String the method to use to build the initial configuration for the LJ fluid simulation. Possible values are 'random'  or 'file' (Default value is 'random')
    file_name : str
        String of the the filename containing the initial starting coordinates. Only required when using the 'fille' method (Default value = None)
    num_particles : int
        Number of particules to use when populating the simualtion box with the 'random' method (Default value = None)
    box_length : float
        Size of one vertices of the simulation box. (Default value = None)

    Returns
    -------

    coordinates : np.array
        A (num_particles x 3) numpy array containing the coordinates of each LJ particle.

    Examples
    --------

    >>> generate_initial_state('random', num_particles = 1000, box_length = 20)
    array([[ 1.10202674,  4.24975121, -5.03322129],
        [ 9.13676284,  4.78807621, -8.26008762],
        [ 6.24720765, -7.17769567,  9.61620896],
        ...,
        [-3.47864571,  2.32867699, -1.31176807],
        [ 1.3302019 , -3.4160087 , -1.34698966],
        [ 0.56410479, -1.2309513 ,  4.71009776]])
    """


    if method is 'random':

        coordinates = (0.5 - np.random.rand(num_particles, 3)) * box_length

    elif method is 'file':

        coordinates = np.loadtxt(file_name, skiprows=2, usecols=(1,2,3))
    
    return coordinates


def lennard_jones_potential(rij2):
    """
    Function evaluates the unitless LJ potential given a squared distance

    Parameters
    ----------
    rij2 : float
        Distance squared between two particles

    Returns
    -------

    float
        Unitless LJ potential energy
    """
    # This function computes the LJ energy between two particles

    sig_by_r6 = np.power(1 / rij2, 3)
    sig_by_r12 = np.power(sig_by_r6, 2)
    return 4.0 * (sig_by_r12 - sig_by_r6)

def calculate_tail_correction(box_length, cutoff, number_particles):
    # This function computes the standard tail energy correction for the LJ potential

    volume = np.power(box_length, 3)
    sig_by_cutoff3 = np.power(1.0 / cutoff, 3)
    sig_by_cutoff9 = np.power(sig_by_cutoff3, 3)
    e_correction = sig_by_cutoff9 - 3.0 * sig_by_cutoff3

    e_correction *= 8.0 / 9.0 * np.pi * number_particles / volume * number_particles
 
    return e_correction

def minimum_image_distance(r_i, r_j, box_length):
    # This function computes the minimum image distance between two particles

    rij = r_i - r_j
    rij = rij - box_length * np.round(rij / box_length)
    rij2 = np.dot(rij, rij)
    return rij2

def get_particle_energy(coordinates, box_length, i_particle, cutoff2):
    #This function computes the energy of a particle with
    #the rest of the system

    e_total = 0.0

    i_position = coordinates[i_particle]

    particle_count = len(coordinates)

    for j_particle in range(particle_count):

        if i_particle != j_particle:
            
            j_position = coordinates[j_particle]

            rij2 = minimum_image_distance(i_position, j_position, box_length)

            if rij2 < cutoff2:
                e_pair = lennard_jones_potential(rij2)
                e_total += e_pair

    return e_total

def calculate_total_pair_energy(coordinates, box_length, cutoff2):
    e_total = 0.0
    particle_count = len(coordinates)

    for i_particle in range(particle_count):
        for j_particle in range(i_particle):

            r_i = coordinates[i_particle]
            r_j = coordinates[j_particle]
            rij2 = minimum_image_distance(r_i, r_j, box_length)
            if rij2 < cutoff2:
                e_pair = lennard_jones_potential(rij2)
                e_total += e_pair

    return e_total

def accept_or_reject(delta_e, beta):
    # This function accepts or reject a move given the
    # energy difference and system temperature

    if delta_e < 0.0:
        accept = True

    else:
        random_number = np.random.rand(1)
        p_acc = np.exp(-beta * delta_e)

        if random_number < p_acc:
            accept = True
        else:
            accept = False

    return accept

def adjust_displacement(n_trials, n_accept, max_displacement):
    acc_rate = float(n_accept) / float(n_trials)
    if (acc_rate < 0.38):
        max_displacement *= 0.8

    elif (acc_rate > 0.42):
        max_displacement *= 1.2

    n_trials = 0
    n_accept = 0

    return max_displacement, n_trials, n_accept

def plot_frame(coordinates, box_length):
    ax = plt.axes(projection='3d')
    ax.set_xlim([-box_length/2, box_length/2])
    ax.set_ylim([-box_length/2, box_length/2])
    ax.set_zlim([-box_length/2, box_length/2])
    ax.plot3D(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2], 'o')
    plt.pause(0.05)



def main():
    #----------------
    # Parameter setup
    #----------------

    reduced_temperature = 0.9
    reduced_density = 0.9
    n_steps = 1000000
    freq = 1000
    num_particles = 100
    simulation_cutoff = 3.0
    max_displacement = 0.1
    tune_displacement = True
    plot = True
    build_method = 'random'

    box_length = np.cbrt(num_particles / reduced_density)
    beta = 1.0 / reduced_temperature
    simulation_cutoff2 = np.power(simulation_cutoff, 2)
    n_trials = 0
    n_accept = 0
    energy_array = np.zeros(n_steps)

    #-----------------------
    # Monte Carlo simulation
    #-----------------------

    coordinates = generate_initial_state(method=build_method, num_particles=num_particles, box_length=box_length)

    total_pair_energy = calculate_total_pair_energy(coordinates, box_length, simulation_cutoff2)
    tail_correction = calculate_tail_correction(box_length, simulation_cutoff, num_particles)

    n_trials = 0

    for i_step in range(n_steps):

        n_trials += 1

        i_particle = np.random.randint(num_particles)

        random_displacement = (2.0 * np.random.rand(3) - 1.0) * max_displacement

        current_energy = get_particle_energy(coordinates, box_length, i_particle, simulation_cutoff2)

        proposed_coordinates = coordinates.copy()
        proposed_coordinates[i_particle] += random_displacement
        proposed_coordinates -= box_length * np.round(proposed_coordinates / box_length)

        proposed_energy = get_particle_energy(proposed_coordinates, box_length, i_particle, simulation_cutoff2)

        delta_e = proposed_energy - current_energy

        accept = accept_or_reject(delta_e, beta)

        if accept:

            total_pair_energy += delta_e
            n_accept += 1
            coordinates[i_particle] += random_displacement

        total_energy = (total_pair_energy + tail_correction) / num_particles

        energy_array[i_step] = total_energy

        if np.mod(i_step + 1, freq) == 0:

            print(i_step + 1, energy_array[i_step])

            if tune_displacement:
                max_displacement, n_trials, n_accept = adjust_displacement(n_trials, n_accept, max_displacement)
            
            if plot:
                plot_frame(coordinates, box_length)


    #plt.plot(energy_array[100:], 'o')
    #plt.xlabel('Monte Carlo steps')
    #plt.ylabel('Energy (reduced units)')
    #plt.grid(True)
    #plt.show()

    #plt.figure()
    #ax = plt.axes(projection='3d')
    #ax.plot3D(coordinates[:,0], coordinates[:,1], coordinates[:,2], 'o')
    #plt.show()

if __name__ == "__main__":
    main()
