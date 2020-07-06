from todgame.drawables import Drawable, FourSideDrawable
from todgame.side import Side
from todgame.stage import Stage

from abc import abstractmethod
from typing import NewType, Tuple

import pygame as pg  # type: ignore
from svec import Point2d, Vector2d


ZKey = NewType('ZKey', Tuple[int, float])


class BasicSprite:
    def __init__(self, stage: Stage, coords: Point2d):
        self.stage = stage
        self.coords = coords

    @abstractmethod
    def draw(self, destination: pg.Surface) -> None:
        ...

    def update(self, time_delta: float) -> None:
        del self, time_delta
        pass

    def zkey(self) -> ZKey:
        return ZKey((self.z_layer(), self.z_coord()))

    def z_layer(self) -> int:
        return 0

    def z_coord(self) -> float:
        return self.coords.vec.y


class Sprite(BasicSprite):
    def __init__(self, stage: Stage, coords: Point2d, drawable: Drawable):
        super().__init__(stage=stage, coords=coords)
        self._drawable = drawable

    def draw(self, destination: pg.Surface) -> None:
        self._drawable.draw(coords=self.coords, destination=destination)


def _get_side_for_vector(vec: Vector2d) -> Side:
    x, y = vec.coords()
    if abs(x) < abs(y):
        if y < 0:
            return Side.BACK
        else:
            return Side.FRONT
    else:
        if x < 0:
            return Side.LEFT
        else:
            return Side.RIGHT


class WalkingSprite(BasicSprite):
    def __init__(
        self,
        stage: Stage,
        coords: Point2d,
        four_drawable: FourSideDrawable,
        initial_side: Side = Side.FRONT
    ):
        super().__init__(stage=stage, coords=coords)
        self._four_drawable = four_drawable
        self._static_four_drawable = four_drawable.map(lambda x: x.static_frame())
        self._side = initial_side
        self._momentum = Vector2d(0, 0)

    def draw(self, destination: pg.Surface) -> None:
        drawable = self._four_drawable if self.is_moving() else self._static_four_drawable
        drawable.draw(coords=self.coords, destination=destination, side=self._side)

    def is_moving(self) -> bool:
        return abs(self._momentum) > 0

    def turn(self, new_side: Side) -> None:
        self._side = new_side

    async def walk(self, coords_delta: Vector2d, speed: float) -> None:
        if speed == 0.0:
            raise ZeroDivisionError('WalkingSprite.walk: speed cannot be 0')

        path_length = abs(coords_delta)
        if path_length == 0.0:
            # Nothing to do if no movement is necessary
            return

        self.turn(_get_side_for_vector(coords_delta))

        destination_point = self.coords + coords_delta

        self._momentum = coords_delta.normalized() * speed
        walk_time = path_length / speed
        await self.stage.coroutine_manager.sleep(walk_time)
        self._momentum = Vector2d(0.0, 0.0)
        self.coords = destination_point
