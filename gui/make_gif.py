import os
import glob

from PIL import Image

from functions.name_functions import result_gif_name_template


def make_gif(settings, gen):

    file_list = glob.glob(os.getcwd() + '/results/temp/**/*.png', recursive=True)

    list.sort(file_list, key=lambda x: int(os.path.basename(x).split('.png')[0].split('-')[1]))
    frames = []
    for filename in file_list:
        with Image.open(filename) as frame:  # closed right away, so the png can be removed on Windows
            frames.append(frame.convert('RGB'))
    # loop=0 - the animation repeats forever instead of stopping on the last frame
    frames[0].save(result_gif_name_template(settings, gen), save_all=True, append_images=frames[1:],
                   loop=0, duration=round(1000 / settings['gif_fps']))

    [os.remove(f) for f in file_list]
