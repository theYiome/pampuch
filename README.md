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
	
- Machine Learning
    - tensorFlow 
    - Keras 
    - numpy 
    - skimage

## Machine Learning
- Dataset:
    - [keras.datasets](https://keras.io/datasets/) To begin we will be using datasets provided with Keras Library cause 
    of their easy of use for people like us not knowledgeable in the ML field
        -  CIFAR10 - initially fulfills all of our requirements.
        -  CIFAR100 - is bigger version of CIFAR10
    - If there will be such requirement we would experiment with much bigger datasets. 
- Method
    - CNN - Convolutional Neural Network
        - We will start with CNN cause the internet says that it's good with image recognition and classification. 
        Two areas that we interested in. 
    - If time will allow we would like to experiment with other neural networks.
    

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
- Backend that is able to get a request and send any response
- Basic frontend-backend communication (file transfer in json requests)

### Sprint 02 - End 2020.05.07
- Endpoint for retriving all available labels in database
- Endpoint for retriving images with choosen label from database
- Working Catalog site on frontend
- Datasate is prepared

### Sprint 03 - End 2020.05.14
- Working Categorization site on frontend
- Backend is able to save labeled image to dataset
- Determining correct format of our images
- Basing work on ML model creation

### Sprint 04 - End 2020.05.21
- Working Recognition site on frontend
- ML model is discussed by the team (knowleage sharing)
- Backend endpoint for recognition mocked

### Sprint 05 - End 2020.05.28
- Fully functional frontend
- Basic model working
- Backend sending request to ML part

### Sprint 06 - End 2020.06.04
- Frontend polishing after team discussion
- Whole system integration discussed (knowleage sharing)
- Functional ML model
- Dockerization

### Sprint 07 - End 2020.06.11
- Fully working app
- All functionalities tested manualy
- Hosting out app online
