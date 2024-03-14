#!/usr/bin/env python
# encoding: utf-8

import subprocess

def callMe(subject, content):
    command = "osascript email.applescript '" + subject + "' '" + content + "'"
    output = subprocess.check_output(command, shell=True)
    print(output.decode('utf-8'))

