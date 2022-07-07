import os
from merge import process

if __name__ == '__main__':

    file_path = 'iris'
    
    names = os.listdir(file_path)

    for name in names:
        if name == 'Thumbs.db': continue # 跳过缩略图数据库
        process(file_path, 'out', name)
        # print(name)
