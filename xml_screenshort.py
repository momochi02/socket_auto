import os
import cv2
import xml.etree.ElementTree as ET
import subprocess
from collections import Counter
import testmate
d = testmate.connect()

xmls_dir = 'xmls_dir'
images_dir='images_dir'


def get_ui_xml_and_screenshot():
    xml_txt = d.dump_hierarchy()
    with open(f"{xmls_dir}/window_dump.xmls", "w", encoding="utf-8") as f:
        f.write(xml_txt)
    print("Đã lấy ảnh và XML từ thiết bị.")

