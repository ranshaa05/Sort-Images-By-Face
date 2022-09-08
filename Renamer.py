import os

class Renamer:
    def __init__(self):
        self.filenum = {}


    def rename(self, directory, files_to_rename):
        files = list(files_to_rename.keys())
        names = list(files_to_rename.values())
        for file, name in zip(files, names):
            name = str(name).strip("[]'")
            if not name in self.filenum:
                self.filenum[name] = 1
            while os.path.isfile(directory + "/" + str(name).strip("[]'").replace("'", "") + " (" + str(self.filenum[name]) + ")." + file.split(".")[1]):
                self.filenum[name] += 1
            os.rename(directory + "/" + file, directory + "/" + str(name).strip("[]'").replace("'", "") + " (" + str(self.filenum[name]) + ")." + file.split(".")[1])
