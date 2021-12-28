# # import configparser
# # import sys
# # import importlib
# # import importlib.abc
# # import importlib.machinery
# # from types import ModuleType
# #
# # c = configparser.ConfigParser()
# # c.read('some_config.ini')
# # print(c)
# # path = sys.meta_path
# #
# #
# # class ConfigLoader(importlib.abc.SourceLoader):
# #     def __init__(self):
# #         self.fullname =
# #
# #
# #     def get_data(self, path: path) -> bytes:
# #         return  b'a=1'
# #
# #     def exec_module(self, module: ModuleType):
# #         module.a = 1
# #     def module_repr(self, module: ModuleType) -> str:
# #         return f'<module {module.__name__}>'
# #     def get_filename(self, fullname: str):
# #         return fullname
# #
# #
# #
# # class IniFinder(importlib.abc.MetaPathFinder):
# #     def find_spec(self, fullname: str, path, target=None):
# #         print(f'{fullname=} {path=} {target=}')
# #         if fullname == 'some_config':
# #             return importlib.machinery.ModuleSpec(
# #                 name=fullname,
# #                 loader=ConfigLoader(fullname, path, target),
# #                 origin='some_config.ini'
# #             )
# #         path = path or sys.path
# #         return None
# #
# #
# # sys.meta_path.append(IniFinder())
# # import some_config
# # print(some_config.a)
# #
# # #import some_config
#
#
# # 1. научится парсить ini-файлы
# import configparser
# import os
# from types import ModuleType
# from typing import Optional, Sequence
#
# c = configparser.ConfigParser()
# c.read('some_config.ini')
# #print(c)
#
# # 2. нам нужно научиться загружать их как модуль
# # 3. воткнуться в систему импорта python'а
# import sys
# #print(sys.meta_path)
# import importlib
# import importlib.abc
#
#
# class ConfigLoader(importlib.abc.Loader):
#     def __init__(self, fullname, path, target):
#         self.fullname = fullname
#         self.path = path
#
#     def create_module(self, spec) -> Optional[ModuleType]:
#         return None
#
#     def exec_module(self, module: ModuleType) -> None:
#         module
#
#
#
# class IniFinder(importlib.abc.MetaPathFinder):
#     # def find_spec(
#         # self, fullname: str, path, target=None):
#         # print(f'{fullname=} {path=} {target=}')
#         # path = path or sys.path
#         # filename = f'{fullname}.ini'
#         # for p in path:
#         #  )   full_path = os.path.join(p, filename)
#         #     if os.path.isfile(full_path):
#         #         return importlib.machinery.ModuleSpec(
#         #             name=fullname,
#         #             loader=ConfigLoader(fullname, path, target),
#         #             origin=full_path
#         #         )
#         # if fullname == 'some_config':
#         #     return importlib.machinery.ModuleSpec(
#         #         name=fullname,
#         #         loader=ConfigLoader(fullname, path, target),
#         #         origin='some_config.ini'
#         #     )
#         # return None
#     path = r"C:\Users\lessy\OneDrive\Рабочий стол\Dropbox\Python\Asteroids\Asteroids"
#     fullname = r"some_config"
#     def find_module(self, fullname, path=path):
#         return self.find_spec(fullname, path)
#
#     def find_spec(self, fullname, path, target=None):
#         import os.path
#         from importlib.machinery import ModuleSpec
#
#         if os.path.exists(fullname + ".ini"):
#             return ModuleSpec(os.path.realpath(fullname + ".ini"), ConfigLoader(fullname, path, None))
#         else:
#             return None
#
# sys.meta_path.append(IniFinder())
#
# import some_config
#
# path = r"C:\Users\lessy\OneDrive\Рабочий стол\Dropbox\Python\Asteroids\Asteroids"
# fullname = r"some_config"
# l = ConfigLoader(fullname, path, None)
# print(some_config.database)

#import some_config


# 1. научится парсить ini-файлы
import configparser
import os
from types import ModuleType
from typing import Optional, Sequence

c = configparser.ConfigParser()
c.read('some_config.ini')
#print(c)

# 2. нам нужно научиться загружать их как модуль
# 3. воткнуться в систему импорта python'а
import sys
#print(sys.meta_path)
import importlib
import importlib.abc

def load_ini_as_dict(path):
    c = configparser.ConfigParser()
    c.read(path)

    return {section: dict(values)
            for (section, values) in dict(c).items()}


class MyConfigLoader(importlib.abc.Loader):
    def __init__(self, ini_path):
        self.ini_path = ini_path

    def create_module(self, spec):
        return None

    def exec_module(self, module: ModuleType):
        module.a = 1
        module.b = 'что душа пожелает'
        module.__dict__.update(load_ini_as_dict(self.ini_path))


class IniFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname: str, path, target=None):
        #print(f'{fullname=} {path=} {target=}')
        path = path or sys.path
        filename = f'{fullname}.ini'
        for p in path:
            full_path = os.path.join(p, filename)
            if os.path.isfile(full_path):
                return importlib.machinery.ModuleSpec(
                    name=fullname,
                    loader=MyConfigLoader(full_path),
                    origin=full_path
                )
        return None

sys.meta_path.append(IniFinder())

import some_config
print(some_config)
print(dir(some_config))
print(some_config.DEFAULT)