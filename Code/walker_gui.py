"""
FILE : walker_gui.py
WRITER : Dori_Peleg , dori.plg , 207685306
EXERCISE : intro2cs final_project 2024
DESCRIPTION: A calss for barrier objects within a simulation
STUDENTS I DISCUSSED THE EXERCISE WITH:
WEB PAGES I USED:
NOTES: ...
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import functools as ft
from typing import Optional
from Code.helper_functions import SimulationError, is_intable,is_int,is_float,save_to_json
from Code.simulation import run_and_plot, run_from_json
from Code.td_simulation import run_from_dict
from Code.walker import Walker
from Code.data_generator import random_simulation

MOVE_DICT = {Walker.move_dict()[k]: k for k in Walker.move_dict()}
COLOR_PALLET = Walker.color_pallet()
SIMU_SUFIX = "_simulation.json"



class SimulationGUI:
    """
    A class managing the program UI and user input for the Random Walker Simulation App.

    Attributes:
        root (tk.Tk): The root window of the application.

    Methods:
        __init__(self, root: tk.Tk) -> None:
            Initializes the SimulationGUI class.

        load_from_file(self) -> None:
            Loads a simulation from a JSON file.

        clear_frame(self) -> None:
            Clears the frame by destroying all widgets.

        user_input(self, frame: tk.Frame, var_type: Type[tk.Variable], n_inputs: int = 1,
                   message: str = None, def_values: List = None, width: int = 5) 
                   -> List[tk.Variable]:
            Creates input fields for user input.

        add_exit_button(self) -> None:
            Adds an exit button to the GUI.

        add_home_button(self) -> None:
            Adds a home button to the GUI.

        build_simulation(self, err_message: str = None) -> None:
            Builds the simulation UI for user input.

        check_build_input(self) -> bool:
            Checks the user input for building the simulation.

        create_walker_input(self) -> None:
            Creates input fields for walker data.

        create_barrier_input(self) -> None:
            Creates input fields for barrier data.
    """


    def __init__(self, root: tk.Tk) -> None:
        """
        Initializes the WalkerGUI class.

        Args:
            root: The root window of the application.

        Returns:
            None
        """
        self.__root = root
        self.clear_frame()
        self.__root.title("Simulation App")
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        window_position_x = int((screen_width - window_width) / 2)
        window_position_y = int((screen_height - window_height) / 2)
        self.__root.geometry(
            f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")

        welcome_label = tk.Label(self.__root,
                                      text="Welcome to the Random Walker Simulation App!")
        welcome_label.pack(pady=10)

        load_button = tk.Button(self.__root,
                                     text="Load Simulation from JSON",
                                     command=self.load_from_file)
        load_button.pack()

        manual_button_2d = tk.Button(self.__root,
                                       text="Manually Build 2D Simulation",
                                       command=ft.partial(self.build_simulation,dimension=2))
        manual_button_2d.pack()

        random_2d_button = tk.Button(self.__root,
                                        text="Randomly Build 2D Simulation",
                                        command=self.run_random_simulation)
        random_2d_button.pack()
        
        manual_button_3d = tk.Button(self.__root,
                                       text="Manually Build 3D Simulation, plotting only",
                                       command=ft.partial(self.build_simulation,dimension=3))
        manual_button_3d.pack()

        # Setting the GUI attributes
        self.__num_walkers = tk.DoubleVar()
        self.__num_barriers = tk.DoubleVar()
        self.__num_portals = tk.DoubleVar()
        self.__num_mudspots = tk.DoubleVar()

        self.__walkers_data: list[dict[str, tk.Variable]] = []
        self.__barriers_data: list[dict[str, tk.Variable]] = []
        self.__portals_data: list[dict[str, tk.Variable]] = []
        self.__mudspots_data: list[dict[str, tk.Variable]] = []
        self.__simulation_variables: dict[str, tk.Variable] = {}
        self.__simulation_path: dict[str, tk.Variable] = {}

        self.bottom_buttons()

    def load_from_file(self) -> None:
        """
        Loads data from a JSON file and runs the simulation.

        If the JSON file is valid, it clears the frame and runs the simulation.
        If the JSON file is invalid, it displays an error message and prompts
        the user to enter the data manually.
        """
        try:
            self.run_simulation()
        except ValueError:
            self.build_simulation(2,err_message="Invalid input, please enter manually")
        except AttributeError:
            self.clear_frame()
            SimulationGUI(root=self.__root)

    def clear_frame(self) -> None:
        """
        Clears the frame by destroying all widgets.
        """
        for widgets in self.__root.winfo_children():
            widgets.destroy()

    def user_input(self, frame: tk.Frame, var_type = tk.Variable, n_inputs: int =1,
                   message: Optional[str] = None, def_values: Optional[list] = None, width: int =5)\
                      -> list[tk.Variable]:
        """
        A function for recieving user input
        :param frame: the frame in which it will exist
        :param var_type: the type of variable to recieve
        :param n_inputs: the number of inputs to recieve
        :def_values: the default values for the entry, as a tuple
        :param message: the message to display, if None, no label willl be shown
        :param width: the width of the input box
        """
        variables = []
        if message:
            label = tk.Label(frame, text=message)
            label.pack(side=tk.TOP)
        if var_type is tk.IntVar:
            # Function to validate entry input
            validate = (self.__root.register(is_intable), '%P')
        elif var_type is tk.DoubleVar:
            # Function to validate entry input
            validate = (self.__root.register(is_float), '%P')
        input_frame = tk.Frame(frame)
        for i in range(n_inputs):
            var = var_type()
            entry = tk.Entry(input_frame, textvariable=var, width=width)
            if def_values and len(def_values)>i:
                var.set(value=def_values[i] if def_values[i] != 0 else "")
            else:
                var.set("")
            entry.pack(side=tk.LEFT)

            # Apply validation
            entry.config(validate="key", validatecommand=validate)
            variables.append(var)

        input_frame.pack()
        return variables
    single_int_user_input = ft.partial(user_input,var_type=tk.IntVar,n_inputs=1)
    single_float_user_input = ft.partial(user_input,var_type=tk.DoubleVar,n_inputs=1)
    double_float_user_input = ft.partial(user_input,var_type=tk.DoubleVar,n_inputs=2)
    triple_float_user_input = ft.partial(user_input,var_type=tk.DoubleVar,n_inputs=3)

    def bottom_buttons(self) -> None:
        """
        Adds the home and exit buttons to the GUI.

        This method adds the "Home" and "Exit" buttons to the GUI window.

        Args:
            None

        Returns:
            None
        """
        def add_exit_button(frame: tk.Frame):
            """
            Add an exit button to the GUI.

            This method creates a button labeled "Exit" and adds it to the GUI window.
            When the button is clicked, it will quit the application.

            Args:
                None

            Returns:
                None
            """
            exit_button = tk.Button(frame, text="Exit", command=self.__root.quit)
            exit_button.pack(side=tk.RIGHT, padx=10)

        def add_home_button(frame: tk.Frame):
            """
            Adds a home button to the GUI.

            This method creates a tkinter Button widget with the text "Home" and
            associates it with the `build_simulation` method as the command to be
            executed when the button is clicked. The button is then packed into the root window.

            Parameters:
                None

            Returns:
                None
            """
            home_button = tk.Button(frame, text="Home",
                                    command=ft.partial(SimulationGUI,root=self.__root))
            home_button.pack(side=tk.LEFT, padx=10)

        button_frame = tk.Frame(self.__root)
        add_home_button(button_frame)
        add_exit_button(button_frame)
        button_frame.pack(side=tk.BOTTOM, pady=5)

    def build_simulation(self, dimension: int, err_message: Optional[str] = None) ->None:
        """
        Builds the simulation GUI by creating and packing the necessary widgets.
        
        Args:
            err_message (str, optional): Error message to display. Defaults to None.
        """

        self.clear_frame()
        self.__num_walkers.set(1)
        self.__num_barriers.set(0)
        self.__num_portals.set(0)
        self.__num_mudspots.set(0)


        if err_message:
            error_message = tk.Label(self.__root,text= err_message, fg="red2")
            error_message.pack()
        num_walkers_label = tk.Label(self.__root, text="Number of Walkers:")
        num_walkers_label.pack()
        num_walkers_entry = tk.Entry(self.__root, textvariable=self.__num_walkers)
        num_walkers_entry.pack()

        num_barriers_label = tk.Label(self.__root, text="Number of Barriers:")
        num_barriers_label.pack()
        num_barriers_entry = tk.Entry(self.__root, textvariable=self.__num_barriers)
        num_barriers_entry.pack()

        num_portals_label = tk.Label(self.__root, text="Number of Portals:")
        num_portals_label.pack()
        num_portals_entry = tk.Entry(self.__root, textvariable=self.__num_portals)
        num_portals_entry.pack()

        num_mudspots_label = tk.Label(self.__root, text="Number of Mudspots:")
        num_mudspots_label.pack()
        num_mudspots_entry = tk.Entry(self.__root, textvariable=self.__num_mudspots)
        num_mudspots_entry.pack()


        build_button = tk.Button(self.__root, text="Build", command=ft.partial(self.check_build_input,dimension=dimension))
        build_button.pack()

        self.bottom_buttons()

    def check_build_input(self,dimension: int) -> bool:
        """
        Checks the input values for building the simulation.

        Returns:
            bool: True if the input values are valid, False otherwise.
        """
        try:
            if is_int(self.__num_walkers.get()) and \
            is_int(self.__num_barriers.get()) and \
            is_int(self.__num_portals.get()) and \
            is_int(self.__num_mudspots.get()):
                num_walkers = int(self.__num_walkers.get())
                num_barriers = int(self.__num_barriers.get())
                num_portals = int(self.__num_portals.get())
                num_mudspots = int(self.__num_mudspots.get())
            else:
                self.build_simulation(dimension, err_message="All input must be whole numbers!")
                return False
        except Exception as ex:
            self.build_simulation(dimension, err_message=f"{ex}\nAll input must be numbers!")
            return False

        if num_walkers <1 or num_barriers < 0 or\
            num_portals <0 or num_mudspots <0:
            err_msg =""
            if num_walkers <1:
                err_msg += "Simulation must have at least one walker\n"
            if num_barriers < 0 or\
                num_portals <0 or num_mudspots <0:
                err_msg += "Negative number of obstacles impossible"
            self.build_simulation(dimension, err_message=err_msg)
            return False
        self.create_walker_input(dimension)
        return True

    def create_walker_input(self, dimension: int) -> None:
        """
        Creates the input interface for walkers.

        It creates a frame for walker input and iterates over the number of walkers specified.
        For each walker, it creates a frame and adds input fields for walker type and color.
        It also prompts the user for the starting location of the walker.
        The walker data is stored in the __walkers_data list.

        Finally, it adds a "Next" button to proceed to creating barrier input and
        calls the bottom_buttons method.
        """
        self.clear_frame()


        walker_input_frame = tk.Frame(self.__root)
        walker_input_frame.pack()

        if dimension == 2:
            walker_types = tuple(MOVE_DICT.keys())
            walker_colors = tuple(COLOR_PALLET)

            num_walkers = int(self.__num_walkers.get())
            for i in range(num_walkers):
                walker_frame = tk.Frame(walker_input_frame)
                walker_frame.pack()

                walker_type_label = tk.Label(walker_frame, text=f"Input for Walker {i+1}: Type:")
                walker_type_label.pack(side=tk.LEFT)
                walker_type_var = tk.StringVar()
                walker_type_var.set(walker_types[0])  # Set default value
                walker_type_optionmenu = tk.OptionMenu(walker_frame, walker_type_var, *walker_types)
                walker_type_optionmenu.config(width=20)
                walker_type_optionmenu.pack(side=tk.LEFT)

                walker_color_label = tk.Label(walker_frame, text="Color:")
                walker_color_label.pack(side=tk.LEFT)
                walker_color_var = tk.StringVar()
                walker_color_var.set(walker_colors[0])  # Set default value
                walker_color_optionmenu = tk.OptionMenu(walker_frame, walker_color_var, *walker_colors)
                walker_color_optionmenu.config(width=5)
                walker_color_optionmenu.pack(side=tk.LEFT)

                walker_center_x,walker_center_y=\
                    self.double_float_user_input(self,walker_frame,def_values=[0,0],
                                                message="Starting location (x,y):",width=5)

                self.__walkers_data.append({
                    "Type": walker_type_var, 
                    "Color": walker_color_var,
                    "Locationx": walker_center_x,
                    "Locationy": walker_center_y,
                    })
        elif dimension == 3:
            num_walkers = int(self.__num_walkers.get())
            for i in range(num_walkers):
                walker_frame = tk.Frame(walker_input_frame)
                walker_frame.pack()

                walker_center_x, walker_center_y, walker_center_z =\
                    self.triple_float_user_input(self, walker_frame,
                                                 message="Starting location (x,y,z):", width=5)
                
                self.__walkers_data.append({
                    "Locationx": walker_center_x,
                    "Locationy": walker_center_y,
                    "Locationz": walker_center_z
                })
        next_button = tk.Button(self.__root, text="Next",
                                command=ft.partial(self.create_barrier_input,dimension=dimension))
        next_button.pack()

        self.bottom_buttons()

    def create_barrier_input(self, dimension: int) -> None:
        """
        Creates the barrier input interface.

        This method clears the frame, creates a barrier input frame, and prompts the user to input
        information for each barrier. The barrier information includes the center location (x, y),
        length, and angle. The barrier data is stored in the __barriers_data list.

        If there are no barriers, the method calls the create_portal_input method. Otherwise, it
        creates a "Next" button and calls the bottom_buttons method.

        Returns:
            None
        """
        self.clear_frame()

        barrier_input_frame = tk.Frame(self.__root)
        barrier_input_frame.pack()

        num_barriers = int(self.__num_barriers.get())
        for i in range(num_barriers):
            barrier_frame = tk.Frame(barrier_input_frame)
            barrier_frame.pack()

            if dimension == 2:
                barrier_center_x, barrier_center_y = self.double_float_user_input(
                    self, barrier_frame,
                    message=f"Input for Barrier {i+1}: Center Location (x, y):", width=5
                )
                barrier_length = self.single_float_user_input(
                    self, barrier_frame, message="Length"
                )[0]

                barrier_angle = self.single_float_user_input(
                    self, barrier_frame, message="Angle:"
                )[0]

                self.__barriers_data.append(
                    {
                        "Locationx": barrier_center_x,
                        "Locationy": barrier_center_y,
                        "Length": barrier_length,
                        "Angle": barrier_angle,
                    })
            elif dimension == 3:
                instrustions =\
                    "Barrieres are defined by three points projected to a parallelogram,\n\
with the second two points serving as the corners between a diagonal. The fourth corner will be projected from the first corner."
                message = tk.Label(barrier_input_frame, text=instrustions)
                message.pack(side=tk.TOP)

                barrier_corner_x, barrier_corner_y, barrier_corner_z =\
                    self.triple_float_user_input(self, barrier_frame,
                                                    message="First corner (x,y,z):", width=5)
                barrier_point1_x, barrier_point1_y, barrier_point1_z =\
                    self.triple_float_user_input(self, barrier_frame,
                                                    message="Second corner (x,y,z):", width=5)
                barrier_point2_x, barrier_point2_y, barrier_point2_z =\
                    self.triple_float_user_input(self, barrier_frame,
                                                    message="Third corner (x,y,z):", width=5)
                
                self.__barriers_data.append({
                    "Cornerx": barrier_corner_x,
                    "Cornery": barrier_corner_y,
                    "Cornerz": barrier_corner_z,
                    "Point1x": barrier_point1_x,
                    "Point1y": barrier_point1_y,
                    "Point1z": barrier_point1_z,
                    "Point2x": barrier_point2_x,
                    "Point2y": barrier_point2_y,
                    "Point2z": barrier_point2_z
                })

        if num_barriers == 0:
            self.create_portal_input(dimension=dimension)
            return

        next_button = tk.Button(self.__root, text="Next",
                                command=ft.partial(self.create_portal_input,dimension=dimension))
        next_button.pack()

        self.bottom_buttons()

    def create_portal_input(self, dimension: int) -> None:
        """
        Creates the input interface for the portals.
        Clears the frame and creates a new frame for portal input.
        Prompts the user to input the center location, radius, and destination for each portal.
        Stores the portal data in the __portals_data list.
        If there are no portals, calls the create_mudspots_input method.
        Adds the "Next" button to proceed to the mudspots input.
        Adds the home and exit buttons.
        """
        self.clear_frame()
        portal_input_frame = tk.Frame(self.__root)
        portal_input_frame.pack()

        num_portals = int(self.__num_portals.get())
        for i in range(num_portals):
            portal_frame = tk.Frame(portal_input_frame)
            portal_frame.pack()

            if dimension == 2:
                portal_center_x, portal_center_y = \
                    self.double_float_user_input(self, portal_frame,
                                        message=f"Input for Portal {i+1}: Center Location (x,y):",
                                        width=5)
                portal_radius = \
                    self.single_float_user_input(self, portal_frame,
                                                message="Portal radius:")[0]

                portal_dest_x, portal_dest_y = \
                    self.double_float_user_input(self, portal_frame,
                                                message="Destination (x,y):", width=5)

                self.__portals_data.append({"Centerx": portal_center_x,
                                            "Centery": portal_center_y,
                                            "Radius": portal_radius,
                                            "Destinationx": portal_dest_x,
                                            "Destinationy": portal_dest_y})
            elif dimension == 3:
                portal_center_x, portal_center_y, portal_center_z =\
                    self.triple_float_user_input(self, portal_frame,
                                                 message=f"Input for Portal {i+1}: Center Location (x,y,z):",
                                                 width=5)
                portal_radius = self.single_float_user_input(
                    self, portal_frame, def_values=[1], message="Portal radius:"
                )[0]
                portal_dest_x, portal_dest_y, portal_dest_z =\
                    self.triple_float_user_input(self, portal_frame,
                                                 message="Destination (x,y,z):", width=5)

                self.__portals_data.append({
                    "Centerx": portal_center_x,
                    "Centery": portal_center_y,
                    "Centerz": portal_center_z,
                    "Radius": portal_radius,
                    "Destinationx": portal_dest_x,
                    "Destinationy": portal_dest_y,
                    "Destinationz": portal_dest_z
                })
        if num_portals == 0:
            self.create_mudspots_input(dimension=dimension)
            return
        next_button = tk.Button(self.__root, text="Next",
                                command=ft.partial(self.create_mudspots_input,dimension=dimension))
        next_button.pack()

        self.bottom_buttons()

    def create_mudspots_input(self, dimension: int) -> None:
        """
        Creates the input interface for specifying mudspots.

        This method clears the frame, creates a new frame for mudspot input,
        and prompts the user to input the details of each mudspot, such as
        the bottom-left corner coordinates and the width and height of the patch.

        Returns:
            None
        """
        self.clear_frame()
        mudspot_input_frame = tk.Frame(self.__root)
        mudspot_input_frame.pack()

        num_mudspots = int(self.__num_mudspots.get())
        for i in range(num_mudspots):
            mudspot_frame = tk.Frame(mudspot_input_frame)
            mudspot_frame.pack()

            if dimension == 2:
                bottom_left_x, bottom_left_y = self.double_float_user_input(
                    self, mudspot_frame,
                    message=f"Input for Mudspot{i+1} Bottom-left corner (x,y):"
                )
                width, height = self.double_float_user_input(
                    self, mudspot_frame, def_values=[1, 1],
                    message="Width and Height of the patch:"
                )

                self.__mudspots_data.append({
                    "Locationx": bottom_left_x,
                    "Locationy": bottom_left_y,
                    "Width": width,
                    "Height": height
                })
            elif dimension == 3:
                bottom_left_x, bottom_left_y, bottom_left_z =\
                    self.triple_float_user_input(self, mudspot_frame,
                                                 message=f"Input for Mudspot{i+1} Bottom-left corner (x,y,z):",
                                                 width=5)
                width, height, depth = self.triple_float_user_input(
                    self, mudspot_frame, def_values=[1, 1, 1],
                    message="Width, Height and Depth of the patch:"
                )

                self.__mudspots_data.append({
                    "Locationx": bottom_left_x,
                    "Locationy": bottom_left_y,
                    "Locationz": bottom_left_z,
                    "Width": width,
                    "Height": height,
                    "Depth": depth
                })
        if num_mudspots == 0:
            self.simulation_variables(dimension=dimension)
            return

        next_button = tk.Button(self.__root, text="Next",
                                command=ft.partial(self.simulation_variables,dimension=dimension))
        next_button.pack()
        self.bottom_buttons()

    __gravity_dictionary = {"No gravity": 0, "Possitive gravity": 1, "Negative gravity": -1}
    __plotting_simulation = True
    def simulation_variables(self, dimension: int) -> None:
        """
        Sets up the simulation variables and user interface for selecting simulation options.

        This method clears the frame, creates a new frame for simulation input, and adds buttons
        and input fields for selecting simulation options. The user can toggle between plotting
        simulation and graphing simulation, and provide input values such as number of steps, number
        of iterations, maximum depth, and step interval.

        The selected simulation options are stored in the `__simulation_data` dictionary and the
        selected directory path and simulation name are stored in the `__simulation_path`
        dictionary.

        This method also adds labels and buttons for selecting the directory path and
        simulation name, and a button for running the simulation.

        Returns:
            None
        """
        self.clear_frame()
        simulation_input_frame = tk.Frame(self.__root)
        simulation_input_frame.pack()


        if dimension == 2:
            def switch_simulation() -> None:

                if self.__plotting_simulation:
                    self.__plotting_simulation = False
                    self.simulation_variables(dimension=dimension)
                else:
                    self.__plotting_simulation = True
                    self.simulation_variables(dimension=2)
            simulation_type = tk.Button(simulation_input_frame,
                                        text="Toggle the type of simulation you would prefer",
                                            command=switch_simulation)
            simulation_type.pack()

        # The parts differing between the two types of simulations
        if self.__plotting_simulation or dimension == 3:
            title =\
                tk.Label(self.__root,
                text="\nPlotting simulation (will show graphs tracing each walker)")
            title.pack()
            iterations =self.single_int_user_input(self,
                simulation_input_frame, def_values=[200],
                message="How many steps do you wish to plot for?", width= 20)[0]

            plotting = tk.StringVar(value="plot")
            self.__simulation_variables = {"type": plotting,
                                    "n": iterations}
        else:
            title =\
                    tk.Label(self.__root,
            text="\nGraphing simulation (will show graphs detailing different\
data for different number of iterations)")
            title.pack()

            iterations =self.single_int_user_input(self,
                simulation_input_frame, def_values=[5],
                message="How many iterations do you wish to average for?", width= 5)[0]

            n_iterations =self.single_int_user_input(self,
                simulation_input_frame, def_values=[1000],
                message="How many maximum steps do you wish to plot for?", width= 5)[0]

            steps=self.single_int_user_input(self,
                simulation_input_frame, def_values=[20],
                message="How many every how many steps do you want a point?", width= 5)[0]

            max_depth = self.single_int_user_input(self,
                simulation_input_frame, def_values=[100000],
                message="What is the max depth you'll allow the simulation to run for?",width= 5)[0]


            graph = tk.StringVar(value="graph")
            self.__simulation_variables = {"type": graph,
                                        "iterations": iterations,
                                        "max_depth": max_depth,
                                        "n": n_iterations,
                                        "steps": steps
            }


        gravity = tk.StringVar(value=list(self.__gravity_dictionary.keys())[0])
        gravity_checkbox = tk.OptionMenu(simulation_input_frame, gravity,
                                         *self.__gravity_dictionary.keys())
        gravity_checkbox.config(width=20)
        gravity_checkbox.pack()
        self.__simulation_variables["gravity"] = gravity

        reset = self.single_int_user_input(self,
            simulation_input_frame,
            message="What are the odds of a walker resetting?", width= 5)[0]
        self.__simulation_variables["reset"] = reset

        self.__simulation_variables["dimension"] = tk.IntVar(value=dimension)

        if dimension == 2:
            directory_path_var = tk.StringVar()
            def browse_directory() -> None:
                """
                Allows the user to browse for a directory to save the simulation data.
                """
                nonlocal directory_path_var
                file_path = filedialog.askdirectory()
                if file_path:
                    directory_path_var.set(file_path)
            dir_path_label = tk.Label(self.__root, text="Directory Path:")
            dir_path_label.pack(pady=10)
            directory_path_entry = tk.Entry(self.__root,
                                            textvariable=directory_path_var,
                                            state="readonly", width=50)
            directory_path_entry.pack()
            browse_button = tk.Button(self.__root,
                                            text="Choose where the simulation data will be saved",
                                            command=browse_directory)
            browse_button.pack(pady=10)
            file_path_label = tk.Label(self.__root, text="Simulation name:")
            file_path_label.pack(pady=10)
            file_path_var = tk.StringVar()
            file_path_entry = tk.Entry(self.__root,
                                            textvariable=file_path_var, width=20)
            file_path_entry.pack()


            self.__simulation_path = {"Directory": directory_path_var,
                                    "Filename":file_path_var}
        run_button = tk.Button(self.__root, text="Run simulation",
                                command=ft.partial(self.parse_simulation_data,dimension=dimension))
        run_button.pack()
        self.bottom_buttons()

    def parse_simulation_data(self, dimension: int) -> None:
        """
        Runs the simulation with the user input data.
        Returns: None
        """
        self.clear_frame()
        simulation_data: dict = {"Walkers": [], "Barriers": [], "Portals": [], "Mudspots": [], "Simulation": {}}

        try:
            if dimension == 2:
                for walker in self.__walkers_data:
                    location = [walker["Locationx"].get(), walker["Locationy"].get()]
                    simulation_data["Walkers"].append({"movement": MOVE_DICT[walker["Type"].get()],
                                                        "color": walker["Color"].get(),
                                                        "location": location})

                for barrier in self.__barriers_data:
                    location = [barrier["Locationx"].get(), barrier["Locationy"].get()]
                    simulation_data["Barriers"].append({"center": location,
                                                        "length": barrier["Length"].get(),
                                                        "angle": barrier["Angle"].get()})

                for portal in self.__portals_data:
                    center_location = [portal["Centerx"].get(), portal["Centery"].get()]
                    dest_location = [portal["Destinationx"].get(), portal["Destinationy"].get()]
                    simulation_data["Portals"].append({"center": center_location,
                                                        "endpoint": dest_location,
                                                        "radius": portal["Radius"].get()})

                for mudspot in self.__mudspots_data:
                    location = [mudspot["Locationx"].get(), mudspot["Locationy"].get()]
                    simulation_data["Mudspots"].append({"bottom_left": location,
                                                        "width": mudspot["Width"].get(),
                                                        "height": mudspot["Height"].get()})
            elif dimension == 3:
                for walker in self.__walkers_data:
                    location_t = (walker["Locationx"].get(), walker["Locationy"].get(), walker["Locationz"].get())
                    simulation_data["Walkers"].append({"position": location_t})

                for barrier in self.__barriers_data:
                    corner_t = (barrier["Cornerx"].get(), barrier["Cornery"].get(), barrier["Cornerz"].get())
                    point1_t = (barrier["Point1x"].get(), barrier["Point1y"].get(), barrier["Point1z"].get())
                    point2_t = (barrier["Point2x"].get(), barrier["Point2y"].get(), barrier["Point2z"].get())
                    simulation_data["Barriers"].append({"corner": corner_t,
                                                        "point_1": point1_t,
                                                        "point_2": point2_t})

                for portal in self.__portals_data:
                    center_location_t = (portal["Centerx"].get(), portal["Centery"].get(), portal["Centerz"].get())
                    dest_location_t = (portal["Destinationx"].get(), portal["Destinationy"].get(), portal["Destinationz"].get())
                    simulation_data["Portals"].append({"center": center_location_t,
                                                        "endpoint": dest_location_t,
                                                        "radius": portal["Radius"].get()})

                for mudspot in self.__mudspots_data:
                    location_t = (mudspot["Locationx"].get(), mudspot["Locationy"].get(), mudspot["Locationz"].get())
                    simulation_data["Mudspots"].append({"bottom_left": location_t,
                                                        "width": mudspot["Width"].get(),
                                                        "height": mudspot["Height"].get(),
                                                        "depth": mudspot["Depth"].get()})

            try:
                self.__simulation_variables["reset"].get()
            except tk.TclError:
                self.__simulation_variables["reset"].set(0)
            finally:
                simulation_data["Simulation"] =\
                    {item[0]: item[1].get() for item in self.__simulation_variables.items()}

        except tk.TclError:
            self.build_simulation(dimension, err_message="Invalid input, please re-enter.\n\
Did you remember to fill in all the fields?")
            return

        simulation_data["Simulation"]["gravity"] =\
            self.__gravity_dictionary[simulation_data["Simulation"]["gravity"]]

        if dimension == 2:
            directory = self.__simulation_path["Directory"].get()
            filename = self.__simulation_path["Filename"].get()
            if directory == "":
                directory = os.path.realpath(__file__).removesuffix("/walker_gui.py")
            if filename == "":
                filename = "null_name"
            path = directory + "/" + filename

            simulation_data["Simulation"]["filename"] = path

            if path == "/":
                path = os.path.realpath(__file__).removesuffix("walker_gui.py")+"null_name"
            save_to_json(simulation_data,path+SIMU_SUFIX)

        try:
            if dimension == 2:
                self.run_simulation(path)
            elif dimension == 3:
                self.simulation_3d(simulation_data)
        except ValueError:
            self.build_simulation(simulation_data["Simulation"]["dimension"], err_message="Invalid input, please re-enter")
        except AttributeError:
            self.clear_frame()
            SimulationGUI(self.__root)

    def show_results(self, path: str) -> None:
        """
        Shows the results of the simulation.
        Takes them from the photos with the same name as the simulation.
        """
        def shuffle_image():
            """
            An inner function to shuffle the image.
            """
            nonlocal current, image, image_label
            if current == "all":
                current = 0
            else:
                current += 1  # Increment the value of current
            try:
                image = tk.PhotoImage(file=f"{path}_{current}.png")
                image_label.configure(image=image)
            except tk.TclError:
                try:
                    current = "all"
                    image = tk.PhotoImage(file=f"{path}_{current}.png")
                    image_label.configure(image=image)
                except tk.TclError:
                    current = 0
                    image = tk.PhotoImage(file=f"{path}_{current}.png")
                    image_label.configure(image=image)

        #self.clear_frame()
        results_frame = tk.Frame(self.__root)
        results_frame.pack()

        results_label = tk.Label(results_frame, text="Results")
        results_label.pack()
        try:
            current = 0
            image = tk.PhotoImage(file=f"{path}_{current}.png")
            image_label = tk.Label(results_frame, image=image)
            image_label.pack()

            shuffle_button = tk.Button(results_frame, text="Change Image", command=shuffle_image)
            shuffle_button.pack()
        except tk.TclError:
            print(path)
            results_label = tk.Label(results_frame, text="No results to show")
            results_label.pack()
        finally:
            self.bottom_buttons()

    def run_simulation(self, path: Optional[str] = None) -> None:
        """
        Runs the simulation with the user input data.

        Args:
            path (str): A string containing the path to a simulation json.

        Returns:
            None
        """
        if path is None:
            path = ""
        data,path = run_from_json(path+SIMU_SUFIX)
        loading_screen = tk.Toplevel(self.__root)
        loading_screen.title("Loading")
        loading_screen.geometry("400x300")
        loading_label = tk.Label(loading_screen,
                                 text="Running simulation\nThis may take a while...")
        loading_label.pack()
        loading_screen.update()
        try:
            run_and_plot(data, path+SIMU_SUFIX)
        except SimulationError as e:
            messagebox.showerror("Error",
                                  f"There was a fundemental problem with the simulation: {e}")
        loading_screen.destroy()
        self.clear_frame()
        self.show_results(path)

    def run_random_simulation(self) -> None:
        """
        Runs a random simulation.

        Returns:
            None
        """
        path = random_simulation()
        self.run_simulation(path)

    def simulation_3d(self, data: dict) -> None:
        """
        Runs the 3D simulation with the user input data.

        Args:
            simulation_data (dict): A dictionary containing the simulation data.

        Returns:
            None
        """
        loading_screen = tk.Toplevel(self.__root)
        loading_screen.title("Loading")
        loading_screen.geometry("400x300")
        loading_label = tk.Label(loading_screen,
                                 text="Running simulation\nThis may take a while...")
        loading_label.pack()
        loading_screen.update()
        try:
            run_from_dict(data)
        except SimulationError as e:
            messagebox.showerror("Error",
                                  f"There was a fundemental problem with the simulation: {e}")
        except tk.TclError:
            pass
        finally:
            loading_screen.destroy()
            self.clear_frame()
            self.bottom_buttons()
