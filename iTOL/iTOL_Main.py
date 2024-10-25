from time import time
import random

class generalFunc:
    def __init__(self, fi, fo, sep):
        # fi should contain at least 2 columns:
        # Leaf_ID,Leaf_Label
        self.fi = fi
        self.fo = fo
        self.sep = sep

        random.seed(time())

    def get_relations(self, file):
        relations = {}
        with open(file, 'r') as filo:
            # label-symbol
            for line in filo:
                curr_label = line.split('-')[0]
                curr_symbol = line.split('-')[1]

                relations.setdefault(curr_label)
                relations[curr_label] = curr_symbol

        return relations

    def generate_random_color_code(self):
        # Generate three random numbers between 0 and 255
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)

        # Convert the RGB values to a hexadecimal color code
        color_code = "#{:02X}{:02X}{:02X}".format(R, G, B)

        return color_code

    def write_fo(self, df, annotation_prefix):
        with open(self.fo, 'w') as out:
            out.write(f'{annotation_prefix}\n')
            for i in range(df.shape[0]):
                curr_line = ','.join(list(map(str, list(df.iloc[i, :]))))
                out.write(curr_line + '\n')
