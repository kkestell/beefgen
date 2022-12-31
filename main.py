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

# g = Generator('third-party/test/test.h', 'third-party/test/test.c', 'Test', 'Test')
generator = Generator('third-party/SDL/include/SDL.h', 'third-party/SDL/src/SDL.c')
# g = Generator('third-party/cglm/include/cglm/mat4.h', 'third-party/cglm/src/mat4.c', 'GLM', 'Mat4')
# g = Generator('third-party/genann/genann.h', 'third-party/genann/genann.c', 'GenANN', 'GenANN')
# g = Generator('third-party/sqlite3/sqlite3.h', 'third-party/sqlite3/sqlite3.c')
module = generator.generate()
# e = Emitter(module, 'SQLite', 'SQLite')

emitter_options = EmitterOptions(
    function_name  = lambda x: x.removeprefix('SDL_'),
    parameter_name = lambda x: snake_to_camel(x),
    enum_name      = lambda x: snake_to_pascal(x.removeprefix('SDL_')))

emitter = Emitter(module, class_name, namespace, emitter_options)
source = emitter.emit()

writer = Writer('SDL')
writer.write_class('SDL', source)

# FIXME: Move elsewhere

