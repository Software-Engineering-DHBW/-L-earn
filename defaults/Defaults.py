import os
import pickle
import Exceptions as ex


class Defaults(object):
    class __Defaults:
        file_path = os.path.abspath(os.path.dirname(__file__)) + "/defaults.pkl"

        def __init__(self, filename=file_path):
            self.filename = filename
            self.__defaults = {}
            try:
                self.getDefaults()
            except FileNotFoundError:
                self.__saveDefaults()

        def __saveDefaults(self):
            with open(self.filename, "wb") as pkl_handle:
                pickle.dump(self.__defaults, pkl_handle)

        def getDefaults(self):
            with open(self.filename, "rb") as pkl_handle:
                self.__defaults = pickle.load(pkl_handle)
            return self.__defaults

        def get(self, key):
            if len(self.__defaults) == 0:
                self.getDefaults()
            try:
                return self.__defaults[key]
            except KeyError as e:
                # return ex.NotFoundError()
                return ""

        def set(self, key, val):
            self.__defaults[key] = val
            self.__saveDefaults()

    instance = None

    def __new__(cls, *args, **kwargs):
        if not Defaults.instance:
            Defaults.instance = Defaults.__Defaults()
        return Defaults.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)


if __name__ == "__main__":
    defaults = Defaults()
    defaults.set("a", 1)
    defaults.set("b", 2)
    print(defaults.getDefaults())
    print(defaults.get("a"))
    print(defaults.get("c"))
