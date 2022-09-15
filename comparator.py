import face_recognition as fr

class Comparator:
    def __init__(self):
        self.recognised_people = []
        self.names = []
        self.file_name_binder = {}
        self.num_of_catagorized_faces = 0
    
    def compare(self, encoded_faces_to_compare, encoded_reference_faces):
        self.names = encoded_reference_faces.keys()
        
        for face in encoded_faces_to_compare:
            for name in self.names: 
                same_person = fr.compare_faces(encoded_reference_faces[name][0], encoded_faces_to_compare[face], tolerance=0.6) #returns a list of booleans
                if any(same_person):
                    self.recognised_people.append(name)
                    self.num_of_catagorized_faces += 1
                    if self.num_of_catagorized_faces == len(encoded_faces_to_compare[face]):
                        break
            if self.recognised_people:
                self.file_name_binder[face] = self.recognised_people #puts face in recognised people for this picture
                self.recognised_people = []
                self.num_of_catagorized_faces = 0

            
            
        return self.file_name_binder


            