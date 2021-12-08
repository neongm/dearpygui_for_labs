import numpy as np
from random import normalvariate, randint

def main():
    a1 = 10
    a2 = -5
    a3 = 1
    x_size = 4

    arr_x = []
    for i in range(x_size): arr_x.append([x*10 + normalvariate(0, 1)/100 for x in range(0, x_size)])
    #for i in range(x_size): arr_x.append([normalvariate(0, 1) * 10 + normalvariate(0, 1) / 100 for x in range(0, x_size)])

    coeffs = [randint(-10, 10) for i in range(x_size)]

    print(coeffs)
    COEFF = 5
    arr_y = []
    for i in range(x_size):
        s = 0
        for x in range(x_size):
            s += arr_x[x][i] * coeffs[i]
        arr_y.append(s)


    for line_x in arr_x:
        [print(str(round(x, 4))+'\t', end='') for x in line_x]
        print('\n')

    xnp = np.array(arr_x)
    ynp =  np.array(arr_y)


    w = np.linalg.solve(np.dot(xnp.T, xnp), np.dot(xnp.T, ynp))
    Yhat = np.dot(xnp, w)
    print(f"yhat: {Yhat}")
    print(f"actual coeffs: {coeffs}")
    d1 = ynp - Yhat
    d2 = ynp - ynp.mean()
    print(f'determination: {1 - d1.dot(d1)/d2.dot(d2)}')




if __name__ == "__main__": main()