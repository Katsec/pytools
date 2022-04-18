import os

path = input("输入绝对路径或相对路径：")
for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
        print(os.path.join(dirpath, filename))
