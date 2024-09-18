
# Sentiment Analysis on Electronic Product Reviews

## Project Overview
This project performs sentiment analysis on electronic product reviews scraped from **Flipkart**. The goal is to classify reviews as positive or negative, and based on this, a recommendation system is developed that displays the percentage of positive and negative reviews for various products. This helps potential buyers make informed decisions when purchasing products.

## Features
- **Review Scraping**: Automated scraping of product reviews from Flipkart.
- **Data Preprocessing**: Includes cleaning, tokenization, and vectorization of the review data.
- **Sentiment Analysis**: Uses a machine learning model to classify the sentiment of the reviews as positive or negative.
- **Recommendation System**: Displays the positive and negative review percentages for each product to help users make purchasing decisions.

## Technology Stack
- **Frontend**: 
  - HTML
  - CSS
  - Tailwind CSS
  - JavaScript
- **Backend**:
  - Python Django
  - SQLite3 (Database)
- **Machine Learning**:
  - Natural Language Processing (NLP) techniques for sentiment analysis
  - Libraries: NLTK, Scikit-learn

## Project Architecture
1. **Web Scraping**: Collects product reviews data from Flipkart.
2. **Preprocessing**: Prepares the scraped data by cleaning, tokenizing, and converting it into a format suitable for the machine learning model.
3. **Sentiment Analysis**: 
   - Applies a machine learning classifier to predict the sentiment of each review.
   - Classifies the reviews into positive or negative categories.
4. **Recommendation System**: Calculates the percentage of positive and negative reviews for each product and displays it to the users.
5. **User Interface**: Presents the reviews and sentiment analysis results in a clean, user-friendly interface.

## How to Run the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/Satish-Kumar-Verma/Sentiment-Analysis-on-Electronic-Product-Reviews.git
   cd Sentiment-Analysis-on-Electronic-Product-Reviews
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the Django development server:
   ```bash
   python manage.py runserver
   ```
5. Access the project via your browser at `http://127.0.0.1:8000/`.

## Key Components
- **Scraper Module**: Collects data from Flipkart’s product pages.
- **Sentiment Classifier**: A machine learning model using Natural Language Processing (NLP) to classify sentiment.
- **Web Interface**: Built using Django and Tailwind CSS, provides an intuitive and responsive design.
- **SQLite Database**: Stores the scraped reviews and sentiment classification results.

## Future Improvements
- Expand the dataset by scraping reviews from multiple e-commerce platforms.
- Enhance the machine learning model by incorporating advanced NLP techniques.
- Implement user login and session management for personalized recommendations.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
