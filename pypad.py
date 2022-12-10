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


# def setNonBlocking(fd):
#     """
#     Set the file description of the given file descriptor to non-blocking.
#     """
#     flags = fcntl.fcntl(fd, fcntl.F_GETFL)
#     flags = flags | os.O_NONBLOCK
#     fcntl.fcntl(fd, fcntl.F_SETFL, flags)

def run_editor(py_file):
    # with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    py_file.write(initial_message.encode('utf-8'))
    py_file.flush()


    use_tty = sys.stdin.isatty() and not sys.stdout.isatty()
    if use_tty:
        stdout = open("/dev/tty", 'wb')
    else:
        stdout = sys.stdout

    args = EDITOR.split() + [py_file.name]
    print(args)
    subprocess.run(args, shell=False, text=True, stdin=subprocess.PIPE, close_fds=True)

    # do the parsing with `tf` using regular File operations.
    # for instance:
    py_file.seek(0)
    edited_message = py_file.read()

    # curses.setupterm()
    # sys.stdout.write(curses.tigetstr('sgr0').decode("utf-8"))

    os.system('stty ^U')
    os.system('reset')

    # subprocess.run(["clear"], shell=True)
    # os.system("stty sane")

    print("Output:")
    print(edited_message)
    for i in range(5):
        print(i)

    print("From stdin")
    for el in sys.stdin:
        print(el)


def run():
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        run_editor(tf)



# run_1()

run()

import fcntl
from subprocess import Popen, PIPE
import os


def setNonBlocking(fd):
    """
    Set the file description of the given file descriptor to non-blocking.
    """
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)


def run_2():

    args = EDITOR.split() + ["tmp.py"]
    print(args)
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    setNonBlocking(p.stdout)
    setNonBlocking(p.stderr)

    p.stdin.write(b"1\n")
    while True:
        try:
            out1 = p.stdout.read()
            print(out1)
        except IOError:
            continue
        else:
            break
    out1 = p.stdout.read()
    p.stdin.write(b"5\n")
    while True:
        try:
            out2 = p.stdout.read()
            print(out2)
        except IOError:
            continue
        else:
            break


# run_2()
