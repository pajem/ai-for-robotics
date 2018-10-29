from matrix import *

# kalman filter
# x - initial state/estimate
# P - covariance matrix
def kalman_filter(x, P):
    for n in range(len(measurements)):
        ## measurement update
        err = matrix([[measurements[n]]]) - H * x
        S = H * P * H.transpose() + R
        K = P * H.transpose() * S.inverse()
        x = x + (K * err)
        P = (I - K * H) * P

        ## prediction
        x = F * x + u
        P = F * P * F.transpose()
    return x,P

# Test case
measurements = [1, 2, 3]

# initial state (location and velocity)
x = matrix([[0.],
            [0.]])

# initial uncertainty
P = matrix([[1000., 0.],
            [0., 1000.]])

# external motion
u = matrix([[0.],
            [0.]])

# next state function
F = matrix([[1., 1.],
            [0, 1.]])

# measurement function
H = matrix([[1., 0.]])

# measurement uncertainty
R = matrix([[1.]])

# identity matrix
I = matrix([[1., 0.],
            [0., 1.]])

print(kalman_filter(x, P))
# output should be:
# x: [[3.9996664447958645], [0.9999998335552873]]
# P: [[2.3318904241194827, 0.9991676099921091], [0.9991676099921067, 0.49950058263974184]]
