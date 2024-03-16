# Random_Walk
An application for creating differrent kinds of random walk simulations.

Expansions:

    Has an extensive GUI allowing users to build a simulation manually or upload one from a *.json file - and view results.
    Allows for possitive or negative gravity between walkers.
    Has a class which generates graphs detailing the path a walker went through.
    Mudspots, rectangles where the walkers are "slowed down".
    Tests written >90% coverage (w/o GUI)
    Typing recieves no issues for "mypy ."

Classes:

    Simulation:
    Sets up the simulation, handles saving data and adding the simulation objects

    Walker:
    The core of the simulation, an object that changes it's location in accordance with certtain rules

    Barrier:
    An object that denies passage to the walker.

    Portal:
    An object that teleports the walker to a certain place.

    Mudspot:
    A patch where the walker is slower.

This is my final project in the Introduction to Computer Science course at HUJI.
