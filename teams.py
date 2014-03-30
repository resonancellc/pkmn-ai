from pokemon import Pokemon
from pokemon import Type
from pokemon import Move
from pokemon import Team


def growl_effect(move, atk_pkmn, def_pkmn):
    def_pkmn.stat_mod['atk'] -= 1
    return (atk_pkmn, def_pkmn)


def tail_whip_effect(move, atk_pkmn, def_pkmn):
    def_pkmn.stat_mod['defn'] -= 1
    return (atk_pkmn, def_pkmn)


ally_team = Team(
    Pokemon('Charmander', Type.FIRE, None, 'Blaze', 'Male',
            5, 20, 11, 10, 12, 11, 13,
            Move('Scratch', Type.NORMAL, 40, 35, False),
            Move('Growl', Type.NORMAL, 0, 40, False, 100, 0, growl_effect)),
    Pokemon('Charmander', Type.FIRE, None, 'Blaze', 'Male',
            5, 20, 11, 10, 12, 11, 13,
            Move('Scratch', Type.NORMAL, 40, 35, False),
            Move('Growl', Type.NORMAL, 0, 40, False, 100, 0, growl_effect)),
)

enemy_team = Team(
    Pokemon('Squirtle', Type.WATER, None, 'Torrent', 'Male',
            5, 20, 11, 13, 11, 12, 10,
            Move('Tackle', Type.NORMAL, 35, 35, False, 95),
            Move('Tail Whip', Type.NORMAL, 0, 40, False, 100, 0, tail_whip_effect)),
    Pokemon('Squirtle', Type.WATER, None, 'Torrent', 'Male',
            5, 20, 11, 13, 11, 12, 10,
            Move('Tackle', Type.NORMAL, 35, 35, False, 95),
            Move('Tail Whip', Type.NORMAL, 0, 40, False, 100, 0, tail_whip_effect)),
)



