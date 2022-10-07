Testing is performed using Unittest and Coverage is used to calculate the testing coverage. The current tests are:

### test_proddibilities_are_calculated_properly
This checks whether the markov chain is generated correctly with proper possibility values.

### test_neighbours_collected
This checks the whether the return value of the function get_neighbours is correct and shuffled. This function is important to function correctly. If it returns the wrong neighbours, the image will not be generated properly. If the neighbours aren't shuffled, the image will look unnatural, because the traversal will allways prioritize the same direction.

### test_color_selected_properly
This check whether the randomly selected color is part of the markov chain and has a probability larger than 0. If the probability is 0, it would mean the colors are not properly selected, as they should be randomized by weights.

[Coverage report](/htmlcov/index.html)
If the coverage report does not exist, generate it using:  
```bash
poetry run invoke coverage-report
```