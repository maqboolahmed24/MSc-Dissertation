#!/bin/bash
mkdir 2204389
cd 2204389
sudo apt update
sudo apt install -y python3
sudo apt install -y python3-pip
sudo apt-get install -y python3-venv
python3 -m venv 2204389_env
source 2204389_env/bin/activate
sudo apt update
sudo apt install -y git
git clone https://cseegit.essex.ac.uk/22-23-ce901-ce902-su/22-23_CE901-CE902-SU_inamdar_sayed_m_a.git
cd 22-23_CE901-CE902-SU_inamdar_sayed_m_a/
cd GymTorcs-master/
chmod +x deps_install_script.sh
./deps_install_script.sh 
pip install gym
pip install tensorflow
pip install matplotlib
pip install psutil
pip install pynput
cd ..
cp genTensorAgent.py GymTorcs-master/
cp ignorewarning.py GymTorcs-master/
cp handcoded.py GymTorcs-master/
cp keyboard.py GymTorcs-master/
cp -r Save GymTorcs-master/
cd GymTorcs-master
python genTensorAgent.py
read -p "Would you like to play with the hardcoded agent? (yes/no) " response

if [ "$response" = "yes" ]; then
    echo "Starting the hardcoded agent..."
    cd 2204389
    source 2204389_env/bin/activate
    cd 22-23_CE901-CE902-SU_inamdar_sayed_m_a/GymTorcs-master/
    python handcoded.py

    read -p "Would you like to play TORCS? (yes/no) " response
    if [ "$response" = "yes" ]; then
        echo "Now You are Playing, Enjoy:)"
        python keyboard.py
    else
        exit
    fi

elif [ "$response" = "no" ]; then
    read -p "Would you like to play TORCS? (yes/no) " response
    if [ "$response" = "yes" ]; then
        cd 2204389
        source 2204389_env/bin/activate
        cd 22-23_CE901-CE902-SU_inamdar_sayed_m_a/GymTorcs-master/
        echo "Now You are Playing, Enjoy:)"
        python keyboard.py
    else
        exit
    fi
else
    echo "Invalid response."
    exit
fi

