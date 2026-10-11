import os
import glob
import imageio

from functions.name_functions import result_gif_name_template


def make_gif(settings, gen):

    file_list = glob.glob(os.getcwd() + '/results/temp/**/*.png', recursive=True)

    list.sort(file_list, key=lambda x: int(os.path.basename(x).split('.png')[0].split('-')[1]))
    images = []
    for filename in file_list:
        images.append(imageio.imread(filename))
    imageio.mimsave(result_gif_name_template(settings, gen), images)

    [os.remove(f) for f in file_list]
