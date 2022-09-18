import os
from multiprocessing import Pool
import numpy as np
from tkinter import filedialog

import encoder
import comparator
import Renamer

#QOL
from natsort import natsorted


def main():
    thread_count = os.cpu_count() // 2
    reference_dir = get_path("Select reference folder", "Select the folder containing the reference images.")
    comparison_dir = get_path("Select comparison folder", "Select the folder containing the images to be compared.")

    enc = encoder.Encoder()
    reference_images = natsorted(os.listdir(reference_dir), key=lambda y: y.lower())


    chunks = np.array_split(reference_images, thread_count)
    with Pool(thread_count) as p:
        reference_encodings = p.starmap(enc.encode_faces, [(reference_dir, chunk, "reference") for chunk in chunks])
    p.close()
    


    images_to_compare = natsorted(os.listdir(comparison_dir), key=lambda y: y.lower())

    
    chunks = np.array_split(images_to_compare, thread_count)
    with Pool(thread_count) as p:
        comparison_encodings = p.starmap(enc.encode_faces, [(comparison_dir, chunk, "comparison") for chunk in chunks])

    


    comp = comparator.Comparator()
    ren = Renamer.Renamer()
    #make comparison_encodings and reference_encodings into dicts of {filename: encoding} and {name: encoding} respectively.
    comparison_encodings = {k: v for d in comparison_encodings for k, v in d.items()}
    reference_encodings = {k: v for d in reference_encodings for k, v in d.items()}

    ren.rename(comparison_dir, comp.compare(comparison_encodings, reference_encodings))



def get_path(title, text):
    print(text)
    dir = filedialog.askdirectory(title=title, mustexist=True)
    if dir == "":
        exit("No directory selected. Exiting...")
    print(dir)
    return dir


if __name__ == '__main__':
    main()
