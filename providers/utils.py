import numpy as np

def get_gradient_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T

def get_gradient_3d(width, height, start_list, stop_list, is_horizontal_list):
    result = np.zeros((height, width, len(start_list)), dtype=np.float)

    for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)

    return result
    
    
'''
Converts web colors strings to triplets
in: #B4FBB8
out:(180, 251, 184)
'''
def color_hex2triplet(hex):
  h = hex.lstrip('#')
  return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
  
def color_mult(triplet, factor):
  (a,b,c) = triplet
  return (int(a*factor), int(b*factor), int(c*factor))