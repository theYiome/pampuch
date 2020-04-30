# Project Pampuch

## Participants
-  **Kamil Pasterczyk**
- Dawid Łączek
- Jakub Salamon
### Do you need more people: No

## Short description of the idea

Web app for image cataloging, categorization and recognicion using Machine Learning. One of its features is option of manual segmentation, which means you choose yourself what part of the picture you want to label for our self-learning model. We might implement automatic segmentation as well, and this means that picture segments itself and you rearrange boxes and then label them. In this repository under /doc/ directory you can find mockup of the front-end part as interactive PDF file or preffered .bmpr (Balsamiq Wireframes 4 file).

# Front-end part of application is now on Github Pages!

You can take a look at the current state of out front-end:
https://theyiome.github.io/pampuch/static/menu.html

# Project description

## Tech Stack

Stuff we are going to use:
- Frontend:
	- HTML5
	- CSS3
	- JS (with jQuery)
- Backend:
	- Python3.8
	- Flask (python micro framework for web applications)
	- sqlite3 (light database for web application and out dataset)
	- NumPy (computing liblary)

## Functionalities

Stuff that our app should be able to do:
- Basic
	- Accessible from any modern browser
	- Intuitive for new users
	- Accessible online (maybe www.pythonanywhere.com)
- Categorization
	- User can upload new image to a browser for dataset building
	- Multiple things can be labeled on single image by marking them using squares
	- After labeling can either discard their work or send it to database
	- Saved image will likely not be the same as send one (different resolution, color compression)
- Recognition
	- When we will have decent dataset model will be trained
	- User can upload new image to a browser for recognition
	- After upload user can pick which part of an image should be recognized
	- User can either discard and select another part of an image or accept selection
	- After accepting selection will be sent and server should return most probable known label
- Cataloging
	- User should be able to see current dateset in their browser
	- User can pick any image in dataset for a closer look
	- User can delete picked image from dataset, it will not be used for future model training

## Roadmap

### Sprint 01 - End 2020.04.30 - DONE
- Basic HTML5 and CSS UI template
- Definition of some basic endpoints
- Basic frontend-backend communication (file transfer in json requests)

### Sprint 02 - End 2020.05.07
- TODO

### Sprint 03 - End 2020.05.14
- TODO

### Sprint 04 - End 2020.05.21
- TODO

### Sprint 05 - End 2020.05.28
- TODO

### Sprint 06 - End 2020.06.04
- TODO

### Sprint 07 - End 2020.06.11
- TODO