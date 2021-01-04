Installation
============

The following installation methods are provided:

* a self-contained executable generated using PyInstaller_


Installation as the Self-Contained Executable
---------------------------------------------

Installation of the self-contained executable allows you to install
tcmReceiver on systems even if they do not provide python themselfes.
However, the usage of tcmReceiver is limited to the command line tool
itself, so the integration in other scripts won't be possible::

    $ wget https://github.com/seeraven/tcmReceiver/releases/download/v1.0.0/tcmReceiver_Ubuntu18.04_amd64
    $ mv tcmReceiver_Ubuntu18.04_amd64 /usr/local/bin/tcmReceiver
    $ chmod +x /usr/local/bin/tcmReceiver


.. _PyInstaller: http://www.pyinstaller.org/
