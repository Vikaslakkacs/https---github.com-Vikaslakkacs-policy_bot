import os

def read_file(file_list):
    text=''
    for file in file_list:
        if file.name.endswith(".txt"):
            text=text + "/n/n"+ file.read().decode("utf-8")
        else:
            raise Exception (
                "Un-supported file format, only txt files are allowed."
            )
    return text
        