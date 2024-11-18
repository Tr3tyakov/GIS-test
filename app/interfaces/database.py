from abc import (
    ABC,
    abstractmethod,
)


class IDatabase(ABC):

    @abstractmethod
    def _session(self): ...

    @abstractmethod
    def _connect(self): ...

    @abstractmethod
    def _close(self): ...
