
from Code.td_walker import Walker3D as w3d
from Code.td_barrier import Barrier3D as b3d
from Code.td_portal import Portal3D as p3d
from Code.td_mud import MudPatch3D as m3d
import Code.graph as gr
import Code.helper_functions as helper

Trioordinates = tuple[float,float,float]


class Simulation_3D:
    """
    A class for Simulation objects for random walker simulations in 3D.
    :attribute __walkers: a list containg all walkers added to the simulation by order
    :attribute __location_log: a dictionary where the keys are the indexes of different 
                                walkers in __walker and the values are lists in order of
                                the locations the walker visited.
    :attribute __barriers: a list containg all barriers added to the simulation by order
    :attribute __portals: a list containg all portals added to the simulation by order
    :attribute __iteration: counts the iterations of the simulation
    """

    def __init__(self) -> None:
        """
        The constructor for Simulation objects
        """
        self.__walkers: list[w3d] = []
        self.__barriers: list[b3d]= []
        self.__portals: list[p3d] = []
        self.__mudspots: list[m3d] = []
        self.__iteration = 0

    def add_walker(self, walker: w3d) -> None:
        """
        Adds a walker to the simulation
        Once a walker is added it can't be terminated!
        :param walker: the Walker to add
        """
        self.__walkers.append(walker)

    def add_portal(self, portal: p3d) ->None:
        """"
        Adds a portal to the simulation
        :param portal: The portal to add
        """
        self.__portals.append(portal)

    def add_barrier(self, barrier: b3d) ->None:
        """"
        Adds a barrier to the simulation
        :param barrier: The barrier to add
        """
        self.__barriers.append(barrier)

    def add_mud(self, mud: m3d) -> None:
        """
        Adds mud to the simulation
        :param mus: The mud to add
        """
        self.__mudspots.append(mud)

    def step(self) -> int:
        """
        Preforms one step of the entire simulation.
        Returns the number of the step preformed.
        """
        MAX_BARRIER_HITS = 10**3
        for index, walker in enumerate(self.__walkers):
            current_place = walker.position
            next_place = walker.next_location()
            if next_place:
                for barrier in self.__barriers:
                    barrier_hit = 0
                    while barrier.intersects(current_place, next_place):
                        #print(f"hit barrier on {self.__iteration}th iteration")
                        next_place = walker.next_location()
                        barrier_hit += 1
                        if barrier_hit > MAX_BARRIER_HITS:
                            raise helper.SimulationError(
                                "\nThe walker is stuck in a barrier, please change the simulation")
                for mud in self.__mudspots:
                    if mud.point_in_area(current_place):
                        next_place = (current_place[0] +
                                    (next_place[0] - current_place[0]) * mud.get_lag(),
                                    current_place[1] +
                                    (next_place[1] - current_place[1]) * mud.get_lag(),
                                    current_place[2] +
                                    (next_place[2] - current_place[2]) * mud.get_lag())
                for portal in self.__portals:
                    if portal.inbounds(next_place):
                        #print(f"passed through portal on {self.__iteration}th iteration")
                        next_place = portal.endpoint
                walker.jump(next_place)
            else:
                raise AttributeError(
                    "The walker has no next location, due to having bad type of movement")
        self.__iteration += 1
        return self.__iteration


    def run_simulation(self,n: int) -> None:
        """
        runs the simulation for n steps
        """
        for _ in range(n):
            self.step()

    def mappit(self) -> None:
        """
        maps the locations of the walkers
        """
        gr.map_3d([walker.log for walker in self.__walkers],
                  [barrier.points for barrier in self.__barriers],
                  [(portal.center, portal.radius) for portal in self.__portals],
                  [mud.properties for mud in self.__mudspots])
