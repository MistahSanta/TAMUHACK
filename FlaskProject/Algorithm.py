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

    def is_occupying(self, team: int):
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
        # print(f"huidjshifhsg {sorted[0].strength} {type(sorted[0].strength)}",)
        # print(*sorted)
        # print(*self.floors)
        for team in sorted:
            for floor in self.floors:
                maxPref = 0
                preferred = [0] * len(self.teams)
                maxTol, tolerated = 0, [0] * len(self.teams)
                minNo, noWay = 0, [0] * len(self.teams)
                for compareTeam in range(floor.teamOccupied.size):
                    if math.isnan(team.preferences[compareTeam]): continue
                    preferred[floor.index] += 1 if team.preferences[compareTeam] == 1 else 0
                    tolerated[floor.index] += 1 if team.preferences[compareTeam] == 0 else 0
                    noWay[floor.index] += 1 if team.preferences[compareTeam] == -1 else 0

            maxPref = max(preferred)
            maxTol = max(tolerated)
            minNo = min(noWay)

            if preferred.count(maxPref) == 1 and self.get_occupied_percentage(preferred.index(maxPref)) >= 0.25:
                self.floors[preferred.index(maxPref)].teamOccupied[team] = True
            elif not tolerated.count(maxTol) == 1 and self.get_occupied_percentage(preferred.index(maxPref)) >= 0.25:
                self.floors[preferred.index(maxTol)].teamOccupied[team] = True
            elif not noWay.count(minNo) == 1 and self.get_occupied_percentage(preferred.index(maxPref)) >= 0.25:
                self.floors[preferred.index(minNo)].teamOccupied[team] = True
            else:
                #allocate team to floor with minimum number of teams
                # print(f'the thing {type(self.floors.teams)}')
                self.floors
                reduce(lambda arr, floor: arr.append(floor.teamOccupied), [], self.floors)
                # floor_with_min_teams = self.floors.index(min(self.floors.teams.numberOfTeams))
                floor_with_min_teams = reduce(lambda acc, curr: acc if Counter(curr.teamOccupied)[True] < Counter(acc.teamOccupied)[True] else curr, self.floors)
                self.floors[floor_with_min_teams.index].teamOccupied[team.index] = True

    def get_occupied_percentage(self, team: int):
        return self.returnFloorSize(team) / self.getFloorObj(team).capacity


solver = OfficeSolver()
solver.solve()
