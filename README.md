# Hand-Cursor-Controller

**Version 1.0.0**

This program allows you to control your cursor with you hand, with different types of gestures:<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;`Fist(Finger 0)`&nbsp;&nbsp;: To LeftClick at a specific position<br>
&nbsp;&nbsp;&nbsp;&nbsp;`1 Finger`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: To control the postition of the cursor<br>
&nbsp;&nbsp;&nbsp;&nbsp;`2 Fingers`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: You can assign it to your need<br>
&nbsp;&nbsp;&nbsp;&nbsp;`3 Fingers`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: To Scroll Down <br>
&nbsp;&nbsp;&nbsp;&nbsp;`4 Fingers`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: To Scroll Up<br>
&nbsp;&nbsp;&nbsp;&nbsp;`5 Fingers`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: To Start or Stop the Program<br>

The background needs to be clear and blank to detect the hand correctly. To make sure of that enable set the Debug variable to True.

This program is just an idea of what the future technology will bring with it. It is still a concept with lot of conditions needed to work properly. Its accuracy and movement is not the greatest but it will provide you enough satisfaction to experience what the future will bring with it.

## How it works?

The program first tries to detect a hand by converting the video image to black and white and then subtracts the stable background for better detection of hand. 
Then to detect the number of fingers, different functions like convex hull and countours that gives us the number of valleys that will be formed in the hand image, that is the gaps between the fingers. For finger 1 and fist the area and arearatio covered by the hand tells us which is what.
After that for movement of the mouse the brightest pixel in the image screen is taken as the reference coordinate and then the cursor is moved to that position using the `PyAutoGUI` Automation library.

## Some Tips

1. Keep the background clear when the mask image is created, because the cursor is mapped and moved to the top brightest pixel in the mask.
2. To start and stop the program show the five fingers.
3. To terminate the program press `Ctrl+C` in the console.
