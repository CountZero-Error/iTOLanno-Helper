from iTOL_Main import generalFunc
import pandas as pd
import argparse
import random

class ColorStrip(generalFunc):
    def __init__(self, fi, fo, sep, ID, label, strip_color=None, dataset_label='label1'):
        super().__init__(fi, fo, sep)

        self.ID = ID
        self.label = label
        self.strip_color = strip_color
        self.annotation_prefix = open("../templates/dataset_color_strip_template.txt").read().replace('label1', dataset_label)

    # main
    def generator(self):
        print('[*] Reading data...')
        df = pd.read_csv(self.fi, sep=self.sep)

        # Leaf_ID,strip_color,label

        # Adding content
        leaf_num = df.shape[0]
        color_strip_info = {'leaf_ID': df.loc[:, self.ID][:],
                            'color_strip': [],
                            'label': df.loc[:, self.label][:]}

        # Strip color
        if self.strip_color == None:
            color_strip = {curr_label: self.generate_random_color_code() for curr_label in set(df.loc[:, self.label])}
        else:
            color_strip = self.get_relations(self.strip_color)
        color_strip_info['color_strip'] = [color_strip[df.loc[i, self.label]] for i in range(leaf_num)]

        print("[*] Generating output files...")
        self.write_fo(pd.DataFrame(color_strip_info), self.annotation_prefix)
        print('[*] Done.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--FILE_INPUT', required=True, type=str)
    parser.add_argument('-O', '--FILE_OUTPUT_PATH', required=True, type=str, help="File name is required.")
    parser.add_argument('-SEP', '--SEPARATOR', default=",", help="Default is ',', if is tab, type tab.")
    parser.add_argument('-ID', '--ID', required=True, type=str)
    parser.add_argument('-L', '--LABEL', required=True, type=str)
    parser.add_argument('-DSL', '--DATASET_LABEL', default='label1', type=str)
    parser.add_argument('-SC', '--STRIP_COLOR', default=None, type=str, help="STRIP_COLOR option need a relationship file, check relationship_template.txt file.")

    args = parser.parse_args()
    fi = args.FILE_INPUT
    fo = args.FILE_OUTPUT_PATH
    sep = args.SEPARATOR
    ID = args.ID
    label = args.LABEL
    dataset_label = args.DATASET_LABEL
    strip_color = args.STRIP_COLOR

    if sep.lower() == 'tab':
        sep = '\t'

    annotate = ColorStrip(fi, fo, sep, ID, label, strip_color, dataset_label)
    annotate.generator()
