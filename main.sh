
# First time start command

# Does the following
# 1. Install git if not already installed.
# 2. Removes the Directort "./AutoPi-Hub" if already present.
# 3. Clones the AutoPi-Hub repository.
# 4. Changes the directory to the "./AutoPi-Hub".
# 5. Allows permissions to "setup.sh" shell script.
# 6. Executes "setup.sh" shell script.

sudo apt-get install git -y && 
sudo rm -rf ./AutoPi-Hub && 
git clone https://github.com/Tauqeer-Ahmed-99/AutoPi-Hub.git && 
cd ./AutoPi-Hub && 
chmod +x setup.sh && ./setup.sh


# Update command
# Does the following
# 1. Allows permissions to "update.sh" shell script.
# 2. Executes "update.sh" shell script.
chmod +x update.sh && ./update.sh
