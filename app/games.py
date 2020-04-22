class Game(object):

    def __init__(self, name, description, rooms, start_room):
        self.name = name
        self.description = description
        self.start_room = start_room
        self.current_room = start_room
        self._rooms = {}
        for room in rooms:
            self._rooms[room.name] = room

    def load_room(self, name):
        return self._rooms[name]

    def name_room(self, room):
        for (key, value) in self._rooms.items():
            if value == room:
                return key
        return None


class Room(object):

    # Possible answer outputs: sentences, output types
    # Types

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}

    def go(self, direction):
        if direction in self.paths:
            return self.paths.get(direction, None)
        else:
            return self.paths.get('*', None)

    def add_paths(self, paths):
        self.paths.update(paths)


class Gothon(Game):
    """ Gothon Game """

    central_corridor = Room("Central Corridor",
                            """
    The Gothons of Planet Percal #25 have invaded your ship and destroyed
    your entire crew. You are the last surviving member and your last 
    mission is to get the neutron destruct bomb from the Weapons Armory, put
    it in the bridge, and blow the ship up after getting into an escape pod.

    You're running down the central corridor to the Weapons Armory when a 
    Gothon jumps out, red scaly skin, dark grimy teeth, and evil clown
    costume flowing around his hate filled body. He's blocking the door to
    the Armory and about to pull a weapon to blast you.
    """)

    laser_weapon_armory = Room("Laser Weapon Armory",
                               """
    Lucky for you they made you learn Gothon insults in the academy. You
    tell the one Gothon joke you know: Lbhe zbgure vf fb sng, jura fur fvgf
    nebhaq gur ubhfr, fur fvgf nebhaq gur ubhfr. The Gothon stops, tries
    not to laugh, then busts out laughing and can't move. While he's
    laughing you run up and shoot him square in the head putting him down,
    then jump through the Weapon Armory door.

    You do a dive roll into the Weapon Armory, crouch and scan the room for
    more Gothons that might be hiding. It's dead quiet, too quiet. You
    stand up and run to the far side of the room and find the neutron bomb
    in its container. There's a keypad lock on the box and you need the
    code to get the bomb out. If you get the code wrong 10 times then the 
    lock closes forever and you can't get the bomb. The code is 3 digits.
    """
                               )

    the_bridge = Room("The Bridge",
                      """
    The container clicks open and the seal breaks, letting gas out. You 
    grab the neutron bomb and run as fast as you can to the bridge where 
    you must place it in the right spot.

    Your burst onto the Bridge with the neutron destruct bomb under your arm
    and surprise 5 Gothons who are trying to take control of  the ship. Each
    of them has an even uglier clown costume than the last. They haven't
    pulled their weapons out yet, as they see the active bomb under your arm
    and don't want to set it off.
    """)

    escape_pod = Room("Escape Pod",
                      """
    You point your blaster at the bomb under your arm and the Gothons put
    their hands up and start to sweat. You inch backward to the door, open
    it, and then carefully place the bomb on the floor, pointing your
    blaster at it. You then jump back through the door, punch the close
    button and blast the lock so the Gothons can't get out. Now that the
    bomb is placed you run to the escape pod to get off this tin can.

    You rush through the ship desperately trying to make it to the escape
    pod before the whole ship explodes. It seems like hardly and Gothons
    are on the ship, so your run is clear of interference. You get to the
    chamber with the escape pods, and now need to pick one to take. Some of
    them could be damaged but you don't have time to look. There's 5 pods,
    which one do you take?
    """)

    the_end_winner = Room("The End",
                          """
    You jump into pod 2 and hit the eject button. The pod easily slides out
    into space heading to the planet below. As it flies to the planet, you
    look back and see your ship implode then explode like a bright star,
    taking out the Gothon ship at the same time. You won!
    """)

    the_end_loser = Room("The End",
                         """
    You jump into a random pod and hit the eject button. The pod escapes 
    out into the void of space, then implodes as the hull ruptures, crushing
    your body into jam jelly.
    """)

    generic_death = Room("death", "You died.")

    escape_pod.add_paths({
        '2': the_end_winner,
        '*': the_end_loser
    })

    the_bridge.add_paths({
        'throw the bomb': generic_death,
        'slowly place the bomb': escape_pod
    })

    laser_weapon_armory.add_paths({
        '0132': the_bridge,
        '*': generic_death
    })

    central_corridor.add_paths({
        'shoot!': generic_death,
        'dodge!': generic_death,
        'tell a joke': laser_weapon_armory
    })

    def __init__(self):
        super().__init__(
            'gothon',
            'Escape from planet Gothon!',
            [
                self.central_corridor,
                self.laser_weapon_armory,
                self.the_bridge,
                self.escape_pod,
                self.the_end_winner,
                self.the_end_loser,
                self.generic_death
            ],
            self.central_corridor)


class RiddleMaster(Game):
    """ Riddle Master Game """

    easy_guys_go = Room("Easy Guys, Go!",
                        "What has to be broken before you can use it?")

    son_name = Room("Son name",
                    "David’s parents have three sons: Snap, Crackle, and what’s the name of the third son?")

    car_people = Room("How tight is this car... hmmpf",
                      "One grandfather, two fathers, two sons, and one grandson enter in a car. How many people are in the car?")

    the_end_winner = Room("The End",
                          """
    Congratulations! You are a riddle master after all!
    """)

    the_end_loser = Room("The End",
                         """
    Unfortunately, you are not a riddle master. Come later after you rest in that furniture that has one head, one foot and four legs...
    """)

    easy_guys_go.add_paths({
        'egg': son_name,
        '*': the_end_loser,
    })

    son_name.add_paths({
        'david': car_people,
        '*': the_end_loser,
    })

    car_people.add_paths({
        '3': the_end_winner,
        'three': the_end_winner,
        '*': the_end_loser,
    })

    def __init__(self):
        super().__init__(
            'Riddle Master',
            'What have I got in my pocket?! (Bagins, Bilbo)',
            [
                self.easy_guys_go, 
                self.son_name, 
                self.car_people,
                self.the_end_winner, 
                self.the_end_loser,
            ],
            self.easy_guys_go)


gothon = Gothon()
riddlemaster = RiddleMaster()

available_games = {
    'gothon': gothon,
    'riddlemaster': riddlemaster
}
