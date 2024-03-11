from helper_functions import load_simulation, is_int, is_float
from simulation import Simulation
from walker import Walker
import tkinter as tk
from tkinter import filedialog
from typing import Tuple

Coordinates = Tuple[float,float]
MOVE_DICT = {Walker.move_dict()[k]: k for k in Walker.move_dict()}
COLOR_PALLET = {Walker.color_pallet()[k]: k for k in Walker.color_pallet()}

class SimulationGUI:



    def __init__(self, root) ->None:
        self.root = root
        self.root.title("Simulation App")
        self.root.geometry("700x400")  # Set permanent window size

        self.welcome_label = tk.Label(self.root,
                                      text="Welcome to the Random Walker Simulation App!")
        self.welcome_label.pack(pady=10)

        self.load_button = tk.Button(self.root,
                                     text="Load Simulation from JSON", command=load_simulation)
        self.load_button.pack()

        self.manual_button = tk.Button(self.root,
                                       text="Manually Build Simulation", command=self.build_simulation)
        self.manual_button.pack()

    def clear_frame(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()

    def single_float_user_input(self,frame: tk.Frame,def_value = None,
                           message: str =None, width =5) -> tk.Entry:
        """
        allows user to make an input
        :param frame: the fraame where this is happening
        :def_value: the default value for the entry
        :param message: the message to display, if None, no label willl be shown
        :param width: the width of the input box
        """
        var = tk.DoubleVar()
        if message:
            label = tk.Label(frame, text=message)
            label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, textvariable=var, width=width)
        if def_value:
            entry.insert(0,def_value)
        entry.pack(side=tk.LEFT)
        return var, entry

    def double_float_user_input(self,frame: tk.Frame,def_value1 = None,
                           def_value2 = None, message: str =None, width = 5) -> tk.Entry:
        """
        allows user to make an input
        :param frame: the fraame where this is happening
        :def_value1: the default value for the entry1
        :def_value2: the default value for the entry2
        :param message: the message to display, if None, no label willl be shown
        :param width: the width of the input box
        """
        var1, var2 = tk.DoubleVar(), tk.DoubleVar()
        if message:
            label = tk.Label(frame, text=message)
            label.pack(side=tk.LEFT)
        entry1 = tk.Entry(frame, textvariable=var1, width=width)
        if def_value1:
            entry1.insert(0,def_value1)
        entry1.pack(side=tk.LEFT)
        entry2 = tk.Entry(frame, textvariable=var2, width=width)
        if def_value2:
            entry2.insert(0,def_value2)
        entry2.pack(side=tk.LEFT)
        return var1, var2, entry1, entry2

    def single_int_user_input(self,frame: tk.Frame,def_value = None,
                           message: str =None, width =5) -> tk.Entry:
        """
        allows user to make an input
        :param frame: the fraame where this is happening
        :def_value: the default value for the entry
        :param message: the message to display, if None, no label willl be shown
        :param width: the width of the input box
        """
        var = tk.IntVar()
        if message:
            label = tk.Label(frame, text=message)
            label.pack()
        entry = tk.Entry(frame, textvariable=var, width=width)
        if def_value:
            entry.insert(0,def_value)
        entry.pack()
        return var, entry

    def build_simulation(self, err_message: str = None) ->None:
        self.clear_frame()
        self.__num_walkers = tk.DoubleVar()
        self.__num_walkers.set(1)
        self.__num_barriers = tk.DoubleVar()
        self.__num_barriers.set(0)
        self.__num_portals = tk.DoubleVar()
        self.__num_portals.set(0)
        self.__num_mudspots = tk.DoubleVar()
        self.__num_mudspots.set(0)


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

        
        self.build_button = tk.Button(self.root, text="Build", command=self.check_build_input)
        self.build_button.pack()

    def check_build_input(self) -> bool:
        try:
            if is_int(self.__num_walkers.get()) and \
            is_int(self.__num_barriers.get()) and \
            is_int(self.__num_portals.get()) and \
            is_int(self.__num_mudspots.get()):
                self.__num_walker = int(self.__num_walkers.get())
                self.__num_barrier = int(self.__num_barriers.get())
                self.__num_portal = int(self.__num_portals.get())
                self.__num_mudspot = int(self.__num_mudspots.get())
            else:
                self.build_simulation(err_message="All input must be whole numbers!")
                return False
        except Exception as ex:
            self.build_simulation(err_message=f"{ex}\nAll input must be numbers!")
            return False

        if self.__num_walker <1 or self.__num_barrier < 0 or\
            self.__num_portal <0 or self.__num_mudspot <0:
            err_msg =""
            if self.__num_walker <1:
                err_msg += "Simulation must have at least one walker\n"
            if self.__num_barrier < 0 or\
                self.__num_portal <0 or self.__num_mudspot <0:
                err_msg += "Negative number of obstacles impossible"
            self.build_simulation(err_message=err_msg)
            return False
        self.create_walker_input()
        return True

    def create_walker_input(self):
        self.clear_frame()

        self.__walkers_data = []
        self.__barriers_data = []
        self.__portals_data = []
        self.__mudspots_data = []


        walker_input_frame = tk.Frame(self.root)
        walker_input_frame.pack()

        walker_types = tuple(MOVE_DICT.keys())
        walker_colors = tuple(COLOR_PALLET.keys())

        for i in range(self.__num_walker):
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

            walker_center_x,walker_center_y,\
            walker_center_entry_x, walker_center_entry_y =\
                self.double_float_user_input(walker_frame,0,0,"Starting location (x,y):",5)
            # Function to validate entry input
            validate_float = (self.root.register(is_float), '%P')

            # Apply validation to walker_center_entry_x and walker_center_entry_y
            walker_center_entry_x.config(validate="key", validatecommand=validate_float)
            walker_center_entry_y.config(validate="key", validatecommand=validate_float)

            self.__walkers_data.append({
                "Type": walker_type_var, 
                "Color": walker_color_var,
                "Locationx": walker_center_x,
                "Locationy": walker_center_y,
                 })
        self.next_button = tk.Button(self.root, text="Next", command=self.create_barrier_input)
        self.next_button.pack()

    def create_barrier_input(self) ->None:
        self.clear_frame()

        barrier_input_frame = tk.Frame(self.root)
        barrier_input_frame.pack()

        for i in range(self.__num_barrier):
            barrier_frame = tk.Frame(barrier_input_frame)
            barrier_frame.pack()

            barrier_center_x,barrier_center_y,\
            barrier_center_entry_x, barrier_center_entry_y =\
                self.double_float_user_input(barrier_frame,0,0,
                                             f"Input for Barrier {i+1}: Center Location (x,y):",5)
            barrier_length, barrier_length_entry =\
            self.single_float_user_input(barrier_frame,1,"Length")

            barrier_angle, barrier_angle_entry =\
            self.single_float_user_input(barrier_frame,0,"Angle:")

            # Function to validate entry input
            validate_float = (self.root.register(is_float), '%P')

            # Apply validation to walker_center_entry_x and walker_center_entry_y
            barrier_center_entry_x.config(validate="key", validatecommand=validate_float)
            barrier_center_entry_y.config(validate="key", validatecommand=validate_float)
            barrier_length_entry.config(validate="key", validatecommand=validate_float)
            barrier_angle_entry.config(validate="key", validatecommand=validate_float)

            self.__barriers_data.append({"Locationx": barrier_center_x,
                                         "Locationy":barrier_center_y,
                                       "Length": barrier_length,
                                       "Angle": barrier_angle})
        if self.__num_barrier == 0:
            self.create_portal_input()
            return
        self.next_button = tk.Button(self.root, text="Next", command=self.create_portal_input)
        self.next_button.pack()

    def create_portal_input(self) ->None:
        self.clear_frame()
        portal_input_frame = tk.Frame(self.root)
        portal_input_frame.pack()

        for i in range(self.__num_portal):
            portal_frame = tk.Frame(portal_input_frame)
            portal_frame.pack()

            portal_center_x,portal_center_y,\
            portal_center_entry_x, portal_center_entry_y =\
                self.double_float_user_input(portal_frame,0,0,
                                             f"Input for Portal {i+1}: Center Location (x,y):",5)
            portal_radius, portal_radius_entry =\
            self.single_float_user_input(portal_frame,1,"Portal radius:")

            portal_dest_x,portal_dest_y,\
            portal_dest_entry_x, portal_dest_entry_y =\
                self.double_float_user_input(portal_frame,0,0,
                                             "Destination (x,y):",5)

            # Function to validate entry input
            validate_float = (self.root.register(is_float), '%P')

            # Apply validation to walker_center_entry_x and walker_center_entry_y
            portal_center_entry_x.config(validate="key", validatecommand=validate_float)
            portal_center_entry_y.config(validate="key", validatecommand=validate_float)
            portal_radius_entry.config(validate="key", validatecommand=validate_float)
            portal_dest_entry_x.config(validate="key", validatecommand=validate_float)
            portal_dest_entry_y.config(validate="key", validatecommand=validate_float)

            self.__portals_data.append({"Centerx": portal_center_x,
                                        "Centery": portal_center_y,
                                       "Radius": portal_radius,
                                       "Destinationx": portal_dest_x,
                                       "Destinationy": portal_dest_y})

        if self.__num_portal == 0:
            self.create_mudspots_input()
            return
        self.next_button = tk.Button(self.root, text="Next", command=self.create_mudspots_input)
        self.next_button.pack()

    def create_mudspots_input(self) ->None:
            self.clear_frame()
            mudspot_input_frame = tk.Frame(self.root)
            mudspot_input_frame.pack()

            for i in range(self.__num_mudspot):
                mudspot_frame = tk.Frame(mudspot_input_frame)
                mudspot_frame.pack()

                bottom_left_x, bottom_left_y,\
                bottom_left_entry_x, bottom_left_entry_y =\
                self.double_float_user_input(mudspot_frame,0,0,f"Input for Mudspot{i+1} Bottom-left corner (x,y):")
                width, height, width_entry, height_entry =\
                self.double_float_user_input(mudspot_frame,1,1,"Width and Height of the patch:")

                # Function to validate entry input
                validate_float = (self.root.register(is_float), '%P')

                # Apply validation to walker_center_entry_x and walker_center_entry_y
                bottom_left_entry_x.config(validate="key", validatecommand=validate_float)
                bottom_left_entry_y.config(validate="key", validatecommand=validate_float)
                width_entry.config(validate="key", validatecommand=validate_float)
                height_entry.config(validate="key", validatecommand=validate_float)

                self.__mudspots_data.append({"Locationx": bottom_left_x,
                                             "Locationy": bottom_left_y,
                                        "Width": width,
                                        "Height": height})
            if self.__num_mudspot == 0:
                self.simulation_variables()
                return
            self.next_button = tk.Button(self.root, text="Next", command=self.simulation_variables())
            self.next_button.pack()

    def browse_file(self):
        file_path = filedialog.askopenfile()
        if file_path:
            self.directory_path_var.set(file_path)

    def browse_directory(self):
        file_path = filedialog.askdirectory()
        if file_path:
            self.directory_path_var.set(file_path)

    __ploting_simulation = True
    def simulation_variables(self) ->None:
        self.clear_frame()
        simulation_input_frame = tk.Frame(self.root)
        simulation_input_frame.pack()

        def switch_simulation():
            self.__ploting_simulation
            if self.__ploting_simulation:
                self.__ploting_simulation = False
                self.simulation_variables()
            else:
                self.__ploting_simulation = True
                self.simulation_variables()

        simulation_type = tk.Button(simulation_input_frame,
                                    text="Toggle the type of simulation you would prefer",
                                     command=switch_simulation)
        simulation_type.pack()

        if self.__ploting_simulation:
            title =\
                tk.Label(self.root,
                text="\nPlotting simulation (will show graphs tracing each walker)")
            title.pack()
            iterations, iterations_entry =\
            self.single_int_user_input(simulation_input_frame, def_value=200,
                                         message="How many steps do you wish to plot for?", width= 20)

            # Function to validate entry input
            validate_int = (self.root.register(is_int), '%P')

            # Apply validation to walker_center_entry_x and walker_center_entry_y
            iterations_entry.config(validate="key", validatecommand=validate_int)

            plotting = tk.StringVar(value="Plotting")
            self.__simulation_data = {"Type": plotting,
                                    "Iterations": iterations}
        else:
            title =\
                    tk.Label(self.root,
            text="\nGraphing simulation (will show graphs detailing different\
data for different number of iterations)")
            title.pack()

            iterations, iterations_entry =\
            self.single_int_user_input(simulation_input_frame, def_value=5,
                                         message="How many iterations do you wish to average for?", width= 5)

            max_iterations, max_iterations_entry =\
            self.single_int_user_input(simulation_input_frame, def_value=1000,
                                         message="How many maximum steps do you wish to plot for?", width= 5)

            jumps, jumps_entry =\
            self.single_int_user_input(simulation_input_frame, def_value=20,
                                         message="How many every how many steps do you want a point?", width= 5)

            """Number validation bad"""
            # Function to validate entry input
            validate_int = (self.root.register(is_int), '%P')

            # Apply validation to walker_center_entry_x and walker_center_entry_y
            iterations_entry.config(validate="key", validatecommand=validate_int)
            max_iterations_entry.config(validate="key", validatecommand=validate_int)
            jumps_entry.config(validate="key", validatecommand=validate_int)


            graph = tk.StringVar(value="graph")
            self.__simulation_data = {"Type": graph,
                                      "Iterations": iterations,
                                      "Max iterations": max_iterations,
                                      "Jumps": jumps}


        self.dir_path_label = tk.Label(self.root, text="Directory Path:")
        self.dir_path_label.pack(pady=10)

        self.directory_path_var = tk.StringVar()
        self.directory_path_entry = tk.Entry(self.root,
                                        textvariable=self.directory_path_var,
                                        state="readonly", width=50)
        self.directory_path_entry.pack()

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=10)

        self.file_path_label = tk.Label(self.root, text="File name:")
        self.file_path_label.pack(pady=10)

        self.file_path_var = tk.StringVar()
        self.file_path_entry = tk.Entry(self.root,
                                        textvariable=self.file_path_var, width=20)
        self.file_path_entry.pack()

        self.__simulation_path = {"Directory": self.directory_path_var,
                                  "Filename":self.file_path_var}
        self.run_button = tk.Button(self.root, text="Run simulation", command=self.run_simulation)
        self.run_button.pack()

    def run_simulation(self) ->None:
        self.clear_frame()
        simulation_data = {"Walkers": [], "Barriers": [], "Portals": [], "Mudspots": []}

        print(self.__walkers_data)
        for walker in self.__walkers_data:
            location = [walker["Locationx"].get(), walker["Locationy"].get()]
            simulation_data["Walkers"].append({"Type": MOVE_DICT[walker["Type"].get()],
                                                "Color": COLOR_PALLET[walker["Color"].get()],
                                                "Location": location})

        for barrier in self.__barriers_data:
            location = [barrier["Locationx"].get(), barrier["Locationy"].get()]
            simulation_data["Barriers"].append({"Center Location": location,
                                                 "Length": barrier["Length"].get(),
                                                 "Angle": barrier["Angle"].get()})

        for portal in self.__portals_data:
            center_location = [portal["Centerx"].get(), portal["Centery"].get()]
            dest_location = [portal["Destinationx"].get(), portal["Destinationy"].get()]
            simulation_data["Portals"].append({"Center": center_location,
                                                 "Destination": dest_location,
                                                 "Radius": portal["Radius"].get()})
            
        for mudspot in self.__mudspots_data:
            location = [mudspot["Locationx"].get(), mudspot["Locationy"].get()]
            simulation_data["Mudspots"].append({"Corner": location,
                                                 "Width": mudspot["Width"].get(),
                                                 "Height": mudspot["Height"].get()})

        path = self.__simulation_path["Directory"].get() +\
              self.__simulation_path["Filename"].get()
        simulation_data["Simulation"] =\
            {key: self.__simulation_data[key].get() for key in self.__simulation_data}
        simulation_data["Simulation"]["Path"] = path
        # Process the simulation data
        print("Simulation Data:", simulation_data)
        # Implement simulation logic here
