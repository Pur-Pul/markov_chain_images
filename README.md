## Links:    
[Project specification](Documentation/project_specification.md)  
[Implementation document](Documentation/implementation_document.md)  
[Testing document](Documentation/testing_document.md)  
[Week report 1](Documentation/week_1_report.md)  
[Week report 2](Documentation/week_2_report.md)  
[Week report 3](Documentation/week_3_report.md)  
[Week report 4](Documentation/week_4_report.md)  
[Week report 5](Documentation/week_5_report.md)  

## Instructions
This application was made using python 3.8

## Installation using Docker
Build the docker image using the following command:
```bash
docker build . -t markov_chain
```

And run the application using the following command:
```bash
docker run --rm -it -p 8080:8080 markov_chain
```
The application can then be closed with CTRL + C

## Native installation
Install by running the following command in the root folder:
```bash
poetry install
```
To start the command line interface run:
```bash
poetry run invoke start
```
or start the web application by running: 
```bash
poetry run invoke start --web
```
in the root folder. Make sure you are using the correct python version.

The program will begin by asking the number of neighbours to consider (either 4 or 8). 4 is faster but less detailed.

Next it asks whether to use the Trie datastructure or not. The trie is faster in everyway, so there isn't really any reason to not use it other than seeing the difference in speed.

It will list the pictures it found in the src/input folder and ask how many you wish to use as input. If you wish to use some other pictur place it in the input folder and restart the program.

Next you need to enter the file name of the image to use. If multiple images are to be used, the program will ask over and over. Make sure you spell the filename as it is displayed in the terminal, with filetype included.

Next it asks for a color compression value. This value compresses the colors to decreses the space complexity. This might be needed when not using the trie, but if you are it should not be needed. Smaller value equals less compression. 1 is the smallest.

Lastly you need to give width and height in pixels for the image to be generated. Larger images take longer, but if you use the trie data structure it should be able to handle HD images in an acceptable timeframe.


### Testing  
Run tests with:  
```bash
poetry run invoke test
```

The following commmand will generate a coverage report to the _htmlcov_ directory.  
```bash
poetry run invoke coverage-report
```

Run pylint with:
```bash
poetry run invoke lint
```
