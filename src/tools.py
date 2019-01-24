"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import linear


def show_strct_param(al, cl):
    """Show structural parameters of selected complex

    :param al, cl:
    :return:
    """
    full_atom_list = al
    full_coord_list = cl

    struct = tk.Tk()
    struct.option_add("*Font", "Arial 10")
    struct.geometry("380x530")
    struct.title("Results")

    lbl = tk.Label(struct, text="Structural parameters")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    Box = tkscrolled.ScrolledText(struct, wrap="word", width="50", height="30", undo="True")
    Box.grid(row=1, pady="5", padx="5")

    texts = "Bond distance (Å)"
    Box.insert(tk.INSERT, texts)

    for i in range(len(full_coord_list)):
        for j in range(i+1, len(full_coord_list)):
            if i == 0:
                distance = linear.distance_between(full_coord_list[i], full_coord_list[j])
                texts = "{0}-{1}{2} {3:10.6f}".format(full_atom_list[i], full_atom_list[j], j, distance)
            else:
                distance = linear.distance_between(full_coord_list[i], full_coord_list[j])
                texts = "{0}{1}-{2}{3} {4:10.6f}".format(full_atom_list[i], i, full_atom_list[j], j, distance)
            Box.insert(tk.END, "\n" + texts)

    texts = "Bond angle (°)"
    Box.insert(tk.END, "\n\n" + texts)

    for i in range(len(full_coord_list)):
        for j in range(i+1, len(full_coord_list)):
            for k in range(j+1, len(full_coord_list)):
                if i == 0:
                    angle = linear.angle_between(full_coord_list[j], full_coord_list[i], full_coord_list[k])
                    texts = "{0}{1}-{2}-{3}{4} {5:10.6f}"\
                        .format(full_atom_list[k], k, full_atom_list[i], full_atom_list[j], j, angle)
                else:
                    angle = linear.angle_between(full_coord_list[j], full_coord_list[i], full_coord_list[k])
                    texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}" \
                        .format(full_atom_list[k], k, full_atom_list[i], i, full_atom_list[j], j, angle)
                Box.insert(tk.END, "\n" + texts)
    Box.insert(tk.END, "\n")

    struct.mainloop()

