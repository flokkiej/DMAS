#!/usr/bin/python
import agent, config, numpy

def emotionize(me, neighbours):
	intensities = {'Joy': 0, 'Distress': 0, 'Anger': 0, 'Pity': 0}

	# Rule for Joy:
	#	IF player has collected at least y points OR at least x neighbours are joyful
	n_neighbours_joyful = numpy.sum([1 for neigh in neighbours if neigh.emotion == 'Joy'])
	if (me.points > config.y) or (n_neighbours_joyful > config.x):
		potential_joy = config.increment
		if potential_joy > config.threshold_joy:
			intensities['Joy'] = potential_joy - config.threshold_joy

	# Rule for Distress
	#	IF player has not collected at least y points OR at least x neighbours are distressful
	n_neighbours_distress = numpy.sum([1 for neigh in neighbours if neigh.emotion == 'Distress'])
	if (me.points < config.y) or (n_neighbours_distress > config.x):
		potential_distress = config.increment
		if potential_distress > config.threshold_distress:
			intensities['Distress'] = potential_distress - config.threshold_distress

	# Rule for Anger
	#	IF player has not collected at least y points AND opponent has defected
	defector = False
	for i in xrange(len(neighbours)):
		if neighbours[i].status == 'D': defector = True
	if (me.points < config.y) and defector:
		potential_anger = config.increment
		if potential_anger > config.threshold_anger:
			intensities['Anger'] = potential_anger - config.threshold_anger

	# Rule for Pity
	#	IF neighbour has not collected at least y points
	low_scorer = False
	for i in xrange(len(neighbours)):
		if neighbours[i].points < config.y: low_scorer = True
	if low_scorer:
		potential_pity = config.increment
		if potential_pity > config.threshold_pity:
			intensities['Pity'] = potential_pity - config.threshold_pity

	#return emotion with highest value
	highest = max(intensities, key=intensities.get)
	if intensities[highest] == 0: return None
	else: return highest
