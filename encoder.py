
import filetype as ft
import face_recognition as fr
import os


class Encoder:
    def __init__(self):
        self.loading_progress = 0
        self.encoded_reference_images = {}
        self.encoded_comparison_images = {}
        

    def encode_faces(self, directory, files_to_encode, reference_or_comparison):
        for file in files_to_encode:
            if os.path.isdir(directory + "\\" + file) or not ft.is_image(directory + "\\" + file):
                continue
            loaded_image = fr.load_image_file(directory + "/" + file)
            encoded_faces = fr.face_encodings(loaded_image)
            self.loading_progress += 1
            print(f"Encoding {reference_or_comparison} images... {self.loading_progress}/{len(files_to_encode)} ({round(self.loading_progress / len(files_to_encode) * 100)}%) images encoded.\r", end="")
            if self.check_picture_validity(encoded_faces, file, reference_or_comparison):
                if reference_or_comparison == "comparison":
                    self.encoded_comparison_images[file] = encoded_faces #assign comparison file's name to its encoded faces

                elif reference_or_comparison == "reference":
                    name = (file.split(".")[0]).title()
                    self.encoded_reference_images[name] = encoded_faces #assign person's name to reference picture
                
                else:
                    raise Exception("Invalid reference_or_comparison argument.")

        self.loading_progress = 0
        if reference_or_comparison == "reference":
            return self.encoded_reference_images
        elif reference_or_comparison == "comparison":
            return self.encoded_comparison_images
        else:
            raise Exception("Invalid reference_or_comparison argument.")
        

    def check_picture_validity(self, encoded_faces, filename, reference_or_comparison):
        if reference_or_comparison == "comparison":
            if len(encoded_faces) > 0:
                return True
            else:
                return False

        elif reference_or_comparison == "reference":
            if  len(encoded_faces) == 1:
                return True
            elif len(encoded_faces) > 1:
                raise Exception("Multiple faces detected in '" + filename + ".' Please use a different file with only one face.")
        
            else:
                input(f"Could not find a face in file '{filename}'. Press enter to continue.")
                return
        else:
            raise Exception("Invalid reference_or_comparison argument.")
        
        
        




        