import argparse
from ast import literal_eval
import pprint

class Dumper():
    def __init__(self):
        pass

    # Recursively digs into the dict and adds values as necessary
    def insert_values(self, local_array, local_dict):
        # Last element in dictionary, so won't be another nested dict
        if len(local_array) == 1:
            local_dict = local_array[0]
        # If the key already exists, pop the first value off the array and continue with the rest
        elif local_array[0] in local_dict.keys():
            key = local_array.pop(0)
            local_dict[key] = self.insert_values(local_array, local_dict[key])
        # If the key doesn't exists, add it as a new nested dict, and continue with the rest
        else:
            local_dict[local_array[0]] = {}
            key = local_array.pop(0)
            local_dict[key] = self.insert_values(local_array, local_dict[key])
        return local_dict
    
    # input: must be array or tuple of strings
    def explodereport(self, input):
        exploded_report = {}
        # Loop over each section, split the string on the pipe, and let the "insert_values"
        # function recursively build the hash tree
        for section in literal_tuple:
            section_array = section.split('|')
            exploded_report = self.insert_values(section_array, exploded_report)
        # Didn't print it in the exact format shown in the prompt, but figured that was just pseudocode
        # This prints it in a nice way still. Could have done this without pprint, but this was easier 
        # and didn't really seem like part of the challenge.
        pprint.pprint(exploded_report)

'''
# THIS IS ALL TEST INPUT, UNCOMMENT TO USE

# Only argument is the file with the input text, which is required
parser = argparse.ArgumentParser(description='create dictionary')
parser.add_argument('--input_file', required=True, help='file that contains input for the program')
args = parser.parse_args()

# Get the text from the file
with open(args.input_file, 'r') as input_file:
    input = input_file.read()

# Convert the string to a tuple so we can use it. Could do some string manipulation, but this is more direct.
literal_tuple = literal_eval(input)
dumper = Dumper()
dumper.explodereport(literal_tuple)
'''