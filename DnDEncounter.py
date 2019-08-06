import random

class Character(): #character class for the player and enemy


    #player has a name, health, defense, strength, and weapon
    def __init__(self, name='joedoe', health=10, defense=10, strength=10, weapon="sword"):
        weapon_cache = {"sword": "1d8", "axe": "1d12", "dagger":"1d4"}
        #weapons available for player to use = keywords for damage out        

        self.name = name
        self.health = int(health)
        self.defense = int(defense)
        self.strength = int(strength)
        self.strengthmod = ((self.strength-10)//2) #going by dnd strength modifer (score - 10)/2 round down
        self.weapon = weapon.lower()  #take in integers, lower case words
        self.weapondie = weapon_cache[self.weapon] #assign a weapon die to the player for damage


        #print out the stats of the fighter
    def __str__(self):
        return "\n The Fighter's Name is {}, their Health is {}, their defense is {}, their strength is {}, and their weapon is the {}".format(self.name, self.health, self.defense, self.strength, self.weapon)
    
        #retrieves health to allow for comparison to 'death' or zero.
    @property
    def gethealth(self):
        health = self.health
        return int(health)

        #how the player damages something according to weapon
    def weapon_damage(self):
        if  self.weapondie == "1d8":
            y = random.randint(1,8) + self.strengthmod 
            return y

        if self.weapondie == "1d12":
            y = random.randint(1,12) + self.strengthmod + self.strengthmod//2 #axe gives you 1.5 strength mod
            return y

        if self.weapondie == "1d8":
            y = random.randint(1,4) + self.strengthmod
            return y

    def weapon_attack(self, enemy_defense): #pass in the enemies defense character.defense

        enemydef = int(enemy_defense)
        d20 = random.randint(1,20)
        attack = d20 + (self.strengthmod) #going by dnd strength modifer (score - 10)/2 round down
        #sword does a d12 of damage, has a 2x critical on a 19-20 only
        if self.weapon == "sword":
            if d20 == 20:
                print("{} rolled a {} -- Critical Hit!".format(self.name, d20))  #value rolled for the sake of troubleshoot and visiibility
                return int(self.weapon_damage() + self.weapon_damage()) #2x multipler on 19-20

            elif attack >= enemydef and d20 == 19:  #2x multiplier on 19-20
                print("{} rolled a {} -- Critical Hit!".format(self.name, d20)) 
                return int(self.weapon_damage() + self.weapon_damage())

            elif attack >= enemydef:  #regular hit
                print("{} rolled a {} -- Hit!".format(self.name, d20)) 
                return int(self.weapon_damage())

            else: #miss
                print("{} rolled a {} -- Miss!".format(self.name, d20)) 


        #axe does a d12 of damage, has a 3x critical on a 20 only
        if self.weapon == "axe":
            if d20 == 20:
                print("{} rolled a {} -- Critical Hit!".format(self.name, d20))  #value rolled for the sake of troubleshoot and visiibility
                return int(self.weapon_damage() + self.weapon_damage() + self.weapon_damage()) #3x multipler on 20

            elif attack >= enemydef:  #regular hit
                print("{} rolled a {} -- Hit!".format(self.name, d20)) 
                return int(self.weapon_damage())

            else: #miss
                print("{} rolled a {} -- Miss!".format(self.name, d20))


        #dagger does a d4 of damage, has a 2x critical on a 17 - 20        
        if self.weapon == "dagger":
            if d20 == 20:
                print("{} rolled a {} -- Critical Hit!".format(self.name, d20))  #value rolled for the sake of troubleshoot and visiibility
                return int(self.weapon_damage() + self.weapon_damage()) #2x multipler on 17-20

            elif attack >= enemydef and d20 >= 17:  #2x multiplier on 17-20    
                print("{} rolled a {} -- Critical Hit!".format(self.name, d20)) 
                return int(self.weapon_damage() + self.weapon_damage())

            elif attack >= enemydef:  #regular hit
                print("{} rolled a {} -- Hit!".format(self.name, d20)) 
                return int(self.weapon_damage())

            else: #miss
                print("{} rolled a {} -- Miss!".format(self.name, d20)) 
                
    def i_attack(self, enemy_health, enemy_defense):
        enemyhealth = int(enemy_health) #cast the enemy health from a string to an int
        damagedone = self.weapon_attack(enemy_defense) #cast the enemy defense from a string to an int
        if damagedone == None: #cast the enemy defense from a string to an int
            print("Next Turn")
            return enemyhealth
        damagedone = int(damagedone)
        damagedhealth = enemyhealth - damagedone
        print("{} did {} damage!  Enemy health now at {}...Next Turn!".format(self.name, damagedone, damagedhealth))
        if(damagedhealth < 0):
            print("The Enemy has Collapsed!")
        return damagedhealth


    #
    #def i_attack(self, enemy_health, enemy_defense):    
     #   try:
      #      damagedone = int(self.weapon_attack(enemy_defense))
       #     damagedhealth = enemy_health - damagedone
        #    print("{} did {} damage!  Enemy health now at {}...Next Turn!".format(self.name, damagedone, damagedhealth))
         #   if(damagedhealth < 0):
           #     print("The Enemy has Collapsed!")
          #  return damagedhealth
        #except:
         #   print("Next Turn")```


            #lets start a fight
fighter1 = Character()
fighter2 = Character()  #create the fighters

#player inputs the figthers attributes
fighter1.name = input("Pick Fighter1's name:")
fighter1.health = input("Set Fighter1's health:")
fighter1.defense = input("Set Fighter1's defense:")
fighter1.strength = input("Set Fighter1's strength:")
fighter1.weapon = input("Pick Fighter1's weapon (sword, dagger, or axe):")

print(fighter1) #check the attributes


fighter2.name = input("Pick Fighter2's name:")
fighter2.health = input("Set Fighter2's health:")
fighter2.defense = input("Set Fighter2's defense:")
fighter2.strength = input("Set Fighter2's strength:")
fighter2.weapon = input("Pick Fighter2's weapon (sword, dagger, or axe):")

print(fighter2)  #check attributes

input("Ready to fight?")

fighter1.health = fighter2.i_attack(fighter1.health, fighter1.defense)
input()
fighter2.health = fighter1.i_attack(fighter2.health, fighter2.defense)
input()
fighter1.health = fighter2.i_attack(fighter1.health, fighter1.defense)
input()
fighter2.health = fighter1.i_attack(fighter2.health, fighter2.defense)
input()
fighter1.health = fighter2.i_attack(fighter1.health, fighter1.defense)
input()
fighter2.health = fighter1.i_attack(fighter2.health, fighter2.defense)
input()
fighter1.health = fighter2.i_attack(fighter1.health, fighter1.defense)
input()
fighter2.health = fighter1.i_attack(fighter2.health, fighter2.defense)
input()

