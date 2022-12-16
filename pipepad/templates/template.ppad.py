"""
START_HEADER
pipepad-version: v1
name: main-template
date: 2022-12-11 11:17:23.624458
language: python
END_HEADER
"""
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


%%%FIRST_ELEMENTS%%%
"""
import pipepad

#
for line in pipepad.line_generator():
    tot = sum(int(i) for i in line.split())
    print(tot)
#
#
# for line in pipepad.all_lines():
#     for el in line.split(" "):
#         print(el)
#     pass
#


# There are two ways to save a pipepad:

## First is by registering it.
pipepad.register(repo="samples", name="sum_ints")


## The second is by saving it to a file of your choice
pipepad.save("foo.pad.py")
