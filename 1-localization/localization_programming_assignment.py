# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

# sense
# p = probability grid
# world_map = map of colorts
# sensor_result = color read by sensor
# sensor_right = probability that sensor is correct
def sense(p, world_map, sensor_result, sensor_right):
    # output probability
    q = []

    # total sum for normalization
    total_sum = 0

    # iterate over rows of the grid
    for i in range(len(p)):
        row=[]
        # iterate over columns of the grid
        for j in range(len(p[i])):
            # update probability on grid based on sensor data
            if (sensor_result == world_map[i][j]):
                row.append(p[i][j] * sensor_right)
            else:
                row.append(p[i][j] * (1.0 - sensor_right))
        q.append(row)
        total_sum = total_sum + sum(row)

    # normalize
    for i in range(len(p)):
        for j in range(len(p[i])):
            q[i][j] = q[i][j]/total_sum

    return q

# move_down
# p = probability grid
# steps = steps to move
def move_down(p, steps):
    # output probability
    q = []
    for i in range(len(p)):
        q.append(p[(i - steps) % len(p)])
    return q

# move_up
# p = probability grid
# steps = steps to move
def move_up(p, steps):
    # convert the steps as a move_down action by inverting
    # since the world is cyclic
    num_rows = len(p)
    steps_move_down = num_rows - steps
    # perform move_down with the converted step count
    q = move_down(p, steps_move_down)
    return q

# move_right
# p = probability grid
# steps = steps to move
def move_right(p, steps):
    q = []
    # iterate over rows of the grid
    for i in range(len(p)):
        row=[]
        # iterate over columns of the grid
        for j in range(len(p[i])):
            row.append(p[i][(j - steps) % len(p[i])])
        q.append(row)
    return q

# move_left
# p = probability grid
# steps = steps to move
def move_left(p, steps):
    # convert the steps as a move_right action by inverting
    # since the world is cyclic
    num_columns = len(p[0])
    steps_move_right = num_columns - steps
    # perform move_down with the converted step count
    q = move_right(p, steps_move_right)
    return q

# scalar_product
# p = probability grid
# factor = mulitplication factor
def scalar_product(p, factor):
    q = []
    # iterate over rows of the grid
    for i in range(len(p)):
        row=[]
        # iterate over columns of the grid
        for j in range(len(p[i])):
            row.append(p[i][j] * float(factor))
        q.append(row)
    return q

# matrix_product
# p1 = probability grid 1
# p1 = probability grid 2
def matrix_addition(p1, p2):
    q = []
    # iterate over rows of the grid
    for i in range(len(p1)):
        row=[]
        # iterate over columns of the grid
        for j in range(len(p1[i])):
            row.append(p1[i][j] + p2[i][j])
        q.append(row)
    return q

# move
# p = probability grid
# p_move = probability that the robot moved and did not stay in place
def move(p, motion, p_move):
    if (motion == [0, 0]):
        p_after_move = p
    elif (motion == [0, 1]):
        p_after_move = move_right(p, 1)
    elif (motion == [0, -1]):
        p_after_move = move_left(p, 1)
    elif (motion == [1, 0]):
        p_after_move = move_down(p, 1)
    elif (motion == [-1, 0]):
        p_after_move = move_up(p, 1)
    else:
        # do not move
        p_after_move = p

    # total probability
    q = matrix_addition(scalar_product(p_after_move, p_move), scalar_product(p, 1.0 - p_move))
    return q

def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    
    for i in range(len(motions)):
        p = move(p, motions[i], p_move)
        p = sense(p, colors, measurements[i], sensor_right)

    return p

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
show(p) # displays your answer
