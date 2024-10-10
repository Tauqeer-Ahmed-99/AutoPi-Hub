# AutoPi Hub

## Home Automation System

The AutoPi Hub Home Automation System provides a simple, secure, and flexible way to automate home devices using Raspberry Pi (or similar device(s)) and a mobile app (Control Nest). It consists of two main parts:

1. **AutoPi Hub:** Local Server on Home Network (using Raspberry Pi or similar device)
2. **Control Nest:** Mobile App for control and monitoring. [Download APK](https://github.com/Tauqeer-Ahmed-99/Control-Nest) [Source Code](https://github.com/Tauqeer-Ahmed-99/Control-Nest)

## Get Started

### Part 1: Setting up the AutoPi Hub Local Server on Raspberry Pi

1. **Raspberry Pi (or similar device)** that can run a Python server and has GPIO pins to connect physical devices.
2. **Install the Official Debian OS** on the Raspberry Pi:

   - Follow the official Raspberry Pi guidelines to install the Debian OS provided by the Raspberry Pi Foundation.
   - During installation, **set the hostname to `rpi`** for ease of access.
   - Any Linux Operating System with other devices are supported.

3. **Login to Raspberry Pi**:

   - Once the OS is installed and the Raspberry Pi has started, SSH into the device using the following command:

     ```bash
     ssh username@rpi.local
     ```

     Replace `username` with the username you set during OS installation.

4. **Run the AutoPi Hub Home Automation System Setup**:

   - After logging in, copy and paste the following command into your terminal to install the AutoPi Hub Home Automation System software and its dependencies:

     ```bash
     sudo apt-get install git -y &&
     sudo rm -rf ./RPi_HAS &&
     git clone https://github.com/Tauqeer-Ahmed-99/RPi_HAS.git &&
     cd ./RPi_HAS &&
     chmod +x setup.sh && ./setup.sh
     ```

   - This command will:
     1. Install Git (if not already installed).
     2. Remove any existing `RPi_HAS` directory.
     3. Clone the repository containing the AutoPi Hub Home Automation System.
     4. Run the setup script to install necessary dependencies and software.

5. **Set House Password**:

   - During installation, you will be prompted to **set a house password**. This password is essential for connecting the mobile app to the server.

6. **FastAPI Server Auto Start**:
   - Upon successful installation, the FastAPI server will be started and hosted on the local network.
   - The server is configured to **automatically start on boot**, ensuring that the Home Automation service is always running when the Raspberry Pi is powered on.

### Part 2: Setting up Control Nest the Mobile App

1. **Download the Control Nest Mobile App**:

   - Download the Control Nest mobile app from the following link:
     [ControlNest.apk](https://github.com/Tauqeer-Ahmed-99/Control-Nest)

2. **Login/Signup**:

   - Open the app and log in or sign up with your credentials.

3. **Connect to the Local Server**:

   - After login, you will be asked to enter the following details:
     - **Hostname**: Enter the Raspberry Pi's hostname without `.local` suffix (`rpi` by default).
     - **House Password**: Enter the house password you set during the server setup.

4. **Access the Dashboard**:
   - Upon successful connection, you will be directed to the dashboard where you can manage your home automation setup.

### Adding Rooms and Devices

1. **Create Rooms**:

   - On the app dashboard, create different rooms (e.g. Living Room, Bedroom) where devices will be installed.

2. **Add Devices**:

   - For each room, you can add devices (lights, fans, etc.) by specifying:
     - **Device Name**
     - **GPIO Pin**: The pin on the Raspberry Pi's GPIO header to which the device is connected.

3. **Wiring the Devices**:

   - After adding devices in the app, you need to physically wire the devices to the Raspberry Pi:
     - **Relay Wiring**: For example, to control a light or fan, wire a relay's:
       - VCC to 5V power,
       - GND to ground,
       - IN to the GPIO pin selected in the app.
     - **Relay to Switch Wiring**: Connect the relay’s Normally Open (NO) pin to the external switch, and the Common (COM) pin to the device (light/fan).
   - This wiring ensures the device can be controlled both manually and via the mobile app.

4. **Control and Automate Devices**:
   - Once devices are connected, they can be controlled and scheduled through the mobile app.

## Benefits of AutoPi Hub Home Automation System

1. **Security**:

   - All data is stored locally on the Raspberry Pi, meaning no information is shared over the internet.
   - Devices can only be controlled when connected to the local network, ensuring privacy and security.

2. **Cost Flexibility**:

   - Users can choose their own devices, allowing for customization of system cost.
   - The setup can be adjusted based on the quality and type of devices chosen by the user or contractor.

3. **Simplified Installation**:
   - **Step 1**: Install the OS on the Raspberry Pi.
   - **Step 2**: SSH into the system.
   - **Step 3**: Run the installation command (server setup and hosted on the local network).
   - **Step 4**: Add/Create rooms and devices in the mobile app.
   - **Step 5**: Wire the devices according to simple schematic diagrams.
   - **Done**: The home is now automated.

## Want to Contribute?

- We welcome contributions! If you're interested in improving Control Nest, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/feature-name or bug/bug-name`).
3. Make your changes and commit them (`git commit -m 'added: feature name' or 'resolved: bug name'`).
4. Push to the branch (`git push origin feature/feature-name or bug/bug-name`).
5. Open a pull request.

- Please check the issues section for existing bugs or features you'd like to work on.

## License

- This project is licensed under the MIT License. See the LICENSE file for more details.
