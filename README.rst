====================================
A small console events investigation
====================================

How do Windows console events work under Python? Check it yourself using:

.. code:: bash

    python main.py <creation flags> <signal number> [--mode=send]

For example:

.. code:: bash

    python main.py CREATE_NEW_PROCESS_GROUP CTRL_BREAK_EVENT

Available `creation flags`_ and `console events`_ are listed on MSDN.
Mode can be one of: ``send`` for `Popen.send_signal`_, ``kill`` for
`os.kill`_, or ``gcce`` for `kernel32.GenerateConsoleCtrlEvent`_.

.. _`creation flags`: https://msdn.microsoft.com/en-us/library/windows/desktop/ms684863(v=vs.85).aspx
.. _`console events`: https://msdn.microsoft.com/en-us/library/windows/desktop/ms683242(v=vs.85).aspx
.. _`Popen.send_signal`: https://docs.python.org/3/library/subprocess.html#subprocess.Popen.send_signal
.. _`os.kill`: https://docs.python.org/3/library/os.html?highlight=os.kill#os.kill
.. _`kernel32.GenerateConsoleCtrlEvent`: GenerateConsoleCtrlEvent_

What happens
============

A tree of processes is created:

.. code::

    Main <-- Sub <-- Subsub

``Sub`` is created with the given creation flags and registers no-op
handlers for all available signals. The most interesting flag is 512 or
``CREATE_NEW_PROCESS_GROUP``. ``Main`` generates the given console event
after a few seconds (targeting just ``Sub``).
All three processes loop printing "alive" for 90 seconds.

Some results
============

Windows 10 with Python 3.5.2:

* ``CTRL_C_EVENT``: Without the new group flag raises `KeyboardInterrupt` for
  all processes in the group (after about 30 seconds). With the flag does not
  terminate anything. Without the flag only, ``SIGINT`` handlers can be used
  to modify the behavior.
* ``CTRL_BREAK_EVENT``: Without the flag terminates the main process together
  with its console, with a delay. With the flag terminates the targeted group.
  Possibly with the flag only, `SIGBREAK` handlers can prevent termination.
* ``CTRL_CLOSE_EVENT``, ``CTRL_LOGOFF_EVENT``, and ``CTRL_SHUTDOWN_EVENT``:
  These only terminate the target, not its descendants, with or without the
  flag. No handlers are called in any case.

The close, logoff, and shutdown events are converted_ by Python to
TerminateProcess_, likely due to GenerateConsoleCtrlEvent_ not supporting
these events (calling the function with any of them actually fails with
``ERROR_INVALID_PARAMETER``).

.. _converted: https://github.com/python/cpython/blob/3.6/Modules/posixmodule.c#L6367
.. _TerminateProcess: https://msdn.microsoft.com/en-us/library/windows/desktop/ms686714(v=vs.85).aspx
.. _GenerateConsoleCtrlEvent: https://msdn.microsoft.com/en-us/library/windows/desktop/ms683155(v=vs.85).aspx
