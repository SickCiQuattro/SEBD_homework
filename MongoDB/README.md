# Homework #1 - MongoDB

## Amazon Fine Food Reviews Analysis

Course: Advanced Information Systems and Big Data (SEBD) - Academic Year 2025-2026  
Author: Filippo Camossi

## Project Overview

This module analyzes the Amazon Fine Food Reviews dataset (about 568k records) with MongoDB as a document store.
The goal is to combine document-based analytics, sentiment analysis, and recommendation logic in a single end-to-end pipeline.

## Goals

- Ingest and organize large review data in MongoDB collections.
- Run analytical queries with aggregation pipelines.
- Apply VADER sentiment analysis with parameter tuning.
- Build a hybrid recommender (collaborative + content + sentiment).
- Study sentiment evolution over time.

## Tech Stack

- Python 3.8+
- MongoDB (local instance on localhost:27017)
- Jupyter Notebook
- pymongo, pandas, scikit-learn, vaderSentiment, matplotlib, seaborn

## Repository Structure

```text
MongoDB/
|- amazon_fine_food_reviews.ipynb
|- Reviews.csv
|- requirements.txt
`- README.md
```

## Setup

1. Install MongoDB and start the service.

macOS (Homebrew):

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

2. Download the dataset from Kaggle and place `Reviews.csv` in this folder:
https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews

3. Install Python dependencies:

```bash
cd MongoDB
pip install -r requirements.txt
```

## Run Locally

```bash
jupyter notebook amazon_fine_food_reviews.ipynb
```

Recommended execution order inside the notebook:

1. Data loading and MongoDB ingestion
2. VADER parameter optimization
3. Sentiment classification
4. Aggregation-based analytics
5. Hybrid recommendation
6. Temporal analysis and plots

## Key Implemented Features

- Data split into score-based collections (1-5 plus no-text) for targeted analysis.
- MongoDB aggregation pipelines for product, user, and sentiment insights.
- VADER tuning through grid search to improve baseline accuracy.
- Hybrid recommendation score combining:
  - collaborative signals
  - TF-IDF content similarity
  - sentiment quality score
- Monthly sentiment trend analysis with anomaly inspection.

## Notable Technical Choices

- Separate score collections were used to simplify some analytical slices and comparisons.
- Recommendation combines heterogeneous signals with explicit weights for interpretability.
- Temporal analysis is integrated with recommendation discussion to reason about model adaptation over time.

## Expected Outcome

After a full run, you should obtain:

- A populated MongoDB dataset for review analytics.
- Sentiment labels and quality metrics.
- Top products/users and score-sentiment correlation views.
- Hybrid recommendations with explainable component scores.

## Troubleshooting

- If MongoDB connection fails, verify the service is running (`mongosh` should connect).
- If memory usage is high, reduce optimization sample size in the notebook.
- If dataset is not found, confirm `Reviews.csv` is in the `MongoDB/` directory.

## Related Docs

- Root portfolio: ../README.md
- MongoDB docs: https://www.mongodb.com/docs/
- VADER: https://github.com/cjhutto/vaderSentiment
