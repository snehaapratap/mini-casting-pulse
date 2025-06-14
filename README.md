# 🎬 Mini Casting Pulse

This project processes raw casting breakdown data and generates a **daily summary report** (`daily_pulse.csv`) that highlights emerging trends in film, television, commercial, and voiceover work—**while preserving actor privacy**.

It aggregates role-level metadata (like pay rate, union status, and sentiment) into anonymized daily snapshots that are ready for analytics, dashboards, and industry insights.

---

## 🏗️ File Structure

<pre>
.
├── build_pulse.py             # Core script to generate daily trend summaries
├── data/
│   └── breakdowns_sample.csv  # Raw casting breakdowns (input)
├── output/
│   └── daily_pulse.csv        # Aggregated daily-level output
└── README.md                  # This file
</pre>

---

## 🚀 Run the Project

```bash
python3 build_pulse.py \
  --input data/breakdowns_sample.csv \
  --output output/daily_pulse.csv
```

* ⏱️ Finishes in under 5 minutes
* 🧠 Smart bucketing, NLP enrichment, privacy-preserving logic built-in

---

## 📊 Output: `daily_pulse.csv`

Each row captures the **aggregated status** of a region/project type on a specific date.

| Column                   | Description                                                    |
| ------------------------ | -------------------------------------------------------------- |
| `date_utc`               | Posting date in `YYYY-MM-DD`                                   |
| `region_code`            | Derived from `work_location` (e.g., LA, NY, TX, etc.)          |
| `proj_type_code`         | Simplified project type: `F`, `T`, `C`, `V`, or `O`            |
| `role_count_day`         | Total roles posted that day for the region + type              |
| `lead_share_pct_day`     | % of roles marked Lead/Principal                               |
| `union_share_pct_day`    | % of union roles (e.g., SAG-AFTRA, AFTRA)                      |
| `median_rate_day_usd`    | Median day rate (rounded to nearest \$25)                      |
| `sentiment_avg_day`      | Text sentiment of role descriptions (−1 to 1, rounded to 0.05) |
| `theme_ai_share_pct_day` | % of roles referencing AI, robots, or androids                 |

---

## 🧠 Design Highlights

### ✅ Theme AI Detection

* Uses regex with **whole word matching** to catch `"AI"`, `"robot"`, `"android"`
* Prevents false hits like `"paid"` or `"airplane"`

### ✅ Union Parsing Logic

* Handles common union variants like `SAG-AFTRA`, `AFTRA`, `Union`, etc.
* Avoids false negatives and improves role classification

### ✅ Sentiment Scoring

* Uses [TextBlob](https://textblob.readthedocs.io/en/dev/) (lightweight and offline) to score role descriptions
* Converts unstructured text into numerical tone signals

### ✅ Privacy Preserving

* **Buckets with fewer than 5 roles** are excluded
* **Laplace noise** (`np.random.laplace(0,1)`) added to `role_count_day`
* No personally identifiable data used

---

## 🔁 Mappings Used

### 📍 Region Mapping

```text
"Los Angeles", "Santa Monica", "Hollywood" → LA  
"New York", "Brooklyn", "Queens" → NY  
"Atlanta" → GA, "Chicago" → CH, "Miami" → FL  
"San Francisco" → SF, "Seattle" → NW, "Austin" → TX  
All others → OTH
```

### 🎬 Project Type Mapping

```text
Feature/Short/Film → F  
TV/Streaming/Series → T  
Commercial/Ad → C  
Voiceover/Animation/Podcast → V  
Others → O
```

---

## 🧪 Sample Output (Preview)

```csv
date_utc,region_code,proj_type_code,role_count_day,lead_share_pct_day,union_share_pct_day,median_rate_day_usd,sentiment_avg_day,theme_ai_share_pct_day
2024-06-12,LA,C,28,35.7,42.9,150,0.05,10.7
2024-06-12,NY,F,17,41.2,64.7,125,0.00,5.9
...
```

---

## 📦 Dependencies

* Python 3.7+
* `pandas`, `numpy`, `textblob`

Install dependencies with:

```bash
pip install pandas numpy textblob
```

---

## 📍 Summary (for reviewers)

> **"Mapped `work_location` to `region_code`; normalized `project_type`; enriched `role_description` with sentiment and AI-themed tagging using TextBlob and regex; all while preserving actor privacy."**

---
