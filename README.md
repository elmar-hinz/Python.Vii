# Python.Vii
Python based Vim clone

* Author: Elmar Hinz
* License: MIT

# Goal

A fully compatible clone of Vim written in Python, that is configurable and
extensible both in VimScript and in Python.

# Roadmap

1. Getting usable
2. Getting compatible
3. Enter the future

# Reasoning

Vim is a great editor, but VimScript is difficult. This lowers the acceptance
of Vim and slows down it's evolution.

By migrating Vim to a beatiful and widely used programming language, I try
to bring the editor to a new starting position. I hope to get two communities
into the boat, convinced Vim users as well as a lot of Python developers.
The PEP processess may serve as a role model how the future evolution can be
organized.

There are other projects with the goal to write a better editor than Vim. I
think an editor should first catch up with Vim before it can outrun. Without
full Vim compatibility the habitual users will not join the company.

# Component model

May be a little out of sync with actual development.

* Config
* Logger
* App
    * Model
        * CommandLine
        * BufferList
            * Buffer
                * Cursor
                * Line
                * Line
            * Buffer
                * Cursor
                * Line
                * Line
    * View
        * CommandLineWindow
        * WindowList
            * Window
                * Sheet
            * Window
                * Sheet
    * Controller
        * NormalMode
        * InsertMode
        * VisualMode
        * OperatorPendingMode
        * CommandLineMode
        * CommandHistory

The criterium of this model is, in which class other classes are instantiated.
There are a lot more of relations not shown in this overview.
The directory structure isn't that deep.


