from common.platform_layer import PlatformLayerBase


class PlatformLayerLinuxImpl(PlatformLayerBase):
    def get_pid(self, name) -> int | None:
        return 1

    def launch(self, exe_path) -> bool:
        return True
