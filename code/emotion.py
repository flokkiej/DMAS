import config
import numpy


def emotionize(me, neighbours):
    intensities = {'Joy': 0, 'Distress': 0, 'Anger': 0, 'Pity': 0, 'Threat': 0, 'Boredom': 0}

    # Rule for Joy:
    # IF player has collected at least y points OR at least x neighbours are joyful
    n_neighbours_joyful = numpy.sum([1 for neigh in neighbours if neigh.emotion == 'Joy'])
    if (me.points > config.y) or (n_neighbours_joyful > config.x):
        potential_joy = config.increment
        if potential_joy > config.threshold_joy:
            intensities['Joy'] = potential_joy - config.threshold_joy

    # Rule for Distress
    # IF player has not collected at least y points OR at least x neighbours are distressful
    n_neighbours_distress = numpy.sum([1 for neigh in neighbours if neigh.emotion == 'Distress'])
    if (me.points < config.y) or (n_neighbours_distress > config.x):
        potential_distress = config.increment
        if potential_distress > config.threshold_distress:
            intensities['Distress'] = potential_distress - config.threshold_distress

    # Rule for Anger
    # IF player has not collected at least y points AND opponent has defected
    # Each D neighbour contributes to potential_anger individually
    # This way, the more neighbours Deflect, the more potential is generated
    if me.points < config.y:
        potential_anger = 0
        for i in xrange(len(neighbours)):
            if neighbours[i].status == 'D' and (not me.coalition or not neighbours[i].coalition):
                potential_anger += config.increment
        if potential_anger > config.threshold_anger:
            intensities['Anger'] = potential_anger - config.threshold_anger

    # Rule for Pity
    # IF neighbour has not collected at least y points
    potential_pity = 0
    for i in xrange(len(neighbours)):
        if neighbours[i].points < config.y:
            potential_pity += config.increment

    if potential_pity > config.threshold_pity:
        intensities['Pity'] = potential_pity - config.threshold_pity

    # Rule for Threat
    # IF at least x neighbours are identical in type of emotion AND type is different from its own
    n_neighbours_threat = 0
    for i in xrange(len(neighbours)):
        if neighbours[i].status != me.status and neighbours[i].emotion == me.emotion and type(me.emotion) == str:
            n_neighbours_threat += 1
    if n_neighbours_threat > config.x:
        potential_threat = config.increment
        if potential_threat > config.threshold_threat:
            intensities['Threat'] = potential_threat - config.threshold_threat

    # Rule for Boredom
    # IF at least x neighbours are identical in type of emotion
    n_neighbours_boring = 0
    for i in xrange(len(neighbours)):
        if neighbours[i].emotion == me.emotion and type(me.emotion) == str:
            n_neighbours_boring += 1

    if n_neighbours_boring > config.x:
        potential_boredom = config.increment
        if potential_boredom > config.threshold_boredom:
            intensities['Boredom'] = potential_boredom - config.threshold_boredom

    # return emotion with highest value
    highest = max(intensities, key=intensities.get)
    if intensities[highest] == 0:
        return None
    else:
        return highest
