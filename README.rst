########
JSON Cat
########

|Version Status|

Concatenate JSON file(s) or standard input to standard output.


Installation
============
pip install json-cat


Usage
=====

.. code-block:: bash

    Usage: jsoncat [OPTIONS] [JSONFILES]...

    Concatenate JSON FILE(s), or standard input, format standard output.

    Options:
      -c, --compact  Compact JSON.
      --version      Show the version and exit.
      --help         Show this message and exit.

Overview
========

JSON can be output as pretty JSON (nicely indented
with sorted keys) for readability, or as compacted JSON for efficient
machine use.


JSON File Patterns
==================

+---------+-------------------+--------------------------------+
| Stdin   | File Name(s)      | Defined Behavior               |
+=========+===================+================================+
| No Data | No Filename       | Print command usage message    |
+---------+-------------------+--------------------------------+
| Data    | No Filename       | Read JSON data from STDIN      |
+---------+-------------------+--------------------------------+
| Data    | Dash char. (-)    | Read JSON data from STDIN      |
+---------+-------------------+--------------------------------+
| No Data | Dash char. (-)    | Accept user input until EOF    |
+---------+-------------------+--------------------------------+
| N/A     | Filename          | Read JSON data from file       |
+---------+-------------------+--------------------------------+
| N/A     | File1, File2, ... | Concatenate JSON data in array |
+---------+-------------------+--------------------------------+

Compact Settings
================

+---------+---------------------------------------------------------+
| Compact | Description                                             |
+=========+=========================================================+
| True    | No newlines, no indent and no spaces after punctuation. |
+---------+---------------------------------------------------------+
| False   | Indent-level 2 w/ sorted keys                           |
+---------+---------------------------------------------------------+

Features
========

1. **JSON Decoder**:  Read JSON data from standard input and/or one or more
   paths/filenames.

2. **JSON Concatenation**:  If multiple JSON files/input-streams are
   provided then concatenate the JSON data into a JSON array in the sequence
   the files were specified. 

3. **JSON Formatting**:  JSON can be output as pretty JSON (nicely indented
   with sorted keys) for readability, or as compacted JSON for efficient
   machine use.

4. **Keyboard Interrupt Handling**:  When writing data to standard output or
   standard error if a SIGINT ("program interrupt") signal is sent the
   KeyboardInterrupError message and stack trace will be suppressed; this
   makes a nice clean break when the user types the INTR character;
   normally Ctrl-c.

5. **Command-line Interface Tool**: For interactive usage.

6. **Reusable JSON I/O Functions**: Off-loads I/O handling allowing the
   individual JSON command-line programs to focus on their core functions.  


*JSON Cat was originally designed for use with the JSON Translations project,
but it was split out as a separate Python micro-package since it may be
useful with other applications that read and/or write JSON.  The
command-line interface is also a handy tool for testing & proto-typing.*


Python Developer API
====================

Standard Output Writer w/ KeyboardInterrupt Wrapper
---------------------------------------------------

.. code:: python

  output_text(text, color=None, err=False)

  output_lines(text, color=None, err=Fase)

JSON Helper Functions
---------------------
.. code:: python

  json_load_file(filename)

  json_dump(data, compact=False)


.. |Version Status| image:: https://badge.fury.io/py/json-cat.svg
    :target: https://badge.fury.io/py/json-cat
