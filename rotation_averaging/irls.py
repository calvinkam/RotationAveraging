#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Bryce Evans
# @Date:   2014-11-07
# @Last Modified by:   Rafael Marinheiro
# @Last Modified time: 2014-11-08

import logging
import numpy
import scipy
import scipy.sparse
import scipy.sparse.linalg
import scipy.linalg
import math

def ilrs_phi(e, sigma=5*math.pi/180):
	diagonal = []
	for el in e:
		diagonal.append(sigma*sigma/(el[0]*el[0] + sigma*sigma))

	return scipy.sparse.diags([diagonal], [0])

def ilrs_solve(A, b, x0, tol=1e-3):
	""" Iteratively Reweighted Least Squares

	Computes the solution :math:`x^*` of the :math:`\\ell_1` approximation problem:

		:math:`x^* = \\underset{x}{\\arg\\min} \\quad \\left\\lVert Ax - b\\right\\rVert _1`

	This implementation is entirely based on *l1decode_pd.m*, part of l1 magic software (<http://users.ece.gatech.edu/~justin/l1magic/>)

	:param A: A full rank matrix. Optionally sparse.
	:type A: :math:`M\\times N` matrix

	:param b:
	:type b: :math:`M\\times 1` column-vector

	:param x0: An initial guess of the solution
	:type x0: :math:`N\\times 1` column-vector

	:param tol: Tolerance for primal-dual algorithm (algorithm terminates if the duality gap is less than pdtol)
	:param max_iterations: Maximum number of primal-dual iterations

	:returns: xstar -- the solution to the approximation problem
	"""
	x_prev = x0*0.0
	x = x0
	while scipy.linalg.norm(x-x_prev) > tol:
		x_prev = x
		e = A.dot(x) - b
		phi_m = ilrs_phi(e)
		T1 = scipy.sparse.linalg.inv(scipy.transpose(A).dot(phi_m.dot(A)))
		T2 = phi_m.dot(b)
		T3 = scipy.transpose(A).dot(T2)
		x = T1.dot(T3)
	
	return x