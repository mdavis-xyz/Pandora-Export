
Linux, MacOS X:

- Clone the repo, as per `README.md`, and run any of `export.py`
  (command-line interface), `export_gui.py` (GUI interface), or
  `export_web.py <someport>` (runs a simple web server on port
  "`someport`").

Windows:

It is possible to build self-contained binaries for Windows,
even without access to a Windows machine, using <https://www.appveyor.com/>,
a free CI (continuous integration) service.



- Fork this repo.
- Go to [appveyor.com](http://appveyor.com), and use the "sign in with GitHub"
  feature to sign in.
- Click "`+NEW PROJECT`"; you should be given a list of your GitHub projects
  - select the forked `Pandora-Export`.
- 'Enter' the new `Pandora-Export` build by clicking on "`Pandora-Export`".
- Click `NEW BUILD` to start a build.
- At the end of the process, if all goes well, there should be a
  link titled "`ARTIFACTS`"; click on that, and a download of `export_gui.exe`
  should be available.

The "build script" for Appveyor is in `appveyor.yml`, and can be tweaked
if you desire.

