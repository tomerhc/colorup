from collections import namedtuple
from math import sqrt
import os
import cv2
import colortrans
import re

def sort_colors(color_list):
    """
    sort colors by brightness.
    doing it so when i use the colors to make the powerline shell I can be fairly certain
    ill have light colors as foreground and dark colors as backrounds
    :param color_list: list of rgb tuples
    :return: sorted list of rgb colors
    """
    sums = {sum(x): x for x in color_list}
    sorted_keys = sorted(sums.keys())
    sorted_colors = [sums.get(key) for key in sorted_keys]
    return sorted_colors


def rgb_to_xterm(rgb):
    """
    convert rgb tuples to xterm256 ints
    """
    hex_list = ['#%02x%02x%02x' % x for x in rgb]
    xterm_list = [colortrans.rgb2short(x)[0] for x in hex_list]
    return xterm_list


def hex_to_rgb(h):
    return 'rgb'+str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))


def xterm_compatible_rgb(xterm_list):
    """
    take a list of xterm256 ints and convert it to a list that can be used in the dconf command
    :return: list that looks like: ['rgb(x,x,x)','rgb(y,y,y)']
    """
    term_hex = [colortrans.short2rgb(x) for x in xterm_list]
    rgb_list = [hex_to_rgb(h) for h in term_hex]
    return rgb_list


def xterm_remove_dups(xterm_list):
    """
    remove duplicates in the xterm list, so if the extraction comes up with the same colors, the powerline
    wont be boring
    """
    xterm_no_dups = []
    for item in xterm_list:
        if item not in xterm_no_dups:
            xterm_no_dups.append(item)
    return xterm_no_dups

def get_abund_color(color_ratios):
    abund_color = color_ratios.get(max(color_ratios.keys()))
    darker = namedtuple('color', ('r g b'))

    darker.g = (abund_color.g * 0.5)
    darker.b = (abund_color.b * 0.5)
    darker.r = (abund_color.r * 0.5)
    return darker

def calc_color_dist(col1, col2):
    r1, g1, b1 = col1.r, col1.g, col1.b
    r2, g2, b2 = col2.r, col2.g, col2.b

    if (r1+r2)/2 < 128:
        return sqrt(2*(r1-r2)**2+4*(g1-g2)**2+3*(b1-b2)**2)
    else:
        return sqrt(3*(r1-r2)**2+4*(g1-g2)**2+2*(b1-b2)**2)

def brighten(color):
    new = []
    for i in color:
        new.append(int(min(255, i*1.25)))
    return tuple(new)
