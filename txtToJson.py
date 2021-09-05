# -*- coding: utf-8 -*-
"""
Created on Sat Sep 4 12:01:02 2021
@author: deniz.kilic
"""

import os
from skimage import io
import json
from skimage import color
import cv2

def append_to_json(json_struct,id,x,y,width,height,class_num):
    json_struct['samples'].append({
        'idx': id,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "class": class_num
    })
    return json_struct

def write_to_json(json_file_name,data):
    with open(json_file_name, 'w') as json_file:
        json.dump(data, json_file,indent=2)
    json_file.close()



input_path = '//txt_files' # Edit here
images_path = '//image_files' # Edit here
output_path = '//output_path' # Edit here
json_struct = {
  "samples": [{
    "idx":      { "type": "string" },
    "x": { "type": "string" },
    "y": { "type": "string"},
    "width" : {"type" : "string"},
    "height" : {"type" : "string"},
      "class" : {"type" : "string"}
  }]
}

image_list = os.listdir(images_path)
txt_list = os.listdir(input_path)
print(txt_list)
image_list.remove('Thumbs.db') #unkown hidden file, removed from list
image_format = '.jpg' # Edit this part wrt the format of images

for txt in txt_list:
    if((os.path.isdir(os.path.join(input_path,txt)))):
        continue
    filename, file_extension = os.path.splitext(txt)
    f = open(os.path.join(input_path,txt))
    lines = f.readlines()
    id = 1
    json_struct["samples"].clear()
    for line in lines:
        image = io.imread(os.path.join(images_path, filename + image_format))

        im_width = image.shape[1]
        im_height = image.shape[0]

        line_arguments = line.split()
        class_num = line_arguments[0]
        width = str(float(line_arguments[3]) * im_width)
        height = str(float(line_arguments[4]) * im_height)
        x_min = str(float(line_arguments[1]) * im_width - float(width-1)/2)
        y_min = str(float(line_arguments[2]) * im_height - float(height-1)/2)
        json_struct = append_to_json(json_struct,str(id),x_min,y_min,width,height,class_num)
        id += 1
    write_to_json(os.path.join(output_path,filename+'.json'),json_struct)

    f.close()
