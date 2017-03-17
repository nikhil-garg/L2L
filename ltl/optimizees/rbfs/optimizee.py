import numpy as np

from ltl.optimizees.rbfs.rbf import RBF
from ltl.optimizees.optimizee import Optimizee


class RBFOptimizee(Optimizee):
    """
    Implements a simple function optimizee. Functions are generated using the RBF generator.
    NOTE: Make sure the optimizee_fitness_weights is set to (-1,) to minimize the value of the function

    :param rbf_params: dictionary describing the functions to be generated (see syntax in RBF generator)
    :param dims: defines the dimensionality of the function inputs
    """

    def __init__(self, traj, rbf_params, dims):
        super().__init__(traj)
        self.dims = dims
        rbf_instance = RBF(rbf_params, dims)
        self.cost_fn = rbf_instance.cost_function
        self.bound = rbf_instance.bound

        # create_individual can be called because __init__ is complete except for traj initializtion
        indiv_dict = self.create_individual()
        for key, val in indiv_dict.items():
            traj.individual.f_add_parameter(key, val)

    def create_individual(self):
        """
        Creates a random value of parameter within given bounds
        """
        # Define the first solution candidate randomly
        return {'coords':(np.random.rand(self.dims) * (self.bound[1] - self.bound[0]) + self.bound[0])}

    def bounding_func(self, individual):
        """
        Bounds the individual within the required bounds via coordinate clipping
        """
        return {'coords':np.clip(individual['coords'], a_min=self.bound[0], a_max=self.bound[1])}

    def simulate(self, traj):
        """
        Returns the value of the function chosen during initialization

        :param ~pypet.trajectory.Trajectory traj: Trajectory
        :return: a single element :obj:`tuple` containing the value of the chosen function
        """
        individual = np.array(traj.individual.coords)
        return (self.cost_fn(individual),)