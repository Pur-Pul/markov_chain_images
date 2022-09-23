Testing is performed using Unittest and Coverage is used to calculate the testing coverage. The current tests are:

### test_proddibilities_are_calculated_properly
This checks whether the markov chain is generated correctly with proper possibility values.

### test_neighbours_collected
This checks the whether return value of the function get_neighbours is correct and shuffled. This function is important to function correctly. If it returns the wrong neighbours, the image will not be generated properly. If the neighbours aren't shuffled, the image will look unnatural, because the traversal will allways prioritize the same direction.

[Coverage report](/htmlcov/index.html)
If the coverage report does not exist, generate it using:  
```bash
poetry run invoke coverage-report
```