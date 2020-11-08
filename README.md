# Image Detection Analysis
UMGC CMSC 495 Current Trends Capstone Project comparing and researching Computer Vision algorithms for image detection.


## Image Results
The following table will depict the status of each test sheet, its success level, and notes for any hand ups or issues.

| Sheet Name | Waldo Found (Y/N) | Notes |
| :--- | :---: | :--- |
| Buffet | N | |
| City | N |
| Store | N | |
| Siege | N | |

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
