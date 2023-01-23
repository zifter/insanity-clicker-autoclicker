from subprocess import check_output

from common.platform_layer import PlatformLayerBase


class PlatformLayerWinImpl(PlatformLayerBase):
    def get_pid(self, name) -> int | None:
        return check_output(["pidof", name])

    def launch(self, exe_path) -> bool:
        pass
