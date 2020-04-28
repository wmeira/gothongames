from app.games import *

def test_room():
    gold = Room("GoldRoom",
                """This room has gold in it you can grab. There's a door to the north.""")
    assert gold.name == "GoldRoom", "test success"
    assert gold.paths == {}


def test_room_paths():
    center = Room("Center", "Test room in the center.")
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")

    center.add_paths({'north': (north, 10), 'south': (south, 10)})
    assert center.go('north')[0] == north
    assert center.go('south')[0] == south

def test_map():
    start = Room('Start', 'You can go west and down a hole.')
    west = Room('Trees', 'There are trees here, you can go east')
    down = Room('Dungeon', "It's dark down here, you can go up")

    start.add_paths({'west': (west, 10), 'down': (down, 10)})
    west.add_paths({'east': (start, 10)})
    down.add_paths({'up': (start, 10)})

    assert start.go('west')[0] == west
    assert start.go('west')[0].go('east')[0] == start
    assert start.go('down')[0].go('up')[0] == start

def test_gothon_game_map():
    game = available_games['gothon']()
    start_room = game.start_room

    assert start_room.go('shoot!')[0] == game.generic_end
    assert start_room.go('dodge!')[0] == Game.generic_end

    room = start_room.go('tell a joke')[0]
    assert room == game.laser_weapon_armory