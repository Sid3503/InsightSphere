# InsightSphere: Social Media Engagement Insights 🚀

This project leverages **LangFlow**, **Astra DB**, and **Groq LLM** to analyze social media engagement data across platforms like **LinkedIn**, **Twitter**, **Facebook**, and **Instagram**. The goal is to build an interactive and insightful platform to help users understand trends, engagement patterns, and performance of their social media posts in an easy-to-use, dynamic web interface.

## Project Overview 📊

The solution begins by ingesting a **Social Media Engagement Dataset** containing metrics like:

- **Platform**: LinkedIn, Twitter, Facebook, Instagram
- **Post Type**: Reel, Image, Carousel
- **Metrics**: Likes, Shares, Comments, Reach, Engagement, Impressions

These data points are stored in **Astra DB** to create a collection that will be used for **vector search** to retrieve relevant insights. Through this, we generate a **comprehensive prompt** that includes the context from the database, historical queries from the user, and the current question. This prompt is passed to the **Groq LLM**, which processes the query and provides contextually-aware responses.

The entire process is integrated into a **Flask web app** with interactive data visualizations created using **Chart.js**, allowing users to monitor trends and make informed decisions.

## Workflow Breakdown 🔄

### 1. **Data Upload to Astra DB** 🗂️

- Upload the social media engagement dataset into **Astra DB**.
- Create a **collection** in Astra DB to store the data.
- This collection will allow fast querying and vector-based searches.

### 2. **LangFlow Workflow** ⚙️

- Design a **workflow in LangFlow** for handling user input, data retrieval, and interaction with the database.
- The workflow starts by taking the user input as a query.
- Perform **vector search** on the dataset in Astra DB, retrieving the most relevant records based on the user’s query.

### 3. **Prompt Generation** 📝

- Construct a **dynamic prompt** combining:
  - **Context**: Fetched from the similarity search results in Astra DB.
  - **History**: A record of the user’s previous questions and answers.
  - **Current Question**: The new query from the user.
- This diverse prompt is sent to the **Groq LLM model** for generating insightful and accurate responses.

### 4. **LLM Integration (Groq)** 🤖

- The **Groq LLM model** receives the comprehensive prompt and returns a context-aware response considering all variables.
- The output is designed to answer the user query while considering social media data trends and metrics.

### 5. **Python API Creation** 🐍

- Convert the LangFlow workflow into a **Python API** to handle requests, process queries, and serve insights.
- The API will act as the backend for the **Flask app**, interacting with Astra DB, LangFlow, and Groq to generate responses.

### 6. **Flask Web App** 🌐

- Build a **Flask web application** to host the backend API.
- Design the frontend for **interactive data exploration** using **Chart.js** to display key metrics like:
  - Engagement over time
  - Performance comparison between different post types (Reels, Images, Carousels)
  - Social media platform-wise metrics (LinkedIn, Twitter, etc.)

### 7. **Interactive Data Visualization** 📈

- Utilize **Chart.js** to create **dynamic charts**:
  - Line charts to display engagement trends over time.
  - Bar charts for comparing post types and platforms.
  - Pie charts to show distribution of engagement metrics (Likes, Comments) across different post types and platforms.

### 8. **User Interaction and Decision Making** 💬

- The Flask app provides users with an intuitive interface to interact with data.
- Users can ask specific questions about their social media engagement, and the app will provide real-time insights generated by the **Groq LLM**.
- The app helps users understand how different metrics (likes, shares, comments) influence overall engagement and performance of posts.

## Technologies Used 🧑‍💻

| Technology       | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **LangFlow**         | For designing and managing AI-driven workflows for processing user queries. |
| **Astra DB**         | Cloud-native NoSQL database for storing social media engagement data.       |
| **Groq LLM**         | Large language model used for generating context-aware responses.           |
| **Flask**            | Lightweight Python web framework for building backend APIs.                 |
| **Chart.js**         | Library for creating interactive charts and graphs.                         |
| **Python**           | For creating APIs and backend logic.                                       |

## Setup and Installation 🛠️

### Prerequisites 📋

- Python 3.8+
- Astra DB Account
- Groq LLM Access (API Key or Token)
- Flask
- LangFlow
- Chart.js

### Steps 🏃‍♂️

1. **Clone the repository**:

    Clone the project to your local machine:

    ```bash
    git clone https://github.com/yourusername/social-media-engagement.git
    cd social-media-engagement
    ``` 

2. Set up a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate # For macOS/Linux
    venv\Scripts\activate # For Windows
    ```

3. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure Astra DB:

  - Set up your Astra DB account and create a new collection for social media engagement data.
  - Update connection details in `config.py`.

5. Run the Flask app:

    ```bash
    python app.py
    ```

6. Access the app:

  Open a web browser and go to `http://127.0.0.1:5000` to interact with the app.


