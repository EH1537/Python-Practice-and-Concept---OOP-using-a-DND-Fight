
import random
from collections import defaultdict

class DieRoll:
    # takes as input an arbitrary number of the following two types of inputs:
    #    - int : 1 die roll of a die with this number of sides
    #    - tuple : (N,S) where N is the number of S-sided dice to roll
    # the value property performs a new roll each time it is accessed. It will
    # return the sum of all of the specified dice.
    def __init__(self,*dice):
        # a mapping with:
        #    key = number of sides on the die (or S)
        #    value = number of these dice to roll (or N)
        self.dice = defaultdict(int)
        for d in dice:
            if type(d) == int:
                N = 1
                S = d
            elif type(d) == tuple:
                N,S = d # expand the tuple into N (# of dice) and S (# of sides per die)
            
            # some basic sanity checking
            else:
                raise Exception("Only int or tuple are accepted as die values (got {})".format(type(d)))
            if N<0:
                raise Exception("cannot roll negative dice (got {})".format(N))
            if S<1:
                raise Exception("cannot roll a {}-sided die".format(S))
            self.dice[S] += N
    
    @property
    def value(self):
        ret = 0
        # todo: optimize this for large numbers of dice using numpy. Right now
        #       its time complexity is O(N) in the number of dice, and it can
        #       potentially be much lower.
        for S,N in self.dice.items():
            for i in range(N):
                ret += random.randint(1,S)
        return ret


class Character:
    
    # set this as a class attribute because it does not hold state
    d20 = DieRoll(20)
    
    damage_by_weapon = {
        "sword" : DieRoll(8),
        "axe" : DieRoll(12),
        "dagger" : DieRoll(4)
    }
    
    critical_multiplier_by_weapon = {
        # key: d20 roll outcome
        # value: damage multiplier
        "sword" : {
            19 : 2,
            20 : 2
        } ,
        "axe" : {
            20 : 3
        } ,
        "dagger" : {
            17 : 2,
            18 : 2,
            19 : 2,
            20 : 2
        }
    }
    
    def __init__(self, name='joedoe', health=10, defense=10, strength=10, weapon="sword"):
        self.name = name
        
        self.health = int(health)
        self.defense = int(defense)
        self.strength = int(strength)
        
        self.weapon = weapon.lower()  #take in integers, lower case words
    
    # protip: almost always use __repr__ instead of __str__. __str__ only works for the str()
    # function, while __repr__ works in format strings, etc.
    def __repr__(self):
        return "\n The Fighter's Name is {}, their Health is {}, their defense is {}, their strength is {}, and their weapon is the {}".format(self.name, self.health, self.defense, self.strength, self.weapon)
    
    @property
    def weapondie(self):
        return self.damage_by_weapon[self.weapon] #assign a weapon die to the player for damage
    
    @property
    def strengthmod(self):
        ret = ((self.strength-10)//2) #going by dnd strength modifer (score - 10)/2 round down
        if self.weapon == "axe":
            return ret + ret//2  #axe gives you 1.5 strength mod
        return ret
    
    @property
    def dead(self):
        return self.health<=0 or self.strength<=0 # not sure about defense
    
    @property
    def weapon_damage(self):
        return self.weapondie.value + self.strengthmod
    
    # returns the critical-hit multiplier if there is one, otherwise returns 1
    def critical_multiplier(self, d20):
        if d20 in self.critical_multiplier_by_weapon[self.weapon]:
            return self.critical_multiplier_by_weapon[self.weapon][d20]
        return 1
    
    def weapon_attack(self, enemy_defense):
        attackroll = self.d20.value
        multiplier = self.critical_multiplier(attackroll)
        
        damage = self.weapon_damage

        if attackroll < enemy_defense:
            return 0 # miss, no damage dealt
        
        if multiplier > 1:
            print("{} landed a Critical Hit!".format(self.name))

        return damage * multiplier
    
    def i_attack(self, enemy):
        damagedone = self.weapon_attack(enemy.defense)
        enemy.health -= damagedone
        return damagedone


            #lets start a fight
fighter1 = Character()
fighter2 = Character()  #create the fighters

# a mapping of input attributes to collect, and their types.
input_attributes = {
    "name" : str,
    "health" : int,
    "defense" : int,
    "strength" : int,
    "weapon" : str
}

while True:
    for fighter in [fighter1,fighter2]:
        print("Making a new fighter.")
        for attr,attr_type in input_attributes.items():
            ask_str = attr
            if attr == "weapon": # special case for the weapon
                ask_str += " (sword, dagger, or axe)"
            setattr(fighter,attr,attr_type(input("Pick fighter's {}:".format(ask_str))))
        print()

    print("these are your fighters:")
    print(fighter1,fighter2)
    print()
    if input("OK? (y/n)").lower() == "y":
        break

fighter1_initiative = fighter2_initiative = 0
while fighter1_initiative == fighter2_initiative:
    fighter1_initiative = DieRoll(20).value
    fighter2_initiative = DieRoll(20).value
first = fighter1 if fighter1_initiative > fighter2_initiative else fighter2

print("{} won the initiative roll ({} vs {}).".format(first.name,fighter1_initiative,fighter2_initiative))

attacker = first
defender = fighter2 if first is fighter1 else fighter1
while True:
    print("{} attacks...".format(attacker.name))
    damagedone = attacker.i_attack(defender)
    if not damagedone:
        print("Miss!")
    else:
        print("Hit! {} deals {} damage to {}.".format(attacker.name,damagedone,defender.name))
    if defender.dead:
        break
    _attacker = attacker # save the attacker to swap attacker and defender
    attacker = defender
    defender = _attacker

print("Battle over! {} has defeated {}.".format(attacker.name,defender.name))