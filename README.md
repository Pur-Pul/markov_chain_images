## Links:    
[Project specification](Documentation/project_specification.md)  
[Week report 1](Documentation/week_1_report.md)  

## Instructions
This application was made using python 3.8

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