# ExpressMusic (Other names include Doorman and Emotify):

ExpressMusic lets you identify people in real time and play songs based on their detected facial expressions!

&nbsp;
#### Instructions to run:
1. Clone github repo
2. Open up 2 terminal windows and run the following commands

    Terminal 1: (opens webcam)
    ```bash
    cd ExpressMusic/cv
    python3 cameraCV.py
    ```

    Terminal 2: (runs server)
    ```bash
    cd ExpressMusic
    python3 main.py
    ```
3. Open http://localhost:5000 in browser
4. Change your expression, and enjoy!

&nbsp;
#### Instructions to add new person in classifier:
1. Open the ExpressMusic/cv/take_images.py file
2. Change person variable to the name of the person (No spaces, no commas etc)
3. Assign a new unique person_number
4. In the 'training-data' folder, create a new folder whose name is the unique person_number.
5. Run the following commands: <br>
    ```bash
    cd ExpressMusic/cv
    python3 take_images.py
    ```
6. In cameraCV.py, add an entry to the 'people' dictionary with key=unique_number and value=Name of the new person


Created by Team Compliing... for a hackathon!
