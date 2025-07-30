# YouTube Channel Dashboard

## Overview
This project provides an automated pipeline and interactive dashboard for analyzing YouTube channel video performance. It collects video data using the YouTube Data API, enriches it with custom tags, and visualizes key metrics to help content creators and analysts derive actionable insights. Currently, this is a work in progress! With a free tier YouTube API plan, usage is quite limited in terms of content that can be retrived. I plan to develop more features and fix a handful of bugs!

<img width="1754" height="560" alt="Screenshot 2025-07-28 at 8 52 53 PM" src="https://github.com/user-attachments/assets/19851269-9bf1-4c8c-a90e-f8bb44aba0bb" />

<img width="846" height="388" alt="Screenshot 2025-07-28 at 8 53 50 PM" src="https://github.com/user-attachments/assets/a6c19721-c269-432c-a5ce-155995a9f58f" />

---

## Features

- **Automated Data Collection:**  
  Fetches video metadata (title, description, views, likes, duration, tags, publish date) from any YouTube channel using the official API.

- **Data Enrichment:**  
  Tags videos by genre, animation type, content type (short/long), copyright status, and extracts time-based features.

- **Interactive Dashboard:**  
  Built with Dash and Plotly, allowing dynamic filtering, sorting, and visualization (bar charts, pie charts, time series).

- **Data Inspection:**  
  Includes tools to inspect and validate the collected CSV data.

---

## Technologies Used

- Python
- pandas
- Dash
- Plotly
- google-api-python-client
- isodate

---

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/jordanjho/YouTube-Dashboard.git
   cd YouTube-Dashboard
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   Or manually:
   ```sh
   pip install dash pandas plotly google-api-python-client isodate
   ```

4. **Configure API credentials:**
   - Create a `config.py` file with your YouTube Data API key and channel ID:
     ```python
     API_KEY = "YOUR_API_KEY"
     CHANNEL_ID = "YOUR_CHANNEL_ID"
     ```

5. **Fetch video data:**
   ```sh
   python youtube_api.py
   ```
   This will create/update `data/videos.csv`.

6. **Inspect the data (optional):**
   ```sh
   python inspect_csv.py
   ```

7. **Run the dashboard:**
   ```sh
   python app.py
   ```
   Open the link shown in your terminal in your browser.

---

## Customization

- **Tagging Logic:**  
  Modify `utils.py` to adjust or expand video tagging rules.

- **Dashboard Visuals:**  
  Edit `app.py` to add new charts, filters, or change layout.

---

## Troubleshooting

- **No videos collected:**  
  - Double-check your `CHANNEL_ID` (should start with `UC`).
  - Ensure your API key is enabled for YouTube Data API v3.
  - Check for errors in the terminal.

- **Dependencies not found:**  
  - Make sure your virtual environment is activated.
  - Reinstall dependencies with `pip install ...`.

---

## License

This project is for educational and personal analytics use.  
Please respect YouTube’s Terms of Service regarding data usage and scraping.
