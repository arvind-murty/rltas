from src.player import Player, Input
from src.course import Course, Block


p = Player(0.5, 64.0, -0.3)
inpt = Input(0, 0, 1, 0)
lst = [Block.block(0, 63, 0), Block.block(0, 63, 4)]
c = Course(lst)
print(p)
p.move(inpt, c)
print(p)
p.move(Input(), c)
print(p)
p.move(Input(), c)
print(p)
