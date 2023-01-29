from collections import Counter

import numpy as np
import pandas as pd
from typing import List
from math import isnan
from functools import reduce


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
        self.numberOfTeams = numberOfTeams
        self.teamOccupied = np.zeros(numberOfTeams, dtype=bool)
        self.teamOccupied.fill(False)

    def __str__(self):
        out = f"Floor {self.index} - Capacity: {self.capacity}, Occupied: "
        for i in range(self.numberOfTeams):
            if self.teamOccupied[i] == True:
                out += f"{i}, "
        return out

    def is_occupying(self, team: int):
        self.teamOccupied[team] = True

    def teams_on_floor(self):
        result = []
        for index in range(0,self.capacity):
            # if self.is_occupying(index):
            if self.teamOccupied[index] is True:
                result.append(index)
        return result


class Team:
    def __init__(self, index: int, strength: int, preferences: List[int]):
        self.index = index
        self.strength = strength
        self.preferences = preferences
        self.likePref = []
        self.dislikePref = []

        for i in range(self.preferences.shape[0]):
            if self.preferences[i] == 1:
                self.likePref.append(i + 1)
            elif self.preferences[i] == -1:
                self.dislikePref.append(i + 1)
        print(self.likePref)
        print(self.dislikePref)

    def __str__(self):
        return f"Team {self.index} - Size: {self.strength}, Preferences: {self.preferences}"


class OfficeSolver:
    def __init__(self):
        preferencesArr = np.array(pd.read_csv("team_conflicts.csv", header=0, index_col=0))
        strengthPd = np.transpose(pd.read_csv("strength.csv", header=None))
        floorsPd = np.array(pd.read_csv("floors.csv", header=0))

        self.floors: List[Floor] = []
        self.teams: List[Team] = []
        self.kv: dict[int, Floor] = {}
        """A key value store where team indices are keys and the corresponding floor is the value."""

        for team_index in range(strengthPd.size):
            team = Team(team_index, strengthPd[team_index][0], preferencesArr[team_index])
            self.teams.append(team)

        for floor_index in range(int(floorsPd.size / 2)):
            floor = Floor(floor_index, floorsPd[floor_index][1], strengthPd.size)
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

    def returnFloorSize(self, floorNumber: int):
        total = 0
        floor = self.getFloorObj(floorNumber)
        for i in range(floor.teamOccupied.size):
            if floor.teamOccupied[i] == True:
                total = total + self.getTeamObj(i).strength
        return total

    def getFloorObj(self, floorNumber: int):
        return self.floors[floorNumber]

    def getTeamObj(self, teamNumber: int):
        return self.teams[teamNumber]

    def _floor_needs_more_teams(self, floor: Floor):
        """This function returns a boolean denoting whether a given floor needs more teams to meet the minimum 25% utilization mark."""
        return self.returnFloorSize(floor.index) / floor.capacity < 0.25
    
    def _floor_can_take_team(self, floor: Floor, team: Team):
        """This function returns a boolean denoting whether there is capacity for a given team to be added to a given floor."""
        out = (team.strength + self.returnFloorSize(floor.index)) <= floor.capacity
        print(f"Floor {floor.index} ({self.returnFloorSize(floor.index)}/{floor.capacity})",
              f"{'does' if out else 'does not'} have capacity for team {team.index} ({team.strength}).")
        return out

    def _get_most_preferred_floor(self, team: Team):
        print(f"- Finding the most preferred floor for team {team.index}")
        f = self.floors[0]
        for floor in self.floors:
            preferred = [0] * len(self.teams)
            for compareTeam in range(floor.teamOccupied.size):
                if isnan(team.preferences[compareTeam]):
                    continue
                preferred[floor.index] += 1 if team.preferences[compareTeam] == 1 else 0
            f = self.floors[preferred.index(max(preferred))]
            if f is not None and self._floor_can_take_team(f, team):
                print(f"- {f.index} is the most preferred floor for team {team.index}")
                return f
        if f is not None and self._floor_can_take_team(f, team):
            print(f"- {f.index} is the most preferred floor for team {team.index}")
            return f
        else:
            print(f"- Did not find the most preferred floor for team {team.index}")

    def _get_most_tolerated_floor(self, team: Team):
        f = self.floors[0]
        for floor in self.floors:
            tolerated = [0] * len(self.teams)
            for compareTeam in range(floor.teamOccupied.size):
                if isnan(team.preferences[compareTeam]):
                    continue
                tolerated[floor.index] += 1 if team.preferences[compareTeam] == 0 else 0
            f = self.floors[tolerated.index(max(tolerated))]
        if f is not None and self._floor_can_take_team(f, team):
            return f

    def _get_most_no_way_floor(self, team: Team):
        """Returns a floor that has adequate capacity to hold the given team and no teams that the given team said no way to. If constraints cannot be met, None is returned."""
        f: Floor = None
        for floor in self.floors:
            if not self._floor_can_take_team(floor, team):
                continue

            skip_this_floor = False
            for teamOnFloor in range(floor.teamOccupied.size):
                if isnan(team.preferences[teamOnFloor]) or team.preferences[teamOnFloor] == -1:
                    skip_this_floor = True
                if skip_this_floor:
                    break
            if not skip_this_floor:
                f = floor
        return f

    def solve(self):
        for team in self.sortByStrength():
            mostPreferredFloor = self._get_most_preferred_floor(team)
            if mostPreferredFloor is not None:
                self.floors[mostPreferredFloor.index].teamOccupied[team.index] = True
                self.kv[team.index] = mostPreferredFloor
                continue

            mostToleratedFloor = self._get_most_tolerated_floor(team)
            if mostToleratedFloor is not None:
                self.floors[mostToleratedFloor.index].teamOccupied[team.index] = True
                self.kv[team.index] = mostToleratedFloor
                continue

            mostNoWayFloor = self._get_most_no_way_floor(team)
            if mostNoWayFloor is not None:
                self.floors[mostNoWayFloor.index].teamOccupied[team.index] = True
                self.kv[team.index] = mostNoWayFloor
                continue

    def _solve(self):
        sorted = self.sortByStrength()
        for team in sorted:
            for floor in self.floors:
                preferred = [0] * len(self.teams)
                maxTol, tolerated = 0, [0] * len(self.teams)
                minNo, noWay = 0, [0] * len(self.teams)
                for compareTeam in range(floor.teamOccupied.size):
                    if isnan(team.preferences[compareTeam]):
                        continue
                    preferred[floor.index] += 1 if team.preferences[compareTeam] == 1 else 0
                    tolerated[floor.index] += 1 if team.preferences[compareTeam] == 0 else 0
                    noWay[floor.index] += 1 if team.preferences[compareTeam] == -1 else 0

                maxPref = max(preferred)
                maxTol = max(tolerated)
                minNo = min(noWay)
                # print(maxPref, maxTol, minNo)
                if preferred.count(maxPref) == 1 and self.get_occupied_percentage(preferred.index(maxPref)) >= 0.25:
                    self.floors[preferred.index(maxPref)].teamOccupied[team.index] = True
                elif not tolerated.count(maxTol) == 1 and self.get_occupied_percentage(
                        preferred.index(maxPref)) >= 0.25:
                    self.floors[preferred.index(maxTol)].teamOccupied[team.index] = True
                elif not noWay.count(minNo) == 1 and self.get_occupied_percentage(preferred.index(maxPref)) >= 0.25:
                    self.floors[preferred.index(minNo)].teamOccupied[team.index] = True
                else:
                    # allocate team to floor with minimum number of teams
                    # floor_with_min_teams = self.floors.index(min(self.floors.teams.numberOfTeams))
                    floor_with_min_teams = reduce(
                        lambda acc, curr: acc if Counter(curr.teamOccupied)[True] > Counter(acc.teamOccupied)[
                            True] else curr, self.floors, self.floors[0])
                    if floor_with_min_teams is None:
                        floor_with_min_teams = self.floors[0]
                    self.floors[floor_with_min_teams.index].teamOccupied[team.index] = True
                    # print("--*")
                    # print(floor_with_min_teams)
                    # print("*--")
                    # print(*self.floors, sep="\n")

    def get_occupied_percentage(self, team: int):
        return self.returnFloorSize(team) / self.getFloorObj(team).capacity

    def validate(self):
        print("*** UTILIZATION OVERVIEW")
        for floor in self.floors:
            print(f"Floor {floor.index} - Occupied: {self.returnFloorSize(floor.index)}/{floor.capacity}",
                  f"({(self.returnFloorSize(floor.index) / floor.capacity)*100}% utilization)")


solver = OfficeSolver()
solver.solve()
solver.validate()
print(solver)
