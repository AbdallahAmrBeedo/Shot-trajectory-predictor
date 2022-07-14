# Shot-trajectory-predictor
Brief:
  A program that detect the ball by a webcam, follow its path until it starts to fall and predict the path of the ball using polynomial fitting.

Using OpenCV library, a webcam is used to get the image, using image processing, the ball detection is done by background subtractor using KNN as it leaves just the moving object, the moving object is then identified as the ball. we get the center of the ball and track the movement of it. The centers is seperated in x and y points and then fitted with a polynomial fitting of 2nd degree. a prediction green line is printed as the fitting model is applied for the 1920 pixels. the model starts to fit win the slope ball reverse motion and falls to the ground. 

challenges faced: outlires as the ball moves sometimes it loses trace of the ball and trace its shadow or other object, so to delelte the outlire, I compare slope of the last 2 points with slope of the ones before them and if the error is beyond a certain threshold it deletes the last point considering it as it outlire.
