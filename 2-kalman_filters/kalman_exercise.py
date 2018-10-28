import math

# compute the gaussian probability of x given:
# mu - mean
# sigma2 - variance
def f(x, mu, sigma2):
    return math.exp(-0.5 * math.pow(x - mu, 2) / sigma2) / math.sqrt(2 * sigma2 * math.pi)

# gaussian multiplication of 2 gaussian distributions
def update(mean1, var1, mean2, var2):
    new_mean = (mean1 * var2 + mean2 * var1) / (var1 + var2)
    new_var = 1 / (1 / var1 + 1 / var2)
    return [new_mean, new_var]

# gaussian addition of 2 gaussian distributions
def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

# input for item 20. Quiz: Kalman Filter Code
measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.

# initial location
mu = 0.
sig = 10000.

for i in range(len(measurements)):
    # update with measurement
    [mu, sig] = update(mu, sig, measurements[i], measurement_sig)
    print("update: ", [mu, sig])
    # predict next location with motion
    [mu, sig] = predict(mu, sig, motion[i], motion_sig)
    print("predict: ", [mu, sig])

print("final: ", [mu, sig])
