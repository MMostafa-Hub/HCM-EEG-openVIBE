# Setup OpenVIBE for Python3 development

## Install Python for OpenViBE 3.0.0

* [Python 3.7.8 64bits](https://www.python.org/ftp/python/3.7.8/python-3.7.8-amd64-webinstall.exe) for 64bit OpenViBE on Windows 10
* [Python 3.7.8 32bits](https://www.python.org/ftp/python/3.7.8/python-3.7.8-webinstall.exe) for 32bit OpenViBE on Windows 10

## Python Scripting box not listed in Designer ?

1. Just search "Edit the system environment variables" in the Windows search bar.
2. Environment Variables -> System Variables -> Path -> Edit -> New -> Add the path to the Python folder in your system.
3. If you have more than one Python version installed, make sure to make the path to python3.7 at the top of the list.
4. Then save the changes and restart OpenViBE Designer.

## Visual Studio Code OpenVIBE with python Setup

1. Open Visual Studio Code.
2. Open the settings.json file by clicking on the gear icon in the bottom left corner of the window and selecting "Settings" from the dropdown menu.
3. In the search bar at the top of the "Settings" window, type python.autoComplete.extraPaths and press enter.
4. Click on the "Edit in settings.json" link to open the "settings.json" file.
5. In the settings.json file, locate the `python.autoComplete.extraPaths` setting.
6. Add the include path `C:\\\Program Files\\\openvibe-3.5.0-64bit\\\share\\\openvibe\\\plugins\\\python3` to the list of paths.
7. Save the settings.json file by pressing Ctrl+S or selecting "Save" from the "File" menu.
8. Close the settings.json file and the "Settings" window.

Here's what the updated settings.json file should look like:

```json
{
    "python.autoComplete.extraPaths": [
        "C:\\Program Files\\openvibe-3.5.0-64bit\\share\\openvibe\\plugins\\python3"
    ]
}
```
