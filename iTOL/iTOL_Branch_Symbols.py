from iTOL_Main import generalFunc
import pandas as pd
import argparse
import random

class BranchSymbols(generalFunc):
    def __init__(self, fi, fo, sep, ID, label, dataset_label='example symbols', symbol=None, symbol_size=3, symbol_color=None, fill_color=1, symbol_position=1):
        super().__init__(fi, fo, sep)

        self.ID = ID
        self.label = label
        self.dataset_label = dataset_label
        self.annotation_prefix = open("../templates/dataset_symbols_template.txt").read().replace('example symbols', dataset_label)

        self.symbol = symbol # input should be a txt file contain relationship between label and symbol, check relationship_template under current directory
        self.symbol_size = symbol_size
        self.symbol_color = symbol_color # same as symbol
        self.fill_color = fill_color
        self.symbol_position = symbol_position

    # main
    def generator(self):
        print('[*] Reading data...')
        df = pd.read_csv(self.fi, sep=self.sep)

        # Leaf_ID,symbol,symbol_size,symbol_color,fill_color,symbol_position,label
        #
        # symbol should be a number between 1 and 5:
        # 1: rectangle
        # 2: circle
        # 3: star
        # 4: right pointing triangle
        # 5: left pointing triangle
        # 6: checkmark
        #
        # fill color: 1
        # Don't fill color: 0

        # Adding content
        leaf_num = df.shape[0]
        symbol_info = {'leaf_ID': df.loc[:, self.ID][:],
                       'symbol': [],
                       'symbol_size': [self.symbol_size for i in range(leaf_num)],
                       'symbol_color': [],
                       'fill_color': [self.fill_color for i in range(leaf_num)],
                       'symbol_position': [self.symbol_position for i in range(leaf_num)],
                       'label': df.loc[:, self.label][:]}

        # Symbol
        if self.symbol == None:
            symbols = {curr_label: random.randint(1, 5) for curr_label in set(df.loc[:, self.label])}
        else:
            symbols = self.get_relations(self.symbol)
        symbol_info['symbol'] = [symbols[df.loc[i, self.label]] for i in range(leaf_num)]

        # Symbol color
        if self.symbol_color == None:
            symbols_color = {curr_label: self.generate_random_color_code() for curr_label in set(df.loc[:, self.label])}
        else:
            symbols_color = self.get_relations(self.symbol_color)
        symbol_info['symbol_color'] = [symbols_color[df.loc[i, self.label]] for i in range(leaf_num)]

        print("[*] Generating output files...")
        self.write_fo(pd.DataFrame(symbol_info), self.annotation_prefix)
        print('[*] Done.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--FILE_INPUT', required=True, type=str)
    parser.add_argument('-O', '--FILE_OUTPUT', required=True, type=str, help="File name is required.")
    parser.add_argument('-SEP', '--SEPARATOR', default=",", help="Default is ',', if is tab, type tab.")
    parser.add_argument('-ID', '--ID', required=True, type=str, help="The column name of ID.")
    parser.add_argument('-L', '--LABEL', required=True, type=str, help="The column name of label.")
    parser.add_argument('-DSL', '--DATASET_LABEL', default='example symbols', type=str)
    parser.add_argument('-SYMBOL', '--SYMBOL', default=None, type=str, help="Symbol option need to be relationship file, check relationship_template.txt file.")
    parser.add_argument('-SYMBOL_S', '--SYMBOL_SIZE', default=3, type=int)
    parser.add_argument('-SYMBOL_C', '--SYMBOL_COLOR', default=None, type=str, help="Symbol option need a relationship file, check relationship_template.txt file.")
    parser.add_argument('-FC', '--FILL_COLOR', default=1, choices=[0, 1], type=int, help="1 fill color, 0 don't fill color.")
    parser.add_argument('-SYMBOL_P', '--SYMBOL_POSITION', default=1, type=int)

    args = parser.parse_args()
    fi = args.FILE_INPUT
    fo = args.FILE_OUTPUT
    sep = args.SEPARATOR
    ID = args.ID
    label = args.LABEL
    dataset_label = args.DATASET_LABEL
    symbol = args.SYMBOL
    symbol_size = args.SYMBOL_SIZE
    symbol_color = args.SYMBOL_COLOR
    fill_color = args.FILL_COLOR
    symbol_position = args.SYMBOL_POSITION


    if sep.lower() == 'tab':
        sep = '\t'

    annotate = BranchSymbols(fi, fo, sep, ID, label, dataset_label, symbol, symbol_size, symbol_color, fill_color, symbol_position)
    annotate.generator()
