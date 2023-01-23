import abc


class PlatformLayerBase:
    @abc.abstractmethod
    def get_pid(self, name) -> int | None:
        pass

    @abc.abstractmethod
    def launch(self, exe_path) -> bool:
        pass
