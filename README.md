# Line ChatBot for CS Conversion Programme Application Consultant

## Overview

Welcome to our Line ChatBot designed to assist aspiring students interested in the CS conversion programme application process. This ChatBot provides information, answers queries, and guides users through the application procedure for the Computer Science (CS) conversion programme.

## Getting Started
To use this Line ChatBot for the CS conversion programme application, follow these steps:

### For Users

1. **Download Line app**
2. **Scan this QRcode to add a line friend**
   
   ![Line chatbot QRcode](https://github.com/PeiPeiC/Line_chat_bot/assets/104357328/a21dd7d8-2409-4bc0-9cd0-a3a87b7e9447)

   ![official account](https://github.com/PeiPeiC/Line_chat_bot/assets/104357328/dc3aec4d-3826-47be-b2bb-463b3e6301a0)
3. **Start to chat!**

   [Chat Link](https://github.com/PeiPeiC/Line_chat_bot/assets/104357328/2d1dda34-6ddd-4c34-baa5-e77630fb2635)

### For Developers

1. **Create Line Messaging API Account**:
   - Go to the Line Developer Console and create a Line Messaging API account for your ChatBot.
   - Save the Channel Secret and Channel Access Token provided by Line. You need these to authenticate your bot in the `views.py` file.

2. **Set Up Virtual Environment**:
   - Create a virtual environment based on your operating system in your preferred method. You can use `virtualenv` or `venv` to isolate dependencies.

   ### Using `virtualenv` (Linux, macOS, and Windows):

   1. Install `virtualenv` if you haven't already:

      ```bash
      pip install virtualenv
      ```

   2. Create a virtual environment:

      ```bash
      # For Linux and macOS
      virtualenv venv

      # For Windows
      virtualenv venv
      ```

   3. Activate the virtual environment:

      ```bash
      # For Linux and macOS
      source venv/bin/activate

      # For Windows
      venv\Scripts\activate
      ```

   ### Using `venv` (Python 3.3 and later, built-in) - (Linux, macOS, and Windows):

   1. Create a virtual environment:

      ```bash
      # For Linux and macOS
      python3 -m venv venv

      # For Windows
      python -m venv venv
      ```

   2. Activate the virtual environment:

      ```bash
      # For Linux and macOS
      source venv/bin/activate

      # For Windows
      venv\Scripts\activate
      ```

   Once you activate the virtual environment, you can install the required packages using `pip` without affecting the system-wide Python installation. To deactivate the virtual environment, use the command:

   ```bash
   deactivate


3. **Install Dependencies**:
   - Activate the virtual environment you created in the previous step.
   - Use the `pip install -r requirements.txt` command to install all the packages listed in the `requirements.txt` file. This ensures that the necessary libraries are available for your ChatBot.

4. **Ngrok Setup**:
   - Download the `ngrok` executable from the official website. Ngrok is a tool that allows you to create a secure tunnel to your local development server.
   - In your terminal, navigate to the directory where the `ngrok` executable is located, and run the command: `ngrok http 8000`. This assumes that your local development server is running on port 8000.
   - Ngrok will generate an HTTPS link (e.g., `https://6a3b-2001-b400-e209-c92c-1d2e-53de-ca91-62b2.ngrok-free.app`) that you will use for the webhook configuration.

5. **Webhook Configuration**:
   - In the Line Developer Console, configure the Line Messaging API webhook by appending `/line/webhook/` to the end of your ngrok-generated HTTPS link. For example, if your ngrok HTTPS link is `https://6a3b-2001-b400-e209-c92c-1d2e-53de-ca91-62b2.ngrok-free.app`, the webhook URL will be `https://6a3b-2001-b400-e209-c92c-1d2e-53de-ca91-62b2.ngrok-free.app/line/webhook/`.
   - Save the updated webhook URL in the Line Developer Console.

6. **Allow Hosts Configuration**:
   - In your Django project's `settings.py` file, add the ngrok-generated URL (without the `https://`) to the `ALLOWED_HOSTS` list. For example:
     ```
     ALLOWED_HOSTS = ['6a3b-2001-b400-e209-c92c-1d2e-53de-ca91-62b2.ngrok-free.app', '127.0.0.1']
     ```

7. **Update views.py**:
   - Open the `views.py` file in your Django project.
   - At the beginning of the file, add the Channel Secret and Channel Access Token you obtained from the Line Developer Console. These credentials will be used for authentication.

8. **Run the Server**:
   - In your terminal, navigate to your Django project directory and run the command: `python manage.py runserver`. This starts the Django development server, allowing your Line ChatBot to respond to messages.

9. **Add Line Account as Friend**:
   - Add your Line ChatBot as a friend on your Line account by searching for its name.
   - Start interacting with the ChatBot to seek guidance on the CS conversion programme application.

Remember to keep your Channel Secret and Channel Access Token secure and avoid sharing them publicly to ensure the security of your Line ChatBot.

## Features

- **CS Programme Information**: The ChatBot provides comprehensive information about the CS conversion programme, helping users to make better decisions.



## Disclaimer

Please note that while the ChatBot aims to provide helpful and accurate information, it is not a substitute for official guidance. Users should refer to the official CS conversion programme website and consult with the appropriate authorities for official and up-to-date information regarding the application process.

## Feedback and Contributions

We value your feedback and welcome contributions to enhance the functionality and accuracy of the ChatBot. If you encounter any issues or have suggestions for improvements, please feel free to reach out or submit pull requests.

Happy Chatting, and best of luck with your CS conversion programme application!
