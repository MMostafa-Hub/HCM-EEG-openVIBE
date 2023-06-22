# Visual Studio Code OpenViBE Setup

1. Open Visual Studio Code.
2. Open the settings.json file by clicking on the gear icon in the bottom left corner of the window and selecting "Settings" from the dropdown menu.
3. In the search bar at the top of the "Settings" window, type python.autoComplete.extraPaths and press enter.
4. Click on the "Edit in settings.json" link to open the settings.json file.
5. In the settings.json file, locate the "python.autoComplete.extraPaths" setting.
6. Add the include path "C:\\\Program Files\\\openvibe-3.5.0-64bit\\\share\\\openvibe\\\plugins\\\python3" to the list of paths.
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
