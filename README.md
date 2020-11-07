# Gogoanime Downloader

It's a very orginal name, I know. All this Python script does is download anime from given Gogoanime urls.


## Context

I follow seasonal anime and I rarely watch anime online so I needed a way to download anime without going through a ton of links and pop up ads.


## This is where this script comes in...

For the reason stated above, I created a script, `main.py` containing all the code, to help me do all the hard work.


## How it works (for the nerds)

It uses a module called `selenium` and Firefox's `geckodriver` in order to load the Gogoanime page in a simulated Firefox web browser and find the appropriate download link by scraping the page.


## Long term plans

Since I don't really have much other need for this, you can say it's pretty much "complete." However, as this is open-sourced, I want people to use this script to ease their life too and as such, the features that have yet to be added are listed in the [issues pages](https://github.com/Spimy/gogoanime-downloader/issues). Feel free to fork this repo and contribute.


## Setup

### Prerequisites

You should have the following installed:
1. [Python 3.8.x or above](https://www.python.org/downloads)
2. [Firefox's geckodriver](https://github.com/mozilla/geckodriver/releases)


### Installation

1. Head on over to the [release page](https://github.com/Spimy/gogoanime-downloader/releases) and download the latest version.
2. Extract the folder and open it.
3. Run `pip install -r requirements.txt` in a console opened in the folder.
4. Provide the urls for the script as explained in the [next section](#providing-urls-for-the-script)
5. Run the `main.py` script.


### Providing urls for the script

Create a file called `urls.txt` and add the urls of the anime you want to download separated by a new line in the file. An example can be found in the [`urls.txt.example`](/urls.txt.example) file.