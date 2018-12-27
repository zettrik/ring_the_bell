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

screen_width = 640
screen_height = 480
refresh_rate = 3.0  # values from 3.0 to 130.0
image_width = 100
image_height = 30

class Prototype(pyglet.window.Window):
    def __init__(self):
        super(Prototype, self).__init__()
        pyglet.clock.schedule_interval(self.update, 1.0 / refresh_rate)
        try:
            pyglet.clock.set_fps_limit(125)
        except AttributeError:
            print("clock.set_fps_limit not available, sorry")
        ## set some basic values
        self.width = screen_width
        self.height = screen_height
        self.resizable = False
        self.set2D()
        pyglet.resource.path = ['data/audio', 'data/images']
        pyglet.resource.reindex()
        ## default texts
        self.set_caption("ringt the bell - aber schnell")
        self.headtext = "Ring the bell!"
        self.helptext = "test with keyboard numbers..."
        self.helptext2 = "[q]uit"
        ## default audio
        #pyglet.options['audio'] = ('openal', 'pulse', 'silent')
        #pyglet.options['audio'] = ('pulse', 'silent')
        #self.sound_win = pyglet.resource.media("tada.mp3")
        #self.sound_win = pyglet.media.load("data/audio/tada.wav", streaming = False)
        ## create bar and players
        self.bar = Bar(10, 0, 10, 10)
        #print(self.bar.get_status())
        self.p1 = Player("uno", 150, 10)
        #print(self.p1.get_status())
        self.p2 = Player("dos", 190, 10)
        #print(self.p2.get_status())
        self.p3 = Player("tres", 230, 10)
        #print(self.p3.get_status())

    def update(self, dt):
        """ You need the dt argument there to prevent errors,
            it does nothing as far as I know.
        """
        pass

    def on_draw(self):
        pyglet.clock.tick()  # Make sure you tick the clock!
        self.clear()
        #self.draw_texts() #TODO no text display on python 3.7 yet
        self.draw_sprites()

    def set2D(self):
        """ Configure OpenGL to draw in 2D.
        """
        width, height = self.get_size()
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def draw_texts(self):
        """ draw head- and helpline

            TODO text display doesn't work in python 3.7 yet
            https://bitbucket.org/pyglet/pyglet/issues/168/pyglettextdocument-fails-in-python-37-b1
        """
        self.headline = pyglet.text.Label(self.headtext, font_size = 30,
                x = self.width // 2, y = self.height,
                anchor_x = 'center', anchor_y = 'top')
        self.headline.draw()
        self.helpline = pyglet.text.Label(self.helptext, font_size=10,
                x=150, y=25, anchor_x='left', anchor_y='bottom')
        self.helpline.draw()
        self.helpline2 = pyglet.text.Label(self.helptext2, font_size=10,
                x=150, y=5, anchor_x='left', anchor_y='bottom')
        self.helpline2.draw()

    def draw_sprites(self):
        ## sprites for ladder
        bar_batch = self.bar.get_batch()
        bar_batch.draw()
        ## sprites for players
        p1_batch = self.p1.get_batch()
        p1_batch.draw()
        p2_batch = self.p2.get_batch()
        p2_batch.draw()
        p3_batch = self.p3.get_batch()
        p3_batch.draw()

    def update_sprite(self, number, color):
        if color == 0:
            image = self.bar_grey
        if color == 1:
            image = self.bar_red
        if color == 2:
            image = self.bar_green
        if color == 3:
            image = self.bar_blue
        if color == 4:
            image = self.bar_win
        self.bar_sprites[number] = pyglet.sprite.Sprite(batch=self.batch,
                img = image, x = 10, y = number * 40 + 10)

    def update_player(self, number, button, color):
        if color == 0:
            image = self.button_grey
        if color == 1:
            image = self.button_red
        if color == 2:
            image = self.button_green
        if color == 3:
            image = self.button_blue
        self.player1_sprites = [
            pyglet.sprite.Sprite(img = image, x = 150, y = 10, batch=self.batch),
            pyglet.sprite.Sprite(self.button_green, x = 180, y = 10, batch=self.batch),
            pyglet.sprite.Sprite(self.button_blue, x = 210, y = 10, batch=self.batch),
        ]

    def animate_win(self):
        self.update_sprite(9, 4)
        #self.sound_win.play()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q or symbol == pyglet.window.key.ESCAPE:
            print('INFO "Q" or "ESC" key was pressed. Good bye!')
            pyglet.app.exit()
        elif symbol == pyglet.window.key._1 or symbol == pyglet.window.key.NUM_1:
            print('INFO "1" key was pressed.')
            self.helptext = '"1" key was pressed.'
            self.bar.set_element(1, 1)
        elif symbol == pyglet.window.key._2 or symbol == pyglet.window.key.NUM_2:
            print('INFO "2" key was pressed.')
            self.helptext = '"2" key was pressed.'
            self.bar.set_element(1, 2)
        elif symbol == pyglet.window.key._3 or symbol == pyglet.window.key.NUM_3:
            print('INFO "3" key was pressed.')
            self.helptext = '"3" key was pressed.'
            self.bar.set_element(1, 3)
        elif symbol == pyglet.window.key._4 or symbol == pyglet.window.key.NUM_4:
            print('INFO "4" key was pressed.')
            self.helptext = '"4" key was pressed.'
            self.bar.set_element(1, 0)
        elif symbol == pyglet.window.key._5 or symbol == pyglet.window.key.NUM_5:
            print('INFO "5" key was pressed.')
            self.helptext = '"5" key was pressed.'
            self.p1.set_buttons(0, 1, 0)
        elif symbol == pyglet.window.key._6 or symbol == pyglet.window.key.NUM_6:
            print('INFO "6" key was pressed.')
            self.helptext = '"6" key was pressed.'
            self.p1.set_buttons(0, 2, 0)
        elif symbol == pyglet.window.key._7 or symbol == pyglet.window.key.NUM_7:
            print('INFO "7" key was pressed.')
            self.helptext = '"7" key was pressed.'
            self.p1.set_buttons(0, 3, 0)
        elif symbol == pyglet.window.key._8 or symbol == pyglet.window.key.NUM_8:
            print('INFO "8" key was pressed.')
            self.helptext = '"8" key was pressed.'
            self.p1.set_buttons(0, 0, 0)
        elif symbol == pyglet.window.key._9 or symbol == pyglet.window.key.NUM_9:
            print('INFO "9" key was pressed.')
            self.helptext = '"9" key was pressed.'
            self.p3.set_buttons(1, 2, 3)
        elif symbol == pyglet.window.key._0 or symbol == pyglet.window.key.NUM_0:
            print('INFO "0" key was pressed.')
            self.helptext = '"0" key was pressed.'
            self.p3.set_buttons(2, 3, 1)
        elif symbol == pyglet.window.key.A:
            print('INFO "A" key was pressed.')
            self.helptext = '"A" key was pressed.'
            self.p2.set_buttons(1, 2, 3)
        elif symbol == pyglet.window.key.S:
            print('INFO "S" key was pressed.')
            self.helptext = '"S" key was pressed.'
            self.p2.set_buttons(2, 3, 1)
        elif symbol == pyglet.window.key.D:
            print('INFO "D" key was pressed.')
            self.helptext = '"D" key was pressed.'
            self.p2.set_buttons(3, 1, 2)
        else:
            print('INFO %s key was pressed.' % str(symbol))
            self.helptext = ('symbol "%s" was pressed.' % str(symbol))

class Bar():
    def __init__(self, elements, color, start_x, start_y):
        """ initialize with:
            number of elements, default color, first element x, first element y
        """
        self.x = start_x
        self.y = start_y
        self.bar_grey = pyglet.resource.image("bar_grey.png")
        self.bar_red = pyglet.resource.image("bar_red.png")
        self.bar_green = pyglet.resource.image("bar_green.png")
        self.bar_blue = pyglet.resource.image("bar_blue.png")
        self.bar_win = pyglet.resource.animation("bar_win.gif")
        self.batch_bar = pyglet.graphics.Batch()
        self.sprites_bar = []
        print("intiate game bar with %s elements" % elements)
        self.bar = {}
        for i in range(0, elements):
            self.bar[i] = color

    def set_element(self, number, color):
        self.bar[number] = color

    def get_batch(self):
        self.sprites_bar = []
        color = self.bar_grey
        for i in self.bar:
            if self.bar[i] == 0:
                color = self.bar_grey
            if self.bar[i] == 1:
                color = self.bar_red
            if self.bar[i] == 2:
                color = self.bar_green
            if self.bar[i] == 3:
                color = self.bar_blue
            sprite = pyglet.sprite.Sprite(color, x = self.x, y = self.y + i * 40, batch=self.batch_bar)
            self.sprites_bar.append(sprite)
        return self.batch_bar

    def get_status(self):
        return self.bar

class Player():
    def __init__(self, name, start_x, start_y):
        """ initialize with:
            name, first button x, first button y
        """
        print("hello my name is: %s" % name)
        self.name = name
        self.x = start_x
        self.y = start_y
        self.button_grey = pyglet.resource.image("button_grey.png")
        self.button_red = pyglet.resource.image("button_red.png")
        self.button_green = pyglet.resource.image("button_green.png")
        self.button_blue = pyglet.resource.image("button_blue.png")
        self.batch_player = pyglet.graphics.Batch()
        self.sprites_player = []
        self.buttons = {}
        self.set_buttons(0,0,0)
        #for i in range(0, 3):
            #self.buttons[i] = 0

    def set_buttons(self, color1, color2, color3):
        self.buttons[0] = color1
        self.buttons[1] = color2
        self.buttons[2] = color3

    def get_batch(self):
        self.sprites_player = []
        color = self.button_grey
        for i in self.buttons:
            if self.buttons[i] == 0:
                color = self.button_grey
            if self.buttons[i] == 1:
                color = self.button_red
            if self.buttons[i] == 2:
                color = self.button_green
            if self.buttons[i] == 3:
                color = self.button_blue
            sprite = pyglet.sprite.Sprite(color, x = self.x, y = self.y + i * 30, batch=self.batch_player)
            self.sprites_player.append(sprite)
        return self.batch_player

    def get_status(self):
        return self.buttons

    def print(self):
        print(self.buttons)

if __name__ == "__main__":
    prototype = Prototype()
    pyglet.app.run()
