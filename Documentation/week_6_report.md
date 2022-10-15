This week I have streamlined the UI. Using regular expression I have made the input error free to some degree. Although a memory error can still occour if the color complexity is too large.  
I have also made it possible to change the color compression value. This affects the color complexity, more compression means smaller complexity and less detail.  

The biggest change however is the implementation of trie datastructure. This is an option the user can select when running the program. It was not part of the pseudocode I based the program on, however it does work flawlessly in my program and drastically improves both the space and time complexity of the program. Now only the probability values that are larger than 0 will be allocated space in the markov chain, which makes it much faster to select the next color. Using the trie data structure, HD quality images can be generated and the colors will not have to be compressed to avoid out of memory error.

For the final submission I will need to improve my overall documentation and make new tests to account for the trie data structure.

Hours used this week: 3