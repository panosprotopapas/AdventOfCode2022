from math import ceil
from json import dumps
from copy import copy
from time import time
from re import findall
from collections import deque


class Blueprint:
    def __init__(self, n, ore_r, cla_r, obs_r, geo_r):
        self.n = n
        self.ore_r = ore_r
        self.cla_r = cla_r
        self.obs_r = obs_r
        self.geo_r = geo_r
        self.max_ore = max(self.cla_r, self.obs_r[0], self.geo_r[0])
        self.max_cla = self.obs_r[1]
        self.max_obs = self.geo_r[1]


class NextStateCalculator:
    class State:
        def __init__(self, blueprint, max_t, statezip=(0, 0, 0, 0, 1, 0, 0, 0)):
            self.ore = statezip[0]
            self.cla = statezip[1]
            self.obs = statezip[2]
            self.geo = statezip[3]
            self.ore_r = statezip[4]
            self.cla_r = statezip[5]
            self.obs_r = statezip[6]
            self.time = statezip[7]
            self.bp = blueprint
            self.max_t = max_t

        def zip_state(self):
            return (
                self.ore,
                self.cla,
                self.obs,
                self.geo,
                self.ore_r,
                self.cla_r,
                self.obs_r,
                self.time,
            )

        def advance_time(self, time):
            self.ore += self.ore_r * time
            self.cla += self.cla_r * time
            self.obs += self.obs_r * time
            self.time += time

        def build_robot(self, robot):
            if robot == "ore":
                self.ore -= self.bp.ore_r
                self.ore_r += 1
            elif robot == "cla":
                self.ore -= self.bp.cla_r
                self.cla_r += 1
            elif robot == "obs":
                self.ore -= self.bp.obs_r[0]
                self.cla -= self.bp.obs_r[1]
                self.obs_r += 1
            elif robot == "geo":
                self.ore -= self.bp.geo_r[0]
                self.obs -= self.bp.geo_r[1]
                self.geo += self.max_t - self.time

        def __repr__(self):
            res = {
                "time": self.time,
                "ore reserves": self.ore,
                "clay reserves": self.cla,
                "obsidian reserves": self.obs,
                "geode reserves": self.geo,
                "ore robots": self.ore_r,
                "clay robots": self.cla_r,
                "obsidian robots": self.obs_r,
            }
            return dumps(res, indent=4)

    def __init__(self, blueprint, max_t, statezip=None):
        self.max_t = max_t
        self.bp = blueprint
        self.st = (
            self.State(blueprint=self.bp, max_t=max_t, statezip=statezip)
            if statezip
            else self.State(blueprint=self.bp, max_t=max_t)
        )
        self.next_states = list()
        self.next_r = dict()
        self.find_next_states()

    def find_next_states(self):
        self.next_r = self.next_robots()
        self.sanity_checks()

        for robot_type, when in self.next_r.items():

            if robot_type == "ore":
                next_state = copy(self.st)
                next_state.advance_time(time=when)
                next_state.build_robot(robot=robot_type)
                self.next_states.append(next_state)

            elif robot_type == "cla":
                next_state = copy(self.st)
                next_state.advance_time(time=when)
                next_state.build_robot(robot=robot_type)
                self.next_states.append(next_state)

            elif robot_type == "obs":
                if when > self.next_r.get("cla", 100):
                    temp_state = copy(self.st)
                    temp_state.advance_time(self.next_r["cla"])
                    temp_state.build_robot(robot="cla")
                    next_next_r = self.next_robots(state=temp_state)

                    # Need to account for the lost ore if not choosing to make obs now
                    ore_fixer = (
                        ceil(self.bp.cla_r / self.st.ore_r)
                        if self.st.ore_r < self.bp.max_ore
                        else 0
                    )

                    if next_next_r["obs"] + self.next_r["cla"] + ore_fixer > when:
                        next_state = copy(self.st)
                        next_state.advance_time(time=when)
                        next_state.build_robot(robot=robot_type)
                        self.next_states.append(next_state)

                else:
                    next_state = copy(self.st)
                    next_state.advance_time(time=when)
                    next_state.build_robot(robot=robot_type)
                    self.next_states.append(next_state)

            else:
                if when > self.next_r.get("obs", 100):
                    temp_state = copy(self.st)
                    temp_state.advance_time(self.next_r["obs"])
                    temp_state.build_robot(robot="obs")
                    next_next_r = self.next_robots(state=temp_state)

                    # Need to account for the lost ore if not choosing to make obs now
                    ore_fixer = (
                        ceil(self.bp.obs_r[0] / self.st.obs_r)
                        if self.st.ore_r < self.bp.max_ore
                        else 0
                    )

                    if next_next_r["geo"] + self.next_r["obs"] + ore_fixer > when:
                        next_state = copy(self.st)
                        next_state.advance_time(time=when)
                        next_state.build_robot(robot=robot_type)
                        self.next_states.append(next_state)
                else:
                    next_state = copy(self.st)
                    next_state.advance_time(time=when)
                    next_state.build_robot(robot=robot_type)
                    self.next_states.append(next_state)

    def next_robots(self, state=None):
        state = self.st if not state else state
        next_r = {
            "ore": max(ceil((self.bp.ore_r - state.ore) / state.ore_r) + 1, 1),
            "cla": max(ceil((self.bp.cla_r - state.ore) / state.ore_r) + 1, 1),
        }
        if state.cla_r:
            next_r["obs"] = max(
                max(
                    ceil((self.bp.obs_r[0] - state.ore) / state.ore_r),
                    ceil((self.bp.obs_r[1] - state.cla) / state.cla_r),
                )
                + 1,
                1,
            )
            if state.obs_r:
                next_r["geo"] = max(
                    max(
                        ceil((self.bp.geo_r[0] - state.ore) / state.ore_r),
                        ceil((self.bp.geo_r[1] - state.obs) / state.obs_r),
                    )
                    + 1,
                    1,
                )
        return next_r

    def sanity_checks(self):
        # Dont built more robots than needed for building 1 per period
        if self.st.ore_r == self.bp.max_ore:
            self.next_r.pop("ore", None)
        if self.st.cla_r == self.bp.max_cla:
            self.next_r.pop("cla", None)
        if self.st.obs_r == self.bp.max_obs:
            self.next_r.pop("obs", None)

        for key, val in list(self.next_r.items()):
            # Don't build geo bots early and ore bots late in the game
            if self.st.time <= self.max_t * 0.2 and key == "geo":
                self.next_r.pop(key)
            elif self.st.time >= self.max_t * 0.75 and key == "ore":
                self.next_r.pop(key)

            # Don't build stuff that you need to wait too long, or pretty long but later in the game
            elif val >= 8:
                self.next_r.pop(key)

            # Don't have geode robots ready at T and anything else at T - 1, no use
            elif self.st.time + val >= self.max_t:
                self.next_r.pop(key)
            elif self.st.time + val >= self.max_t - 1 and key != "geo":
                self.next_r.pop(key)

    def __repr__(self):
        return str(self.st)


with open("19/input.txt", encoding="utf-8") as f:
    results = [[int(i) for i in findall(r"\d+", l.strip())] for l in f.readlines()]
    blueprints = [
        Blueprint(
            n=r[0], ore_r=r[1], cla_r=r[2], obs_r=(r[3], r[4]), geo_r=(r[5], r[6])
        )
        for r in results
    ]


def solve(blueprint, max_t, part_1=False):
    result = 0
    calcs = [(0, 0, 0, 0, 1, 0, 0, 0)]
    new_calcs = deque()
    for _ in range(max_t - min(blueprint.ore_r, blueprint.cla_r)):
        for _ in range(len(calcs)):
            calc = calcs.pop()
            ns = NextStateCalculator(blueprint=blueprint, max_t=max_t, statezip=calc)
            if ns.next_states:
                new_calcs.extend(
                    [next_state.zip_state() for next_state in ns.next_states]
                )
        try:
            result = max(result, max(new_calcs, key=lambda x: x[3])[3])
        except ValueError:
            pass
        calcs, new_calcs = new_calcs, deque()
    if part_1:
        return result * blueprint.n
    return result


start = time()
result = 0
for blueprint in blueprints:
    i = solve(blueprint, 24, part_1=True)
    result += i
print(f"Part 1: {result}\n Time taken: {time() - start}\n")

start = time()
a = solve(blueprints[0], 32)
b = solve(blueprints[1], 32)
c = solve(blueprints[2], 32)
print(f"Part 1: {a*b*c}\n Time taken: {time() - start}")
