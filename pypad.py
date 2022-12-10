import fileinput


# Show the command you ran, show the instructions

# Put stdin in a variable that is easily accessible
# Stdout comes from the output of this script when saved

import subprocess
import sys, tempfile, os
from subprocess import call

EDITOR = os.environ.get('EDITOR', 'vim')  # that easy!
EDITOR = "vim -n -E"
EDITOR = "vim "

initial_message = 'hello there'  # if you want to set up the file somehow

with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    tf.write(initial_message.encode('utf-8'))

    tf.flush()
    args = EDITOR.split() + [tf.name]
    print(args)
    subprocess.run(args, shell=False, stdin=subprocess.PIPE)



    # do the parsing with `tf` using regular File operations.
    # for instance:
    tf.seek(0)
    edited_message = tf.read()

    # subprocess.run(["clear"], shell=True)
    os.system("stty sane")

    print("Output:")
    print(edited_message)
    for i in range(100):
        print(i)



