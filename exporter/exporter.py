from abc            import ABCMeta, abstractmethod
from os             import path
from warnings       import warn
from library        import *

class Exporter(metaclass=ABCMeta):

    def __init__(self, library):
        self.__library  = library

    def get_library(self):
        return self.__library

    @abstractmethod
    def export_to_file(self, filename):
        pass
