# OctaDist  Copyright (C) 2019-2024  Rangsiman Ketkaew et al.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import tkinter as tk

import octadist


class ScriptingConsole:
    """
    Start scripting interface for an interactive code.

    User can access to class variable (dynamic variable).

    +------------+
    | Output box |
    +------------+
    | Input box  |
    +------------+

    Parameters
    ----------
    root : object
        Passing self object from another class to this class as root argument.

    See Also
    --------
    settings :
        Program settings.

    Examples
    --------
    >>> import tkinter as tk
    >>> master = tk.Tk()
    >>> console = ScriptingConsole(master)
    >>> console.scripting_start()

    """

    def __init__(self, root):
        self.root = root
        self.wd = None
        self.history_command = []

    def scripting_start(self):
        """
        Start scripting console.

        """

        self.wd = tk.Toplevel(self.root.master)
        if self.root.octadist_icon is not None:
            self.wd.wm_iconbitmap(self.root.octadist_icon)
        self.wd.title("OctaDist Scripting Interface")
        self.wd.bind("<Return>", self.script_execute)
        self.wd.resizable(0, 0)

        lbl = tk.Label(self.wd, text="Output:")
        lbl.grid(padx="5", pady="5", sticky=tk.W, row=0, column=0)
        self.box_script = tk.Text(self.wd, width=70, height=20)
        self.box_script.grid(padx="5", pady="5", row=1, column=0, columnspan=2)
        lbl = tk.Label(self.wd, text="Input:")
        lbl.grid(padx="5", pady="5", sticky=tk.W, row=2, column=0)
        self.entry_script = tk.Entry(self.wd, width=62)
        self.entry_script.grid(padx="5", pady="5", sticky=tk.W, row=3, column=0)
        btn_script = tk.Button(self.wd, text="Run")
        btn_script.bind("<Button-1>", self.script_execute)
        btn_script.grid(padx="5", pady="5", row=3, column=1)

        self.box_script.insert(
            tk.INSERT, "Welcome to OctaDist interactive scripting console\n"
        )
        self.box_script.insert(
            tk.INSERT,
            "If you have no idea what to do about scripting, "
            'type "help" to get started.\n\n',
        )

        self.wd.mainloop()

    def script_run_help(self):
        """
        Show help messages.

        """
        help_msg = f"""\
>>> Interactive code console for OctaDist.
>>> This scripting interface supports built-in commands as follows:
>>> 
>>> Command\t\tDescription
>>> =======\t\t===========
>>> help\t\tShow this help info.
>>> list\t\tList all commands.
>>> info\t\tShow info of program.
>>> doc\t\tShow docstring of this function.
>>> show\t\tShow values of variables.
>>> \t\tUsage: show var1 [var2] [var3] [...]
>>> type\t\tShow type of variables.
>>> \t\tUsage: type var1 [var2] [var3] [...]
>>> set\t\tSet new value to variable.
>>> \t\tUsage: set var value
>>> clear\t\tClear stdout/stderr.
>>> clean\t\tClear stdout/stderr and command history.
>>> \t\thistory - Clean previous commands history.
>>> \t\tmaster - Clean cache of OctaDist master class.
>>> restore\t\tRestore program settings.
>>> history\t\tCommand history.
>>> 
>>> Rangsiman Ketkaew\t\t<rangsiman1993@gmail.com>\t\tOctaDist {octadist.__version__}
"""

        self.box_script.insert(tk.INSERT, help_msg + "\n")

    def script_run_list(self):
        """
        Show list of commands in scripting run.

        """
        all_command = (
            "help, list, info, doc, show, type, set, "
            "clear, clean, restore, history, exit"
        )
        self.box_script.insert(tk.INSERT, f">>> {all_command}\n")

    def script_run_info(self):
        """
        Show info of program.

        """
        self.box_script.insert(tk.INSERT, f">>> {octadist.__description__}\n")

    def script_run_doc(self):
        """
        Show document of program.

        """
        self.box_script.insert(tk.INSERT, f">>> {octadist.__doc__}\n")

    def script_run_show(self, args):
        """
        Show value of variable that user requests.

        Parameters
        ----------
        args : str
            Arbitrary argument.

        """
        if not args:
            self.box_script.insert(
                tk.INSERT, ">>> show command needs at least 1 parameter\n"
            )
            return 1

        first_arg = args[0].lower()
        if first_arg == "all" or first_arg == "*":
            for key in self.root.__dict__.keys():
                value = self.root.__dict__[key]
                self.box_script.insert(tk.INSERT, f">>> {key} = {value}\n")
            return 0

        for i in range(len(args)):
            try:
                key = args[i]
                value = self.root.__dict__[f"{key}"]
                self.box_script.insert(tk.INSERT, f">>> {key} = {value}\n")
            except KeyError:
                self.box_script.insert(
                    tk.INSERT, f'>>> variable "{args[i]}" is not defined\n'
                )

    def script_run_type(self, args):
        """
        Show data type of variable.

        Parameters
        ----------
        args : str
            Arbitrary argument.

        """
        if not args:
            self.box_script.insert(
                tk.INSERT, '>>> "type" command needs at least 1 parameter\n'
            )
            return 1

        for i in range(len(args)):
            try:
                key = args[i]
                data_type = type(self.root.__dict__[f"{key}"])
                self.box_script.insert(tk.INSERT, f">>> {key} : {data_type}\n")
            except KeyError:
                self.box_script.insert(
                    tk.INSERT, f'>>> variable "{args[i]}" is not defined\n'
                )

    def script_run_set(self, args):
        """
        Set new value to variable.

        Parameters
        ----------
        args : str
            Arbitrary argument.

        """
        if len(args) != 2:
            self.box_script.insert(tk.INSERT, ">>> No variable specified\n")
            self.box_script.insert(tk.INSERT, ">>> set command needs 2 parameters\n")
            return 1

        key = args[0]
        value = args[1]

        self.root.__dict__[f"{key}"] = value

        if f"key" not in self.root.__dict__:
            self.box_script.insert(
                tk.INSERT, f'>>> new dynamic variable "{key}" defined\n'
            )

        self.box_script.insert(tk.INSERT, f">>> {key} = {value}\n")

    def script_run_clear(self):
        """
        Clear output box.

        """
        self.box_script.delete(1.0, tk.END)

    def script_run_clean(self, args):
        """
        Clear output box and clean variable.

        """
        if not args:
            # clean scripting console
            self.script_run_clear()
        elif args[0].lower() == "history":
            self.history_command = []
        elif args[0].lower() == "master":
            # clean master windows
            self.root.clear_cache()

    def script_run_restore(self):
        """
        Restore all default settings.

        """
        self.root.cutoff_metal_ligand = self.root.backup_cutoff_metal_ligand
        self.root.cutoff_global = self.root.backup_cutoff_global
        self.root.cutoff_hydrogen = self.root.backup_cutoff_hydrogen
        self.root.text_editor = self.root.backup_text_editor
        self.root.show_title = self.root.backup_show_title
        self.root.show_axis = self.root.backup_show_axis
        self.root.show_grid = self.root.backup_show_grid

        self.box_script.insert(tk.INSERT, f">>> Restore all settings\n")

        var_settings = (
            "cutoff_metal_ligand",
            "cutoff_global",
            "cutoff_hydrogen",
            "text_editor",
            "show_title",
            "show_axis",
            "show_grid",
        )

        for key in var_settings:
            value = self.root.__dict__[f"{key}"]
            self.box_script.insert(tk.INSERT, f">>> {key} = {value}\n")

    def script_run_history(self):
        """
        Show history of command.

        """
        if not self.history_command:
            self.box_script.insert(tk.INSERT, f">>> no history\n")
        for item in self.history_command:
            self.box_script.insert(tk.INSERT, f">>> {item}\n")

    def script_no_command(self, command):
        """
        Show statement if command not found.

        Parameters
        ----------
        command : str
            Command that user submits.

        """
        self.box_script.insert(tk.INSERT, f'>>> Command "{command}" not found\n')

    def script_execute(self, event):
        """
        Execute input command scripting.

        Parameters
        ----------
        event : object
            Object for button interaction

        """
        user_command = self.entry_script.get().strip().split()
        self.entry_script.delete(0, tk.END)

        # print input command
        if user_command:
            res = " ".join([str(i) for i in user_command])
            self.box_script.insert(tk.INSERT, f"{res}\n")
            # collect command to history list
            if res.lower() != "history":
                self.history_command.append(res)

        if len(user_command) == 0:
            self.box_script.insert(tk.INSERT, ">>> no command\n")
            self.box_script.see(tk.END)
            return 1

        command = user_command[0].lower()
        args = user_command[1:]

        if command == "help":
            self.script_run_help()
        elif command == "list":
            self.script_run_list()
        elif command == "info":
            self.script_run_info()
        elif command == "doc":
            self.script_run_doc()
        elif command == "show":
            self.script_run_show(args)
        elif command == "type":
            self.script_run_type(args)
        elif command == "set":
            self.script_run_set(args)
        elif command == "clear":
            self.script_run_clear()
        elif command == "clean":
            self.script_run_clean(args)
        elif command == "restore":
            self.script_run_restore()
        elif command == "history":
            self.script_run_history()
        elif command == "exit" or command == "quit":
            self.wd.destroy()
            return 1
        else:
            self.script_no_command(command)

        self.box_script.see(tk.END)
