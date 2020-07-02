from todgame.side import Side

import time
from abc import abstractmethod
from math import floor
from typing import Callable, Generic, List

import pygame as pg  # type: ignore
from svec import Point2d


class Drawable:
    @abstractmethod
    def draw(self, coords: Point2d, destination: pg.Surface) -> None:
        ...

    @abstractmethod
    def static_frame(self) -> 'StaticDrawable':
        ...


class StaticDrawable(Drawable):
    def static_frame(self) -> 'StaticDrawable':
        return self


class SimpleStaticDrawable(StaticDrawable):
    def __init__(self, draw_func: Callable[[Point2d, pg.Surface], None]):
        self._draw_func = draw_func

    def draw(self, coords: Point2d, destination: pg.Surface) -> None:
        self._draw_func(coords, destination)


class AnimatedDrawable(Drawable):
    def __init__(self, fps: int):
        self._fps = fps
        self._start_time = time.monotonic()

    def draw(self, coords: Point2d, destination: pg.Surface) -> None:
        frame_num = self.get_frame_num()
        self.draw_frame(frame_num, coords, destination)

    def get_frame_num(self) -> int:
        return floor(self.get_elapsed_time() * self.get_fps())

    def get_static_frame_num(self) -> int:
        return 0

    def get_fps(self) -> int:
        return self._fps

    def static_frame(self) -> 'SimpleStaticDrawable':
        def draw_static_frame(coords: Point2d, destination: pg.Surface) -> None:
            self.draw_frame(self.get_static_frame_num(), coords, destination)

        return SimpleStaticDrawable(draw_static_frame)

    def get_elapsed_time(self) -> float:
        return time.monotonic() - self._start_time

    @abstractmethod
    def draw_frame(self, frame_num: int, coords: Point2d, destination: pg.Surface) -> None:
        ...


class FourSideDrawable:
    def __init__(self, left: Drawable, right: Drawable, front: Drawable, back: Drawable):
        self.left = left
        self.right = right
        self.front = front
        self.back = back

    def draw(self, side: Side, coords: Point2d, destination: pg.Surface) -> None:
        self.get_drawable_for_side(side).draw(coords=coords, destination=destination)

    def get_drawable_for_side(self, side: Side) -> Drawable:
        if side == Side.LEFT:
            return self.left
        if side == Side.RIGHT:
            return self.right
        if side == Side.FRONT:
            return self.front
        if side == Side.BACK:
            return self.back

        raise ValueError(f'Invalid side: {side}')


class Texture(StaticDrawable):
    def __init__(self, image: pg.Surface):
        super().__init__()
        self._image = image

    def draw(self, coords: Point2d, destination: pg.Surface) -> None:
        target_rect = self._image.rect
        target_rect.center = coords.ints()
        destination.blit(self._image, target_rect)


class FrameByFrameAnimatiedDrawable(AnimatedDrawable):
    def __init__(self, frames: List[StaticDrawable], fps: int):
        super().__init__(fps=fps)
        self._frames = frames

    def draw_frame(self, frame_num: int, coords: Point2d, destination: pg.Surface) -> None:
        frame_index = frame_num % len(self._frames)
        self._frames[frame_index].draw(coords=coords, destination=destination)
