import face_recognition as fr
from tkinter import filedialog
import os

#QOL
from natsort import natsorted

print("Select folder of reference pictures:")
reference_dir = filedialog.askdirectory(title="Select folder", mustexist=True)
print(reference_dir)
known_images = natsorted(os.listdir(reference_dir))


named_encodings = {}
loading_progress = 0

for i in known_images:  #load and encode all known images
    if not "." in i or i.split(".")[1] not in ["jpg", "jpeg", "png", "webp"]:
        continue
    name = (i.split(".")[0]).title()
    loaded_image = fr.load_image_file(reference_dir + "/" + i)
    known_encoding = fr.face_encodings(loaded_image)
    named_encodings[name] = known_encoding
    loading_progress += 1
    print(f"{loading_progress}/{len(known_images)} images loaded\r", end="")



print("select folder to compare against reference:")
comparison_dir = filedialog.askdirectory(title="Select folder", mustexist=True)
print(comparison_dir)
files_to_compare = natsorted(os.listdir(comparison_dir), key=lambda y: y.lower())

catagorize_progress = 0
num_of_catagorized_faces = 0
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
            if unchecked_faces < 1: #if all faces im image have been checked
                break
            same_person = fr.compare_faces(named_encodings[name][0], unknown_encodings, tolerance=0.57) #lower is more precise
            if any(same_person): #if any of the faces in image match any person in the database
                # print(f"Found {name}.\n")
                recognized_people.append(name) #add name to list of recognized people in image
                unchecked_faces -= 1
            

        
        if recognized_people:
            recognized_people = str(recognized_people).strip("[]'").replace("'", "")
            for i in range(len(files_to_compare)):
                try:
                    os.rename(file_path, f"{comparison_dir}/{recognized_people} {i+1}.{file.split('.')[1]}")
                    break
                except FileExistsError:
                    pass
            num_of_catagorized_faces += 1
                 
    else:
        pass
        # print("No faces detected in image.")
    
    catagorize_progress += 1
    print(f"{catagorize_progress}/{len(files_to_compare)} images catagorized.\r", end="")
    

print(f"Done catagorizing files. Found {num_of_catagorized_faces} matching faces.")
            




