"""
# Welcome To Pypad!!!

# The results of the command you piped into pypad are available to this pyton script. There are various ways to access them:

1) With a function
This allows you to write a simple function to process each line

def process_line(line):
    # This function will run on each line you piped in from stdin
    output = sum(int(i) for i in line.split("-"))
    return output


2) With a generator
This allows you to use the input like a generator conveniently named LINE_GENERATOR

for line in LINE_GENERATOR:
    output = line.split("\t")[3]
    print(output)



3) With all the data
all_lines = GET_ALL_LINES()


"""
