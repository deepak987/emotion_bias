import os

def all_images_in_directory(dir_path):
    directory = os.fsencode(dir_path)
    all_files = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"):
            image_path = (os.path.join(dir_path, filename))
            all_files.append(image_path)
    return all_files