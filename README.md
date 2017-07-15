# README

This script is for exporting all of your likes and dislikes from Pandora.

## Context

Pandora Music is shutting down operations in Australia on July 31st 2017.
You won't be able to access your account after that date.
You can use this script to download a list of your likes and dislikes, to help migrate to another service. (e.g. CDs, torrenting, whatever)

## Usage

* Download this git repo
 * Use `git clone git@github.com:mlda065/Pandora-Export.git`; or
 * Download the zip using the button in the top right of the github page
* You'll need Python3 and the `requests` library
 * Run The makescript with `./makescript` to create a virtual environment; or
 * Run `pip install --user requests`
* Run the main script with `python pandora.py`
* The results are saved in `output.json`. View it with any text editor or browser

## Security

I'm honestly not exactly sure what's going on with encryption of passwords and such. I'm just blindly using someone else's library (mentioned below). Personally I'm not too concerned because my account will be deleted in a few days. If you are concerned, just delete your payment info from your account, and make sure your password is completely unrelated to any other password you use.

## Thanks and License

I used the python library for Pandora from the [Pithos](https://github.com/pithos/pithos) repo (with slight modification), which was written by Kevin Mehall and Christopher Eby. It is distributed under GNU GPLv3. This project is also distributed under the GNU GPLv3 license.

> This program is free software: you can redistribute it and/or modify it
> under the terms of the GNU General Public License version 3, as published
> by the Free Software Foundation.
>
> This program is distributed in the hope that it will be useful, but
> WITHOUT ANY WARRANTY; without even the implied warranties of
> MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
> PURPOSE.  See the GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License along
> with this program.  If not, see <http://www.gnu.org/licenses/>.
