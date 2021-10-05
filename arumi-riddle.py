import numpy as np
import argparse
from queue import PriorityQueue


class Puzzle:
    goal_state = [4, 4, 4, 4]
    heuristic = None
    needs_heuristic = False
    num_of_instances = 0

    def __init__(self, state, parent, action, path_cost, needs_heuristic=False):
        self.parent = parent
        self.state = state
        self.action = action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost

        if needs_heuristic == True:
            self.needs_heuristic = True
            self.generate_heuristic()
            self.evaluation_function = self.heuristic + self.path_cost
        Puzzle.num_of_instances += 1

    def __str__(self):
        return np.reshape(np.array(self.state), (2, 2))

    # h function
    def generate_heuristic(self):
        self.heuristic = 0
        for num in range(0, len(self.state)):
            # step for each place to get 4
            distance = abs(self.state[num] - self.goal_state[num])
            h = self.heuristic = self.heuristic + distance

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    # DO NOT USE this stupid shit for BIGGER puzzle
    def kick(self, state, place):
        if place == 0:
            state[place] += 1
            state[place + 1] += 1
            state[place + 2] += 1
        if place == 1:
            state[place] += 1
            state[place - 1] += 1
            state[place + 2] += 1
        if place == 2:
            state[place] += 1
            state[place + 1] += 1
            state[place - 2] += 1
        if place == 3:
            state[place] += 1
            state[place - 1] += 1
            state[place - 2] += 1
        for i in range(len(state)):
            if state[i] > 4:
                state[i] = 1
        return state

    def generate_child(self):
        children = []
        legal_actions = ['a', 'b', 'c', 'd']
        for action in legal_actions:
            new_state = self.state.copy()
            if action is 'a':
                new_state = self.kick(new_state, 0)
            elif action is 'b':
                new_state = self.kick(new_state, 1)
            elif action is 'c':
                new_state = self.kick(new_state, 2)
            elif action is 'd':
                new_state = self.kick(new_state, 3)
            children.append(Puzzle(new_state, self, action, 1, self.needs_heuristic))
        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution


def Astar_search(initial_state):
    count = 0
    explored = []
    start_node = Puzzle(initial_state, None, None, 0, True)
    q = PriorityQueue()
    q.put((start_node.evaluation_function, count, start_node))

    while not q.empty():
        node = q.get()
        node = node[2]
        explored.append(node.state)
        if node.goal_test():
            return node.find_solution()

        children = node.generate_child()
        for child in children:
            if child.state not in explored:
                count += 1
                teno = (child.evaluation_function, count, child)
                q.put((child.evaluation_function, count, child))
    return


def print_solution(init_state, astar):
    init = Puzzle(init_state, None, None, 0, False)
    temp = init.state
    print(init.state)
    for action in astar:
        init = Puzzle(temp, None, action, 0, False)
        act = None
        if action == 'a':
            act = 0
        elif action == 'b':
            act = 1
        elif action == 'c':
            act = 2
        elif action == 'd':
            act = 3
        temp = init.kick(init.state, act)
        print(action, temp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve Arumi riddle')
    parser.add_argument('input', metavar='input', type=list, nargs='+',
                        help='current state of riddle')
    parser.add_argument('--solve', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='solve the riddle (find the fastest way with A*)')
    args = parser.parse_args()
    # print(args.accumulate(args.input))

    # parse to int list
    input_int = [int(x) for x in args.accumulate(args.input)]
    print("Input state:", input_int)

    # solve problem
    astar = Astar_search(initial_state=input_int)
    print("Solution:", astar)

    # print process
    print_solution(input_int, astar)
