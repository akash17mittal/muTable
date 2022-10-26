import pyglet
from pyglet.canvas import Display


def start_projecting(img, channels="RGBA"):
    pic = pyglet.image.ImageData(img.shape[0], img.shape[1], channels, img.tobytes(), -1 * img.shape[1]*len(channels))
    screens = Display().get_screens()
    window = pyglet.window.Window(fullscreen=True, screen=screens[1])

    @window.event
    def on_draw():
        window.clear()
        pic.blit(0, 0)

    pyglet.app.run()