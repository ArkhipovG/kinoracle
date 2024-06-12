# KinOracle: Your Cinematic Oracle

## Overview

**KinOracle** is a Telegram bot designed to be your ultimate guide in the world of movies and TV shows. Whether you're deciding what to watch tonight or exploring top-rated films and actors, Kinoracle offers personalized recommendations and insights to enhance your viewing experience.

## Project Structure
- **my-lambda-function**: Directory containing all the functionality files of the bot.
- **predict_genres**: Directory containing the Jupyter Notebook with creation of the model for prediction genres based on movie description.
- **movie_dashboard_public.twbx**: The Tableau dashboard created using the analyzed data.

## Features

**Movie and TV Show Suggestions**: 
- Get tailored recommendations based on your preferences.

**Search**: 
- Find information about any movie or TV show in huge database.

**Charts and Ratings**:
- Receive latest updates with popular or upcoming movies and TV shows.

**Collections and Recommendations**: 
- Look through movie collections and recommendations based on any of them.

**Interactive Quizzes**: 
- Test your knowledge with fun quizzes like guessing movies from pictures or descriptions.

**Personal Lists**:
- Create and manage your favorite movies or watchlist for future viewing.

**Interactive Dashboard**: 
- Explore various rankings by movies, genres, countries, production companies and other parameters. 


## Technical Stack

**Python**:
- Core programming language used for developing the bot, collecting data, and implementing the machine learning model to predict genres.

**AWS Lambda**:
- Serverless compute service used to deploy the code and run the bot's backend logic. It receives events and automatically manages the compute resources, ensuring scalability and efficiency.

**AWS DynamoDB**:
- NoSQL database service used for storing and managing users' personal lists, ensuring fast and reliable data retrieval.

**AWS API Gateway**:
- Interface to expose the AWS Lambda function as an API, enabling seamless communication between the bot and backend services.

**APIs**:
- **Telegram API**: Used to interact with Telegram, send and receive messages, and manage bot functionalities.
- **The Movie Database (TMDb) API**: Used to fetch movie data, ratings, genres, and other relevant information.
- **Gemini API**: Integrated to provide a powerful recommendation system based on user-provided information.

**Tableau**:
- Data visualization tool used to create interactive and shareable dashboards that present movie data in a visually appealing format.

## Conclusion

**KinOracle** stands out as a powerful and user-friendly tool for movie enthusiasts. By leveraging advanced technologies and APIs, it provides a seamless and personalized viewing experience. Whether you are looking for movie recommendations, detailed insights, or interactive content, KinOracle has something to offer for every movie lover. Dive into the world of cinema with KinOracle and transform the way you discover and enjoy movies and TV shows.

