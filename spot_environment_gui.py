import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


import os
import spot_environment_controller


class SpotEnviornmentGui():
    def __init__(self, root, sec, name, debug=False):
        assert name != "", "Gui must have a name"

        self.root = root
        self.sec = sec
        self.name = name
        self.debug = debug
        root.title(name)

        self.num_buyers = 0
        self.num_sellers = 0
        self.num_units = 0
        self.string_num_buyers = tk.StringVar()
        self.string_num_sellers = tk.StringVar()
        self.string_num_units = tk.StringVar()
        self.string_project_name = tk.StringVar()
        self.string_eq = tk.StringVar()
        self.string_pl = tk.StringVar()
        self.string_ph = tk.StringVar()
        self.string_ms = tk.StringVar()
        self.current_row = 0
        self.current_row_contents = []
        self.ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.file_name = None
        self.buyer_values = self.build_array(self.num_buyers, self.num_units)
        self.seller_costs = self.build_array(self.num_sellers, self.num_units)

        # self.file_path = "C:\\Users\\Admin\\Desktop\\B04945_02_Code\\icons\\"
        #self.file_path = "C:\\Users\\Ksquared\\Desktop\\spot_market_environment\\icons\\"
        self.file_path = "C:\\Users\\Admin\\Desktop\\spot_market\\icons\\"
        #self.file_path = "C:\\Users\\Admin\\Desktop\\spot_market_environment_v1\\icons\\"
        #self.file_path ="C:\\Users\\kevin\\Desktop\\spot_market_working\\icons\\"
        #self.project_path="C:\\Users\\Ksquared\\Desktop\\spot_market_environment\\projects\\"
        #self.project_path = "C:\\Users\\Admin\\Desktop\\spot_market_environment_v1\\projects\\"
        #self.project_path = "C:\\Users\\kevin\\Desktop\\spot_market_working\\projects\\"
        self.project_path = "C:\\Users\\Admin\\Desktop\\spot_market\\projects\\"

        self.new_file_icon = tk.PhotoImage(file=self.file_path + 'new_file.gif')
        self.open_file_icon = tk.PhotoImage(file=self.file_path + 'open_file.gif')
        self.save_file_icon = tk.PhotoImage(file=self.file_path + 'save.gif')
        self.cut_icon = tk.PhotoImage(file=self.file_path + 'cut.gif')
        self.copy_icon = tk.PhotoImage(file=self.file_path + 'copy.gif')
        self.paste_icon = tk.PhotoImage(file=self.file_path + 'paste.gif')
        self.undo_icon = tk.PhotoImage(file=self.file_path + 'undo.gif')
        self.redo_icon = tk.PhotoImage(file=self.file_path + 'redo.gif')

        self.show_menu()
        self.show_shortcut()
        self.show_infobar()
        self.process_new_project()

    def build_array(self, num_1, num_2):
        x = []
        for j in range(num_1):
            a_row = []
            for k in range(num_2):
                a_row.append(k)
            x.append(a_row)
        return x

    def show_menu(self):
        # getting icons ready for compound menu

        menu_bar = tk.Menu(self.root)  # menu begins

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New', accelerator='Ctrl+N',
                              compound='left', image=self.new_file_icon, underline=0, command=self.process_new_project)
        file_menu.add_command(label='Open', accelerator='Ctrl+O',
                              compound='left', image=self.open_file_icon, underline=0, command=self.open_file)
        file_menu.add_command(label='Save', accelerator='Ctrl+S',
                              compound='left', image=self.save_file_icon, underline=0, command=self.save)
        file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+S', command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', accelerator='Alt+F4', command=self.on_quit_chosen)
        menu_bar.add_cascade(label='File', menu=file_menu)

        show_menu = tk.Menu(menu_bar, tearoff=0)
        show_menu.add_command(label='Plot', command=self.on_plot_clicked)
        show_menu.add_command(label='Show', command=self.on_show_clicked)
        show_menu.add_command(label='Calc EQ', command=self.on_calc_eq_clicked)
        menu_bar.add_cascade(label='Market', menu=show_menu)

        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label='About', command=self.display_about_messagebox)
        about_menu.add_command(label='Help', command=self.display_help_messagebox)
        menu_bar.add_cascade(label='About', menu=about_menu)

        root.config(menu=menu_bar)  # menu ends

    def show_shortcut(self):
        shortcut_bar = tk.Frame(self.root)
        shortcut_bar.grid(row=0, column=0, columnspan=4, sticky='W')

    def show_infobar(self):

        info_bar = tk.LabelFrame(self.root, height=15, text=str(self.name))
        info_bar.grid(row=1, column=0, columnspan=4, sticky='W', padx = 5, pady=5)

        tk.Label(info_bar, text="Project Name:").grid(row=0, column=0)
        tk.Entry(info_bar, width=15, justify=tk.LEFT, textvariable=self.string_project_name).grid(row=0, column=1,
                                                                                                 padx=5)

        tk.Label(info_bar, text="Number of Buyers: ").grid(row=0, column=2)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_num_buyers).grid(row=0, column=3,
                                                                                                 padx=5)
        self.string_num_buyers.set(str(self.num_buyers))

        tk.Label(info_bar, text="Number of Sellers: ").grid(row=0, column=4, padx=5)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_num_sellers).grid(row=0, column=5)
        self.string_num_sellers.set(str(self.num_sellers))

        tk.Label(info_bar, text="Number of Units: ").grid(row=0, column=6, padx=5)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_num_units).grid(row=0, column=7)
        self.string_num_units.set(str(self.num_units))

        info_button = tk.Button(info_bar, text="Set", width=4, command=self.on_set_parms_clicked)
        info_button.grid(row=0, column=8, padx=10, pady=5)

        tk.Label(info_bar, text="Equilibrium Q: ").grid(row=1, column=2)
        tk.Label(info_bar, width=4, justify=tk.CENTER, textvariable=self.string_eq, relief='sunken').grid(row=1, column=3)
        self.string_eq.set("U")

        tk.Label(info_bar, text="EQ Price Low: ").grid(row=1, column=4)
        tk.Label(info_bar, width=4, justify=tk.CENTER, textvariable=self.string_pl, relief='sunken').grid(row=1, column=5)
        self.string_pl.set("U")

        tk.Label(info_bar, text="EQ Price High: ").grid(row=1, column=6)
        tk.Label(info_bar, width=4, justify=tk.CENTER, textvariable=self.string_ph, relief='sunken').grid(row=1, column=7)
        self.string_ph.set("U")

        tk.Label(info_bar, text="   Max Surplus: ").grid(row=1, column=8, pady=15)
        tk.Label(info_bar, width=4, justify=tk.CENTER, textvariable=self.string_ms, relief='sunken').grid(row=1, column=9, padx=15)
        self.string_ms.set("U")

    def on_quit_chosen(self):
        if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
            root.destroy()

    def process_sd_string(self):
        if self.num_buyers == 0:
            return "Empty"
        else:
            s_d_list = self.sec.get_supply_demand_list()
            return s_d_list

    def on_calc_eq_clicked(self):
        qt, pl, ph, ms = sec.get_equilibrium()
        self.string_eq.set(str(qt))
        self.string_pl.set(str(pl))
        self.string_ph.set(str(ph))
        self.string_ms.set(str(ms))

    def on_show_clicked(self):
        if self.debug:
            print("In GUI -> on_show_clicked -> begin")
        self.set_market()
        lfr_show = tk.LabelFrame(root, text="List of Supply and Demand")
        lfr_show.grid(row=2, rowspan=3, column=2, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        lbl_show = tk.Label(lfr_show, text=self.process_sd_string())
        lbl_show.grid(row=0, column=0)
        if self.debug:
            print("In GUI -> on_show_clicked -> end")

    def on_plot_clicked(self):

        """ Plot Supply and Demand

        Plot supply and demand in a frame with toolbar.

        """
        # TODO: Fix axis labels and Title.  Commented out below.  Fail as is.
        if self.debug:
            print("In Gui -> on_plot_clicked --> begin")
        self.set_market()

        # set up frame to plot in
        fr_plot = tk.LabelFrame(root, text="Plot of Supply and Demand")
        fr_plot.grid(row=2, rowspan=2, column=3, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)

        # set up plot figure
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        if self.num_buyers == 0:
            canvas = FigureCanvasTkAgg(f, fr_plot)
            canvas.get_tk_widget().pack()  # Have to use pack here to work with toolbar.  Not sure why.
            canvas.show()
            if self.debug:
                print("In Gui -> on_plot_clicked --> early end")
            self.set_market()
            return
        # get some model information here
        dunits, sunits, munits, demand_values, supply_costs, eq_price_high, eq_price_low = sec.get_supply_demand_plot_info()
        if self.debug:
            print("In Gui --> 0n_plot_clicked  --> info from model")
            print("demand = {}".format(demand_values))
            print("supply = {}".format(supply_costs))

        # do some plotting here

        if eq_price_high != eq_price_low:
            a.plot(munits, [eq_price_high for x in munits], label='Price High')  # High Price Line
            a.plot(munits, [eq_price_low for x in munits], label='Price Low')  # Low Price Line
        else:
            a.plot(munits, [eq_price_high for x in munits], label='Price')  # Just one price

        a.step(dunits, demand_values, label='Demand')  # generate the demand plot
        a.step(sunits, supply_costs, label='Supply')  # generate the supply plot

        a.legend(bbox_to_anchor=(0.65, 0.98))  # places a legend on the plot
        #a.title('Supply and Demand')  # add the title
        #a.xlabel('Units')  # add the x axis label
        #a.ylabel('$')  # add the y axis label

        # finish setting up the canvas here
        canvas = FigureCanvasTkAgg(f, fr_plot)
        canvas.get_tk_widget().pack()  # Have to use pack here to work with toolbar.  Not sure why.
        canvas.show()

        # Add navigation bar:  This adds a toolbar.  This is optional and does not work yet
        toolbar = NavigationToolbar2TkAgg(canvas, fr_plot)
        toolbar.pack()  # This is the other pack.  Both go itno frame fr_plot
        toolbar.update()

        if self.debug:
            print("In Gui -> on_plot_clicked --> end")

    def set_market(self):

        """ Sends all values on screen to model
        """

        # Start with name and all that
        if self.debug:
            print("In Gui -> set_market -> begin")
        self.sec.set_market_parms([self.string_project_name.get(), self.num_buyers, self.num_sellers, self.num_units])

        make_d = {}

        # Now Add Buyer Values and Seller Costs
        make_d["buyers"]={}
        for k in range(self.num_buyers):
            make_d["buyers"][k]=[]
            for j in range(self.num_units):
                make_d["buyers"][k].append(int(self.buyer_values[k][j].get()))

        make_d["sellers"] = {}
        for k in range(self.num_sellers):
            make_d["sellers"][k] = []
            for j in range(self.num_units):
                make_d["sellers"][k].append(int(self.seller_costs[k][j].get()))

        # now make supply and demand
        if self.debug:
            print("In Gui -> set_market -> make_d")
            self.show_market(make_d)

        self.sec.make_market(make_d)
        self.sec.make_supply()
        self.sec.make_demand()
        if self.debug:
            print("In Gui -> set_market -> end")

    def show_market(self, make_d):

        if self.debug: print ("In Gui -> show_market -> begin")

        print("... name = {}".format(self.name))
        print("... num_buyers = {}".format(self.num_buyers))
        print("... num_sellers = {}".format(self.num_sellers))
        print("... num_units = {}".format(self.num_units))

        for k in range(self.num_buyers):
            print("... make_d[buyers][{}] = {}".format(k, make_d["buyers"][k]))
        for k in range(self.num_sellers):
            print("... make_d[sellers][{}] = {}".format(k, make_d["sellers"][k]))

        if self.debug: print("In Gui -> show_market -> end")


    def on_set_parms_clicked(self):
        """ Set parameters from info_bar
            Used to initalize a new experiment.  A messagebox allows the user to opt out.

        """

        if not messagebox.askyesno("DESTROY WORK", "This will destoy your work \n Do you wish to continue?"): return


        self.num_buyers = int(self.string_num_buyers.get())
        self.num_sellers = int(self.string_num_sellers.get())
        self.num_units = int(self.string_num_units.get())
        self.root.title(self.string_project_name.get())

        if self.num_buyers > 0 and self.num_units> 0:  # Build array if useful
            self.buyer_values = self.build_array(self.num_buyers, self.num_units)
        if self.num_sellers > 0 and self.num_units > 0:  # Build array if useful
            self.seller_costs = self.build_array(self.num_sellers, self.num_units)

        self.show_player_frames()
        self.sec.set_market_parms([self.string_project_name.get(), self.num_buyers, self.num_sellers, self.num_units])


    def on_button_clicked(self, row, col):
        def event_handler():
            self.process_button_clicked(row, col)

        return event_handler

    def process_button_clicked(self, row, col):
        self.target_row = row
        if self.debug == True:
            print("In GUI -> process button click row {} col {}".format(row, col))

        # implement copy button
        if col == 0:
            self.current_row_contents = [x for x in range(self.num_units)]
            if row < self.num_buyers:  # implement copy on buyers
                for k in range(self.num_units):
                    self.current_row_contents[k] = self.buyer_values[row][k].get()
            else:  # implement copy on sellers
                for k in range(self.num_units):
                    self.current_row_contents[k] = self.seller_costs[row-self.num_buyers][k].get()  # fix row to seller
        # implement replace buttons
        elif col == 1:
            if row < self.num_buyers:  # implement replace on buyers
                if len(self.current_row_contents) != self.num_units:
                    return
                for k in range(self.num_units):
                    self.buyer_values[row][k].set(self.current_row_contents[k])
            else:  # implement replace on sellers
                if len(self.current_row_contents) != self.num_units:
                    return
                for k in range(self.num_units):
                    self.seller_costs[row-self.num_buyers][k].set(self.current_row_contents[k])

        return

    def show_player_frames(self):
        self.show_buyers_frame()
        self.show_sellers_frame()

    def show_buyers_frame(self):
        bf = tk.LabelFrame(self.root, text="Buyer Entries")
        bf.grid(row=2, column=0, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        if self.num_buyers == 0: return   # Notihing to show
        self.buttons = [[None for x in range(3)] for x in range(self.num_buyers + self.num_sellers)]

        buy_ids = [k for k in range(self.num_buyers)]
        tk.Label(bf, text="ID").grid(row=0, column=0)
        for unit in range(self.num_units):
            sunit = "Unit " + str(unit + 1)
            tk.Label(bf, text=sunit).grid(row=0, column=unit + 1)
        for buyer in range(self.num_buyers):
            buy_ids[buyer] = tk.StringVar()
            tk.Entry(bf, width=5, justify=tk.CENTER, textvariable=buy_ids[buyer]).grid(row=buyer + 1, column=0)
            buy_ids[buyer].set(str(buyer + 1))
            for unit in range(self.num_units):
                self.buyer_values[buyer][unit] = tk.StringVar()
                tk.Entry(bf, width=5, justify=tk.RIGHT, textvariable=self.buyer_values[buyer][unit]).grid(row=buyer + 1,
                                                                                                          column=unit + 1)
                self.buyer_values[buyer][unit].set("")
            self.buttons[buyer][0] = tk.Button(bf, width=2, text="C", command=self.on_button_clicked(buyer, 0))
            self.buttons[buyer][0].grid(row=buyer + 1, column=self.num_units + 2)
            self.buttons[buyer][1] = tk.Button(bf, width=2, text="R", command=self.on_button_clicked(buyer, 1))
            self.buttons[buyer][1].grid(row=buyer + 1, column=self.num_units + 3)

    def show_sellers_frame(self):
        sf = tk.LabelFrame(self.root, text="Seller Entries")
        sf.grid(row=2, column=1, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        if self.num_sellers == 0: return  # Notihing to show
        sell_ids = [k for k in range(self.num_sellers)]
        tk.Label(sf, text="ID").grid(row=0, column=0)
        for unit in range(self.num_units):
            sunit = "Unit " + str(unit + 1)
            tk.Label(sf, text=sunit).grid(row=0, column=unit + 1)
        for seller in range(self.num_sellers):
            sell_ids[seller] = tk.StringVar()
            tk.Entry(sf, width=5, justify=tk.CENTER, textvariable=sell_ids[seller]).grid(row=seller + 1, column=0)
            sell_ids[seller].set(str(seller + 1))
            for unit in range(self.num_units):
                self.seller_costs[seller][unit] = tk.StringVar()
                tk.Entry(sf, width=5, justify=tk.RIGHT, textvariable=self.seller_costs[seller][unit]).grid(
                    row=seller + 1,
                    column=unit + 1)
                self.seller_costs[seller][unit].set("")
            row = self.num_buyers + seller
            self.buttons[row][0] = tk.Button(sf, width=2, text="C", command=self.on_button_clicked(row, 0))
            self.buttons[row][0].grid(row=seller + 1, column=self.num_units + 2)
            self.buttons[row][1] = tk.Button(sf, width=2, text="R", command=self.on_button_clicked(row, 1))
            self.buttons[row][1].grid(row=seller + 1, column=self.num_units + 3)

    def show_info_bar_parms(self):
        self.string_num_buyers.set(str(self.num_buyers))
        self.string_num_sellers.set(str(self.num_sellers))
        self.string_num_units.set(str(self.num_units))

    def process_new_project(self, event=None):
        if self.debug == True:
            print("In GUI -> process_new_project -> begin")
        self.root.title("Untitled")
        self.file_name = None
        self.string_project_name.set("Untitled")

        self.num_buyers = 0
        self.num_sellers = 0
        self.num_units = 0

        self.show_info_bar_parms()
        self.show_player_frames()

        self.on_show_clicked()
        self.on_plot_clicked()

        #self.set_market()
        #self.sec.reset_market()
        self.sec.show_environment()

        if self.debug == True:
            print("In GUI -> process_new_project -> end")

    def open_file(self, event=None):
        input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".csv",
                                                             filetypes=[("All Files", "*.*"),
                                                                        ("Text Documents", "*.txt")])
        if input_file_name:
            # global file_name
            self.file_name = input_file_name
            self.name = os.path.basename(self.file_name)
            indx = self.name.find(".")   # look for strt of .csv
            self.name = self.name[:indx] # and remove it from project name

            self.root.title('{}'.format(self.name))
            self.sec.load_file(self.file_name)
            self.show_project()

    def write_to_file(self, file_name):
        pass
        """
        try:
            content = content_text.get(1.0, 'end')
            with open(self.file_name, 'w') as the_file:
                the_file.write(content)
        except IOError:
            pass  # in actual we will show a error message box.
            # we discuss message boxes in the next section so ignored here.
        """

    def save_as(self, event=None):
        pass

    def save(self, event=None):
        # TODO:  Add existing file check
        self.set_market()
        self.project_path += self.string_project_name.get()
        self.sec.save_project(self.project_path)

    def display_about_messagebox(self, event=None):
        tkinter.messagebox.showinfo(
            "About", "{}{}".format(self.name, "\n\n Kevin McCabe \n\n August, 2017"))

    def display_help_messagebox(self, event=None):
        help_msg =  "Quick Help: \n\n"
        help_msg += "   File Menu \n"
        help_msg += "      New  - Create New Project \n"
        help_msg += "      Load - Load Project \n"
        help_msg += "      Save - Save Project \n\n"
        help_msg += "   Getting Started \n"
        help_msg += "      Enter unique Project Name\n"
        help_msg += "      Enter Number of Buyers \n"
        help_msg += "      Enter Number of Sellers \n"
        help_msg += "      Enter Number of Units \n"
        help_msg += "      Click Set Button \n"
        help_msg += "         Say yes to message box\n"
        help_msg += "         You will see Buyers and Sellers entries \n"
        tkinter.messagebox.showinfo("Help", help_msg)

    def show_project(self):
        self.num_buyers = sec.get_num_buyers()
        self.num_sellers = sec.get_num_sellers()
        self.num_units = sec.get_num_units()
        self.string_project_name.set(self.name)
        self.string_num_buyers.set(str(self.num_buyers))
        self.string_num_sellers.set(str(self.num_sellers))
        self.string_num_units.set(str(self.num_units))
        self.buyer_values = self.build_array(self.num_buyers, self.num_units)
        self.seller_costs = self.build_array(self.num_sellers, self.num_units)

        self.buyer_values = self.build_array(self.num_buyers, self.num_units)
        self.show_buyers_frame()
        self.set_all_buyer_values()

        self.seller_costs = self.build_array(self.num_sellers, self.num_units)
        self.show_sellers_frame()
        self.set_all_seller_costs()

    def set_all_buyer_values(self):
        for buyer in range(self.num_buyers):
            values = sec.get_buyer_values(buyer)
            self.set_buyer_values(buyer, values)

    def set_all_seller_costs(self):
        for seller in range(self.num_sellers):
            costs = sec.get_seller_costs(seller)
            self.set_seller_costs(seller, costs)

    def set_buyer_values(self, buyer, values):
        assert buyer < self.num_buyers, "Buyer {} not in range".format(buyer)
        assert len(values) == self.num_units, "values {} shoud have {} value units".format(values, self.num_units)
        for unit in range(self.num_units):
            self.buyer_values[buyer][unit].set(str(values[unit]))

    def set_seller_costs(self, seller, costs):
        assert seller < self.num_sellers, "seller {} not in range".format(seller)
        assert len(costs) == self.num_units, "costs {} shoud have {} cost units".format(costs, self.num_units)
        for unit in range(self.num_units):
            self.seller_costs[seller][unit].set(str(costs[unit]))

    def blank_arrays(self):
        for j in range(self.num_buyers):
            for k in range(self.num_units):
                self.buyer_values[j][k].set("")
        for j in range(self.num_sellers):
            for k in range(self.num_units):
                self.seller_costs[j][k].set("")


if __name__ == "__main__":
    # setup gui
    root = tk.Tk()
    debug_test = True
    if debug_test:
        print("In Gui -> START")
    sec = spot_environment_controller.SpotEnvironmentController(debug_test)
    gui = SpotEnviornmentGui(root, sec, "Spot Market Editor", debug_test)
    root.mainloop()
    if debug_test:
        print("In Gui -> END")