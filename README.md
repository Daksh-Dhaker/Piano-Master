# How to Run the Game
To run the game, follow these steps:
### 1. Start the Server:
       -> Open your terminal or command prompt.
       -> Navigate to the server directory using the command cd server.
       -> Run the server using the command: 
          python3 server.py
### 2. Run Loop MIDI:
       -> Ensure that Loop MIDI is installed on your system.
       -> Start Loop MIDI and make sure it is running in the background. This is necessary for MIDI functionality within the game.
### 3. Run the Client:
       -> Open another terminal or command prompt window.
       -> Navigate to the root directory of the project.
       -> Run the client using the command:
          python3 main.py
### Note:
    -> If you are running the game locally and not on Azure, please make sure to update the IP address in the following files:
       -> 'server/server.py'
       -> 'client/utils/network.py'
    -> Ensure that MIDI is running in the background. If you are not using a real piano, you can use a virtual MIDI synth to emulate the game.
### Hosting on Azure:
    -> If you are hosting this game on Azure, ensure that your server is properly configured to run on Azure's platform.

          
          
