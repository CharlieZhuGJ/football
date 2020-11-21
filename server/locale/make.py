# !/usr/bin/env pythons
# -*- coding:utf-8 -*-

import argparse
import os


def generate_translate_file(directory):
    """
    """
    sub_modules = os.listdir(directory)
    for module in sub_modules:
        if not os.path.isdir(module):
            continue

        module_path = os.path.abspath(os.path.join(directory, module))
        po_file_path = os.path.join(module_path, "LC_MESSAGES/lang.po")
        mo_file_path = os.path.join(module_path, "LC_MESSAGES/lang.mo")
        cmd = "msgfmt %s -o %s" % (po_file_path, mo_file_path)
        os.system(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-directory', default="./")
    args = parser.parse_args()
    generate_translate_file(args.directory)
