from todgame.drawables import Drawable, FourSideDrawable
from todgame.side import Side
from todgame.stage import Stage

from abc import abstractmethod

import pygame as pg
from svec import Vector2d


class BasicSprite:
    def __init__(self, stage: Stage, coords: Vector2d):
        self.stage = stage
        self.coords = coords


    @abstractmethod
    def draw(self, destination: pg.Surface) -> None:
        ...


    def update(self, time_delta: float) -> None:
        del self, time_delta
        pass


class Sprite(BasicSprite):
    def __init__(self, stage: Stage, coords: Vector2d, drawable: Drawable):
        super.__init__(stage=stage, coords=coords)
        self._drawable = drawable


    def draw(self, destination: pg.Surface) -> None:
        self._drawable.draw(coords=self.coords, destination=destination)


class WalkingSprite(BasicSprite):
    def __init__(
        self,
        stage: Stage,
        coords: Vector2d,
        four_drawable: FourSideDrawable,
        initial_side: Side = Side.FRONT
    ):
        super.__init__(stage=stage, coords=coords)
        self._four_drawable = four_drawable
        self._side = initial_side
        self._momentum = Vector2d(0, 0)


    def draw(self, destination: pg.Surface) -> None:
        self._four_drawable.draw(coorde=self.coords, destination=destination, side=self._side)


    def turn(self, new_side: Side) -> None:
        self._side = new_side


    async def walk(self, coords_delta: Vector2d) -> Coroutine[None, Any, None]:
        pass


