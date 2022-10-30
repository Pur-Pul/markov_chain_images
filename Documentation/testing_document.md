Testing is performed using Unittest and Coverage is used to calculate the testing coverage. The current tests are:
## Markov chain tests

### test_proddibilities_are_calculated_properly
This checks whether the markov chain is generated correctly with proper possibility values.

### test_neighbours_collected
This checks the whether the return value of the function get_neighbours is correct and shuffled. This function is important to function correctly. If it returns the wrong neighbours, the image will not be generated properly. If the neighbours aren't shuffled, the image will look unnatural, because the traversal will allways prioritize the same direction.

### test_color_selected_properly
This checks whether the randomly selected color is part of the markov chain and has a probability larger than 0. If the probability is 0, it would mean the colors are not properly selected, as they should be randomized by weights.

### test_generated_image_is_correct_size
This checks whether the generated image is the correct size and orientation.

## TrieNode tests

### test_color_is_correct
This checks whether the node has stored the correct color value.

### test_nodes_are_added_correctly
This checks whether the add_node function adds the nodes correctly to the next list. This is important because the next list is used to generate the probabilities for the colors.

### test_color_frequency_list_is_constructed_correctly
The color frequency list contains the frequency for each color in specific directions from other colors. This is used as probabilities when choosing the next color. This test checks whether the said list is generated properly.

## Trie tests

### test_node_dict_is_constructed_properly
The node dict keeps track of the individual nodes and is used to get the node object based on color values. This test checks if the dict has been generated correctly.

### test_color_frequency_list_returns_correct_value
Checks if the color_frequency_list function returns the correct value.

A simple performance test is implemented in the form of a timer when the markov chain is trained and the image generated during normal usage.

[Coverage report](/htmlcov/index.html)
If the coverage report does not exist, generate it using:  
```bash
poetry run invoke coverage-report
```