"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict, Tuple


class DistanceMap:
    """A map of distances between two different cities.

    === Private Attributes ===
    _dist:
        The distance from city 'a' to city 'b' AND city 'b' to 'a'.

    === Sample Usage ===
    >>> m = DistanceMap()
    >>> m.add_distance('Toronto', 'York', 5, 9)
    >>> m.add_distance('Hamilton', 'York', 22)
    >>> m.distance('Toronto', 'York')
    5
    >>> m.distance('York', 'Toronto')
    9
    >>> m.distance('Hamilton', 'York')
    22
    >>> m.distance('York', 'Hamilton')
    22
    >>> m.distance('Toronto', 'Brampton')
    -1
    >>> m.distance('Brampton', 'Toronto')
    -1

    === Representation Invariants ===
    - Each key in the _dist dictionary is a tuple of two cities.
    - If a key of cities (a, b) exists, then a key of cities (b, a) must exist.
    - Distance are positive integers.
    """
    _dist: Dict[Tuple[str, str], int]

    def __init__(self) -> None:
        """Initialize a new DistanceMap.
        """

        self._dist = {}

    def add_distance(self, a: str, b: str, d_ab: int, d_ba: int = -1) -> None:
        """Add a distance between to our distance map.

        Precondition: d_ab > 0
        """

        if d_ba == -1:
            d_ba = d_ab

        self._dist[(a, b)] = d_ab
        self._dist[(b, a)] = d_ba

    def distance(self, a: str, b: str) -> int:
        """Return the distance between city a and city b.
        >>> m = DistanceMap()
        >>> m.add_distance('Scarborough', 'York', 15, 19)
        >>> m.distance('Scarborough', 'York')
        15
        >>> m.distance('York', 'Scarborough')
        19
        >>> m.add_distance('Hamilton', 'Mississauga', 57)
        >>> m.distance('Mississauga', 'Hamilton')
        57
        >>> m.distance('Hamilton', 'Mississauga')
        57
        >>> m.distance('Vaughn', 'Mississauga')
        -1
        """
        if (a, b) in self._dist:
            return self._dist[(a, b)]
        return -1


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
