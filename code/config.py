# Global variables
gridSize = 50
nAgents = gridSize * gridSize
epochs = 300
initialCoopRate = 0.75
emotionsRate = 0.8

plot = False
emotions = True
coalitions = False

# Local variables
x = 3
y = 9
increment = 1
threshold_joy = 0
threshold_anger = 6
threshold_pity = 7
threshold_distress = 0.5
threshold_boredom = -.2
threshold_threat = -10

# Prisoner's Dilemma Payoff
T = 1.9  # Triumph
R = 1.0  # Dual coop
P = 0.0  # Dual defect
S = 0.0  # Sucker
