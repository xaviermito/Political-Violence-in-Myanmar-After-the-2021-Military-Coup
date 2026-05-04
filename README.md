### From Protest to Civil War

## Political Violence in Myanmar After the 2021 Military Coup

This project analyzes how political violence in Myanmar changed following the February 1, 2021 military coup. Using event level data from the Armed Conflict Location and Event Data Project (ACLED), the analysis examines changes in conflict intensity, lethality, composition, geographic spread, and severity.

The central argument is that the coup represents a structural break. Myanmar transitioned into a sustained and nationwide civil war, defined by persistent violence, higher lethality, and broader geographic diffusion.

---

## Project Structure

project_folder/
├── README.md
├── note_on_ai_use.md
├── data/
│   ├── ACLED Data.csv
│   └── cleaned_acled.csv
├── code/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_analysis.ipynb
│   └── generate_report.py
└── docs/
    ├── index.html

---

## Data

The dataset is sourced from ACLED and covers Myanmar from January 2019 to May 2025. It includes event level records containing information on date, location, actors, event type, and fatalities.

Filtering applied:
- Country: Myanmar
- Time range: 2018-12-01 to 2025-05-04
- Event types:
  - Battles
  - Explosions/Remote violence
  - Violence against civilians

---

## Methodology

The project uses Python to clean, structure, analyze, and visualize the dataset.

### Data Cleaning

The notebook `code/01_data_cleaning.ipynb`:
- Loads the raw ACLED dataset
- Converts event dates into datetime format
- Creates a period variable for before and after the coup
- Creates a monthly time variable
- Cleans fatality values
- Exports `cleaned_acled.csv`

### Analysis

The notebook `code/02_analysis.ipynb`:
- Aggregates events by month
- Calculates monthly fatalities
- Compares event types before and after the coup
- Examines geographic spread
- Calculates average fatalities per event
- Produces interactive visualizations

### Report Generation

The script `code/generate_report.py`:
- Loads the cleaned dataset
- Recreates the visualizations
- Embeds the graphs and map into an HTML report
- Outputs the final report as `docs/index.html`

---

## Key Findings

- Political violence increased sharply after the coup.
- Fatalities rose significantly after February 2021.
- Violence shifted toward battles, explosions, remote attacks, and violence against civilians.
- Conflict spread beyond traditional border regions into central Myanmar.
- Average fatalities per event increased, suggesting that individual incidents became more destructive.

---

## Interactive Report

The final report is located at:

docs/index.html

To open it locally:

open docs/index.html

For best rendering, use a local server:

python -m http.server 8000

Then open:

http://localhost:8000/docs/index.html

---

## Notes

- ACLED data depends on reported events, so some areas may be underreported.
- Fatality counts are estimates.
- The analysis focuses only on direct violence events.
- AI tools were used for coding support and visualization formatting, as detailed in `note_on_ai_use.md`.

---

## Author

Xavier Mito  
University of Hong Kong  
POLI3148