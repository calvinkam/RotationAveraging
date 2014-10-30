#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Rafael Marinheiro
# @Date:   2014-10-28 18:01:58
# @Last Modified by:   Rafael Marinheiro
# @Last Modified time: 2014-10-29 00:34:20

import common
from .. import l1

import numpy.linalg
import logging

def L1RA(num_nodes, rotations, indices, initial_guess, tol=0.001, max_iterations=100, num_l1_steps=2, change_threshold=0.001):
	eps = numpy.spacing(1)
	A = common.create_matrix_from_indices(num_nodes, indices)

	global_rotations = initial_guess

	done = False

	default_estimate = numpy.zeros((num_nodes, 3))

	wdelta = common.compute_relative_log_matrix(global_rotations, rotations, indices)

	if numpy.linalg.norm(wdelta) < tol:
		done = True

	it = 0
	while not done:
		wglobal = l1.l1_msolve(A, wdelta, default_estimate, tol=eps, num_l1_steps)
		global_rotations = common.update_global_rotation_from_log(global_rotations, wglobal)

		wdelta = common.compute_relative_log_matrix(global_rotations, rotations, indices)

		norm_rel = numpy.linalg.norm(wdelta)
		norm_glob = numpy.linalg.norm(wglobal)

		it = it+1

		if norm_rel < tol:
			logging.info("Algorithm converged to the error bound.")
			done = True
		elif it >= max_iterations:
			logging.info("Maximum iterations reached")
			done = True
		else:
			if norm_glob < change_threshold:
				logging.info("Increasing the number of L1 steps")
				num_l1_steps = 4*num_l1_steps
				change_threshold = change_threshold/100

	return global_rotations
