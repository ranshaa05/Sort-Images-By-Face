import face_recognition as fr
from tkinter import filedialog
import os

#QOL
from natsort import natsorted

print("Select person to catagorize:")
known_image = fr.load_image_file(filedialog.askopenfilename(title="Select image", filetypes=(("jpeg files", "*.jpg"), ("PNG files", "*.png*"), ("all files", "*.*"))))
known_encoding = fr.face_encodings(known_image)[0]
name = input("Name of person in image:\n").title()

print("select folder to compare against:")
folder = filedialog.askdirectory(title="Select folder", mustexist=True)


files = natsorted(os.listdir(folder), key=lambda y: y.lower())
filenum = 1


for file in files:
    if not "." in file or file.split(".")[1] not in ["jpg", "jpeg", "png", "webp"]:
        continue

    print(file)
    file_path = os.path.join(folder + "/", file)
    unknown_image = fr.load_image_file(file_path)
    unknown_encodings = fr.face_encodings(unknown_image)

    if unknown_encodings:
        num_of_faces_in_image = len(unknown_encodings)
        for face in unknown_encodings:
            same_person = fr.compare_faces([known_encoding], unknown_encodings[num_of_faces_in_image - 1], tolerance=0.55)
            num_of_faces_in_image -= 1
            if same_person[0]:
                print(f"This is {name}.")
                os.rename(file_path, folder + "/" + name + " " + str(filenum) + "." + file.split(".")[1])
                filenum += 1
                break

            else:
                print("This is a different person.")

    else:
        print("No faces detected in image.")

print(f"Done catagorizing files. Found {filenum -1} identical faces.")
            




