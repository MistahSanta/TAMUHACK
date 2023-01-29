import os

from Algorithm import OfficeSolver
from flask import Flask, render_template, abort
import decimal

app = Flask(__name__)

exampleTeamArray = [
    [10, "Floor A", .8],
    [30, "Floor B", .7],
    [20, "Floor C", .9],
    [50, "Floor D", 1]
]

exampleFloorOccupied = [
    .25, .10, 1, .93
]


@app.route('/')
def main():  # put application's code here
    solver = OfficeSolver()
    solver.solve()
    solver.validate()
    overview = [[k.strength, f"{'No Availability' if k.index not in solver.kv else solver.kv[k.index].index + 1}", k.likePref, k.dislikePref] for
                k in solver.teams]
    return render_template('teams.html',
                           numTeams=len(solver.teams),
                           numFloors=len(solver.floors),
                           teamOverview=overview,
                           floorOccupied=[
                               [round(
                                   decimal.Decimal(solver.returnFloorSize(floor.index) / floor.capacity), 4),
                                   solver.returnFloorSize(floor.index),
                                   floor.capacity] for floor in solver.floors
                           ])


@app.route('/<site>')
def setting(site):
    if (site == "Setting"):
        print('setting page is loaded')
        return render_template('setting.html', sites="Setting")
    elif (site == "Preferences"):
        print('preference page is loaded')
        return render_template('preference.html', sites="Preferences")
    elif(site == "test"):
        return render_template('TableTest.html', sites="test")
    else:
        return abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=os.environ["PORT"] if "PORT" in os.environ else 5000)
