#!/bin/python3


from teams import ally_team
from teams import enemy_team
from ai import SearchNode
from ai import PkmnState
from pokemon import Action
from config import CONF
import random
import re


def ai_get_enemy_action(game_tree):
    raise NotImplementedError('Computer-Controlled playing not ready yet. Please try the "user-controlled" or "random" setting.')


def random_get_enemy_action(game_tree):
    valid_actions = []
    for a in Action.get_all():
        if game_tree.state.is_action_valid(a, game_tree.state.team2):
            valid_actions.append(a)
    return random.choice(valid_actions)


def uc_get_enemy_action(game_tree):
    accept_action = False
    while not accept_action:
        s = input('Please enter an action for Team2 (enter h for help): ')
        if s == 'h' or s == 'help':
            print('Help:')
            print('move#: the move you wish to select, #={1[2,3,4]}*')
            print('switch#: the switch you wish to make, #={[1,2,3,4,5,6]}*')
            print('*brackets denote that moves may be invalid')

        elif len(s) == 5 and s[0:4] == 'move':
            try:
                b = int(s[4]) - 1 # don't delete this! we need to return something
            except:
                pass
            else:
                accept_action = game_tree.state.is_action_valid(b, game_tree.state.team2)
            #TODO: query for modifiers (e.g. crit, effects, etc.)
            
        elif len(s) == 7 and s[0:6] == 'switch':
            try:
                b = int(s[6]) - 1 + Action.SWITCH_OFFSET # don't delete this! we need to return something
            except:
                pass
            else:
                accept_action = game_tree.state.is_action_valid(b, game_tree.state.team2)
            #TODO: query for modifiers
        else:
            print('Invalid command. Please try again.')
            if CONF['debug_level'] >= 1:
                print(len(s))
                print(s[0:3])
    return b


if __name__ == '__main__':
    if 'enemy_config' in CONF:
        if CONF['enemy_config'] == 'computer-controlled' or CONF['enemy_config'] == 'ai':
            get_enemy_action = ai_get_enemy_action
        elif CONF['enemy_config'] == 'random':
            get_enemy_action = random_get_enemy_action
        else:
            # This is supposed to be a "battle aid" and not a simulator,
            # so user-control should be the default
            get_enemy_action = uc_get_enemy_action
    else:
        get_enemy_action = uc_get_enemy_action

    # main loop
    game_state = PkmnState(ally_team, enemy_team, True)
    while True:
        print("Current State: \n%s" % str(game_state))
        game_tree = SearchNode(game_state)
        if game_tree.is_goal() == 1:
            print('The enemy team wins!')
            break
        elif game_tree.is_goal() == -1:
            print('The ally team wins!')
            break

        a = game_tree.get_next_action()
        print('Best action for Team 1: %s' % Action.to_str(a))
        b = get_enemy_action(game_tree) 

        game_state = game_state.mutate(a, b)
        
    if CONF['debug_level'] >= 1:
        print('yay!')
