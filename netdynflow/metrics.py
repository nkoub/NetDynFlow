# -*- coding: utf-8 -*-
# Copyright (c) 2019, Gorka Zamora-López, Matthieu Gilson and Nikos E. Kouvaris
# <galib@Zamora-Lopez.xyz>
#
# Released under the Apache License, Version 2.0 (the "License");
# you may not use this software except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""
Analysis of dynamic communicability and flow
============================================

Functions to analyse the dynamic communicability or flow "tensors", which have
been previously calculated from a given network.

Metrics derived from the tensors
--------------------------------
TotalEvolution
    Calculates total communicability or flow over time for a network.
NodeEvolution
    Temporal evolution of all nodes' input and output communicability or flow.
Diversity
    Temporal diversity for a networks dynamic communicability or flow.
TTPdistance
    Pair-wise node distance, measured as the time-to-peak of their interaction.
    TO BE WRITTEN AND ADDED !! INCLUDE THE TEMPORAL RESOLUTION !!

Reference and Citation
----------------------
1. M. Gilson, N. Kouvaris, G. Deco & G.Zamora-Lopez "Framework based on communi-
cability and flow to analyze complex networks" Phys. Rev. E 97, 052301 (2018).
2. M. Gilson, N. Kouvaris, et al. "Analysis of brain network dynamics estimated
from fMRI data: A new framework based on communicability and flow"
bioRxiv (2018). DOI: https://doi.org/10.1101/421883.


...moduleauthor:: Gorka Zamora-Lopez <galib@zamora-lopez.xyz>

"""
from __future__ import division, print_function

import numpy as np
import numpy.linalg
import scipy.linalg


## METRICS EXTRACTED FROM THE FLOW AND COMMUNICABILITY TENSORS ################
def TotalEvolution(dyntensor):
    """Calculates total communicability or flow over time for a network.

    Parameters
    ----------
    dyntensor : ndarray of rank-3
        Temporal evolution of the network's dynamic communicability. A tensor
        of shape timesteps x N x N, where N is the number of nodes.

    Returns
    -------
    totaldyncom : ndarray of rank-1
        Array containing temporal evolution of the total communicability.
    """
    # 0) SECURITY CHECKS
    tensorshape = np.shape(dyntensor)
    assert len(tensorshape) == 3, 'Input not aligned. Tensor of rank-3 expected'
    nsteps, N1, N2 = tensorshape
    assert N1 == N2, 'Input not aligned. Shape (nsteps x N x N) expected'

    totaldyncom = dyntensor.sum(axis=1).sum(axis=1)

    return totaldyncom

def NodeEvolution(dyntensor, directed=False):
    """Temporal evolution of all nodes' input and output communicability or flow.

    Parameters
    ----------
    dyntensor : ndarray of rank-3
        Temporal evolution of the network's dynamic communicability. A tensor
        of shape timesteps x N x N, where N is the number of nodes.

    Returns
    -------
    nodedyncom : tuple.
        Temporal evolution of the communicability or flow for all nodes.
        The result consists of a tuple of two ndarrays of shape (N x timesteps)
        each. The first is for the inputs to the node and the second for its
        outputs.
    """
    # 0) SECURITY CHECKS
    tensorshape = np.shape(dyntensor)
    assert len(tensorshape) == 3, 'Input not aligned. Tensor of rank-3 expected'
    nsteps, N1, N2 = tensorshape
    assert N1 == N2, 'Input not aligned. Shape (nsteps x N x N) expected'

    # 1) Calculate the input and output node properties
    innodedyn = dyntensor.sum(axis=1).T
    outnodedyn = dyntensor.sum(axis=2).T
    nodedyn = ( innodedyn, outnodedyn )

    return nodedyn

def Diversity(dyntensor):
    """Temporal diversity for a networks dynamic communicability or flow.

    Parameters
    ----------
    dyntensor : ndarray of rank-3
        Temporal evolution of the network's dynamic communicability or flow. A
        tensor of shape timesteps x N x N, where N is the number of nodes.

    Returns
    -------
    diversity : ndarray of rank-1
        Array containing temporal evolution of the diversity.
    """
    # 0) SECURITY CHECKS
    tensorshape = np.shape(dyntensor)
    assert len(tensorshape) == 3, 'Input not aligned. Tensor of rank-3 expected'
    nsteps, N1, N2 = tensorshape
    assert N1 == N2, 'Input not aligned. Shape (nsteps x N x N) expected'

    diversity = np.zeros(nsteps, np.float)
    for t in range(nsteps):
        diversity[t] = dyntensor[t].std() / dyntensor[t].mean()

    return diversity



##
