from src.player import Player, Input
from src.course import Course, Block


p = Player(0.5, 64.0, -0.3)
inpt = Input(1, 0, 0, 0, 1, 0, 0, 45.0)
inpt1 = Input(1, 0, 0, 0, 1, 0, 0)
inpt2 = Input(1, 0, 0, 0, 1, 0, 0)
inpt3 = Input(1, 0, 0, 0, 1, 0, 0)
inpt4 = Input(1, 0, 0, 0, 1, 0, 0)
inpt5 = Input(1, 0, 0, 0, 1, 0, 0)
inpt6 = Input(1, 0, 0, 0, 1, 0, 1)
inpt7 = Input(1, 0, 0, 0, 1, 0, 0)
inpt8 = Input(1, 0, 0, 0, 1, 0, 0)
inpt9 = Input(1, 0, 0, 0, 1, 0, 0)
inpt10 = Input(1, 0, 0, 0, 1, 0, 0)
inpt11 = Input(1, 0, 0, 0, 1, 0, 0)
inpt12 = Input(1, 0, 0, 0, 1, 0, 0)
inpt13 = Input(1, 0, 0, 0, 1, 0, 0)
inpt14 = Input(1, 0, 0, 0, 1, 0, 0)
inpt15 = Input(1, 0, 0, 0, 1, 0, 0)
inpt16 = Input(1, 0, 0, 0, 1, 0, 0)
inpt17 = Input(1, 0, 0, 0, 1, 0, 0)
inpt18 = Input(1, 0, 0, 0, 1, 0, 1)
inpt19 = Input(1, 0, 0, 0, 1, 0, 0)
inpt20 = Input(1, 0, 0, 0, 1, 0, 0)
inpt21 = Input(1, 0, 0, 0, 1, 0, 0)
inpt22 = Input(1, 0, 0, 0, 1, 0, 0)
inpt23 = Input(1, 0, 0, 0, 1, 0, 0)
inpt24 = Input(1, 0, 0, 0, 1, 0, 0)
inpt25 = Input(1, 0, 0, 0, 1, 0, 0)
inpt26 = Input(1, 0, 0, 0, 1, 0, 0)
inpt27 = Input(1, 0, 0, 0, 1, 0, 0)
inpt28 = Input(1, 0, 0, 0, 1, 0, 0)
inpt20 = Input(1, 0, 0, 0, 1, 0, 0)
lst = [Block.block(0, 63, 0), Block.block(-3, 63, 3), Block.block(-3, 65, 4), Block.block(-5, 65, 3), Block.block(-5, 63, 5)]
c = Course(lst)
print(p)
p.move(inpt, c)
print(p)
p.move(inpt1, c)
print(p)
p.move(inpt2, c)
print(p)
p.move(inpt3, c)
print(p)
p.move(inpt4, c)
print(p)
p.move(inpt5, c)
print(p)
p.move(inpt6, c)
print(p)
p.move(inpt7, c)
print(p)
p.move(inpt8, c)
print(p)
p.move(inpt9, c)
print(p)
p.move(inpt10, c)
print(p)
p.move(inpt11, c)
print(p)
p.move(inpt12, c)
print(p)
p.move(inpt13, c)
print(p)
p.move(inpt14, c)
print(p)
p.move(inpt15, c)
print(p)
p.move(inpt16, c)
print(p)
p.move(inpt17, c)
print(p)
p.move(inpt18, c)
print(p)
p.move(inpt19, c)
print(p)
p.move(inpt20, c)
print(p)
p.move(inpt21, c)
print(p)
p.move(inpt22, c)
print(p)
p.move(inpt23, c)
print(p)
p.move(inpt24, c)
print(p)
p.move(inpt25, c)
print(p)
p.move(inpt26, c)
print(p)
p.move(inpt27, c)
print(p)
p.move(inpt28, c)
print(p)
