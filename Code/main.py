"""
FILE : main.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: The page where the whole program will run
STUDENTS I DISCUSSED THE EXERCISE WITH: 
WEB PAGES I USED:
NOTES: ...
"""

from walker import Walker
from barrier import Barrier
from portal import Portal
from mud import Mud
from helper_functions import load_simulation
from simulation import Simulation
import tkinter as tk

class SimulationApp:
    def __init__(self, root) ->None:
        self.root = root
        self.root.title("Simulation App")
        self.root.geometry("500x600")  # Set permanent window size

        self.welcome_label = tk.Label(self.root, text="Welcome to the Random Walker Simulation App!")
        self.welcome_label.pack(pady=10)

        self.load_button = tk.Button(self.root, text="Load Simulation from JSON", command=load_simulation)
        self.load_button.pack()

        self.manual_button = tk.Button(self.root, text="Manually Build Simulation", command=self.build_simulation)
        self.manual_button.pack()

    def clear_frame(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()

    def build_simulation(self, err_message: str = None) ->None:
        self.clear_frame()
        self.__num_walkers = tk.IntVar()
        self.__num_walkers.set(1)
        self.__num_barriers = tk.IntVar()
        self.__num_portals = tk.IntVar()
        self.__num_mudspots = tk.IntVar()

        if err_message:
            self.error_message = tk.Label(self.root,text= err_message, fg="red2")
            self.error_message.pack()
        self.num_walkers_label = tk.Label(self.root, text="Number of Walkers:")
        self.num_walkers_label.pack()
        self.num_walkers_entry = tk.Entry(self.root, textvariable=self.__num_walkers)
        self.num_walkers_entry.pack()

        self.num_barriers_label = tk.Label(self.root, text="Number of Barriers:")
        self.num_barriers_label.pack()
        self.num_barriers_entry = tk.Entry(self.root, textvariable=self.__num_barriers)
        self.num_barriers_entry.pack()

        self.num_portals_label = tk.Label(self.root, text="Number of Portals:")
        self.num_portals_label.pack()
        self.num_portals_entry = tk.Entry(self.root, textvariable=self.__num_portals)
        self.num_portals_entry.pack()

        self.num_mudspots_label = tk.Label(self.root, text="Number of Mudspots:")
        self.num_mudspots_label.pack()
        self.num_mudspots_entry = tk.Entry(self.root, textvariable=self.__num_mudspots)
        self.num_mudspots_entry.pack()

        
        self.build_button = tk.Button(self.root, text="Build", command=self.create_walker_input)
        self.build_button.pack()

    def create_walker_input(self):
        self.clear_frame()

        self.__walkers_data = []
        self.__barriers_data = []
        self.__portals_data = []
        self.__mudspots_data = []

        try:
            self.__num_walkers = self.__num_walkers.get()
            self.__num_barriers = self.__num_barriers.get()
            self.__num_portals = self.__num_portals.get()
            self.__num_mudspots = self.__num_mudspots.get()
        except tk.TclError:
            self.build_simulation(err_message="All input must be whole numbers!")

        walker_input_frame = tk.Frame(self.root)
        walker_input_frame.pack()

        walker_types = tuple(Walker.move_dict().values())
        walker_colors = tuple(Walker.color_pallet().values())

        for i in range(self.__num_walkers):
            walker_frame = tk.Frame(walker_input_frame)
            walker_frame.pack()

            walker_type_label = tk.Label(walker_frame, text=f"Input for Walker {i+1}: Type:")
            walker_type_label.pack(side=tk.LEFT)
            walker_type_var = tk.StringVar()
            walker_type_var.set(walker_types[0])  # Set default value
            walker_type_optionmenu = tk.OptionMenu(walker_frame, walker_type_var, *walker_types)
            walker_type_optionmenu.config(width=10)
            walker_type_optionmenu.pack(side=tk.LEFT)

            walker_color_label = tk.Label(walker_frame, text="Color:")
            walker_color_label.pack(side=tk.LEFT)
            walker_color_var = tk.StringVar()
            walker_color_var.set(walker_colors[0])  # Set default value
            walker_color_optionmenu = tk.OptionMenu(walker_frame, walker_color_var, *walker_colors)
            walker_color_optionmenu.config(width=5)
            walker_color_optionmenu.pack(side=tk.LEFT)

            walker_location_label = tk.Label(walker_frame, text="Starting location (x,y):")
            walker_location_label.pack(side=tk.LEFT)
            walker_center_entry_x = tk.Entry(walker_frame, width=5)
            walker_center_entry_x.pack(side=tk.LEFT)
            walker_center_entry_y = tk.Entry(walker_frame, width=5)
            walker_center_entry_y.pack(side=tk.LEFT)

            self.__walkers_data.append({"Type": walker_type_var, "Color": walker_color_var,
                                         "Location": (walker_center_entry_x,walker_center_entry_y)})

        self.next_button = tk.Button(self.root, text="Next", command=self.create_barrier_input)
        self.next_button.pack()

    def create_barrier_input(self) ->None:
        self.clear_frame()

        barrier_input_frame = tk.Frame(self.root)
        barrier_input_frame.pack()

        for i in range(self.__num_barriers):
            barrier_frame = tk.Frame(barrier_input_frame)
            barrier_frame.pack()

            barrier_center_label = tk.Label(barrier_frame, text=f"Input for Barrier {i+1}: Center Location (x,y):")
            barrier_center_label.pack(side=tk.LEFT)
            barrier_center_entry = [0,0]
            barrier_center_entry_x = tk.Entry(barrier_frame, width=5)
            barrier_center_entry_x.pack(side=tk.LEFT)
            barrier_center_entry_y = tk.Entry(barrier_frame, width=5)
            barrier_center_entry_y.pack(side=tk.LEFT)

            barrier_length_label = tk.Label(barrier_frame, text=f"Length:")
            barrier_length_label.pack(side=tk.LEFT)
            barrier_length_entry = tk.Entry(barrier_frame)
            barrier_length_entry.pack(side=tk.LEFT)

            barrier_angle_label = tk.Label(barrier_frame, text=f"Angle:")
            barrier_angle_label.pack(side=tk.LEFT)
            barrier_angle_entry = tk.Entry(barrier_frame)
            barrier_angle_entry.pack(side=tk.LEFT)

            self.__barriers_data.append({"Center Location": float(barrier_center_entry),
                                       "Length": float(barrier_length_entry),
                                       "Angle": float(barrier_angle_entry)})
        if self.__num_barriers == 0:
            self.create_portal_input()
            pass
        self.next_button = tk.Button(self.root, text="Next", command=self.create_portal_input)
        self.next_button.pack()

    def create_portal_input(self) ->None:
        self.clear_frame()
        portal_input_frame = tk.Frame(self.root)
        portal_input_frame.pack()

        for i in range(self.__num_portals):
            portal_frame = tk.Frame(portal_input_frame)
            portal_frame.pack()

            portal_center_label = tk.Label(portal_frame, text=f"Center Location for Portal {i+1}  (x,y):")
            portal_center_label.pack(side=tk.LEFT)
            portal_center_entry = [0,0]
            portal_center_entry_x = tk.Entry(portal_frame)
            portal_center_entry_x.pack(side=tk.LEFT)
            portal_center_entry_y = tk.Entry(portal_frame)
            portal_center_entry_y.pack(side=tk.LEFT)

            barrier_length_label = tk.Label(portal_frame, text=f"Length for Portal {i+1}:")
            barrier_length_label.pack(side=tk.LEFT)
            barrier_length_entry = tk.Entry(portal_frame)
            barrier_length_entry.pack(side=tk.LEFT)

            barrier_angle_label = tk.Label(portal_frame, text=f"Angle for Portal {i+1}:")
            barrier_angle_label.pack(side=tk.LEFT)
            barrier_angle_entry = tk.Entry(portal_frame)
            barrier_angle_entry.pack(side=tk.LEFT)

            self.__barriers_data.append({"Center Location": (portal_center_entry_x,portal_center_entry_y),
                                       "Length": float(barrier_length_entry),
                                       "Angle": float(barrier_angle_entry)})

        if self.__num_portals == 0:
            self.create_mudspots_input()
            pass
        self.next_button = tk.Button(self.root, text="Next", command=self.create_mudspots_input)
        self.next_button.pack()

    def create_mudspots_input(self) ->None:
            self.clear_frame()
            barrier_input_frame = tk.Frame(self.root)
            barrier_input_frame.pack()

            for i in range(self.__num_mudspots):
                barrier_frame = tk.Frame(barrier_input_frame)
                barrier_frame.pack()

                barrier_center_label = tk.Label(barrier_frame, text=f"Center Location for Barrier {i+1}:")
                barrier_center_label.pack(side=tk.LEFT)
                barrier_center_entry = tk.Entry(barrier_frame)
                barrier_center_entry.pack(side=tk.LEFT)

                barrier_length_label = tk.Label(barrier_frame, text=f"Length for Barrier {i+1}:")
                barrier_length_label.pack(side=tk.LEFT)
                barrier_length_entry = tk.Entry(barrier_frame)
                barrier_length_entry.pack(side=tk.LEFT)

                barrier_angle_label = tk.Label(barrier_frame, text=f"Angle for Barrier {i+1}:")
                barrier_angle_label.pack(side=tk.LEFT)
                barrier_angle_entry = tk.Entry(barrier_frame)
                barrier_angle_entry.pack(side=tk.LEFT)

                self.__barriers_data.append({"Center Location": float(barrier_center_entry),
                                        "Length": float(barrier_length_entry),
                                        "Angle": float(barrier_angle_entry)})
            if self.__num_mudspots == 0:
                self.simulation_variables()
                pass
            self.next_button = tk.Button(self.root, text="Next", command=self.simulation_variables())
            self.next_button.pack()

    def simulation_variables(self) ->None:
        self.clear_frame()
        pass

    def run_simulation(self) ->None:
        simulation_data = {"Walkers": [], "Barriers": [], "Portals": [], "Mudspots": []}

        for walker in self.__walkers_data:
            simulation_data["Walkers"].append({"Type": walker["Type"].get(), "Color": walker["Color"].get()})

        for barrier in self.__barriers_data:
            simulation_data["Barriers"].append({"Center Location": barrier["Center Location"].get(),
                                                 "Length": barrier["Length"].get(),
                                                 "Angle": barrier["Angle"].get()})

        # Process the simulation data
        print("Simulation Data:", simulation_data)
        # Implement simulation logic here


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()



if __name__ == "__main__":
    simulation = Simulation()
    letters = ('Dup','Dright','Ddown','Dleft','Daxis')
    colors = "GCYR"
    for i in range(5):
        simulation.add_walker(Walker(letters[i], color= colors[1]))
    simulation.add_barrier(Barrier((0,10), 5, 0))
    simulation.add_portal(Portal((5,12),2.3))
    simulation.add_portal(Portal((-5,12),2.3))
    simulation.add_mud(Mud((-3,-4),6,3))

    simulation.plot_simulation(100)
    #simulation.simulation_average(5,500,10**5,"results.json")
    print("Done")
