#!/usr/bin/env python3

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
        """ power saving with interval 1/3
            use 1/130 for more realtime at the cost of higher cpu usage
        """
        pyglet.clock.schedule_interval(self.update, 1.0 / refresh_rate)
        try:
            pyglet.clock.set_fps_limit(125)
        except AttributeError:
            print("clock.set_fps_limit not available, sorry")
        ## set some basic values
        self.width = screen_width
        self.height = screen_height
        self.resizable = True
        self.set_caption("ringt the bell - aber schnell")
        ## define resources
        pyglet.resource.path = ['data/audio', 'data/images']
        pyglet.resource.reindex()
        self.red = pyglet.resource.image("red.png")
        self.green = pyglet.resource.image("green.png")
        self.blue = pyglet.resource.image("blue.png")
        self.grey = pyglet.resource.image("grey.png")
        self.batch = pyglet.graphics.Batch()
        self.sprites = [
            pyglet.sprite.Sprite(self.grey, x = 10, y = 10, batch=self.batch),
            pyglet.sprite.Sprite(self.grey, x = 10, y = 50, batch=self.batch),
            pyglet.sprite.Sprite(self.grey, x = 10, y = 90, batch=self.batch),
            pyglet.sprite.Sprite(self.grey, x = 10, y = 130, batch=self.batch),
            pyglet.sprite.Sprite(self.grey, x = 10, y = 170, batch=self.batch),
            pyglet.sprite.Sprite(self.grey, x = 10, y = 210, batch=self.batch),
            pyglet.sprite.Sprite(self.grey, x = 10, y = 250, batch=self.batch),
            pyglet.sprite.Sprite(self.grey, x = 10, y = 290, batch=self.batch),
            pyglet.sprite.Sprite(self.grey, x = 10, y = 330, batch=self.batch),
            pyglet.sprite.Sprite(self.grey, x = 10, y = 370, batch=self.batch),
        ]

        ## OSD
        self.headline = pyglet.text.Label('Ring the bell!', font_size = 30,
                                          x = self.width // 2, y = self.height,
                                          anchor_x = 'center', anchor_y = 'top')
        self.helptext = "test with keyboard numbers..."
        self.helptext2 = "[q]uit"
        self.set2D()

    # You need the dt argument there to prevent errors,
    # it does nothing as far as I know.
    def update(self, dt):
        pass

    def on_draw(self):
        pyglet.clock.tick()  # Make sure you tick the clock!
        self.clear()
        self.draw_texts()
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
        """
        self.headline.draw()
        self.helpline = pyglet.text.Label(self.helptext, font_size=10,
                                          x=150, y=25, anchor_x='left', anchor_y='bottom')
        self.helpline.draw()
        self.helpline2 = pyglet.text.Label(self.helptext2, font_size=10,
                                          x=150, y=5, anchor_x='left', anchor_y='bottom')
        self.helpline2.draw()

    def draw_sprites(self):
        ## 2D Sprites
        self.batch.draw()

    def update_sprite(self, number, color):
        if color == 0:
            image = self.grey
        if color == 1:
            image = self.red
        if color == 2:
            image = self.green
        if color == 3:
            image = self.blue
        self.sprites[number] = pyglet.sprite.Sprite(batch=self.batch,
                img = image, x = 10, y = number * 40 + 10)

    def animate_win(self):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q or symbol == pyglet.window.key.ESCAPE:
            print('INFO "Q" or "ESC" key was pressed. Good bye!')
            pyglet.app.exit()
        elif symbol == pyglet.window.key._0 or symbol == pyglet.window.key.NUM_0:
            print('INFO "0" key was pressed.')
            self.helptext = '"0" key was pressed.'
            self.update_sprite(0, 1)
        elif symbol == pyglet.window.key._1 or symbol == pyglet.window.key.NUM_1:
            print('INFO "1" key was pressed.')
            self.helptext = '"1" key was pressed.'
            self.update_sprite(1, 2)
        elif symbol == pyglet.window.key._2 or symbol == pyglet.window.key.NUM_2:
            print('INFO "2" key was pressed.')
            self.helptext = '"2" key was pressed.'
            self.update_sprite(2, 3)
        elif symbol == pyglet.window.key._3 or symbol == pyglet.window.key.NUM_3:
            print('INFO "3" key was pressed.')
            self.helptext = '"3" key was pressed.'
            self.update_sprite(3, 1)
        elif symbol == pyglet.window.key._4 or symbol == pyglet.window.key.NUM_4:
            print('INFO "4" key was pressed.')
            self.helptext = '"4" key was pressed.'
            self.update_sprite(4, 2)
        elif symbol == pyglet.window.key._5 or symbol == pyglet.window.key.NUM_5:
            print('INFO "5" key was pressed.')
            self.helptext = '"5" key was pressed.'
            self.update_sprite(5, 3)
        elif symbol == pyglet.window.key._6 or symbol == pyglet.window.key.NUM_6:
            print('INFO "6" key was pressed.')
            self.helptext = '"6" key was pressed.'
            self.update_sprite(6, 1)
        elif symbol == pyglet.window.key._7 or symbol == pyglet.window.key.NUM_7:
            print('INFO "7" key was pressed.')
            self.helptext = '"7" key was pressed.'
            self.update_sprite(7, 2)
        elif symbol == pyglet.window.key._8 or symbol == pyglet.window.key.NUM_8:
            print('INFO "8" key was pressed.')
            self.helptext = '"8" key was pressed.'
            self.update_sprite(8, 3)
        elif symbol == pyglet.window.key._9 or symbol == pyglet.window.key.NUM_9:
            print('INFO "9" key was pressed.')
            self.helptext = '"9" key was pressed.'
            self.update_sprite(9, 1)
            self.animate_win()
        else:
            print('INFO %s key was pressed.' % str(symbol))
            self.helptext = ('symbol "%s" was pressed.' % str(symbol))

if __name__ == "__main__":
    prototype = Prototype()
    pyglet.app.run()
