# Copyright (c) 2014, Javier Gonzalez
# Copyright (c) 2014, the GPy Authors (see GPy AUTHORS.txt)
# Licensed under the BSD 3-clause license (see LICENSE.txt)

import GPy
from ..core.entropysearch import EntropyLoss # work in progress
from ..core.es import ES  # work in progress

class EntropySearch(ES): #work in progress
	"""
	Entropy seach method proposed by Henning and Schuler (2012)

	This is a thin wrapper around the methods.BO class, with a set of sensible defaults

	:param bounds: Tuple containing the box contrains of the function to optimize. Example: for [0,1]x[0,1] insert [(0,1),(0,1)]  
	:param kernel: a GPy kernel, defaults to rbf
	:param optimize_model: Unless specified otherwise the parameters of the model are updated after each iteration. 
	:param acquisition_par: parameter of the acquisition function. To avoid local minima 
	:param invertsign: minimization is done unles invertsing is True
	:param Nrandom: number of initial random evaluatios of f is X and Y are not provided  

    .. Note:: Multiple independent outputs are allowed using columns of Y

    """
	def __init__(self, bounds=None, kernel=None, optimize_model=None, acquisition_par=None, invertsign=None, Nrandom = None):
		self.input_dim = len(bounds)
		if bounds==None: 
			raise 'Box contrainst are needed. Please insert box constrains'	
		if kernel is None: 
			self.kernel = GPy.kern.RBF(self.input_dim, variance=.1, lengthscale=.1)
		else: 
			self.kernel = kernel
		acq = AcquisitionUBC(acquisition_par, invertsign)  ## change to Entropy Seach optimization
		super(BayesianOptimizationEI ,self ).__init__(acq, bounds, optimize_model,Nrandom)
        
	def _init_model(self, X, Y):
		'''
		Initializes the prior measure, or Gaussian Process, over the function f to optimize

		:param X: input observations
		:param Y: output values

		..Note : X and Y can be None. In this case Nrandom*model_dimension data are uniformly generated to initialize the model.

		'''
		self.model = GPy.models.GPRegression(X,Y,kernel=self.kernel)   ### this part remains the same