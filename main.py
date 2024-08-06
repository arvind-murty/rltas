from src.player import Player, Input
from src.block import Block
from src.course import Course


p = Player()
inpt = Input()
p.move(inpt)
lst = [Block(), Block(0.0, 0.0, 4.0)]
c = Course(lst)
