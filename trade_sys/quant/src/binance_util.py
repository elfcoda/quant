#!/usr/bin/env python
# encoding: utf-8

import subprocess

PID_DEFAULT = -1
PID_WENJIE = 0
PID_ZIYAN = 1
PID_YOLANDA = 2

def callMe(subject, content):
    command = "osascript email.applescript '" + subject + "' '" + content + "'"
    output = subprocess.check_output(command, shell=True)
    print(output.decode('utf-8'))

def callSomeone(subject, content, pid):
    command = "osascript email.applescript '" + subject + "' '" + content + "'"
    if pid == PID_WENJIE:
        command = "osascript email.applescript '" + subject + "' '" + content + "'"
    elif pid == PID_ZIYAN:
        command = "osascript ziyan.email.applescript '" + subject + "' '" + content + "'"
    elif pid == PID_YOLANDA:
        command = "osascript yolanda.email.applescript '" + subject + "' '" + content + "'"

    output = subprocess.check_output(command, shell=True)
    print(output.decode('utf-8'))
