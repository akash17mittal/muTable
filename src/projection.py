import pyglet
from pyglet.canvas import Display


class Projection:

    def __init__(self, img, channels="RGBA"):
        self.pic = pyglet.image.ImageData(img.shape[1], img.shape[0], channels, img.tobytes(),
                                          -1 * img.shape[1] * len(channels))

    def update_pic(self, img, channels="RGBA"):
        self.pic = pyglet.image.ImageData(img.shape[1], img.shape[0], channels, img.tobytes(),
                                          -1 * img.shape[1] * len(channels))

    def get_pic(self):
        return self.pic


def start_projecting(projection_data):
    screens = Display().get_screens()
    window = pyglet.window.Window(fullscreen=True, screen=screens[1])

    def update(dt):
        pass

    @window.event
    def on_draw():
        window.clear()
        projection_data.get_pic().blit(0, 0)

    pyglet.clock.schedule_interval(update, 1 / 30.0)
    pyglet.app.run()
