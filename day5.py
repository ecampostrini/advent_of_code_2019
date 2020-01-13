from utils import get_absolute_path
from intcode import Intcode, load_program_from_file

machine = Intcode.from_file(get_absolute_path("day5.input"))
achine.run()
