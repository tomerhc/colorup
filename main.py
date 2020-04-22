import sys
sys.path.append('//home//tomerh//PycharmProjects//colorup')
import os
from random import choice
import commands
import color_ops
import img_ops

def pick_img(dir_path):
    files_in_dir = os.listdir(pictures_dir)
    random_pic = pictures_dir + "/" + choice(files_in_dir)
    return random_pic

def sort_for_powerline(extracted_colors):
    sorted_colors = color_ops.sort_colors(extracted_colors)
    xterm_colors = color_ops.rgb_to_xterm(sorted_colors)
    xterm_no_dups = color_ops.xterm_remove_dups(xterm_colors) # this if for powerline-shell
    return xterm_no_dups 

def sort_for_terminal(color_ratios):
    
    abund_color = color_ops.get_abund_color(color_ratios)
    color_dists = {color_ops.calc_color_dist(col, abund_color): col for col in color_ratios.values()}
    dist_sorted_rgb = [color_dists.get(dist) for dist in sorted(color_dists.keys())]
    dist_sorted_rgb = [(x.r,x.g,x.b) for x in dist_sorted_rgb]
    top_five = dist_sorted_rgb[len(dist_sorted_rgb)-5:]
    rest_of_colors = dist_sorted_rgb[:-5]
    syntax_colors = [top_five[1], top_five[3], top_five[4], top_five[0], top_five[2]]
    final_layout = rest_of_colors+syntax_colors
    if len(final_layout) < 16:
        for i in range(16-len(final_layout)):
            final_layout.insert(0, (192,192,192))

    final_layout = list(map(color_ops.brighten, final_layout))
    final_layout = ['rgb'+str(x) for x in final_layout]
    return final_layout

if __name__ == '__main__':
    pictures_dir = "/home/tomerh/Pictures"
    random_pic = pick_img(pictures_dir)
    commands.set_wallpaper(random_pic)
    commands.edit_slim_theme(random_pic)


    img_ops.make_resized_image(img_path=random_pic, factor=50)
    extracted_colors, color_ratios = img_ops.extract_palette()
    
   #term_compat_rgb = color_ops.xterm_compatible_rgb(xterm_no_dups) # this is for terminal palette
    terminal_colors = sort_for_terminal(color_ratios)
    commands.set_term_palette(terminal_colors)

    xterm_no_dups = sort_for_powerline(extracted_colors)
    bg_colors, fg_colors = commands.make_powerline_lud(xterm_no_dups)
    commands.edit_powerline(bg_colors, fg_colors)



