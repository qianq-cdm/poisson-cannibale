from pathlib import Path


class FileIO:
    def __init__(self, file_name: str):
        self.path = Path(f"{file_name}.txt")
        self.path.touch(exist_ok=True)

    def read_tuple_list(self):
        file = open(self.path, mode="r+")
        tuple_list = []
        for line in file:
            tuple_element = line.split(";")
            tuple_list.append((tuple_element[0], int(tuple_element[1])))
        file.close()
        return tuple_list

    def write_tuple_list(self, tuple_list):
        file = open(self.path, mode="r+")
        file.truncate(0)
        for tuple_element in tuple_list:
            k = tuple_element[0]
            v = tuple_element[1]
            file.writelines(f"{k};{v}\n")
        file.close()
