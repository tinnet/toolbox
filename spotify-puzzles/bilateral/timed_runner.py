import imp
import os
import sys
import threading

USAGE = "python %s YOUR_MODULE TIMEOUT_IN_SECONDS arg1 arg2 arg3" % sys.argv[0]

class ModuleRunner(threading.Thread):
    def __init__(self, module_name):
        threading.Thread.__init__(self)
        # strip the ".py" from the modulename (if the user gave it)
        path,ext = os.path.splitext(module_name)
        if ext == ".py":
            self.module_name = path
        else:
            self.module_name = module_name

    def run(self, *args, **kwargs):
        fp, pathname, description = imp.find_module(self.module_name)
        try:
            # FIXME multiple threads + global sys.argv = problems! use multiprocessing instead of threading?
            sys.argv[0] = pathname
            imp.load_module("__main__", fp, pathname, description)
        finally:
            fp.close()

    @classmethod
    def runModule(cls, module_name):
        worker = ModuleRunner(module_name)
        worker.start()
        return worker

    @classmethod
    def runModuleWithTimeout(cls, module_name, timeout):
        worker = ModuleRunner(module_name)
        worker.start()
        worker.join(timeout)
        if worker.is_alive():
            worker._Thread__stop()
            raise Exception("module took longer than %f seconds, worker was killed" % timeout)

def main():
    if len(sys.argv) < 3:
        print "missing arguments, usage:", USAGE
        return 1

    max_seconds = float(sys.argv[2])
    del sys.argv[2]
    module = sys.argv[1]
    del sys.argv[1]

    try:
        ModuleRunner.runModuleWithTimeout(module, max_seconds)
    except Exception as e:
        print >> sys.stderr, "Exception:", e
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())