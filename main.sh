
# First time start command

# Does the following
# 1. Install git if not already installed.
# 2. Removes the Directort "./RPi_HAS" if already present.
# 3. Clones the RPi_HAS repository.
# 4. Changes the directory to the "./RPi_HAS".
# 5. Allows permissions to "setup.sh" shell script.
# 6. Executes "setup.sh" shell script.

sudo apt-get install git -y && 
sudo rm -rf ./RPi_HAS && 
git clone https://github.com/Tauqeer-Ahmed-99/RPi_HAS.git && 
cd ./RPi_HAS && 
chmod +x setup.sh && ./setup.sh


# Update command
# Does the following
# 1. Allows permissions to "update.sh" shell script.
# 2. Executes "update.sh" shell script.
chmod +x update.sh && ./update.sh
