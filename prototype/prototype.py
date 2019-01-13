#!/usr/bin/env python3
"""
Prototype for game development and testing. All parts of the game are
implemented in software to test the rules and the general experience.
Later this Prototype could be the interface to connect all hardware parts of
the game.

It uses latest pyglet as engine:
https://pyglet.readthedocs.io/en/latest/
"""

import pyglet
import pyglet.gl as gl
import random
import datetime
import time
import libs.udp_server
import libs.dmx

screen_width = 640
screen_height = 480
refresh_rate = 60.0  # values from 3.0 to 130.0
image_width = 100
image_height = 30
bar_elements = 10 # aka number of levels
udp_server_port = 3333

window = pyglet.window.Window()
window.set_caption("ring the bell - aber schnell")
window.width = screen_width
window.height = screen_height
window.resizable = False

"""
joysticks = pyglet.input.get_joysticks()
for i in joysticks:
    print(i.device)
joystick = joysticks[0]
joystick.open()
print("DEBUG A: %s" % joystick.device)
print("DEBUG A: %s" % joystick.buttons)
print("DEBUG A: %s" % joystick.x)
"""

""" Initializations
"""
def set2D():
    """ Configure OpenGL to draw in 2D.
    """
    width, height = window.get_size()
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, width, 0, height, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

def init_gamepad():
    """ try to initialise the gamepad
    """
    print("INFO init: gamepad")
    joysticks = pyglet.input.get_joysticks()
    try:
        assert joysticks
        global gamepad
        gamepad = joysticks[0]
        print("DEBUG opened gamepad: %s" % gamepad.device)
        gamepad.open()
    except AssertionError as error:
        print("ERROR No gamepad found: %s" % error)
        gamepad = None
    if gamepad:
        print("DEBUG A: %s" % gamepad.buttons)


""" Game States & Helper Routines
"""
def set_freeze():
    round_color = random.randint(1,3)
    bar.set_all_at_level(round_color)
    draw_sprites()
    #round_starttime = time.time()
    count_time = int((bar_elements - bar.get_level()) / 3 )
    print("DEBUG countdown starts with: %s" % count_time)
    recieved_packets = {}
    udp.clear_packet_cache()
    bar.save_state()
    p1.save_state()
    p2.save_state()
    p3.save_state()
    #TODO in thread
    print("DEBUG starting countdown")
    for t in range(count_time):
        print(count_time - t)
        time.sleep(1)
    print(bar.get_saved_state())
    print(p1.get_saved_state())
    print(p2.get_saved_state())
    print(p3.get_saved_state())
    #saved_state = all saved player states
    recieved_packets = udp.get_packets()
    reactions = {}
    for p in recieved_packets:
        print("DEBUG udp packet at: %s from: %s contained: %s" \
                % (p, recieved_packets[p][0], recieved_packets[p][1]))
        if not reactions[str(recieved_packets[p][0])]:
            reactions[str(recieved_packets[p][0])] = recieved_packets[p][1]
    """
    for p in active_players:
         for button in p.get_saved_state():
            if pad_button[color] == round_color and \
               pad_button[time] < round_starttime + count_time:
                    add to round_state

        if round_state == saved_state():
            level_up()
        else:
            let bar and every right pressed button blink for 5 seconds
            and start same round again
    """

def set_release():
    """ things to do after freeze
    """
    pass

def set_random():
    bar.set_random_at_level()
    p1.set_random()
    p2.set_random()
    p3.set_random()
    bar.save_state()
    p1.save_state()
    p2.save_state()
    p3.save_state()
    print(p1.get_saved_state())
    print(p2.get_saved_state())
    print(p3.get_saved_state())
    print(bar.get_level())

def animate_fall():
    print(bar.get_status())
    print(bar.get_element(len(bar.get_status().keys())-1))
    for i in bar.get_status():
        print(i)
        if i == 9:
            bar.set_element(i, bar.get_element(0))
        else:
            bar.set_element(i, bar.get_element(i+1))


""" Game Classes
"""
class Bar():
    def __init__(self, elements, color, start_x, start_y):
        """ initialize with:
            number of elements, default color, first element x, first element y
        """
        self.x = start_x
        self.y = start_y
        self.bar_grey = pyglet.resource.image("comb_grey.png")
        self.bar_red = pyglet.resource.image("comb_red.png")
        self.bar_green = pyglet.resource.image("comb_green.png")
        self.bar_blue = pyglet.resource.image("comb_blue.png")
        self.bar_gold = pyglet.resource.image("comb_gold.png")
        self.bar_white = pyglet.resource.image("comb_white.png")
        self.batch_bar = pyglet.graphics.Batch()
        self.sprites_bar = []
        print("DEBUG intiate game bar with %s elements" % elements)
        self.bar_level = 0
        self.bar_saved = {}
        self.bar = {}
        self.par_offset = 7 ## number of channels per par
        for i in range(0, elements):
            self.bar[i] = color
            dmx.set_rgb(i * self.par_offset + 1, color)
        dmx.render()
        self.game_state = 0

    def set_game_state(self, state):
        """ set game state in master and broadcast to all gamepads
            see all possible game states below
        """
        self.game_state = state
        udp.send(self.game_state)
        if self.game_state == 0:
            print("INFO game state: START")
        elif self.game_state == 1:
            print("INFO game state: NTP_SYNC")
            print("DEBUG time: %s  unix: %s" % (datetime.datetime.now(),
                        time.time()))
            time.sleep(2)
        elif self.game_state == 2:
            print("INFO game state: RANDOM")
            set_random()
        elif self.game_state == 3:
            print("INFO game state: FREEZE")
            set_freeze();
            set_release();
        elif self.game_state == 4:
            print("INFO game state: RELEASE")
            set_release();
        elif self.game_state == 5:
            print("INFO game state: LEVEL_UP")
            self.level_up()
        elif self.game_state == 6:
            print("INFO game state: LEVEL_DOWN")
            self.level_down()
        elif self.game_state == 7:
            print("INFO game state: WIN")
            self.set_level(bar_elements)
        else:
            print("INFO no such game state")

    def set_element(self, number, color):
        self.bar[number] = color
        dmx.set_rgb(number * self.par_offset + 1, color)
        dmx.render()

    def get_element(self, number):
        return self.bar[number]

    def set_all(self, color):
        for i in self.bar:
            self.bar[i] = color
            dmx.set_rgb(i * self.par_offset + 1, color)
        dmx.render()

    def set_all_at_level(self, color):
        for i in self.bar:
            if i >= self.bar_level:
                self.bar[i] = color
                dmx.set_rgb(i * self.par_offset + 1, color)
        dmx.render()

    def set_random(self):
        for i in self.bar:
            color = random.randint(1,3)
            self.bar[i] = color
            dmx.set_rgb(i * self.par_offset + 1, color)
        dmx.render()

    def set_random_at_level(self):
        for i in self.bar:
            if i >= self.bar_level:
                color = random.randint(1,3)
                self.bar[i] = color
                dmx.set_rgb(i * self.par_offset + 1, color)
        dmx.render()

    def get_batch(self):
        self.sprites_bar = []
        sprite = pyglet.sprite.Sprite(self.bar_grey, batch=self.batch_bar,
                x = self.x + 50, y = self.y)
        self.sprites_bar.append(sprite)
        for i in self.bar:
            color = self.bar_grey
            #levelmarker = 0
            if self.bar[i] == 0:
                color = self.bar_grey
            if self.bar[i] == 1:
                color = self.bar_red
            if self.bar[i] == 2:
                color = self.bar_green
            if self.bar[i] == 3:
                color = self.bar_blue
            if self.bar[i] == 4:
                color = self.bar_white
            if self.bar[i] == 5:
                color = self.bar_gold
            if i < self.bar_level:
                sprite = pyglet.sprite.Sprite(self.bar_gold, batch=self.batch_bar,
                        x = self.x + (i % 2) * 50,
                        y = self.y + 30 + i * 30,)
                self.sprites_bar.append(sprite)
            else:
                sprite = pyglet.sprite.Sprite(color, batch=self.batch_bar,
                        x = self.x + (i % 2) * 50,
                        y = self.y + 30 + i * 30,)
                self.sprites_bar.append(sprite)
        return self.batch_bar

    def save_state(self):
        self.bar_saved = self.bar

    def get_saved_state(self):
        return self.bar_saved

    def level_up(self):
        if self.bar_level < len(self.bar):
            self.bar_level += 1

    def level_down(self):
        if self.bar_level > 0:
            self.bar_level -= 1

    def set_level(self, number):
        if number >= 0 and number <= len(self.bar):
            self.bar_level = number

    def get_level(self):
        return self.bar_level

class Player():
    def __init__(self, name, start_x, start_y):
        """ initialize with:
            name, first button x, first button y
        """
        print("hello my name is: %s" % name)
        self.name = name
        self.x = start_x
        self.y = start_y
        self.pad_grey = pyglet.resource.image("pad_grey.png")
        self.button_grey = pyglet.resource.image("button_grey.png")
        self.button_red = pyglet.resource.image("button_red.png")
        self.button_green = pyglet.resource.image("button_green.png")
        self.button_blue = pyglet.resource.image("button_blue.png")
        self.batch_player = pyglet.graphics.Batch()
        self.sprites_player = []
        self.buttons = {}
        self.buttons_saved = {}
        self.set_buttons(0,0,0)
        #for i in range(0, 3):
            #self.buttons[i] = 0

    def set_buttons(self, color1, color2, color3):
        self.buttons[0] = color1
        self.buttons[1] = color2
        self.buttons[2] = color3

    def set_random(self):
        for i in self.buttons:
            self.buttons[i] = random.randint(1,3)

    def get_batch(self):
        self.sprites_player = []
        sprite = pyglet.sprite.Sprite(self.pad_grey, x = self.x, y = self.y, batch=self.batch_player)
        self.sprites_player.append(sprite)
        for i in self.buttons:
            color = self.button_grey
            if self.buttons[i] == 1:
                color = self.button_red
            if self.buttons[i] == 2:
                color = self.button_green
            if self.buttons[i] == 3:
                color = self.button_blue
            sprite = pyglet.sprite.Sprite(color, x = self.x + 20 + i * 20, y =
                    self.y + 15 + ((i + 1) % 2 * 28), batch=self.batch_player)
            self.sprites_player.append(sprite)
        return self.batch_player

    def print(self):
        print(self.buttons)

    def save_state(self):
        self.buttons_saved = self.buttons

    def get_saved_state(self):
        return self.buttons_saved


""" Ingame reactions
"""
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q or symbol == pyglet.window.key.ESCAPE:
        print('INFO "Q" or "ESC" key was pressed. Good bye!')
        pyglet.app.exit()
        udp.stop()
    elif symbol == pyglet.window.key._1 or symbol == pyglet.window.key.NUM_1:
        print('INFO "1" key was pressed.')
        bar.set_element(1, 1)
    elif symbol == pyglet.window.key._2 or symbol == pyglet.window.key.NUM_2:
        print('INFO "2" key was pressed.')
        bar.set_element(1, 2)
    elif symbol == pyglet.window.key._3 or symbol == pyglet.window.key.NUM_3:
        print('INFO "3" key was pressed.')
        bar.set_element(1, 3)
    elif symbol == pyglet.window.key._4 or symbol == pyglet.window.key.NUM_4:
        print('INFO "4" key was pressed.')
        bar.set_element(1, 0)
    elif symbol == pyglet.window.key._5 or symbol == pyglet.window.key.NUM_5:
        print('INFO "5" key was pressed.')
        p1.set_buttons(1, 2, 3)
        p2.set_buttons(1, 2, 3)
        p3.set_buttons(1, 2, 3)
        bar.set_all(5)
    elif symbol == pyglet.window.key._6 or symbol == pyglet.window.key.NUM_6:
        print('INFO "6" key was pressed.')
        p1.set_buttons(0, 0, 0)
        p2.set_buttons(0, 0, 0)
        p3.set_buttons(0, 0, 0)
        bar.set_all(0)
        #dmx.blackout()
        #dmx.render()
    elif symbol == pyglet.window.key._7 or symbol == pyglet.window.key.NUM_7:
        print('INFO "7" key was pressed.')
        p1.set_buttons(4, 4, 4)
        p2.set_buttons(4, 4, 4)
        p3.set_buttons(4, 4, 4)
        bar.set_all(4)
    elif symbol == pyglet.window.key._8 or symbol == pyglet.window.key.NUM_8:
        print('INFO "8" key was pressed.')
        p1.set_buttons(1, 1, 1)
        p2.set_buttons(1, 1, 1)
        p3.set_buttons(1, 1, 1)
        bar.set_all(1)
        #dmx.set_red(1)
        #dmx.render()
    elif symbol == pyglet.window.key._9 or symbol == pyglet.window.key.NUM_9:
        print('INFO "9" key was pressed.')
        p1.set_buttons(2, 2, 2)
        p2.set_buttons(2, 2, 2)
        p3.set_buttons(2, 2, 2)
        bar.set_all(2)
    elif symbol == pyglet.window.key._0 or symbol == pyglet.window.key.NUM_0:
        print('INFO "0" key was pressed.')
        p1.set_buttons(3, 3, 3)
        p2.set_buttons(3, 3, 3)
        p3.set_buttons(3, 3, 3)
        bar.set_all(3)
    elif symbol == pyglet.window.key.S:
        print('INFO "S" key was pressed.')
        bar.set_game_state(0)
    elif symbol == pyglet.window.key.T:
        print('INFO "T" key was pressed.')
        bar.set_game_state(1)
    elif symbol == pyglet.window.key.R:
        print('INFO "R" key was pressed.')
        bar.set_game_state(2)
    elif symbol == pyglet.window.key.F:
        print('INFO "F" key was pressed.')
        bar.set_game_state(3)
    elif symbol == pyglet.window.key.U:
        print('INFO "U" key was pressed.')
        bar.set_game_state(5)
    elif symbol == pyglet.window.key.D:
        print('INFO "D" key was pressed.')
        bar.set_game_state(6)
    elif symbol == pyglet.window.key.W:
        print('INFO "W" key was pressed.')
        bar.set_game_state(7)
    elif symbol == pyglet.window.key.E:
        print('INFO "E" key was pressed.')
        recieved_packets = udp.get_packets()
        for p in recieved_packets:
            print("udp packet at: %s from: %s contained: %s" \
                    % (p, recieved_packets[p][0], recieved_packets[p][1]))
    else:
        print('INFO %s key was pressed.' % str(symbol))

@window.event
def on_draw():
    pyglet.clock.tick()  # Make sure you tick the clock!
    window.clear()
    draw_sprites()

@window.event
def update(dt):
    """ You need the dt argument there to prevent errors,
        it does nothing as far as I know.
    """
    #print(dt)
    pass

@window.event
def draw_sprites():
    ## sprites for ladder
    bar_batch = bar.get_batch()
    bar_batch.draw()
    ## sprites for players
    p1_batch = p1.get_batch()
    p1_batch.draw()
    p2_batch = p2.get_batch()
    p2_batch.draw()
    p3_batch = p3.get_batch()
    p3_batch.draw()
    ## win animation
    if bar.get_level() == bar_elements:
        win_animation.draw()

@window.event
def on_joybutton_press(joystick, button):
    print("DEBUG A: %s" % joystick.buttons)
    print(button)

@window.event
def on_joybutton_release(joystick, button):
    print("DEBUG A: %s" % joystick.buttons)
    print(button)


if __name__ == "__main__":
    ## start local UDP server on given port 
    udp = libs.udp_server.UDP_Server(udp_server_port)
    udp.start()
    ## set pyglet details
    pyglet.clock.schedule_interval(update, 1.0 / refresh_rate)
    pyglet.clock.set_fps_limit(125)
    pyglet.resource.path = ['data/audio', 'data/images']
    pyglet.resource.reindex()
    ## set OpenGL 2D mode
    set2D()
    """ TODO broken
    ## default audio
    pyglet.options['audio'] = ('openal', 'pulse', 'silent')
    pyglet.options['audio'] = ('pulse', 'silent')
    #sound_win = pyglet.resource.media("tada.mp3")
    sound_win = pyglet.media.load("data/audio/tada.wav", streaming = False)
    """
    ## init DMX
    dmx = libs.dmx.DMX('/dev/ttyUSB0')
    #dmx.set_white(1)
    #dmx.render()
    ## create bar and players
    bar = Bar(bar_elements, 0, 10, 10)
    bar.set_random()
    p1 = Player("uno", 200, 50)
    p1.set_random()
    p2 = Player("dos", 310, 120)
    p2.set_random()
    p3 = Player("tres", 420, 190)
    p3.set_random()
    ## winning animation
    win_animation_res = pyglet.resource.animation("win_animation.gif")
    win_animation = pyglet.sprite.Sprite(win_animation_res, x = 20, y = 100)
    ## inputs
    #init_gamepad()

    pyglet.app.run()
