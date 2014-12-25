import subprocess

__author__ = 'corvis'

XRANDR_EXECUTABLE = 'xrandr'


def run_xrandr_command(args):
    cmd_string = ' '.join([XRANDR_EXECUTABLE, args])
    p = subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    errors = '\n'.join(p.stderr.readline()).strip()
    res = p.stdout.readlines()
    if len(errors) > 0:
        raise Exception(errors)
    return res