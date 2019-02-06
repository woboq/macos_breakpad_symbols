#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-w", action='store_true', help="No dry run, create output directory structure and file")
parser.add_argument("filename", help="Full path to library (dylib or inside Framework)")
args = parser.parse_args()

import os
if not os.path.isfile(args.filename):
    print("file argument given does not exist")
    sys.exit(1)

import subprocess

firstLine = ""

try:
    completedProcess = subprocess.run(["dump_syms", "-a", "x86_64", args.filename], check=True, capture_output=True, encoding="utf-8")
except FileNotFoundError as e:
    print("Try to set dump_syms to PATH, e.g. export PATH=/Users/guruz/software/breakpad/src/tools/mac/dump_syms/build/Release/:$PATH")

firstLine = completedProcess.stdout.splitlines()[0]
#e.g.
#MODULE mac x86_64 0B12D320E66C3DCE9713C7B8D03C97D70 libsystem_kernel.dylib
splitted = firstLine.split(' ', 6)
if not splitted[0] == "MODULE":
    print("Not a MODULE: "+splitted[0] )
    exit(1)

libId = splitted[3]
libFilename = splitted[4]

if not args.w:
    print ("Dry run, would create output "+libFilename+"/"+libId+"/"+libFilename+".sym")
    exit(1)

print ("Will create "+libFilename+"/"+libId+"/"+libFilename+".sym")

thePath = libFilename+"/"+libId+"/"
os.makedirs(thePath, exist_ok=True)

out_file = open(libFilename+"/"+libId+"/"+libFilename+".sym", "w")
out_file.write(completedProcess.stdout)
out_file.close()