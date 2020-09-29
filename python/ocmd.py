#!/usr/bin/env python

import json
import os
import sys
from octorest import OctoRest
import tty
import termios

import argparse

parser = argparse.ArgumentParser(description='Move around 3D Printer via Octoprint')
parser.add_argument('--xmin', dest='xmin', default=10, type=int,
                    help='x-axis min for mesh')
parser.add_argument('--xmax', dest='xmax', default=190, type=int,
                    help='x-axis max for mesh')
parser.add_argument('--ymin', dest='ymin', default=10, type=int,
                    help='y-axis min for mesh')
parser.add_argument('--ymax', dest='ymax', default=180, type=int,
                    help='y-axis max for mesh')
parser.add_argument('--zup', dest='zup', default=10, type=int,
                    help='how much to rise z during moves')
parser.add_argument('--lines', dest='lines', default=3, type=int,
                    help='how many lines in x and y direction')

args = parser.parse_args()

cfg = os.environ["HOME"] + "/.pxl/octo-piprint"
print("cfg:",cfg)

with open(cfg) as json_file:
    ocfg = json.load(json_file)
    #print("ocfg:",ocfg)

def make_client():
    try:
        client = OctoRest(url=ocfg['url'],apikey=ocfg['apikey'])
        return client
    except Exception as e:
        print(e)

def get_version():
    client = make_client()
    message = "You are using OctoPrint v" + client.version['server'] + "\n"
    return message

def get_printer_info():
    try:
        client = OctoRest(url=ocfg['url'],apikey=ocfg['apikey'])
        message = ""
        message += str(client.version) + "\n"
        message += str(client.job_info()) + "\n"
        printing = client.printer()['state']['flags']['printing']
        if printing:
            message += "Currently printing!\n"
        else:
            message += "Not currently printing...\n"
        return message
    except Exception as e:
        print(e)

def main():
    c = make_client()
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    old[3] = old[3] | termios.ECHO
    tty.setcbreak(sys.stdin)
    print(args)
    print("lines:",args.lines)
    print("1 mm up=q / down=a")
    print("0.1 mm up=w / down=s")
    print("home all = z")
    print("Press x or X to exit...")
    initGcode = "G21\nG90\nG0 F1000\n"
    c.gcode(initGcode)
    x_pos = args.xmin
    y_pos = args.ymin
    x_no = 0
    y_no = 0
    z_pos = args.zup
    while True:
        key = ord(sys.stdin.read(1))
        print("key:",key)
        if key==120 or key==88: # x
            print("X/x pressed exiting")
            break
        elif key==122: # z
            c.gcode("G28\n")
        elif key==113: # q
            if (z_pos<30.0):
                z_pos+=1.0
                c.gcode("G0 Z{}".format(z_pos))
        elif key==97:  # a
            if (z_pos>0.0):
                z_pos-=1.0
                c.gcode("G0 Z{}".format(z_pos))
        elif key==119: # w
            if (z_pos<30.0):
                z_pos+=0.1
                c.gcode("G0 Z{}".format(z_pos))
        elif key==115: # s
            if (z_pos>0.0):
                z_pos-=0.1
                c.gcode("G0 Z{}".format(z_pos))
        elif key==27:
            keyB = ord(sys.stdin.read(1))
            keyC = ord(sys.stdin.read(1))
            print("ESC:",key,keyB,keyC)
            if keyB==91 and keyC==65: # up
                if y_no < (args.lines-1):
                    y_no += 1
            elif keyB==91 and keyC==66: # down
                if y_no > 0:
                    y_no -= 1
            elif keyB==91 and keyC==68: # left
                if x_no > 0:
                    x_no -= 1
            elif keyB==91 and keyC==67: # right
                if x_no < (args.lines-1):
                    x_no += 1
            x_pos = args.xmin + (args.xmax-args.xmin)*x_no/(args.lines-1)
            y_pos = args.ymin + (args.ymax-args.ymin)*y_no/(args.lines-1)
            print(x_no,y_no,x_pos,y_pos)
            c.gcode("G0 Z{}\nG0 X{} Y{}\n".format(args.zup,x_pos,y_pos))
            z_pos = args.zup
        else:
            print("you pressed something else ...")
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
    sys.exit(0)

if __name__ == "__main__":
    main()
