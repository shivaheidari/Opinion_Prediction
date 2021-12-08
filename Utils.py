import csv
import glob
from pathlib import Path


class Utils(object):
    def __init__(self):
        self.name = 1

    def save_list_2(self, lst, filename, header):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(lst)

    def get_al_lfilename_in_folder(self, format, path, out_filename):
        files_path = [f for f in glob.glob(path + "**/*." + format, recursive=False)]
        lst = []
        for file in files_path:
            lst.append(Path(file).stem)
        self.save_list(lst, out_filename)
        return lst

    def csv_read(self, filename):
        list_of_rows = []
        with open(filename, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            list_of_rows = list(csv_reader)
        return list_of_rows

    def save_list(self, lst, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for item in lst:
                writer.writerow([item])

    def csv_read_one_col(self, filename):
        results = []
        with open(filename, newline='') as inputfile:
            for row in csv.reader(inputfile):
                results.append(row[0])
        return results

    def save_list_as_dictionary(self, lst, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for item in lst:
                writer.writerow([item[0], item[1:None]])

    def save_list_as_reverse_dictionary(self, lst, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for item in lst:
                for value in item[1:None]:
                    writer.writerow([value, item[0]])

    def load_dictionary_with_list_value(self, filename):
        result = {}
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            result = {rows[0]: rows[1] for rows in reader}
        return result
