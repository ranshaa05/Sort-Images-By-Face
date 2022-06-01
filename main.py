import face_recognition as fr
from tkinter import filedialog
import os

#QOL
from natsort import natsorted

print("Select folder of reference pictures:")
reference_dir = filedialog.askdirectory(title="Select reference folder", mustexist=True)
print(reference_dir)
known_images = natsorted(os.listdir(reference_dir))

print("select folder to compare against reference:")
comparison_dir = filedialog.askdirectory(title="Select destination folder", mustexist=True)
print(comparison_dir)
files_to_compare = natsorted(os.listdir(comparison_dir), key=lambda y: y.lower())


named_encodings = {}
loading_progress = 0

for i in known_images:  #load and encode all known images
    if not "." in i or i.split(".")[1] not in ["jpg", "jpeg", "png", "webp"]:
        continue
    name = (i.split(".")[0]).title()
    loaded_image = fr.load_image_file(reference_dir + "/" + i)
    known_encoding = fr.face_encodings(loaded_image)
    if len(known_encoding) >1:
        print(f"File '{i}' has multiple faces in it. Please use a different file with only one face.")
        exit()
    
    if not len(known_encoding) == 0:
        named_encodings[name] = known_encoding
    else:
        input(f"Could find a face in file '{i}'. Press enter to continue.")
    loading_progress += 1
    print(f"{loading_progress}/{len(known_images)} ({round(loading_progress / len(known_images) * 100)}%) reference images loaded.\r", end="")

print("")

catagorize_progress = 1
num_of_catagorized_faces = 0
existing_filenames = {} #to avoid overwriting files and keep track of how many pics of with the same people have been catagorized.

for file in files_to_compare:
    if not "." in file or file.split(".")[1] not in ["jpg", "jpeg", "png", "webp"]: #if not image file
        continue
    # print(f"Scanning {file}...")
    file_path = comparison_dir + "/" + file
    unknown_image = fr.load_image_file(file_path)
    unknown_encodings = fr.face_encodings(unknown_image)
    recognized_people = []
    
    if unknown_encodings:
        unchecked_faces = len(unknown_encodings)
        # print(f"{unchecked_faces} face(s) found in image")

        for name in named_encodings: #for each person in the database
            if unchecked_faces == 0: #if all faces in image have been checked
                break
            same_person = fr.compare_faces(named_encodings[name][0], unknown_encodings, tolerance=0.57) #lower is more precise
            if any(same_person): #if any of the faces in image match any person in the database
                # print(f"Found {name}.\n")
                recognized_people.append(name) #add name to list of recognized people in image
                unchecked_faces -= 1

        if recognized_people:
            recognized_people = str(recognized_people).strip("[]'").replace("'", "")
            if recognized_people in existing_filenames:
                existing_filenames[recognized_people] += 1
            else:
                existing_filenames[recognized_people] = 1

            while os.path.isfile(f"{comparison_dir}/{recognized_people} {existing_filenames[recognized_people]}{os.path.splitext(file)[1]}"):
                existing_filenames[recognized_people] += 1 #make sure this filename is available
            try:
                os.rename(file_path, f"{comparison_dir}/{recognized_people} {existing_filenames[recognized_people]}{os.path.splitext(file)[1]}")
            except FileExistsError:
                print(f"File '{file}' already exists. Skipping...") #just in case
                continue
                 #TODO: does not account for files that are already in the folder with the same name or files that have been renamed while the program is running.
            num_of_catagorized_faces += 1
                
    else:
        pass
        # print("No faces detected in image.")

    
    catagorize_progress += 1
    print(f"{catagorize_progress}/{len(files_to_compare)} ({round(catagorize_progress / len(files_to_compare) * 100)}%) files proscessed.\r", end="")
    

print(f"\nDone catagorizing files. Found {num_of_catagorized_faces} matching faces.")
            




