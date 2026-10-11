import os
from datetime import datetime


def frame_img_name_template(gen, time):
    return 'results/temp/' + str(gen) + '-' + str(time) + '.png'


def result_img_name_template(settings):
    return 'results/' + settings['name'] + _now() + '.jpg'


def result_gif_name_template(settings, gen):
    return os.getcwd() + '/results/' + settings['name'] + ' gen-' + str(gen) + _now() + '.gif'


def first_gen_org_name_template(org):
    return 'gen[x]-org[' + str(org) + ']'


def next_gen_org_name_template(gen, org):
    return 'gen[' + str(gen) + ']-org[' + str(org) + ']'


def _now():
    return datetime.now().strftime(' %Y-%m-%d %H-%M-%S')
