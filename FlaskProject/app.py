import Algorithm
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():  # put application's code here
    return render_template('teams.html')


@app.get("/run_sample")
def sample():
    return Algorithm.mainAlgorithm()








if __name__ == '__main__':
    app.run()
