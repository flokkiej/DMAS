#!/usr/bin/python
import agent

def desirability(me):
	lastscore = me.lastRound
	emotion = me.returnEmotion()
	D = lastscore - 2
	return D

def praiseworthyness(me, other):
	me_emo = me.returnEmotion()
	other_emo = other.returnEmotion()
	return


