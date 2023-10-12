Sayed Maqbool Ahmed Inamdar
Registration Number: 2204389
Project Title: Create a Neural Network Agent for the game TORCS

Installation and Gameplay Instructions
======================================

Setting up the Environment:

1.  Download play.sh from Faser.

2.  Open a terminal in the directory where play.sh is located.

3.  Make the play.sh script executable:
	chmod +x play.sh

4.  Run the play.sh script:
	./play.sh

5.  Wait for the environment and TORCS binary to install. This may require:
   >Entering your administrative password due to some commands using sudo.
   >Signing in to cseegit for cloning the repository.

6.  Once installed, the trained agent will begin playing. For a better camera angle, press F2.

Note: After the agent finishes playing, the virtual environment will deactivate automatically.

Playing the Agent Again:
========================

1. Navigate to the 2204389 directory:
	cd 2204389

2.  Activate the virtual environment:
	source 2204389_env/bin/activate

3. Move to the game directory:
	cd 22-23_CE901-CE902-SU_inamdar_sayed_m_a/GymTorcs-master

From here, you can choose to:

>   Run the neural network agent:
	python genTensorAgent.py

>   Run the hardcoded agent:
	python handcoded.py

>   Play TORCS using keyboard controls:
	python keyborad.py


thank you for everything.