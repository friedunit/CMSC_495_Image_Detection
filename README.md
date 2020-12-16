# Image Detection Analysis
UMGC CMSC 495 Current Trends Capstone Project comparing and researching Computer Vision algorithms for image detection.

## Overall Design
The purpose of this project is to use computer vision techniques to search for a user selected target image within a user selected large puzzle image. If detected, the target image is bound by a green colored box. The application will be written in the Python programming language and use the open-source computer vision library OpenCV for reading and searching images.  As stated in the Project Plan and Test Plan/User Guide, the application will be opened as a desktop icon, launching the “Where’s Waldo” Graphical User Interface (GUI).  The GUI itself will be intuitive, with two dropdown menus to select: A) a Scene and B) a Character. The user will then have two buttons to choose from. The “Preview” button will display the selected scene and character for view and the “Search” button will perform the image searching and detection to display the results to the user.

## Performance estimates
We estimate that searches will be successfully completed in less than 10 seconds, provided that the user has minimum requirements stated in the original Plan. Changing the scaling numbers has a large effect on accuracy and run-time. Ideally, the template matching takes less than 5 seconds and has an 80% or higher accuracy rate.

## Testing Phases
Testing will occur in three phases.

1. Simple Shape and Color Finder
2. Small Scale Where's Waldo
3. Full Scale Where's Waldo

This will be done inorder to fully understand how edge matching and feature matching function.

*Edge Matching* is taking a gray scale image and getting a rough idea of how the edges in the image behave. In the instance of a 
square, we would expect to see 4 consecutive 90 degree angles. This can also be done for objects such as Waldo. Waldo has a distinct
format in how his face and body (if the posture is the same) is shaped.

*Feature Matching* is looking at the color values of objects. Color values can be broken down into several different value indexes. In 
the instance of RGB, each color can be broken down with a value from 0-255 for Red Green and Blue. This can aid in finding the apporpriate 
image in a scene. In the instance of Waldo, he wears an iconic red and white striped shirt. The program would then be tasked with finding
objects in the scene that match this color schema. 

### Phase 1 - Simple Shape and Color Finder
This testing phases will consist of a GUI that is pre-loaded with a scene image of 3 unique shapes with 3 unique colors. The user will
then have the option to select from a drop down what they would like to search for. The program will then find the object in the scene 
image that the user has specified.

### Phase 2 - Small Scale Where's Waldo
The small scale Where's Waldo testing phases will start with a pre-loaded scene and will run a process to find Waldo in that scene. This
porcess will start with just Waldo and 2-5 other distinct objects. As the team hones the program on how to find Waldo, the lens will be
taken back to allow more distinct objects into the scene. This will allow the team to adjust for changes are trickery that is common
in many Where's Waldo scenes.

### Phase 3 - Full Scale Where's Waldo
The full scale test will encompass all the lessons learned form the previous two phases. In this testing phases the program will have a GUI
with 2 drop down boxes. One for the scene and another for the character they would like to find. Waldo has 4 friends that appear with him in
all of his scenes, Odlaw, Wenda, Wizard, and Woof. The user can select from any of these people and the program will attempt to find that 
person in whichever scene the user decides. The scenes varry in difficulty with the easiest being a simple city square, and the hardest 
being a siege on a castle. These scenes become harder to search because of how much noise and detail is in the images. 

### Final – Full Scale Where’s Waldo & Friends GUI

For the final program, we decided to increase accuracy by removing Woof from the available characters to search for. Woof’s tail was never able to be found in the puzzle images with the template matching search we were conducting. Further research would need to be done to find something as small and hidden as his tail. We also removed the Department Store puzzle which was giving an error when searching for Wizard Whitebeard. 

Building on Phase III, the GUI remains largely unchanged but now includes options to search for Waldo, Odlaw, Wenda, and Wizard Whitebeard in six different puzzles. We also removed the tutorial option, so the application opens directly to the Waldo search GUI. Changing the argument numbers in the scaling algorithm changed the results drastically and we found the best run-time/accuracy ration was scaling 2.0 to 0.5 with 10 scales to loop through. The accuracy is 87.5% with finding 21 of 24 characters successfully. The three that were not correct found Odlaw instead of Waldo. To increase accuracy, further research and techniques would need to be used to differentiate between Waldo and Odlaw as they look very similar but with different colors. The table below shows the results of searching the six different puzzles.

| 0.5, 2.0, 10	| Waldo | Wenda | Wizard	| Odlaw |
| :--- | :---: | :--- | :---: | :--- |
| City	| Found |	Found |	Found |	Found |
| Beach	| Odlaw	| Found	| Found	| Found |
| Zoo	| Found	| Found	| Found	| Found |
| Ski Resort | Odlaw | Found | Found | Found |
| Train Station	| Odlaw	| Found	| Found	| Found |
| Museum	| Found	| Found	| Found	| Found |



## Design Strengths
Using Python and OpenCV proved to be a design strength in that we could use both cross-platform. Two of our group members used MacOS, while the other two used Windows, so having a cross-platform solution was critical. In addition, using edge detection with Gaussian-adaptive thresholding proved to be an efficient way of identifying our target images within the puzzle images. This method does not overload processing power and meets our threshold of finding the image within a 10 second window.

## Limitations
Limitations included our 8-week time restraint, processing power, and use of open source/free software. The 8-week time restraint limited our ability to find a feature matching solution to identify Waldo, forcing us into various methods of edge detection. Processing power was also a restraint that affected feature matching capabilities as explained in the next section in our suggestions for future improvement. Finally, the use of open source/free software to complete our project placed limitations on the methods that were available to us. It was important to use open-source solutions so that anyone in the class (and the professor) could run our program without having to purchase something. Image detection can get quite complicated and many commercial solutions 	exist to overcome the challenges we documented. In the end, we went with Python and OpenCV which proved to be pretty good in accomplishing our goals.

## Suggestions for Future Improvement
Suggestions for future improvement include continued research into feature matching capabilities to better distinguish between Waldo and Odlaw. Feature matching involves intensive AI training to teach the program/computer the subtle differences between images. This takes extensive processing power and thousands of example images to obtain our desired accuracy. Unfortunately, given an 8-week time period to 	complete this project, we simply did not have the time or resources to implement feature matching in its purest form. Exploring featuring matching more would undoubtedly be our next step towards future improvement and increased accuracy.

## Screen shots:

### Initial Application page

![Screenshot1](https://raw.githubusercontent.com/friedunit/CMSC_495_Image_Detection/main/Screenshots/Screen%20Shot%202020-12-16%20at%204.20.36%20PM.png)

### Searching for Waldo in the City

![Screenshot2](https://raw.githubusercontent.com/friedunit/CMSC_495_Image_Detection/main/Screenshots/Screen%20Shot%202020-12-16%20at%204.21.00%20PM.png)

### Searching for Wizard Whitebeard in the Zoo

![Screenshot3](https://raw.githubusercontent.com/friedunit/CMSC_495_Image_Detection/main/Screenshots/Screen%20Shot%202020-12-16%20at%204.24.20%20PM.png)

### Searching for Wenda in the Train Station

![Screenshot4](https://raw.githubusercontent.com/friedunit/CMSC_495_Image_Detection/main/Screenshots/Screen%20Shot%202020-12-16%20at%204.24.47%20PM.png)


