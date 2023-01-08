from emitter import Emitter, EmitterOptions
from generator import Generator
from writer import Writer


def snake_to_pascal(str):
    return str.replace("_", " ").title().replace(" ", "")


def snake_to_camel(str):
    temp = str.split('_')
    return temp[0] + ''.join(ele.title() for ele in temp[1:])


class_name = 'SDL'
workspace_name = 'SDL'
namespace = 'SDL'

generator = Generator('third-party/SDL/include/SDL.h', 'third-party/SDL/src/SDL.c')

module = generator.generate()

emitter_options = EmitterOptions(
    function_name  = lambda x: x.removeprefix('SDL_'),
    parameter_name = lambda x: snake_to_camel(x),
    enum_name      = lambda x: snake_to_pascal(x.removeprefix('SDL_')))

emitter = Emitter(module, class_name, namespace, emitter_options)
source = emitter.emit()

writer = Writer(workspace_name)
writer.write_class('SDL', source)
