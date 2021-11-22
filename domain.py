"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """A parcel with a unique id and volume in cubic centimeters.

    === Instance Attributes ===
    p_id: The unique id of a parcel.
    p_vol: The volume of a parcel in cubic centimeters.
    source: The source of the parcel.
    dest: The final destination of a parcel.

    === Sample Usage ===
    >>> p1 = Parcel(342, 10, 'New York', 'Mississauga')
    >>> p1.p_id
    342
    >>> p1.p_vol
    10
    >>> p1.source
    'New York'
    >>> p1.dest
    'Mississauga'
    >>> p2 = Parcel(343, 25, 'London', 'Vaughan')
    >>> p2.dest
    'Vaughan'

    === Representation Invariants ===
    - Parcel have a unique id that cannot be duplicated.
    - Parcel don't have their source as a destination.
    """
    p_id: int
    p_vol: int
    source: str
    dest: str

    def __init__(self, p_id: int, vol: int, source: str, dest: str) -> None:
        """Initialize a parcel.
        """

        self.p_id = p_id
        self.p_vol = vol
        self.source = source
        self.dest = dest


class Truck:
    """A truck with a unique id that can be filled up with parcel up to its
       maximum volume capacity. A truck is also assigned to depot and follows a
       route to deliver parcels. It then returns to the depot.

    === Instance Attributes ===
    t_id: The unique id of a truck.
    cap: The truck's initial capacity when empty.
    dep: The truck's assigned depot location.
    avail: The available volume in the truck.
    par: The parcels conatained by the truck
    route: The trucks route to deliver parcels.

    === Sample Usage ===
    >>> t1 = Truck(888, 70, 'Toronto')
    >>> p1 = Parcel(342, 10, 'New York', 'Mississauga')
    >>> p2 = Parcel(343, 25, 'London', 'Vaughan')
    >>> t1.pack(p1)
    True
    >>> t1.pack(p2)
    True
    >>> t1.avail
    35
    >>> p3 = Parcel(345, 90, 'Quebec', 'Mississauga')
    >>> t1.pack(p3)
    False
    >>> t1.avail
    35
    >>> round(t1.fullness(), 2) == 50.0
    True
    >>> t1.par == [p1, p2]
    True

    === Representation Invariants ===
    - A parcel cannot be added to a truck if it exceeds its available capacity.
    - No parcels have the depot as their destination.
    - All trucks have a unique id that cannont be duplicated.
    """
    t_id: int
    cap: int
    dep: str
    avail: int
    par: List[Parcel]
    route: List[str]

    def __init__(self, t_id: int, cap: int, dep: str) -> None:
        """Initialize a truck.
        """

        self.t_id = t_id
        self.cap = cap
        self.dep = dep
        self.avail = cap
        self.par = []
        self.route = [dep]

    def pack(self, parcel: Parcel) -> bool:
        """Pack the given parcel in the truck if there is enough space
        available.
        >>> t1 = Truck(888, 100, 'Quebec')
        >>> p1 = Parcel(342, 10, 'New York', 'Mississauga')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(343, 90, 'London', 'Vaughan')
        >>> t1.pack(p2)
        True
        >>> p3 = Parcel(343, 1, 'London', 'Vaughan')
        >>> t1.pack(p3)
        False
        """

        if parcel.p_vol <= self.avail:
            self.par.append(parcel)
            self.avail -= parcel.p_vol
            if self.route[-1] != parcel.dest:
                self.route.append(parcel.dest)
            return True
        return False

    def fullness(self) -> float:
        """Return the percentage of a truck's used space compared to its
        capacity.

        Precondition: A truck does not a have a capacity of 0.

        >>> t1 = Truck(999, 1005, 'Toronto')
        >>> p3 = Parcel(345, 92, 'Quebec', 'Mississauga')
        >>> t1.pack(p3)
        True
        >>> round(t1.fullness(), 2) == 9.15
        True
        """
        return ((self.cap - self.avail) / self.cap) * 100

    def num_par(self) -> int:
        """Return the number of parcels in a truck.

        >>> t1 = Truck(888, 100, 'Quebec')
        >>> t1.num_par()
        0
        >>> p1 = Parcel(342, 10, 'New York', 'Mississauga')
        >>> t1.pack(p1)
        True
        >>> t1.num_par()
        1
        >>> p2 = Parcel(343, 25, 'London', 'Vaughan')
        >>> t1.pack(p2)
        True
        >>> t1.num_par()
        2
        >>> p3 = Parcel(344, 70, 'London', 'Vaughan')
        >>> t1.pack(p3)
        False
        >>> t1.num_par()
        2
        """
        return len(self.par)

    def empty_truck(self) -> bool:
        """Return True if a truck is empty.
        >>> t1 = Truck(888, 100, 'Quebec')
        >>> t1.empty_truck()
        True
        >>> p1 = Parcel(342, 10, 'New York', 'Mississauga')
        >>> t1.pack(p1)
        True
        >>> t1.empty_truck()
        False
        """
        return self.cap == self.avail

    def parcel_ids(self) -> List[int]:
        """Return a list of id of each parcels in the truck in order added.
        >>> t1 = Truck(888, 100, 'Quebec')
        >>> p1 = Parcel(342, 10, 'New York', 'Mississauga')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(343, 25, 'London', 'Vaughan')
        >>> t1.pack(p2)
        True
        >>> p3 = Parcel(344, 25, 'London', 'Vaughan')
        >>> t1.pack(p3)
        True
        >>> t1.parcel_ids()
        [342, 343, 344]
        """
        x = []

        for parcel in self.par:
            x.append(parcel.p_id)

        return x

    def truck_distance(self, dmap: DistanceMap) -> int:
        """Return the distance travelled by a truck according to the distances
        in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled

        >>> t1 = Truck(1423, 100, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(343, 12, 'London', 'Vaughan')
        >>> t1.pack(p2)
        True
        >>> p3 = Parcel(344, 25, 'New York', 'Vaughan')
        >>> t1.pack(p3)
        True
        >>> p4 = Parcel(345, 25, 'Chicago', 'York')
        >>> t1.pack(p4)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> m.add_distance('Hamilton', 'Vaughan', 12)
        >>> m.add_distance('Vaughan', 'York', 15)
        >>> m.add_distance('Toronto', 'York', 21, 25)
        >>> t1.truck_distance(m)
        61
        >>> t2 = Truck(1541, 200, 'Mississauga')
        >>> t2.truck_distance(m)
        0
        """
        x = 0

        if len(self.route) > 1:
            for i in range(len(self.route) - 1):
                x += dmap.distance(self.route[i], self.route[i+1])
            x += dmap.distance(self.route[-1], self.route[0])
            return x
        return x


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    def __str__(self) -> str:
        """Produce a string representation of this fleet
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> t2 = Truck(5912, 20, 'Scarborough')
        >>> t3 = Truck(1111, 50, 'York')
        >>> f = Fleet()
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.add_truck(t3)
        >>> print(f)
        Truck id1423: Capacity=10, Depot=Toronto
        Truck id5912: Capacity=20, Depot=Scarborough
        Truck id1111: Capacity=50, Depot=York
        """
        return "\n".join(f"Truck id{i.t_id}: Capacity={i.cap}, Depot={i.dep}"
                         for i in self.trucks)

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        x = 0
        for truck in self.trucks:
            if not truck.empty_truck():
                x += 1
        return x

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        d = {}

        for truck in self.trucks:
            d[truck.t_id] = truck.parcel_ids()

        return d

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        >>> t2 = Truck(1424, 50, 'Toronto')
        >>> f.add_truck(t2)
        >>> p2 = Parcel(2, 15, 'Buffalo', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> p3 = Parcel(3, 5, 'Buffalo', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.total_unused_space()
        1025
        >>> t3 = Truck(1425, 10000, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.total_unused_space()
        1025
        >>> p4 = Parcel(3, 1, 'Buffalo', 'Hamilton')
        >>> t3.pack(p4)
        True
        >>> f.total_unused_space()
        11024
        """
        total_avail = 0
        for truck in self.trucks:
            if not truck.empty_truck():
                total_avail += truck.avail

        return total_avail

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        >>> t2 = Truck(1424, 50, 'Toronto')
        >>> f.add_truck(t2)
        >>> p2 = Parcel(2, 15, 'Buffalo', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> p3 = Parcel(3, 25, 'Buffalo', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f._total_fullness()
        130.0
        """
        x = 0
        for truck in self.trucks:
            if not truck.empty_truck():
                x += truck.fullness()

        return x

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        >>> p1 = Parcel(13, 2, 'Buffalo', 'Hamilton')
        >>> t.pack(p1)
        True
        >>> t2 = Truck(1424, 150, 'Toronto')
        >>> f.add_truck(t2)
        >>> t3 = Truck(1425, 20, 'Toronto')
        >>> f.add_truck(t3)
        >>> p2 = Parcel(2, 12, 'York', 'Hamilton')
        >>> t3.pack(p2)
        True
        >>> f.average_fullness()
        65.0
        """
        return self._total_fullness() / self.num_nonempty_trucks()

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        td = 0

        for truck in self.trucks:
            td += truck.truck_distance(dmap)

        return td

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> t3 = Truck(1334, 100, 'Toronto')
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.add_truck(t3)
        >>> f.average_distance_travelled(m)
        18.0
        """

        return self.total_distance_travelled(dmap) / self.num_nonempty_trucks()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
