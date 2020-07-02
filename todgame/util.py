from typing import TypeVar, Iterable, List


_T = TypeVar('_T')


def robust_list_iter(lst: List[_T], *, iter_new: bool = True) -> Iterable[_T]:
    i = 0
    initial_len = len(lst)
    while i < (len(lst) if iter_new else initial_len):
        yield lst[i]
