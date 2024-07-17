# eeg_databaseGame

https://github.com/user-attachments/assets/3c3f8a1b-acaf-4a53-9978-5e0761e14691

Reads test data from a datasheet and predicts the label using neural network model. Predicted label is assigned value "left" or "right" accordingly which makes the spaceship in the game move. 
1. Used pickle to import model in game.
2. Used threading so that game moves independently(parallely) to the data predicting speed of the model


How to run:
1. Extract zip file in the same folder and run the collision_game.py file
