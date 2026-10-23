# MongoDB: Amazon Fine Food Reviews

Analysis of the Amazon Fine Food Reviews dataset (about 568k reviews) using MongoDB as a document store. Homework #1 for the SEBD course.

## What it does

- Loads the reviews into MongoDB, split into one collection per score (1 to 5) plus one for reviews without text.
- Answers product, user and sentiment questions with aggregation pipelines.
- Tunes VADER sentiment parameters with a grid search to improve baseline accuracy.
- Recommends products by combining collaborative signals, TF-IDF content similarity and a sentiment quality score. The weights are explicit, so each recommendation can be explained.
- Tracks monthly sentiment over time and inspects anomalies.

## Requirements

- Python 3.8+
- MongoDB running on `localhost:27017`
- `Reviews.csv` from [Kaggle](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews), placed in this folder

## Usage

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

pip install -r requirements.txt
jupyter notebook amazon_fine_food_reviews.ipynb
```

The notebook runs in order: data loading and ingestion, VADER tuning, sentiment classification, aggregation analytics, hybrid recommendation, temporal analysis.

## Troubleshooting

- Connection errors: check that the service is running (`mongosh` should connect).
- High memory use: reduce the sample size used for VADER optimization in the notebook.
- Dataset not found: `Reviews.csv` must be in the `MongoDB/` folder.

## Files

- `amazon_fine_food_reviews.ipynb`: the full pipeline
- `MongoDB_Camossi.pdf`: written report
- `Homework_MongoDB_2025.2026.pdf`: assignment
