from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

app = Flask(__name__)

BASE_API_URL = os.environ.get("BASE_API_URL")
LANGFLOW_ID = os.environ.get("LANGFLOW_ID")
FLOW_ID = os.environ.get("FLOW_ID")
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "lang1"  

conversation = []


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


# Home route
@app.route("/")
def home():
    return render_template("home.html")


# Chat route
@app.route("/chat")
def index():
    return render_template("index.html", conversation=conversation)
# Dashboard route
@app.route("/dashboard")
def dashboard():
    csv_file = "/cleaned_10k_new.csv"
    
    df = pd.read_csv(csv_file)
    
    platform_stats = df.groupby('Platform').agg({'Likes': 'sum', 'Comments': 'sum'}).reset_index()
    
    df['Engagement Rate'] = (df['Likes'] + df['Comments']) / df['Impressions']
    engagement_stats = df.groupby('Platform')['Engagement Rate'].mean().reset_index()

    df['Likes-to-Comments Ratio'] = df['Likes'] / df['Comments'].replace(0, 1)
    ratio_stats = df.groupby('Platform')['Likes-to-Comments Ratio'].mean().reset_index()

    reach_impressions_stats = df.groupby('Platform').agg({'Reach': 'sum', 'Impressions': 'sum'}).reset_index()

    age_stats = df.groupby('Audience_Age').agg({'Likes': 'mean', 'Comments': 'mean'}).reset_index()

    post_type_stats = df.groupby('Post_Type').agg({'Likes': 'sum', 'Comments': 'sum', 'Shares': 'sum'}).reset_index()

    df['Shares-to-Likes Ratio'] = df['Shares'] / df['Likes'].replace(0, 1)
    df['Shares-to-Comments Ratio'] = df['Shares'] / df['Comments'].replace(0, 1)

    shares_ratios = df.groupby('Post_Type').agg({
        'Shares-to-Likes Ratio': 'mean',
        'Shares-to-Comments Ratio': 'mean',
    }).reset_index()

    df['Date'] = pd.to_datetime(df['Post_Timestamp'])

    df['Month'] = df['Date'].dt.to_period('M')
    monthly_stats = df.groupby('Month').agg({
        'Likes': 'sum',
        'Comments': 'sum',
        'Shares': 'sum'
    }).reset_index()

    chart_data = {
        'labels': platform_stats['Platform'].tolist(),
        'likes': platform_stats['Likes'].tolist(),
        'comments': platform_stats['Comments'].tolist(),
        'platforms': engagement_stats['Platform'].tolist(),
        'engagement_rate': engagement_stats['Engagement Rate'].tolist(),
        'ratio_platforms': ratio_stats['Platform'].tolist(),
        'likes_to_comments_ratio': ratio_stats['Likes-to-Comments Ratio'].tolist(),
        'reach_platforms': reach_impressions_stats['Platform'].tolist(),
        'reach': reach_impressions_stats['Reach'].tolist(),
        'impressions': reach_impressions_stats['Impressions'].tolist(),
        'age_labels': age_stats['Audience_Age'].tolist(),
        'age_likes': age_stats['Likes'].tolist(),
        'age_comments': age_stats['Comments'].tolist(),
        'post_type_labels': post_type_stats['Post_Type'].tolist(),
        'post_type_likes': post_type_stats['Likes'].tolist(),
        'post_type_comments': post_type_stats['Comments'].tolist(),
        'post_type_shares': post_type_stats['Shares'].tolist(),
        'post_type_shares_likes_ratio': shares_ratios['Shares-to-Likes Ratio'].tolist(),
        'post_type_shares_comments_ratio': shares_ratios['Shares-to-Comments Ratio'].tolist(),
        'monthly_labels': monthly_stats['Month'].astype(str).tolist(),
        'monthly_likes': monthly_stats['Likes'].tolist(),
        'monthly_comments': monthly_stats['Comments'].tolist(),
        'monthly_shares': monthly_stats['Shares'].tolist()
    }
    
    return render_template('dashboard.html', chart_data=chart_data)



@app.route("/run_flow", methods=["POST"])
def run_flow_endpoint():
    user_message = request.form.get("message")
    if not user_message.strip():
        return jsonify({"error": "Please enter a message"}), 400

    conversation.append({"role": "User", "message": user_message})

    try:
        response = run_flow(user_message)
        response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]

        conversation.append({"role": "Chatbot", "message": response_text})
        return jsonify({"user_message": user_message, "response_text": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
