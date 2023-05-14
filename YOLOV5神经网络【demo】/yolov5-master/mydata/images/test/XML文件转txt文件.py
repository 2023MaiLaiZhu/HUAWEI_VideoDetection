import os
import shutil

'***转换xml标注文件为txt格式，无法直接运行***'

from lxml.etree import Element, SubElement, tostring, ElementTree

import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join

classes = ["normal_face", "close_eye","yawn","calls","turn_around"]  # 类别


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open('../label_test_images/%s.xml' % (image_id), encoding='UTF-8')#xml文件

    out_file = open('../yolo_test_dataset/labels/test/%s.txt' % (image_id), 'w')  # 生成txt格式文件, 保存在yolov7训练所需的数据集路径中
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        print(cls)
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')



source_address="../label_test_images"
des_address_img="../yolo_test_dataset/images/test"
des_address_lab="../yolo_test_dataset/labels/test"
imagelist=os.listdir(source_address)
print(imagelist)
for name in imagelist:
    if name[-1]=="l":#xml文件
        print("xml files")
        label_name = name.split('.')[0]#文件名
        convert_annotation(label_name)

    else:
        print("png files")
        src_path = os.path.join(source_address, name)  # 原文件夹
        dst_path = os.path.join(des_address_img, name)
        shutil.copyfile(src_path, dst_path)
print("finish")

