from copy import deepcopy
from math import floor
import pdb

class Action():
    MOVE1 = 0
    MOVE2 = 1
    MOVE3 = 2
    MOVE4 = 3
    SWITCH1 = 4
    SWITCH2 = 5
    SWITCH3 = 6
    SWITCH4 = 7
    SWITCH5 = 8
    SWITCH6 = 9

    SWITCH_OFFSET = 4
    ACTION_COUNT = 10

    @staticmethod
    def get_all():
        return range(10)

    @staticmethod
    def to_str(val):
        if not (type(val) is int):
            return ''

        l = ['MOVE1', 
             'MOVE2',
             'MOVE3',
             'MOVE4',
             'SWITCH1',
             'SWITCH2',
             'SWITCH3',
             'SWITCH4',
             'SWITCH5',
             'SWITCH6'
        ]
        return l[val]


class Type():
    NORMAL = 0
    FIRE = 1
    WATER = 2
    ELECTRIC = 3
    GRASS = 4
    ICE = 5
    FIGHTING = 6
    POISON = 7
    GROUND = 8
    FLYING = 9
    PSYCHIC = 10
    BUG = 11
    ROCK = 12
    GHOST = 13
    DRAGON = 14
    DARK = 15
    STEEL = 16
    
    type_matchup = [                                                                           #atk 
#def     nrm  fir  wat  ele  grs  ice  fgh  psn  gnd  fly  psy  bug  rck  ght  drg  drk  stl    
        [  1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 0.5,   0,   1,   1, 0.5], #normal
        [  1, 0.5, 0.5,   1,   2,   2,   1,   1,   1,   1,   1,   2, 0.5,   1, 0.5,   1,   2], #fire
        [  1,   2, 0.5,   1, 0.5,   1,   1,   1,   2,   1,   1,   1,   2,   1, 0.5,   1,   1], #water
        [  1,   1,   2, 0.5, 0.5,   1,   1,   1,   0,   2,   1,   1,   1,   1, 0.5,   1,   1], #electric
        [  1, 0.5,   2,   1, 0.5,   1,   1, 0.5,   2, 0.5,   1, 0.5,   2,   1, 0.5,   1, 0.5], #grass
        [  1, 0.5, 0.5,   1,   2, 0.5,   1,   1,   2,   2,   1,   1,   1,   1,   2,   1, 0.5], #ice
        [  2,   1,   1,   1,   1,   2,   1, 0.5,   1, 0.5, 0.5, 0.5,   2,   0,   1,   2,   2], #fighting
        [  1,   1,   1,   1,   2,   1,   1, 0.5, 0.5,   1,   1,   1, 0.5, 0.5,   1,   1,   0], #poison
        [  1,   2,   1,   2, 0.5,   1,   1,   2,   1,   0,   1, 0.5,   2,   1,   1,   1,   2], #ground
        [  1,   1,   1, 0.5,   2,   1,   2,   1,   1,   1,   1,   2, 0.5,   1,   1,   1, 0.5], #flying
        [  1,   1,   1,   1,   1,   1,   2,   2,   1,   1, 0.5,   1,   1,   1,   1,   0, 0.5], #psychic
        [  1, 0.5,   1,   1,   2,   1, 0.5, 0.5,   1, 0.5,   2,   1,   1, 0.5,   1,   2, 0.5], #bug
        [  1,   2,   1,   1,   1,   2, 0.5,   1, 0.5,   2,   1,   2,   1,   1,   1,   1, 0.5], #rock
        [  0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   1,   1,   2,   1, 0.5, 0.5], #ghost
        [  1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   1, 0.5], #dragon
        [  1,   1,   1,   1,   1,   1, 0.5,   1,   1,   1,   2,   1,   1,   2,   1, 0.5, 0.5], #dark
        [  1, 0.5, 0.5, 0.5,   1,   2,   1,   1,   1,   1,   1,   1,   2,   1,   1,   1, 0.5], #steel
    ]

    type_names = [
        'NORMAL', 
        'FIRE',
        'WATER',
        'ELECTRIC',
        'GRASS',
        'ICE',
        'FIGHTING',
        'POISON',
        'GROUND',
        'FLYING',
        'PSYCHIC',
        'BUG',
        'ROCK',
        'GHOST',
        'DRAGON',
        'DARK',
        'STEEL'
     ]

    @staticmethod
    def get_type_multiplier(atk_type, def_type1, def_type2):
        mul = Type.type_matchup[atk_type][def_type1]
        mul = mul * Type.type_matchup[atk_type][def_type2] if def_type2 is not None else mul
        return mul

    @staticmethod
    def to_str(val):
        if not (type(val) is int):
            return ''

        return Type.type_names[val]


class Pokemon():
    def __init__(self, name, type1, type2, ability, gender, 
                 lvl, hp, atk, defn, spatk, spdefn, spd, *moves):
        if len(moves) > 0:
            self.name = name
            self.type1 = type1
            self.type2 = type2

            self.lvl = lvl
            self.ability = ability
            self.curhp = hp
            self.maxhp = hp
            self.atk = atk
            self.defn = defn
            self.spatk = spatk
            self.spdefn = spdefn
            self.spd = spd
            self.stat_mod = {'atk': 0, 'defn':0, 'spatk':0, 'spdefn':0, 'spd':0}

            if len(moves) < 4:
                self.moves = []
                for m in moves:
                    self.moves.append(deepcopy(m))

            else:
                for i in range(4):
                    self.moves.append(deepcopy(moves[i]))
        else:
            raise RuntimeException('Need six stats and at least one move for a pokemon')


    def __str__(self):
        s =  'Pkmn(%s, %d/%d,\n' % (self.name, self.curhp, self.maxhp)
        for m in self.moves:
            s += '\t' + str(m) + ',\n'
        return s + ')'


class Move():
    def __init__(self, name, type, bp, maxpp, is_special, accuracy=100, priority=0, effect=None):
        self.name = name
        self.type = type
        self.bp = bp
        self.maxpp = maxpp
        self.curpp = maxpp
        self.is_special = is_special
        self.accuracy = accuracy
        self.priority = priority
        self.effect = effect

    def __str__(self):
        return 'Move(%s, %s, %d/%d)' % (self.name, Type.to_str(self.type), self.curpp, self.maxpp)


class Team():
    def __init__(self, *pkmn):
        self.curpkmn = 0
        self.pkmn = list(pkmn)
    
    def get_cur_hp(self):
        return sum([p.curhp for p in self.pkmn])

    def get_total_hp(self):
        return sum([p.maxhp for p in self.pkmn])

    def get_cur_pkmn(self):
        return self.pkmn[self.curpkmn]

    def get_next_pkmn(self):
        # returns the first non-fainted pokemon; if none, return current Pokemon
        for i in range(len(self.pkmn)):
            if self.pkmn[i].curhp > 0:
                return i
        return self.curpkmn

    def __str__(self):
        s = 'Team('
        for p in self.pkmn:
            if p:
                s = s + str(p) + ', \n'
        return s + ')\n'
            
    # TODO: if deepcopy is too slow / memory inefficient, implement Team.copy()


def attack(atk_pkmn, def_pkmn, move_index, max_damage=False):
    R = 100 if max_damage else 85

    if atk_pkmn.curhp != 0 and atk_pkmn.moves[move_index].curpp > 0:
        if atk_pkmn.moves[move_index].bp > 0:
            dmg = calculate_damage(atk_pkmn, def_pkmn, move_index, R)
        else:
            dmg = 0

        def_pkmn.curhp = 0 if def_pkmn.curhp - dmg <= 0 else def_pkmn.curhp - dmg
        atk_pkmn, def_pkmn = apply_effect(atk_pkmn, def_pkmn, move_index)
        atk_pkmn.moves[move_index].curpp -= 1

    return def_pkmn


def apply_effect(atk_pkmn, def_pkmn, move_index):
    move = atk_pkmn.moves[move_index]
    if move.effect:
        return move.effect(move, atk_pkmn, def_pkmn)
    else:
        return (atk_pkmn, def_pkmn)


def calculate_damage(atk_pkmn, def_pkmn, move_index, R, crit=False,):
    # Using the DPPt (Gen IV) Damage Formula, courtesy 
    # https://www.smogon.com/dp/articles/damage_formula

    move = atk_pkmn.moves[move_index]
    level = atk_pkmn.lvl
    base_power = move.bp
    if move.is_special:
        atk = atk_pkmn.spatk 
        atk = atk * (1 + atk_pkmn.stat_mod['spatk'] * 0.5) if atk_pkmn.stat_mod['spatk'] >= 0 else atk // (1 + atk_pkmn.stat_mod['apatk'] * 0.5)

        defn = def_pkmn.spdefn 
        defn = defn * (1 + def_pkmn.stat_mod['spdefn'] * 0.5) if def_pkmn.stat_mod['spdefn'] >= 0 else defn // (1 + def_pkmn.stat_mod['spdefn'] * 0.5)

    else:
        atk = atk_pkmn.atk 
        atk = floor(atk * (1 + atk_pkmn.stat_mod['atk'] * 0.5) if atk_pkmn.stat_mod['atk'] >= 0 else atk / (1 - atk_pkmn.stat_mod['atk'] * 0.5))

        defn = def_pkmn.defn
        defn = floor(defn * (1 + def_pkmn.stat_mod['defn'] * 0.5) if def_pkmn.stat_mod['defn'] >= 0 else defn / (1 - def_pkmn.stat_mod['defn'] * 0.5))

    ch = 2 if crit else 1
    stab = 1.5 if move.type == atk_pkmn.type1 or move.type == atk_pkmn.type2 else 1
    type_mul = Type.get_type_multiplier(move.type, def_pkmn.type1, def_pkmn.type2)

    # TODO: implement these mod factors
    # IMO, this will be one of the hardest things to do because of the number of possibilities
    mod1 = 1 # eww
    mod2 = 1 # eww
    mod3 = 1 # eww
    
    
    # CRITICAL: MAKE SURE ALL OPERATIONS RESULT IN A ROUNDED-DOWN WHOLE NUMBER
    return floor(floor(floor((floor((floor(
        ((((level * 2 // 5) + 2) * base_power * atk // 50) // defn) * mod1) + 2) * 
        ch * mod2) *  R // 100) * stab) * type_mul) * mod3)
