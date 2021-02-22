# -*- coding: utf-8 -*-
# @Time    : 2020/5/27 14:17
# @Author  : AP
# @File    : file_helper.py
# @Software: PyCharm
from io import BytesIO


def liner(line: list or tuple, separator: str = ",") -> str:
    this_line = ""
    for index, i in enumerate(line):
        if index < len(line) - 1:
            this_line += str(i) + separator
        else:
            this_line += str(i) + "\n"

    return this_line


def dump_csv_bytes(lines: list, separator: str = ",", header_or_not=True) -> bytes:
    if lines:
        txt_bio = BytesIO()
        if header_or_not:
            txt_bio.write(liner(lines[0], separator=separator).encode("utf-8-sig"))
            del lines[0]
        for i in lines:
            txt_bio.write(liner(i, separator=separator).encode("utf-8-sig"))
        return txt_bio.getvalue()


def dump_txt_bytes(lines: list, separator: str = "|", header_or_not=False) -> bytes:
    txt_bio = BytesIO()
    if lines:
        if header_or_not:
            txt_bio.write(liner(lines[0], separator=separator).encode("utf-8-sig"))
            del lines[0]
        for i in lines:
            txt_bio.write(liner(i, separator=separator).encode("utf-8-sig"))
    return txt_bio.getvalue()
