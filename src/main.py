#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module uses its dependencies to compute the similarity
"""

from textSim import fast_text_sim
from contextSim import contextSim

DEFAULT_CSTE = [0.5, 0.3, 0.3]

def similarity(fArticle, sArticle, cstes = DEFAULT_CSTE):
	"""
	Computes the similarity between two wikipedia articles based on context and text similarity
	"""
	similarity = cstes[0] * fast_text_sim(fArticle, sArticle) + (1-cstes[0]) * contextSim(fArticle, sArticle, cstes)
	return similarity
