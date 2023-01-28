import numpy as np
from flask import Flask

app = Flask(__name__)


@app.route('/')
def main():  # put application's code here
    teamStrength = np.array([22, 45, 34, 51, 11, 37, 42, 16, 29, 56, 49])
    teamPreference = np.array([[2,4,6,11],
                      [1,3,5],
                      [1,2,11],
                      [10],
                      [1,2,3,4],
                      [7,10],
                      [1,2,3,4,5,6],
                      [1,10],
                      [1,5],
                      [2,6,7,11],
                      [1,4,5]])
    teamNoway = np.array(
                [[5,7,9],
                 [4,8,9,10],
                 [4,5,6,8,9,10],
                 [2,5,6,7,8,9,11],
                 [6,7,8],
                 [2,3,4,5,9,11],
                 [8,9],
                 [3,5,6,7,9],
                 [3,4,6,7,8,11],
                 [1,3,9],
                 [8]])
    teamIn = np.full((5), True)
    floorMax = np.array([43, 81, 73, 54, 97])
    floorCurr = np.zeros(5)

    while ()

    return 'Hello World'




if __name__ == '__main__':
    app.run()
