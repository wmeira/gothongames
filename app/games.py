class Room(object):
    """
    Room phase of a game

    Paths options:
        *: path to an unexpected (or wrong) answer
        -: path after maximum number of errors
        string: path to given action string (must be exact)


    The end room should be named as: "The End", "Game Over",
    "Quiz End" or "You died"
    """

    _stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again',
                  'there', 'about', 'once', 'during', 'out', 'very', 'having',
                  'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do',
                  'yours', 'such', 'into', 'of', 'most', 'itself', 'other',
                  'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him',
                  'each', 'the', 'themselves', 'until', 'below', 'are', 'we',
                  'these', 'your', 'his', 'through', 'don', 'at', 'me', 'were',
                  'her', 'more', 'himself', 'this', 'down', 'should', 'our',
                  'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had',
                  'she', 'all', 'no', 'when', 'nor', 'any', 'before', 'them',
                  'same', 'and', 'been', 'have', 'now', 'will', 'on', 'does',
                  'yourselves', 'then', 'that', 'because', 'what', 'over',
                  'why', 'so', 'can', 'did', 'not', 'in', 'under', 'he', 'its',
                  'you', 'herself', 'has', 'just', 'where', 'too', 'only',
                  'myself', 'which', 'those', 'i', 'after', 'few', 'whom',
                  't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
                  'doing', 'it', 'how', 'further', 'was', 'here', 'than',
                  ]

    # Possible answer outputs: sentences, output types
    # Types

    def __init__(self, name, description,
                 img_file=None, room_type="action", max_errors=10000):
        """

        :param description describes the room to the player
        :param image_file allows an image to complement the description
        :param room_type options are: 'action' (text input) and 'quiz'
            (multiple choices input). When the room type is 'quiz', the paths
            are displayed as radio field options.
        """
        self.name = name
        self.description = description
        self.img_file = img_file
        self.room_type = room_type
        self.max_errors = max_errors
        self.paths = {}

    def is_quiz(self):
        return self.room_type == 'quiz'

    def split_action(self, action):
        if self.is_quiz():
            return [action]
        words = [w.strip().lower()
                 for w in action.split() if w not in self._stopwords]
        return words

    def go(self, action):
        if action is None:
            return self, 0, 'Invalid action...'

        splited_action = self.split_action(action)

        for word in splited_action:
            if word in self.paths:
                return *self.paths.get(action, None), None
        else:
            if self.paths.get('*'):
                return *self.paths.get('*', None), 'You got it wrong...'
            elif self.max_errors <= 1:
                if self.paths.get('-'):
                    return *self.paths['-'], 'You failed (trials limit)...'
                else:
                    return None, 0, 'You failed (trials limit)...'
            else:
                self.max_errors -= 1
        return self, 0, 'Wrong answer.. Try again!'

    def add_paths(self, paths):
        self.paths.update(paths)


class Game(object):
    score = 0
    trials = 0

    generic_end = Room("The End",
                       """<b style='color:red; font-size: 20px'>
                            You failed...
                          </b>
                        """)

    def __init__(self, name, rooms, start_room,
                 show_name=None, description=''):
        self.name = name
        if show_name is None:
            self.show_name = name
        else:
            self.show_name = show_name
        self.description = description
        self.start_room = start_room
        self.current_room = start_room
        self._rooms = self._init_rooms(rooms)

    def _init_rooms(self, rooms):
        dict_rooms = {}
        for room in rooms:
            dict_rooms[room.name] = room
        return dict_rooms

    def _load_room(self, name):
        return self._rooms[name]

    def _name_room(self, room):
        for (key, value) in self._rooms.items():
            if value == room:
                return key
        return None

    def go(self, action):
        new_room, points, message = self.current_room.go(action)
        if new_room is None:
            self.current_room = self.generic_end
        else:
            self.current_room = new_room
        self.score += points
        return self.current_room, message

    def is_game_over(self):
        return self.current_room.name in ['Game Over',
                                          'The End',
                                          'You died',
                                          'Quiz End']

    def calculated_score(self):
        return self.score

    def reset(self):
        self.current_room = self.start_room
        self.score = 0
        self.trials = 0

    def load_current_room(self):
        return load_room(self.current_room)


class Gothon(Game):
    """
    --------------------------------------------------------------------------
    ESCAPE GOTHON

    Game example from "Learn Python 3 the Hard Way" (Zed Shaw)
    --------------------------------------------------------------------------
    """

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
    """, room_type='quiz')

    laser_weapon_armory = Room("Laser Weapon Armory",
                               """
    Lucky for you they made you learn Gothon insults in the academy. You
    tell the one Gothon joke you know: Lbhe zbgure vf fb sng, jura fur fvgf
    nebhaq gur ubhfr, fur fvgf nebhaq gur ubhfr. The Gothon stops, tries
    not to laugh, then busts out laughing 3 times and can't move. While he's
    laughing you run up and shoot him square in the head putting him down,
    then jump through the Weapon Armory door.

    You do a dive roll into the Weapon Armory, crouch and scan the room for
    more Gothons that might be hiding. It's dead quiet, too quiet. You
    stand up and run two the far side of the room and find the neutron bomb
    in its container. There's a keypad lock on the box and you need the
    code to get the bomb out. If you get the code wrong <b>10 times</b> then
    the lock closes forever and you can't get the bomb. The code is <b>3
    digits</b> (interesting leads my be found in the description text, so look
    for numbers...)
    """, room_type='action', max_errors=10)

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
    """, room_type='quiz')

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
    which one do you take? (You have 2 chances)
    """, room_type='action', max_errors=2)

    the_end_winner = Room("The End",
                          """
    You jump into pod 2 and hit the eject button. The pod easily slides out
    into space heading to the planet below. As it flies to the planet, you
    look back and see your ship implode then explode like a bright star,
    taking out the Gothon ship at the same time.
    <b>Congratulations, you won!</b>!
    """)

    the_end_loser = Room("The End",
                         """
    You jump into a random pod and hit the eject button. The pod escapes
    out into the void of space, then implodes as the hull ruptures, crushing
    your body into jam jelly.
    """)

    central_corridor.add_paths({
        'shoot!': (Game.generic_end, 0),
        'dodge!': (Game.generic_end, 0),
        'tell a joke': (laser_weapon_armory, 10)
    })

    laser_weapon_armory.add_paths({
        '132': (the_bridge, 10),
        '-': (Game.generic_end, 0)
    })

    the_bridge.add_paths({
        'throw the bomb': (Game.generic_end, 0),
        'slowly place the bomb': (escape_pod, 10)
    })

    escape_pod.add_paths({
        '2': (the_end_winner, 20),
        '-': (the_end_loser, 0)
    })

    def __init__(self):
        super().__init__(
            name='gothon',
            show_name='Escape Gothon',
            description='Escape from planet Gothon!',
            rooms=[
                self.central_corridor,
                self.laser_weapon_armory,
                self.the_bridge,
                self.escape_pod,
                self.the_end_winner,
                self.the_end_loser,
            ],
            start_room=self.central_corridor)

    def calculated_score(self):
        calculated_score = self.score
        if self.trials >= 15:
            calculated_score -= 15
        else:
            calculated_score -= self.trials
        if calculated_score < 0:
            return 0
        return calculated_score


class RiddleMaster(Game):
    """
    --------------------------------------------------------------------------
    RIDDLE MASTER GAME
    --------------------------------------------------------------------------
    """

    easy_guys_go = Room("Easy Guys, Go!",
                        "<b>What has to be broken before you can use it?</b>",
                        room_type="action",
                        max_errors=10)

    son_name = Room("Son name",
                    """<b>David’s parents have three sons: Snap, Crackle, and
                        what’s the name of the third son?</b>""",
                    room_type="action",
                    max_errors=10)

    car_people = Room("How tight is this car... hmmpf",
                      """
                      One grandfather, two fathers, two sons, and one grandson
                      enter in a car. How many people are in the car?
                      """,
                      room_type="action",
                      max_errors=10)

    the_end_winner = Room("The End",
                          """Congratulations!
                             You are a riddle master after all!
                          """)

    the_end_loser = Room("The End",
                         """
                         Unfortunately, you are not a riddle master.
                         Come later, after you have rested in that furniture
                         that has one head, one foot and four legs...
                         """)

    easy_guys_go.add_paths({
        'egg': (son_name, 100),
        '-': (the_end_loser, 0),
    })

    son_name.add_paths({
        'david': (car_people, 100),
        '-': (the_end_loser, 0),
    })

    car_people.add_paths({
        '3': (the_end_winner, 100),
        'three': (the_end_winner, 100),
        '-': (the_end_loser, 0),
    })

    def __init__(self):
        super().__init__(
            name='riddlemaster',
            show_name='Riddle Master',
            description='What have I got in my pocket?! (Baggins, Bilbo)',
            rooms=[
                self.easy_guys_go,
                self.son_name,
                self.car_people,
                self.the_end_winner,
                self.the_end_loser,
            ],
            start_room=self.easy_guys_go)

    def calculated_score(self):
        calculated_score = self.score - self.trials
        if calculated_score < 0:
            return 0
        return calculated_score


class WorldFlagQuiz(Game):
    """
    --------------------------------------------------------------------------
    WORLD FLAG QUIZ
    --------------------------------------------------------------------------
    """
    total_flags = 21

    the_end = Room("Quiz End",
                   """<b style='font-size: 20px'>
                        You completed the quiz!</b>
                   """)

    brazil = Room(f"Flag 1 of {total_flags}",
                  "Which country's flag is this?",
                  img_file="01_12cb30ba94032221ae9c864bed322b58.png",
                  room_type="quiz")

    germany = Room(f"Flag 2 of {total_flags}",
                   "Which country's flag is this?",
                   img_file="02_410c74697cce4eefdcc0e65e1308eb91.png",
                   room_type="quiz")

    portugal = Room(f"Flag 3 of {total_flags}",
                    "Which country's flag is this?",
                    img_file="03_b42fc57358603c783f76de7ee4cffa69.png",
                    room_type="quiz")

    south_korea = Room(f"Flag 4 of {total_flags}",
                       "Which country's flag is this?",
                       img_file="04_850bdc496f33175f58fff453d0e2c15f.png",
                       room_type="quiz")

    france = Room(f"Flag 5 of {total_flags}",
                  "Which country's flag is this?",
                  img_file="05_6120138f01dc6a289b10f61fbe811047.png",
                  room_type="quiz")

    england = Room(f"Flag 6 of {total_flags}",
                   "Which country's flag is this?",
                   img_file="06_ed28d15adf40423b9a367b1340485251.png",
                   room_type="quiz")

    uruguay = Room(f"Flag 7 of {total_flags}",
                   "Which country's flag is this?",
                   img_file="07_a5ae5ce08ed702ff837901c8540c05f0.png",
                   room_type="quiz")

    finland = Room(f"Flag 8 of {total_flags}",
                   "Which country's flag is this?",
                   img_file="08_e33a1b32a19a24d0155dab427a6a32e5.png",
                   room_type="quiz")

    cuba = Room(f"Flag 9 of {total_flags}",
                "Which country's flag is this?",
                img_file="09_3b68daaf3dd9efbde28fffd7f795cb2d.png",
                room_type="quiz")

    south_africa = Room(f"Flag 10 of {total_flags}",
                        "Which country's flag is this?",
                        img_file="10_ebf1636363a169eff9fa4eadaa6235e4.png",
                        room_type="quiz")

    jamaica = Room(f"Flag 11 of {total_flags}",
                   "Which country's flag is this?",
                   img_file="11_255e5ea53c42e41a88fd0e390c3afb50.png",
                   room_type="quiz")

    austria = Room(f"Flag 12 of {total_flags}",
                   "Which country's flag is this?",
                   img_file="12_a9fe0c7db98f5d4fc4094243d310028f.png",
                   room_type="quiz")

    tunisia = Room(f"Flag 13 of {total_flags}",
                   "Which country's flag is this?",
                   img_file="13_14f8dafbb33b782d27421556052b5211.png",
                   room_type="quiz")

    croatia = Room(f"Flag 14 of {total_flags}",
                   "Which country's flag is this?",
                   img_file="14_eaac050115db0a727892464506818ca0.png",
                   room_type="quiz")

    egypt = Room(f"Flag 15 of {total_flags}",
                 "Which country's flag is this?",
                 img_file="15_0e16f48fe68f60dfc7f7434c11053f7b.png",
                 room_type="quiz")

    wales = Room(f"Flag 16 of {total_flags}",
                 "Which country's flag is this?",
                 img_file="16_d165fd066a81e6090559429e88fa6b27.png",
                 room_type="quiz")

    angola = Room(f"Flag 17 of {total_flags}",
                  "Which country's flag is this?",
                  img_file="17_172a1b1673fe23115060e5e8cf791ec0.png",
                  room_type="quiz")

    iran = Room(f"Flag 18 of {total_flags}",
                "Which country's flag is this?",
                img_file="18_0e16f48fe68f60dfc7f7434c11053f7b.png",
                room_type="quiz")

    nepal = Room(f"Flag 19 of {total_flags}",
                 "Which country's flag is this?",
                 img_file="19_da5cef462e9167aea5e3fefbea205123.png",
                 room_type="quiz")

    bangladesh = Room(f"Flag 20 of {total_flags}",
                      "Which country's flag is this?",
                      img_file="20_9830c8910dddee0967cf4280c30efd69.png",
                      room_type="quiz")

    qatar = Room(f"Flag 21 of {total_flags}",
                 "Which country's flag is this?",
                 img_file="21_83882b9be88c540181f317e3a2a6c599.png",
                 room_type="quiz")

    brazil.add_paths({
        'Brazil': (germany, 1),
        'Argentina': (germany, 0),
        'Colombia': (germany, 0),
        'Chile': (germany, 0)
    })

    germany.add_paths({
        'Belgium': (portugal, 0),
        'Germany': (portugal, 1),
        'France': (portugal, 0),
        'Irland': (portugal, 0)
    })

    portugal.add_paths({
        'Spain': (south_korea, 0),
        'Japan': (south_korea, 0),
        'Guatemala': (south_korea, 0),
        'Portugal': (south_korea, 1)
    })

    south_korea.add_paths({
        'Vietnam': (france, 0),
        'Japan': (france, 0),
        'China': (france, 0),
        'South Korea': (france, 1)
    })

    france.add_paths({
        'Germany': (england, 0),
        'France': (england, 1),
        'Netherlands': (england, 0),
        'Paraguay': (england, 0)
    })

    england.add_paths({
        'Norway': (uruguay, 0),
        'Austria': (uruguay, 0),
        'Denmark': (uruguay, 0),
        'England': (uruguay, 1)
    })

    uruguay.add_paths({
        'Uruguay': (finland, 1),
        'Argentina': (finland, 0),
        'Greece': (finland, 0),
        'Paraguay': (finland, 0)
    })

    finland.add_paths({
        'Norway': (cuba, 0),
        'Argentina': (cuba, 0),
        'Finland': (cuba, 1),
        'Sweden': (cuba, 0)
    })

    cuba.add_paths({
        'Panama': (south_africa, 0),
        'Cuba': (south_africa, 1),
        'Guatemala': (south_africa, 0),
        'Pakistan': (south_africa, 0)
    })

    south_africa.add_paths({
        'South Africa': (jamaica, 1),
        'Lesoto': (jamaica, 0),
        'Angola': (jamaica, 0),
        'Uganda': (jamaica, 0)
    })

    jamaica.add_paths({
        'South Africa': (austria, 0),
        'Marrocos': (austria, 0),
        'Panama': (austria, 0),
        'Jamaica': (austria, 1)
    })

    austria.add_paths({
        'Poland': (tunisia, 0),
        'Lebanon': (tunisia, 0),
        'Denmark': (tunisia, 0),
        'Austria': (tunisia, 1)
    })

    tunisia.add_paths({
        'Tunisia': (croatia, 1),
        'Turkey': (croatia, 0),
        'Switzerland': (croatia, 0),
        'Marrocos': (croatia, 0)
    })

    croatia.add_paths({
        'Slovakia': (egypt, 0),
        'Czechia': (egypt, 0),
        'Croatia': (egypt, 1),
        'Slovenia': (egypt, 0)
    })

    egypt.add_paths({
        'Yemen': (wales, 0),
        'Syria': (wales, 0),
        'Egypt': (wales, 1),
        'Iraq': (wales, 0)
    })

    wales.add_paths({
        'Bhutan': (angola, 0),
        'Wales': (angola, 1),
        'Iran': (angola, 0),
        'Nepal': (angola, 0)
    })

    angola.add_paths({
        'Angola': (iran, 1),
        'Uganda': (iran, 0),
        'Kenya': (iran, 0),
        'Zimbabwe': (iran, 0)
    })

    iran.add_paths({
        'India': (nepal, 0),
        'Tajikistan': (nepal, 0),
        'Iran': (nepal, 1),
        'Kazakhstan': (nepal, 0)
    })

    nepal.add_paths({
        'Thailand': (bangladesh, 0),
        'Sri Lanka': (bangladesh, 0),
        'Wales': (bangladesh, 0),
        'Nepal': (bangladesh, 1)
    })

    bangladesh.add_paths({
        'Pakistan': (qatar, 0),
        'Bangladesh': (qatar, 1),
        'Philippines': (qatar, 0),
        'Myanmar': (qatar, 0)
    })

    qatar.add_paths({
        'United Arab Emirates': (the_end, 0),
        'Bahrain': (the_end, 0),
        'Qatar': (the_end, 1),
        'Kuwait': (the_end, 0)
    })

    def __init__(self):
        super().__init__(
            name='worldflagquiz',
            show_name='World Flag Quiz',
            description='Fun with Flags!',
            rooms=[
                self.brazil,
                self.germany,
                self.portugal,
                self.south_korea,
                self.france,
                self.england,
                self.uruguay,
                self.finland,
                self.cuba,
                self.south_africa,
                self.jamaica,
                self.austria,
                self.tunisia,
                self.croatia,
                self.egypt,
                self.wales,
                self.angola,
                self.iran,
                self.nepal,
                self.bangladesh,
                self.qatar,
                self.the_end],
            start_room=self.brazil
        )


available_games = {
    'gothon': Gothon,
    'riddlemaster': RiddleMaster,
    'worldflagquiz': WorldFlagQuiz
}
