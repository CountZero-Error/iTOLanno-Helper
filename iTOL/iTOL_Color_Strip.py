import pandas as pd
import argparse
import random
import os

class ColorStrip:
    def __init__(self, fi, fo, sep):
        self.fi = fi
        self.fo = fo
        self.sep = sep
        self.annotation_prefix = read("./templates/dataset_color_strip_template.txt")

    def generate_random_color_code(self):
        # Generate three random numbers between 0 and 255
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        
        # Convert the RGB values to a hexadecimal color code
        color_code = "#{:02X}{:02X}{:02X}".format(R, G, B)
        
        return color_code
    
    def write_fo(self, df, colors):
        # Output file format
        # Leaf_ID   Leaf_Color  Leaf_Label
        # 123   #456727 number
        # hello #C23B57 str
        raw_df = {"Leaf_ID": df["Leaf_ID"][:],
                  "Leaf_Color": [],
                  "Leaf_Label": df["Leaf_Label"][:]}

        for elm in raw_df["Leaf_Label"]:
            raw_df["Leaf_Color"].append(colors[elm])

        new_df = pd.DataFrame(raw_df)
        
        # Color table in csv file
        print('[*] Generating color_table.csv...')
        new_df.to_csv(os.path.join(self.fo, "color_table.csv"), sep='\t', index=False)

        # Annotation file
        print('[*] Generating color_strip.txt...')
        with open(os.path.join(self.fo, "color_strip.txt"), 'w') as out:
            out.write(f'{self.annotation_prefix}\n')
            for i in range(new_df.shape[0]):
                out.write(f'{new_df["Leaf_ID"][i]} {new_df["Leaf_Color"][i]} {new_df["Leaf_Label"][i]}\n')

    # main
    def generator(self):
        # Input file format
        # Leaf_ID   Leaf_Label
        # 123   number
        # hello str
        print('[*] Reading data...')
        df = pd.read_csv(self.fi, sep=self.sep)
        
        # Labels
        labels = set()
        for elm in df["Leaf_Label"]:
            labels.add(elm)
        
        # Add color
        print('[*] Assigning color...')
        colors = {}
        color_used = []
        for elm in labels:
            if elm.lower()  == 'fibroblast':
                colors[elm] = '#f44336'
            
            else:
                while True:
                    color = self.generate_random_color_code()

                    if color not in color_used:
                        colors[elm] = color
                        break
        
        print("[*] Generating output files...")
        self.write_fo(df, colors)
        print('[*] Done.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--FILE_INPUT', required=True, type=str)
    parser.add_argument('-O', '--FILE_OUTPUT_PATH', required=True, type=str, help="File name is not required.")
    parser.add_argument('-SEP', '--SEPARATOR', default="\t", help="Default is TAB.")
    args = parser.parse_args()
    fi = args.FILE_INPUT
    fo = args.FILE_OUTPUT_PATH
    sep = args.SEPARATOR

    annotate = ColorStrip(fi, fo, sep)
    annotate.generator()
