from common.platform_layer.base import PlatformLayerBase
import platform


def create_platform_layer() -> PlatformLayerBase:
    name = platform.system()
    if name == 'Linux':
        from common.platform_layer.linux_impl import PlatformLayerLinuxImpl
        return PlatformLayerLinuxImpl()
    elif name == 'Windows':
        from common.platform_layer.win_impl import PlatformLayerWinImpl
        return PlatformLayerWinImpl()
    else:
        assert False, name

