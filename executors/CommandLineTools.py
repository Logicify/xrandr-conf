from . import Executor, registry
import subprocess

__author__ = 'corvis'


class XrandrExecutor(Executor):
    name = "xrandr"

    def __init__(self, ref_name, definition):
        self.cmd_options = definition
        self.xrandrExecutable = 'xrandr'

    def execute(self, configuration):
        cmd_string = ' '.join([self.xrandrExecutable, self.cmd_options])
        p = subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        errors = '\n'.join(p.stderr.readline()).strip()
        res = p.stdout.readline()
        if len(errors) > 0:
            raise Exception(errors)



registry.register(XrandrExecutor)