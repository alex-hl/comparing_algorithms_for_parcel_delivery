"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Dict, Callable
from random import shuffle
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """Randomly schedule the given <parcels> onto the given <trucks>.

    === Representation Invariants ===
    - Truck and parcels have a positive volume.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Randomly schedule the given parcels into randomly chosen trucks
        that have enough available space.
        """

        unsked = []

        temp_p = parcels.copy()
        shuffle(temp_p)

        shuffle(trucks)

        for parcel in temp_p:
            i = 0
            while i < len(trucks) and parcel.p_vol > trucks[i].avail:
                i += 1
            if i == len(trucks):
                unsked.append(parcel)
            else:
                trucks[i].pack(parcel)
        return unsked


# Private comparison methods for volume of parcel

def _non_increasing_vol(a: Parcel, b: Parcel) -> bool:
    """
    Return True if <a> is non_increasing than <b>.
    """
    return a.p_vol > b.p_vol


def _non_decreasing_vol(a: Parcel, b: Parcel) -> bool:
    """
    Return True if <a> is non_decreasing than <b>.
    """
    return a.p_vol < b.p_vol


# Private comparison methods for destination of parcel


def _non_increasing_dest(a: Parcel, b: Parcel) -> bool:
    """
    Return True if <a> is non_increasing than <b>.
    """
    return a.dest > b.dest


def _non_decreasing_dest(a: Parcel, b: Parcel) -> bool:
    """
    Return True if <a> is non_decreasing than <b>.
    """
    return a.dest < b.dest


# Private comparison methods for most or least available space

def _non_increasing_avail(a: Truck, b: Truck) -> bool:
    """
    Return True if <a> is non_increasing than <b>.
    """
    return a.avail > b.avail


def _non_decreasing_avail(a: Truck, b: Truck) -> bool:
    """
    Return True if <a> is non_decreasing than <b>.
    """
    return a.avail < b.avail


class GreedyScheduler(Scheduler):
    """Greedily schedule the given <parcels> onto the given <trucks>.
    This scheduler is deterministic and there can be 6 different outcomes
    depending on the configuration of the algorithm.

    === Private Attributes ===
    _p_prio:
        This is the the type of priority we are considering the parcels in. It
        could be volume or destination.
    _p_order:
        This is the order of the parcels given a priority. It is either
        non-increasing or non decreasing. It applies to the two different types
        of priority.
    _t_order:
        This order in which we are considering which truck to pack. Either by
        non-increasing volume or non-decreasing volume.

    === Representation Invariants ===
    - Truck and parcels have a positive volume.
    - Config parameter has correct values for _p_prio, _p_order, and _t_order.
    """

    _p_order: Callable
    _t_order: Callable

    def __init__(self, config: Dict) -> None:
        """Initializing priorities and orders."""

        if config['parcel_priority'] == 'volume':
            if config['parcel_order'] == 'non-increasing':
                self._p_order = _non_increasing_vol
            else:
                self._p_order = _non_decreasing_vol
        else:
            if config['parcel_order'] == 'non-increasing':
                self._p_order = _non_increasing_dest
            else:
                self._p_order = _non_decreasing_dest

        if config['truck_order'] == 'non-increasing':
            self._t_order = _non_increasing_avail
        else:
            self._t_order = _non_decreasing_avail

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Greedily schedule the given parcels into on trucks according to
        parcel and truck priorities.
        """

        unsked = []

        # Putting the parcels in order

        p_pq = PriorityQueue(self._p_order)

        for parcel in parcels:
            p_pq.add(parcel)

        while not p_pq.is_empty():
            p = p_pq.remove()

            t_avail = []  # All trucks with available space
            t_city = []   # All trucks with parcel’s dest and avail space.

            # Last comparison by most or least avail
            t_pq = PriorityQueue(self._t_order)

            for truck in trucks:
                if p.p_vol <= truck.avail:
                    t_avail.append(truck)

            for truck in t_avail:
                if truck.route[-1] == p.dest:
                    t_city.append(truck)

            if t_city:
                while t_city:
                    t_pq.add(t_city.pop(0))
            elif t_avail and not t_city:
                while t_avail:
                    t_pq.add(t_avail.pop(0))

            if not t_pq.is_empty():
                t_pq.remove().pack(p)
            else:
                unsked.append(p)

        return unsked


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
