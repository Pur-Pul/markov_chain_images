## Links:    
[Project specification](Documentation/project_specification.md)  
[Implementation document](Documentation/implementation_document)  
[Testing document](Documentation/testing_document.md)  
[Week report 1](Documentation/week_1_report.md)  
[Week report 2](Documentation/week_2_report.md)  
[Week report 3](Documentation/week_3_report.md)  
[Week report 4](Documentation/week_4_report.md)  
[Week report 5](Documentation/week_5_report.md)  

## Instructions
This application was made using python 3.8
Install by running the following command in the root folder:
```bash
poetry install
```

The program will begin by asking the number of input images. This can be any number, but the more images the slower the process.  

After that images that are found in src/input will be listed in the terminal. These can be used by the program, and more images can be added to said folder. 

Next you need to enter the file name of the image to use. If multiple images are to be used, the program will ask over and over. Make sure you spell the filename as it is displayed in the terminal, with filetype included.

Next you need to give width and hight in pixels for the image to be generated. 

Lastly you get to choose between 4 or 8 neighbour mode. This affects how many neighbouring pixels the program takes into account when generating the image. 8 neighbours is more detailed but takes longer.

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
