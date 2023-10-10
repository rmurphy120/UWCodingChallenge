# UWCodingChallenge
Take an input file and draw a line of best fit on each line of cones

Uses Python and OpenCV. The basic methodology is that the code finds contours which are orange, and then plots a line of best fit through those contours. It excludes outliers (Which insures that even if there are other orange objects in the image, the line will follow the cones).

I tried multiple different avenues before I arrived at my answer. First, I tried to find triangle contours. I was never able to get this to work I think because I wasn't processing the image as well as I should of before I tried to find the contours. My second attempt was to find all contours in the image, and then filter through the ones which had the most dominant color as orange. I got this to work with questionable results (Only able to recognise 5 of the cones). Finally, I tried a much more elegant version of the prior attempt, where I used the inRange method to create a threshold of only the color orange. From there, I created contours and drew an image through them. To exclude orange contours that were not cones, I tested which datapoints would have statistically signifigant change in the slope of the line.

Output Image:

![alt text](https://github.com/rmurphy120/UWCodingChallenge/blob/main/answer.png?raw=true)
