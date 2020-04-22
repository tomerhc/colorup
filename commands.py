import os
import re

def make_powerline_lud(xterm):
    """
    makes a lookup dictionary to be used in the edit of powerline-shell theme
    """
    backgrounds = ['USERNAME_BG', 'HOSTNAME_BG', 'PATH_BG']
    foregrounds = ['CWD_FG', 'USERNAME_FG', 'SEPARATOR_FG']
    bg_colors = {bg: col for bg, col in zip(backgrounds, xterm[::-1])}
    fg_colors = {fg: col for fg, col in zip(foregrounds, xterm)}
    fg_colors['PATH_FG'] = fg_colors["USERNAME_FG"]
    fg_colors['HOSTNAME_FG'] = fg_colors["USERNAME_FG"]
    return bg_colors, fg_colors


def insert_to_powerline(field, color, text):
    exp = field + ' = (\d{1,3})'
    rpl = field + ' = ' + color
    final_text = re.sub(exp,rpl,text)
    return final_text


def edit_powerline( bg_colors, fg_colors, config_file_path='//home//tomerh//.config//powerline-shell//themes//scripted.py'):
    with open(config_file_path, 'r') as f:
        content = f.read()

    res = content
    for dct in [bg_colors, fg_colors]:
        for k, v in dct.items():
            res = insert_to_powerline(k, v, res)

    with open(config_file_path, 'w') as f:
        f.write(res)


def edit_slim_theme(img_path):
    img_path = img_path.replace('//','/')
    command = 'sudo //home//tomerh//slim_change.sh {img_path}'.format(img_path=img_path)
    os.system(command)


def set_wallpaper(pic_path):
    command = 'feh --bg-scale ' + pic_path
    os.system(command)


def set_term_palette(rgb_list):
    command = "dconf write /org/gnome/terminal/legacy/profiles:/:b1dcc9dd-5262-4d8d-a863-c897e6d979b9/palette "
    command_colors = '"[' + ', '.join(["'" + x + "'" for x in rgb_list]) + ']"'
    os.system(command + command_colors)

