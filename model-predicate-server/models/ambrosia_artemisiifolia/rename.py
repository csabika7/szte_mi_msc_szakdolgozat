import os

dir_pos = os.path.join(os.getcwd(), "training_db", "raw", "positive", "resized")
dir_neg = os.path.join(os.getcwd(), "training_db", "raw", "negative", "resized")


def rename_files(directory):
    filenames = os.listdir(directory)

    for i in range(len(filenames)):
        new_name = f'image_{i:04}.png'
        os.rename(directory + filenames[i], directory + new_name)


rename_files(dir_pos)
rename_files(dir_neg)
