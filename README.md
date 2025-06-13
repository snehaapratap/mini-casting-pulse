
```markdown
# 🎬 Mini Casting Pulse

This project processes raw casting breakdown data and generates a **daily summary** (`daily_pulse.csv`) that helps spot trends in film, TV, commercial, and voiceover work—without exposing any individual actor data.

## 🏗️ File Structure

```

.
├── build\_pulse.py            # Script to build the daily summary
├── data/
│   └── breakdowns\_sample.csv # Raw casting breakdowns (provided)
├── output/
│   └── daily\_pulse.csv       # Final aggregated output
└── README.md                 # This file

````

## 🚀 Run the Project

```bash
python3 build_pulse.py \
  --input data/breakdowns_sample.csv \
  --output output/daily_pulse.csv
````

The script completes in <5 minutes and creates a clean daily trend summary using smart bucketing, aggregation, and light enrichment.

## 📊 Columns in `daily_pulse.csv`

| Column                   | Description                                                    |
| ------------------------ | -------------------------------------------------------------- |
| `date_utc`               | Posted date (UTC), truncated to YYYY-MM-DD                     |
| `region_code`            | Mapped region based on work\_location (e.g., LA, NY, TX, etc.) |
| `proj_type_code`         | Normalized project type: `F`, `T`, `C`, `V`, or `O`            |
| `role_count_day`         | Number of roles posted in the bucket                           |
| `lead_share_pct_day`     | % of Lead/Principal roles (rounded to 1 decimal)               |
| `union_share_pct_day`    | % of union roles (rounded to 1 decimal)                        |
| `median_rate_day_usd`    | Median day rate rounded to nearest \$25                        |
| `sentiment_avg_day`      | Sentiment of role descriptions (rounded to nearest 0.05)       |
| `theme_ai_share_pct_day` | % of roles mentioning "AI", "robot", or "android"              |

## 🧠 Design Choices

* ✅ Buckets with `< 5` roles were dropped to protect anonymity.
* ✅ Light Laplace noise (`np.random.laplace(0,1)`) was added to counts.
* ✅ Median rounding: `int(round(x / 25.0)) * 25`
* ✅ Grouped by `date_utc`, `region_code`, `proj_type_code`

## 🧪 Mappings and Model Used

* **Region Mapping**:

  * `"Los Angeles", "Hollywood", "Santa Monica"` → `LA`
  * `"New York", "Brooklyn", "Queens"` → `NY`
  * `"Atlanta"` → `GA`, `"Chicago"` → `CH`, `"Miami"` → `FL`
  * `"San Francisco"` → `SF`, `"Seattle"` → `NW`, `"Austin"` → `TX`
  * All others → `OTH`

* **Project Type Mapping**:

  * `Feature Film`, `Short Film`, `Film` → `F`
  * `Television`, `TV`, `Streaming`, `Series` → `T`
  * `Commercial`, `Ad` → `C`
  * `Voiceover`, `Animation`, `Podcast` → `V`
  * All others → `O`

* **Sentiment Library**:
  → [`TextBlob`](https://textblob.readthedocs.io/en/dev/) (lightweight, offline)

## 📁 Sample Output (head)

```csv
date_utc,region_code,proj_type_code,role_count_day,lead_share_pct_day,union_share_pct_day,median_rate_day_usd,sentiment_avg_day,theme_ai_share_pct_day
2023-10-12,LA,F,28,35.7,42.9,150,0.05,10.7
2023-10-12,NY,C,17,41.2,64.7,125,0.00,5.9
...
```

---

✅ Everything runs offline, is reproducible, and ensures privacy while enabling industry insights.

```
15-word note (for submission):
Mapped work_location to regions; project_type to F/T/C/V; used TextBlob for sentiment scoring.
```

---
