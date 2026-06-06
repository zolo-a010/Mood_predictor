# Mood Predictor AI 🧠💬

A full-stack web application that predicts the sentiment of user-entered text on a continuous scale from -1.0 (Negative) to 1.0 (Positive). The application features secure user authentication and utilizes a custom Machine Learning pipeline built with Scikit-Learn.

## ✨ Features

* **Machine Learning Integration:** Uses a robust ML pipeline (TF-IDF Vectorization + Ridge Regression) exported via `joblib` to process text and predict mood scores dynamically.
* **Secure User Authentication:** Full registration and login system with securely hashed passwords using `werkzeug.security`.
* **Database Management:** Uses SQLite and `Flask-SQLAlchemy` to store user credentials, ages, emails, and full names.
* **Seamless Frontend:** A clean, single-page interface built with Vanilla HTML/JS and CSS, communicating with the Flask backend via asynchronous Fetch API requests.

## 🛠️ Technologies Used

* **Backend:** Python 3, Flask
* **Database:** SQLite, Flask-SQLAlchemy
* **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib
* **Frontend:** HTML5, CSS3, Vanilla JavaScript

## 📂 Folder Structure

```text
mood-predictor-ai/
│
├── app.py                      # Main Flask application and API routes
├── sentiment_pipeline.joblib   # Trained Scikit-Learn model pipeline
├── users.db                    # SQLite database (auto-generated on first run)
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
│
└── templates/
    └── index.html              # Frontend user interface
🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
You need Python installed on your machine. You can download it from python.org.

1. Clone the Repository
Bash
git clone [https://github.com/YOUR-USERNAME/mood-predictor-ai.git](https://github.com/YOUR-USERNAME/mood-predictor-ai.git)
cd mood-predictor-ai
2. Set Up a Virtual Environment (Recommended)
Bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Make sure you have the required Python libraries installed:

Bash
pip install Flask Flask-SQLAlchemy pandas scikit-learn joblib
4. Run the Application
Start the Flask server:

Bash
python app.py
Note: If users.db does not exist, the app will automatically create it upon launch.

5. Access the Web App
Open your web browser and go to:

Plaintext
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
💡 How to Use
Sign Up: Click "Don't have an account? Sign up here." to register. Enter your username, password, age group, email, and full name.

Login: Log in with your new credentials.

Predict: Enter a sentence in the dashboard (e.g., "I am having a fantastic day!") and click Predict Mood.

Result: The AI will return a continuous score between -1.0 and 1.0 based on your text and your registered age group.

🧠 Model Training Notes
The embedded model (sentiment_pipeline.joblib) was trained on a dataset of over 27,000 text entries.
If you wish to retrain the model with your own dataset:

Ensure your dataset has a text and sentiment column.

Use sklearn.pipeline.Pipeline to vectorize the text and fit a regressor.

Export the newly trained pipeline using joblib.dump(pipeline, 'sentiment_pipeline.joblib') and replace the file in this directory.