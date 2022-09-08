import os

import encoder
import comparator
import Renamer

#QOL
from natsort import natsorted


def main():
    enc = encoder.Encoder()
    reference_images = natsorted(os.listdir(enc.reference_dir), key=lambda y: y.lower())
    reference_encodings = enc.encode(enc.reference_dir, reference_images, "reference")    #these are referenced by name in the code

    images_to_compare = natsorted(os.listdir(enc.comparison_dir), key=lambda y: y.lower())
    comparison_encodings = enc.encode(enc.comparison_dir, images_to_compare, "comparison")    #these are referenced by filemane in the code

    comp = comparator.Comparator()
    ren = Renamer.Renamer()
    ren.rename(enc.comparison_dir, comp.compare(comparison_encodings, reference_encodings))

            



main()
