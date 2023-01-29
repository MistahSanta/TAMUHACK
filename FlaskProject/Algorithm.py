import numpy as np
import pandas as pd
from typing import List

# def mainAlgorithm():
#     floorCurr = np.empty(shape=(np.size(floorMax),np.size(teamStrength)))
#     floorCurr.fill(False)
#     teamIn = np.zeros(np.size(teamStrength))
#     teamPref = pd.read_csv("team_conflicts.csv", header=0, index_col=0)
#     print(floorCurr)
#     team_sort = sortByStrength()
#     for team in team_sort:
#
#         for floor in floorCurr:
#             pass

class Floor:
    def __init__(self, index: int, capacity: int, numberOfTeams: int):
        self.index = index
        self.capacity = capacity
        self.teamOccupied = np.zeros(numberOfTeams, dtype=bool)
        self.teamOccupied.fill(False)

    def __str__(self):
        return f"Floor {self.index} - Capacity: {self.capacity}, Occupied: {self.teamOccupied}"

    def Occupying(self, team: int):
        self.teamOccupied[team - 1] = True

class Team:
    def __init__(self, index: int, strength: int, preferences: List[int]):
        self.index = index
        self.strength = strength
        self.preferences = preferences

    def __str__(self):
        return f"Team {self.index} - Size: {self.strength}, Preferences: {self.preferences}"


class OfficeSolver:
    def __init__(self):
        self.preferencesArr = np.array(pd.read_csv("team_conflicts.csv", header=0, index_col=0))
        self.strengthPd = np.transpose(pd.read_csv("strength.csv", header=None))
        self.floorsPd = np.array(pd.read_csv("floors.csv", header=0))

        self.floors: List[Floor] = []
        """This is a list containing lists for each floor, which contain the teams currently occupying the floor."""
        self.teams: List[Team] = []

        for team_index in range(self.strengthPd.size):
            team = Team(team_index, self.strengthPd[team_index][0], self.preferencesArr[team_index])
            self.teams.append(team)

        for floor_index in range(int(self.floorsPd.size/2)):
            floor = Floor(floor_index, self.floorsPd[floor_index][1], self.strengthPd.size)
            self.floors.append(floor)

    def __str__(self):
        out = "*** FLOORS\n"
        for floor in self.floors:
            out += f"\t{floor}\n"
        out += "*** TEAMS\n"
        for floor in self.teams:
            out += f"\t{floor}\n"
        return out

    def sortByStrength(self):
        arr = list(self.teams)
        arr.sort(key=lambda t: t.strength, reverse=True)
        # sortedStrength = np.sort(self.strengthPd)[::-1]
        # sortedTeam = np.zeros(11)
        # for i in range(np.size(sortedStrength)):
        #     sortedTeam[i] = np.where(sortedStrength == self.strengthPd[i])[0]
        # return sortedTeam.astype(int)
        return arr

    def returnFloorSize(self, floorNumber):
        total = 0
        floor = self.getFloorObj(floorNumber)
        for i in range(floor.teamOccupied.size):
            if floor.teamOccupied[i] == True:
                total = total + self.getTeamObj(i + 1).strength
        return total

    def getFloorObj(self, floorNumber: int):
        if floorNumber <= 0:
            raise Exception("Floor number out of range")
        return self.floors[floorNumber - 1]

    def getTeamObj(self, teamNumber: int):
        if teamNumber <= 0:
            raise Exception("Team number out of range")
        return self.teams[teamNumber - 1]

    def solve(self):
        sorted = self.sortByStrength()
        print(sorted)
        for team in sorted:
            for floor in self.floors:
                """
                This is a list of 3-tuples. 
                There is one tuple for each floor, where:
                    element 1 is the number of preferred teams for `team` on floor `floor`
                    element 2 is the number of tolerated teams for `team` on floor `floor`
                    element 3 is the number of no way teams for `team` on floor `floor`
                """
                preferred = []
                tolerated = []
                noWay = []
                for compareTeam in range(floor.teamOccupied.size):
                    (preferred if team.preferences[compareTeam] == 1
                     else tolerated if team.preferences[compareTeam] == 0
                    else noWay).append(compareTeam)
                mostPreferredFloor = preferred.index(max(preferred))
                mostToleratedFloor = tolerated.index(max(tolerated))
                mostNoWayFloor = noWay.index(min(noWay))
            # for each team
            #bestPreferredFloor =
            #find room with most from prefered list

            #find room with most from tolerated list

            #find room with least form no way

            #non of these work then end the loop and done
        pass


solver = OfficeSolver()
solver.solve()
