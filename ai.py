"""
Holds methods and containers for the AI state program.
Still need a name for the method by which the AI works.
Perhaps something involving pruning?
"""

from copy import deepcopy
from pokemon import Action
from pokemon import Type
from pokemon import attack
from random import randint
from collections import deque
from config import CONF

class PkmnState():
    def __init__(self,  team1, team2, need_copy=False):
        if need_copy:
            self.team1 = deepcopy(team1)
            self.team2 = deepcopy(team2)
        else:
            self.team1 = team1
            self.team2 = team2

    def is_action_valid(self, a, t):
        #import pdb; pdb.set_trace()
        if a < Action.SWITCH_OFFSET: # is a move, not a switch
            if a >= len(t.get_cur_pkmn().moves): # that move slot is not filled
                return False
            elif t.pkmn[t.curpkmn].moves[a].curpp == 0: # that move is out of pp
                return False
        else: # a >= Action.SWITCH_OFFSET
            # TODO: consider moves that prevent switching
            if a - Action.SWITCH_OFFSET >= len(t.pkmn): # that slot is not filled
                return False
            elif t.pkmn[a - Action.SWITCH_OFFSET].curhp == 0: # that pkmn has fainted
                return False
            elif a - Action.SWITCH_OFFSET == t.curpkmn: # that pkmn has already fainted
                return False
        return True
        
    def are_actions_valid(self, *actions):
        return (self.is_action_valid(actions[0], self.team1) and 
                self.is_action_valid(actions[1], self.team2))

    def get_sucessors(self):
        # TODO: consider accuracy, crits, status, move effects, etc. when choosing sucessors
        # TODO: rearrange child order for optimization
        sucessors = []
        #import pdb; pdb.set_trace()
        for a in Action.get_all():
            for b in Action.get_all():
                if self.are_actions_valid(a, b):
                    sucessors.append((a, b, self.mutate(a, b)))
        return sucessors

    def mutate(self, *actions):
        team1 = deepcopy(self.team1)
        team2 = deepcopy(self.team2)

        if actions[0] >= Action.SWITCH_OFFSET and actions[1] >= Action.SWITCH_OFFSET:
            # double switch
            team1.curpkmn = actions[0] - Action.SWITCH_OFFSET
            team2.curpkmn = actions[1] - Action.SWITCH_OFFSET

        elif actions[0] >= Action.SWITCH_OFFSET and actions[1] < Action.SWITCH_OFFSET:
            # team1 switches, then team2 attack
            # TODO: account for Pursuit
            team1.curpkmn = actions[0] - Action.SWITCH_OFFSET
            team1.pkmn[team1.curpkmn] = attack(team2.get_cur_pkmn(), team1.get_cur_pkmn(), actions[1])
            if team1.get_cur_pkmn().curhp == 0:
                # TODO: Implement proper switching
                team1.curpkmn = team1.get_next_pkmn()

        elif actions[0] < Action.SWITCH_OFFSET and actions[1] >= Action.SWITCH_OFFSET:
            # team2 switches, then team1 attacks
            # TODO: account for Pursuit
            team2.curpkmn = actions[1] - Action.SWITCH_OFFSET
            team2.pkmn[team2.curpkmn] = attack(team1.get_cur_pkmn(), team2.get_cur_pkmn(), actions[0])
            if team2.get_cur_pkmn().curhp == 0:
                # TODO: Implement proper switching
                team2.curpkmn = team2.get_next_pkmn()

        else: # both teams attack
            t1p = team1.get_cur_pkmn()
            t2p = team2.get_cur_pkmn()

            if t1p.moves[actions[0]].priority < t2p.moves[actions[1]].priority:
                team1, team2 = self.team2_attacks_first(team1, team2, actions)
            elif t1p.moves[actions[0]].priority > t2p.moves[actions[1]].priority:
                team1, team2 = self.team1_attacks_first(team1, team2, actions)
            else:
                if t1p.spd > t2p.spd:
                    team1, team2 = self.team1_attacks_first(team1, team2, actions)
                elif t1p.spd < t2p.spd:
                    team1, team2 = self.team2_attacks_first(team1, team2, actions)
                else:
                    # speed tie; assume team2 always wins
                    # TODO: change this to a coin flip with 50% chances
                    team1, team2 = self.team2_attacks_first(team1, team2, actions)
                
        return PkmnState(team1, team2)

    def team1_attacks_first(self, team1, team2, actions):
        t1p = team1.get_cur_pkmn()
        t2p = team2.get_cur_pkmn()

        team2.pkmn[team2.curpkmn] = attack(t1p, t2p, actions[0])
        if t2p.curhp == 0:
            # TODO: Implement proper switching
            team2.curpkmn = team2.get_next_pkmn()
        else:
            team1.pkmn[team1.curpkmn] = attack(t2p, t1p, actions[1], True)
            team1.curpkmn = team1.get_next_pkmn() if t1p.curhp == 0 else team1.curpkmn
        return (team1, team2)
    
    def team2_attacks_first(self, team1, team2, actions):
        t1p = team1.get_cur_pkmn()
        t2p = team2.get_cur_pkmn()

        team1.pkmn[team1.curpkmn] = attack(t2p, t1p, actions[1], True)
        if t1p.curhp == 0:
            # TODO: Implement proper switching
            team1.curpkmn = team1.get_next_pkmn()
        else:
            team2.pkmn[team2.curpkmn] = attack(t1p, t2p, actions[0])
            team2.curpkmn = team2.get_next_pkmn() if t2p.curhp == 0 else team2.curpkmn
        return (team1, team2)

    def value(self):
        """Returns the normalized value of the state.
        
        Closer to +1 == team1 closer to winning
        Closer to -1 == team2 closer to winning
        """
        #import pdb; pdb.set_trace()
        return ((self.team1.get_cur_hp() / self.team1.get_total_hp()) - 
                (self.team2.get_cur_hp() / self.team2.get_total_hp()))

    def __str__(self):
        return 'Team1: %s\nTeam2:%s' % (str(self.team1), str(self.team2))

    def is_goal(self):
        """
        Returns 1 if team1 wins, returns -1 if team2 wins, 0 otherwise.
        """
        if self.team1.get_cur_hp() == 0:
            return 1
        elif self.team2.get_cur_hp() == 0:
            return -1
        else:
            return 0


class SearchNode():
    def __init__(self, init_state):
        self.state = init_state
    
    def mutate(self, *actions):
        s = SearchNode(self.state.mutate(actions), self.is_goal)
        return s

    def get_next_action(self):
        build_game_tree(self)

        if CONF['debug_level'] >= 1:
            print('Current State: ' + str(self))
            for c in self.children:
                print('Team1 Move: %s,\nTeam2 Move: %s,\nNew State Value: %f,\nNew State {\n%s\n}' % (
                    Action.to_str(c[0]), 
                    Action.to_str(c[1]), 
                    c[2].worst_child_val,
                    str(c[2])))

        # choose an action: get the worst value from each possible action of the opponent and group
        # it by move. Then, choose the move with the highest value.
        worst_actions_group_by_a = []
        for a in Action.get_all():
            l = []
            for c in self.children:
                if c[0] == a:
                    l.append((c[2].state.value(), c[2].state))
            worst_actions_group_by_a.append(
                min([c[0] for c in l]) if l else -1.0
            )

        best_action = 0
        max_val = worst_actions_group_by_a[0]

        for i in range(1, len(worst_actions_group_by_a)):
            if max_val < worst_actions_group_by_a[i]:
                best_action = i
                max_val = worst_actions_group_by_a[i]

        return best_action

    def get_min_val_state(states):
        if len(states) > 0:
            min_val = states[0].value()
            min_index = 0
            for i in range(1, len(states)):
                if states[i].value() < min_val:
                    min_val = states[i].value()
                    min_index = i
        return min_val
                
    def is_goal(self):
        return self.state.is_goal()

    def __str__(self):
        return str(self.state)


def build_game_tree(root, depth=0):
    root.children = []
    if root.is_goal():
        root.worst_child_val = root.is_goal()
        root.best_child_val = root.is_goal()
        root.avg_child_val = root.is_goal()

    else:
        if depth < CONF['max_depth']:
            for a, b, s in root.state.get_sucessors():
                new_node = SearchNode(s)
                build_game_tree(new_node, depth + 1)
                root.children.append((a, b, new_node))
            
            root.worst_child_val = min([c[2].worst_child_val for c in root.children])
            root.best_child_val = max([c[2].best_child_val for c in root.children])
            l = [c[2].avg_child_val for c in root.children]
            root.avg_child_val = sum(l, 0.0) / len(l)
        else:
            root.worst_child_val = root.state.value()
            root.best_child_val = root.state.value()
            root.avg_child_val = root.state.value()
    
    if CONF['debug_level'] >= 2:
        print("Depth: %d" % (depth))
        print(str(root))
        print(root.best_child_val)
        print(root.worst_child_val)
        print(root.avg_child_val)
        print(); print()


