import abc
import os

import psutil


class PlatformLayerBase:
    def get_pid(self, name):
        "Return a list of processes matching 'name'."
        assert name, name
        for p in psutil.process_iter():
            name_, exe, cmdline = "", "", []
            try:
                name_ = p.name()
                cmdline = p.cmdline()
                exe = p.exe()
            except (psutil.AccessDenied, psutil.ZombieProcess):
                pass
            except psutil.NoSuchProcess:
                continue
            if name == name_ or (cmdline and cmdline[0] == name) or os.path.basename(exe) == name:
                return p
        return None

    def close(self, name) -> bool:
        pid = self.get_pid(name)
        if pid:
            pid.kill()
            return True
        else:
            return False

    def launch(self, exe_path) -> bool:
        os.system(f'cmd /c start {exe_path}')
        return True
