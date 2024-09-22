from page_generation import generate_pages_recursive
import os
import shutil


def move_files(from_dir, to_dir):
    dir_list = os.listdir(from_dir)
    if len(dir_list) == 0:
        return
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    os.makedirs(to_dir)
    for file in dir_list:
        source = os.path.join(from_dir, file)
        dest = os.path.join(to_dir, file)
        if os.path.isdir(source):
            move_files(source, dest)
        if os.path.isfile(source):
            shutil.copy(source, dest)

if __name__ == '__main__':
    home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(home_dir, 'static')
    public_dir = os.path.join(home_dir, 'public')
    content_dir = os.path.join(home_dir, 'content')
    move_files(static_dir, public_dir)
    generate_pages_recursive(content_dir, os.path.join(home_dir, 'template.html'), public_dir)

