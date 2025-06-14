import pandas as pd
import numpy as np
from textblob import TextBlob
import argparse
import os
import re


def map_region(location):
    city_to_region = {
        "Los Angeles": "LA", "Santa Monica": "LA", "Hollywood": "LA",
        "New York": "NY", "Brooklyn": "NY", "Queens": "NY",
        "Atlanta": "GA", "Chicago": "CH", "Miami": "FL",
        "San Francisco": "SF", "Seattle": "NW", "Austin": "TX"
    }
    return city_to_region.get(location, "OTH")

def map_proj_type(proj):
    proj_map = {
        "Feature Film": "F", "Short Film": "F", "Film": "F",
        "Television": "T", "Series": "T", "Streaming": "T", "TV": "T",
        "Commercial": "C", "Ad": "C",
        "Voiceover": "V", "Animation": "V", "Podcast": "V"
    }
    return proj_map.get(proj, "O")


def sentiment_score(text):
    if not isinstance(text, str): return 0.0
    return round(TextBlob(text).sentiment.polarity, 2)


def contains_ai_theme(text):
    if not isinstance(text, str): return False
    return bool(re.search(r'\b(ai|robot|android)\b', text.lower()))


def is_union_role(status):
    if not isinstance(status, str): return False
    status = status.lower().strip()
    return status in ['union', 'sag-aftra', 'aftra', 'sag']


def parse_rate(rate_str):
    if isinstance(rate_str, str):
        digits = ''.join(filter(str.isdigit, rate_str))
        return int(digits) if digits else 0
    return 0


def build_pulse(input_path, output_path):
    df = pd.read_csv(input_path)


    df['date_utc'] = pd.to_datetime(df['posted_date']).dt.date
    df['region_code'] = df['work_location'].apply(map_region)
    df['proj_type_code'] = df['project_type'].apply(map_proj_type)
    df['is_lead'] = df['role_type'].isin(['Lead', 'Principal'])
    df['is_union'] = df['union'].apply(is_union_role)
    df['rate_value'] = df['rate'].apply(parse_rate)
    df['sentiment'] = df['role_description'].apply(sentiment_score)
    df['theme_ai'] = df['role_description'].apply(contains_ai_theme)


    group_cols = ['date_utc', 'region_code', 'proj_type_code']
    agg_df = df.groupby(group_cols).agg(
        role_count_day=('role_type', 'count'),
        lead_share_pct_day=('is_lead', lambda x: round(100.0 * x.sum() / len(x), 1)),
        union_share_pct_day=('is_union', lambda x: round(100.0 * x.sum() / len(x), 1)),
        median_rate_day_usd=('rate_value', lambda x: int(round(np.median(x) / 25.0) * 25)),
        sentiment_avg_day=('sentiment', lambda x: round(x.mean() / 0.05) * 0.05),
        theme_ai_share_pct_day=('theme_ai', lambda x: round(100.0 * x.sum() / len(x), 1))
    ).reset_index()


    agg_df = agg_df[agg_df['role_count_day'] >= 5]
    agg_df['role_count_day'] = agg_df['role_count_day'].apply(lambda x: int(x + np.random.laplace(0, 1)))
    agg_df = agg_df.sort_values(['date_utc', 'region_code', 'proj_type_code'])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    agg_df.to_csv(output_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    build_pulse(args.input, args.output)
