from pokemon import Pokemon
from pokemon import Type
from pokemon import Move
from pokemon import Team

ally_team = Team(
    Pokemon('Charmander', Type.FIRE, None, 'Blaze', 'Male',
            5, 20, 11, 10, 12, 11, 13,
            Move('Scratch', Type.NORMAL, 40, 35, False),
            Move('Growl', Type.NORMAL, 0, 40, False)),
    Pokemon('Charmander', Type.FIRE, None, 'Blaze', 'Male',
            5, 20, 11, 10, 12, 11, 13,
            Move('Scratch', Type.NORMAL, 40, 35, False),
            Move('Growl', Type.NORMAL, 0, 40, False)),
)

enemy_team = Team(
    Pokemon('Squirtle', Type.WATER, None, 'Torrent', 'Male',
            5, 20, 11, 13, 11, 12, 10,
            Move('Tackle', Type.NORMAL, 35, 35, False, 95),
            Move('Tail Whip', Type.NORMAL, 0, 40, False)),
    Pokemon('Squirtle', Type.WATER, None, 'Torrent', 'Male',
            5, 20, 11, 13, 11, 12, 10,
            Move('Tackle', Type.NORMAL, 35, 35, False, 95),
            Move('Tail Whip', Type.NORMAL, 0, 40, False)),
)
