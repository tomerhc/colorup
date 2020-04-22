import sys 
sys.path.append('//home//tomerh//PycharmProjects//colorup')
import matplotlib.image as mpimg
import cv2
import os
import colortrans
import colorgram

def make_resized_image(img_path, factor):
    """
    open an image, resize it and save it in the directory under "temp.png"
    i'm resizing it to make the extraction go faster.
    :param img_path: path to image
    :param factor: the hight of the resized image
    """
    image = mpimg.imread(img_path)
    r = factor / image.shape[0]
    dim = (int(image.shape[1] * r), factor)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    mpimg.imsave('temp.png', resized)


def extract_palette(temp_img_path='temp.png',num_colors=16):
    """
    :param temp_img_path:
    :return: list of rgb tuples [(x,x,x),(y,y,y)...]
    """
    gram = colorgram.extract(temp_img_path, num_colors)
    gram_list_ratio = {x.proportion: x.rgb for x in gram}
    gram_list = [x.rgb for x in gram]
    gram_list = [(x.r, x.g, x.b) for x in gram_list]
    os.remove('temp.png')

    return gram_list, gram_list_ratio

