import pygame  
import os 


def import_img_convert(path="img/nyanCat"): 

    if path[-1] != "/" : path += "/" 
    return [pygame.image.load(path + fname).convert() for fname in os.listdir(path) if fname[-4:] == ".png" or fname[-4:] == ".jpg" ]  


def import_img_convert_alpha(path="img/nyanCat"): 

    if path[-1] != "/" : path += "/" 
    return [pygame.image.load(path + fname).convert_alpha() for fname in os.listdir(path) if fname[-4:] == ".png" or fname[-4:] == ".jpg"  ] 


