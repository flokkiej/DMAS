#!/usr/bin/python
import agent, config, numpy

def emotionize(me, neighbours):
	intensities = {'Joy': 0, 'Distress': 0}

	# Rule for Joy
	n_neighbours_joyful = numpy.sum([1 for neigh in neighbours if neigh.emotion == 'Joy'])
	if (me.points > config.y) or (n_neighbours_joyful > config.x):
		potential_joy = config.increment
		if potential_joy > config.threshold_joy:
			intensities['Joy'] = potential_joy - config.threshold_joy

	# Rule for Distress
	n_neighbours_distress = numpy.sum([1 for neigh in neighbours if neigh.emotion == 'Distress'])
	if (me.points < config.y) or (n_neighbours_distress > config.x):
		potential_distress = config.increment
		if potential_distress > config.threshold_distress:
			intensities['Distress'] = potential_distress - config.threshold_distress

	#return emotion with highest value
	return max(intensities, key=intensities.get)
