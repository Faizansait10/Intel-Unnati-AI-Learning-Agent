# 🌟 Multimodal AI Text and Voice Agent: Your Intelligent Conversational Companion 🗣️✍️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgray?logo=flask)](https://flask.palletsprojects.com/en/latest/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Platform-orange?logo=google-cloud)](https://cloud.google.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-red?logo=google-gemini&logoColor=white)](https://ai.google.dev/gemini)

---

## ✨ Project Overview

Welcome to the **Gemini AI Voice Agent** – a cutting-edge conversational AI designed to interact with you seamlessly through both **voice and text**. Forget clunky interfaces; this agent listens to your spoken words, understands your queries, provides intelligent responses, and even speaks back to you, creating a truly intuitive and dynamic user experience. It's like having your own personal, intelligent assistant, powered by Google's state-of-the-art Gemini AI model.

Developed as a demonstration of robust multi-modal AI integration, this project is built with a Flask backend, a responsive frontend, and leverages powerful Google Cloud APIs for speech recognition (STT) and text-to-speech (TTS).

---

## 🚀 Witness the Magic (Demo)

*(Self-Correction: Replace the image placeholders with actual GIFs/Screenshots as soon as you have them! A visual demo is absolutely key for an "amazing" README.)*

**[CLICK HERE FOR A LIVE DEMO (e.g., YouTube Video / GIF Demo)]**
*(Once you have a GIF or a short video, link it here! You can use tools like Peek, LICEcap, or online GIF makers.)*

![Screenshot 1: Chat Interface](https://via.placeholder.com/600x300?text=Screenshot+of+Chat+Interface)
*Caption: The sleek, radiant dark theme for an immersive experience.*

![Screenshot 2: Voice Input in Action](https://via.placeholder.com/600x300?text=Screenshot+of+Voice+Input)
*Caption: Seamless voice input and real-time status updates.*

---

## 🌟 Key Features

* 🗣️ **Voice Input:** Speak naturally, and the agent transcribes your words in real-time.
* ✍️ **Text Input:** Traditional text-based chat for quiet environments or quick queries.
* 🧠 **Intelligent Responses:** Powered by **Google Gemini 1.5 Flash**, capable of understanding context, generating creative text, and answering complex questions.
* 🔊 **Voice Output:** The agent speaks its responses aloud, providing an engaging auditory experience.
* 📜 **Conversational Memory:** The agent remembers previous turns in the conversation, allowing for natural, flowing dialogues.
* ✨ **Elegant UI/UX:** A visually stunning radiant dark theme with dynamic elements for a delightful user experience.
* 🌐 **Web-Based:** Accessible directly from your browser, no heavy desktop application needed.

---

## 🛠️ Technologies Used

This project seamlessly integrates multiple powerful technologies:

* **Backend:**
    * [**Python 3.9+**](https://www.python.org/): The core programming language.
    * [**Flask**](https://flask.palletsprojects.com/): A lightweight Python web framework for handling server logic and API endpoints.
    * [**Google Cloud Speech-to-Text API**](https://cloud.google.com/speech-to-text): For converting spoken audio into text.
    * [**Google Cloud Text-to-Speech API**](https://cloud.google.com/text-to-speech): For synthesizing natural-sounding speech from text.
    * [**Google Gemini API (Generative AI)**](https://ai.google.dev/gemini): The powerhouse LLM for generating intelligent and contextual responses.
    * [`python-dotenv`](https://pypi.org/project/python-dotenv/): For securely managing environment variables (API keys).
* **Frontend:**
    * **HTML5:** Structure of the web application.
    * **CSS3:** Styling and dynamic effects (including the radiant dark theme!).
    * **JavaScript (ES6+):** Client-side logic for interactive elements, microphone access, and communication with the backend.

---

## 🏁 Getting Started

Follow these steps to set up and run your Gemini AI Voice Agent locally.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.9 or higher**
* **Git**
* A **Google Cloud Platform (GCP) Project** with:
    * **Speech-to-Text API enabled**
    * **Text-to-Speech API enabled**
    * A **Service Account Key** (JSON file) for authentication.
* Access to the **Google Gemini API**.

### Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Faizansait10/Intel-Unnati-AI-Learning-Agent.git](https://github.com/Faizansait10/Intel-Unnati-AI-Learning-Agent.git)
    cd Intel-Unnati-AI-Learning-Agent
    ```

2.  **Create a Virtual Environment:**
    It's best practice to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    Navigate to the `backend` folder and install the required Python packages.
    ```bash
    pip install -r backend/requirements.txt
    ```
    *(If you don't have a `requirements.txt` yet, create one in the `backend` folder by running `pip freeze > requirements.txt` after installing Flask, google-cloud-speech, google-cloud-texttospeech, google-generativeai, and python-dotenv)*

5.  **Set Up API Keys & Credentials (`.env` file):**
    Create a file named `.env` in the **root directory** of your project (the same folder as your `backend` and `frontend` folders).

    **Important:** This file is listed in `.gitignore` to keep your secrets safe and should **NEVER** be committed to public repositories.

    Add the following lines to your `.env` file, replacing the placeholder values:

    ```dotenv
    GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/gcp_service_account_key.json
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    ```
    * **`GOOGLE_APPLICATION_CREDENTIALS`**: This should be the **absolute path** to your downloaded Google Cloud service account JSON key file.
    * **`GEMINI_API_KEY`**: This is your API key obtained from [Google AI Studio](https://ai.google.dev/).

### Running the Application

1.  **Start the Flask Backend Server:**
    From your project's root directory (with the virtual environment activated), navigate into the `backend` folder and run `app.py`:
    ```bash
    python backend/app.py
    ```
    You should see output indicating the Flask server is running, typically on `http://127.0.0.1:5000/`.

2.  **Open the Frontend in Your Browser:**
    Navigate to `http://127.0.0.1:5000/` in your web browser.

---

## 🎤 Usage

Once the application is running and loaded in your browser:

* **To use Text Input:** Type your message into the input field at the bottom and press `Enter` or click the "Send Text" button.
* **To use Voice Input:**
    1.  Click the **"Start Recording"** button.
    2.  Speak clearly into your microphone.
    3.  Click the **"Stop Recording"** button when you're done speaking.
* The AI's response will appear in the chatbox, both as text and as spoken audio.

---

## 📁 Project Structure
### Intel-Unnati-AI-Learning-Agent/
  #### ├── .env                  # Environment variables (API keys, NOT committed to Git!)
  #### ├── .gitignore            # Files/folders ignored by Git
### ├── backend/              # Flask server and AI logic
  ##### │   ├── app.py            # Main Flask application
  ##### │   └── requirements.txt  # Python dependencies for the backend
### ├── frontend/             # HTML, CSS, and JavaScript for the user interface
  #### │   ├── index.html        # The main web page
  #### │   ├── style.css         # Styling for the web page (radiant dark theme!)
  #### │   └── script.js         # Frontend JavaScript logic
#### └── README.md             # This file!
## 🔮 Future Enhancements (Roadmap)

We're always looking to expand the capabilities of this agent! Potential future enhancements include:

* **OpenVINO Integration:** Explore local inference for Speech-to-Text and Text-to-Speech using Intel's OpenVINO toolkit, reducing reliance on cloud APIs and enabling edge AI capabilities.
* **Custom Knowledge Base:** Allow the agent to access and respond based on specific, user-defined knowledge.
* **Persistent Chat History:** Implement database integration for chat history that persists across sessions and users (currently global for demo).
* **Customizable AI Persona:** Allow users to define the AI's personality or style of response.
* **Deployment:** Containerize the application (e.g., with Docker) for easier deployment to cloud platforms or edge devices.

---

## 🙏 Acknowledgments & Credits

A huge thank you to:
* **Google Gemini** for providing the powerful generative AI model.
* **Google Cloud Platform** for the robust Speech-to-Text and Text-to-Speech services.
* **Flask** for making web development a breeze.
* **You (the creator!)** for the vision and effort in building this amazing agent.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Self-correction: If you haven't created a `LICENSE` file yet, you should! You can add one directly on GitHub after pushing, or create a `LICENSE` file in your root directory with the MIT license text.)*

---
