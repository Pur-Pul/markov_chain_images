This week I have improved the algorithm a bit. Now directions are taken into account when the markov chain is generated. This means that for each direction there is a different probability value for the next color. This results in the colors being generated more often in the same orientation relative to eachother as the source picture. I also increased the neighbours that are considered from 4 to the surrounding 8. This can be toggled between 4 or 8, when generating the image.  

I also streamlined the user interface, so that the input images are more easily selected and the output image size can be selected by the user. I changed the tests to be repeatable, as before they tested random input values and now have fixed inputs.   

This week I happened to learn the importance of tests directly. When I was improving the tests, one of them identified that my recently improved algorithm was constructing the markov chain incorrectly. If not for the test I probably wouldn't have found the fault, as the program still ran fine, but gave a noticably different output.  

Next week I will make more tests, document the code and clean up the code and streamline the user-interface further.  

Hours used this week: 4