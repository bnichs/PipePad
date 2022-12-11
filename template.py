"""
# Welcome To Pypad!!!

# The results of the command you piped into pypad are available to this pyton script. There are various ways to access them:

## With a function
This allows you to write a simple function to process each line

```
def process_line(line):
    # This function will run on each line you piped in from stdin
    output = sum(int(i) for i in line.split("-"))
    return output
```

## With a generator
This allows you to use the input like a generator conveniently named LINE_GENERATOR
```
for line in pypad.line_generator():
    output = line.split("\t")[3]
    print(output)
```


## With all the data
all_lines = GET_ALL_LINES()



The sample code below will simply print each line from input
"""
import sys

print(sys.path)
from pypad import line_generator
import pypad


print("\n\n\n\n\n\foooooooo\n\n\n\n")


for line in pypad.line_generator():
    print(line)
