import pandas as pd
import plotly.express as px
import folium
import webbrowser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "Data"
DOCS_DIR = PROJECT_ROOT / "Docs"
DOCS_DIR.mkdir(exist_ok=True)

# Load cleaned data from the analysis notebook
df = pd.read_csv(DATA_DIR / "cleaned_acled.csv")

df["event_date"] = pd.to_datetime(df["event_date"])
df = df[df["event_date"] >= "2019-01-01"]
df["fatalities"] = df["fatalities"].fillna(0)
df["month"] = pd.to_datetime(df["month"].astype(str)).dt.to_period("M")

coup_date = pd.to_datetime("2021-02-01")

if "period" not in df.columns:
    df["period"] = df["event_date"].apply(
        lambda x: "Before Coup" if x < coup_date else "After Coup"
    )

df["period"] = df["period"].replace({
    "pre_coup": "Before Coup",
    "post_coup": "After Coup"
})

df["event_type"] = df["event_type"].replace({
    "Explosions/Remote violence": "Explosions and Remote Attacks",
    "Explosions & Remote Attacks": "Explosions and Remote Attacks",
    "Violence against civilians": "Violence Against Civilians"
})

# Shared graph style
dark_layout = dict(
    template="plotly_dark",
    paper_bgcolor="#1e1e1e",
    plot_bgcolor="#1e1e1e",
    font=dict(family="Helvetica", color="white"),
    margin=dict(l=40, r=40, t=70, b=40)
)

time_axis = dict(
    showgrid=True,
    gridcolor="#333",
    tickformat="%Y",
    dtick="M12"
)

value_axis = dict(
    showgrid=True,
    gridcolor="#333"
)

# Graph 1: Monthly events
monthly_events = df.groupby("month").size().reset_index(name="Events")
monthly_events["month"] = monthly_events["month"].dt.to_timestamp()

fig_events = px.line(
    monthly_events,
    x="month",
    y="Events",
    title="Monthly Political Violence Events in Myanmar"
)

fig_events.update_traces(
    line=dict(color="#4cc9f0", width=3),
    hovertemplate="<b>%{x|%B %Y}</b><br>Events: %{y}<extra></extra>"
)

fig_events.add_shape(
    type="line",
    x0="2021-02-01",
    x1="2021-02-01",
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(color="white", dash="dash", width=2)
)

fig_events.add_annotation(
    x="2021-02-01",
    y=1,
    xref="x",
    yref="paper",
    text="Military Coup",
    showarrow=False,
    yshift=12,
    font=dict(color="white")
)

fig_events.update_layout(
    **dark_layout,
    xaxis=dict(title="Year (Hover for Month)", **time_axis),
    yaxis=dict(title="Number of Events", **value_axis)
)

# Graph 2: Monthly fatalities
monthly_fatalities = df.groupby("month")["fatalities"].sum().reset_index(name="Fatalities")
monthly_fatalities["month"] = monthly_fatalities["month"].dt.to_timestamp()

fig_fatalities = px.line(
    monthly_fatalities,
    x="month",
    y="Fatalities",
    title="Monthly Reported Fatalities in Myanmar",
    labels={
        "month": "Month",
        "Fatalities": "Number of Fatalities"
    }
)

fig_fatalities.update_traces(
    line=dict(color="#4cc9f0", width=3),
    hovertemplate="<b>%{x|%B %Y}</b><br>Fatalities: %{y}<extra></extra>"
)

fig_fatalities.add_shape(
    type="line",
    x0="2021-02-01",
    x1="2021-02-01",
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(color="white", dash="dash", width=2)
)

fig_fatalities.add_annotation(
    x="2021-02-01",
    y=1,
    xref="x",
    yref="paper",
    text="Military Coup",
    showarrow=False,
    yshift=12,
    font=dict(color="white")
)

fig_fatalities.add_vrect(
    x0="2021-02-01",
    x1=monthly_fatalities["month"].max(),
    fillcolor="#4cc9f0",
    opacity=0.08,
    layer="below",
    line_width=0
)

fig_fatalities.update_layout(
    **dark_layout,
    xaxis=dict(title="Month", **time_axis),
    yaxis=dict(title="Number of Fatalities", **value_axis)
)

# Graph 3: Event type comparison
event_types = df.groupby(["period", "event_type"]).size().reset_index(name="Events")

fig_event_types = px.bar(
    event_types,
    x="period",
    y="Events",
    color="event_type",
    barmode="group",
    title="Types of Political Violence Before and After the Coup",
    labels={
        "period": "",
        "event_type": "Type of Violence",
        "Events": "Number of Events"
    },
    color_discrete_sequence=["#4cc9f0", "#4895ef", "#4361ee"]
)

fig_event_types.update_traces(
    hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>"
)

fig_event_types.update_layout(
    **dark_layout,
    legend_title_text="Type of Violence",
    xaxis=dict(
        categoryorder="array",
        categoryarray=["Before Coup", "After Coup"]
    )
)

# Graph 4: Regions affected over time
regions_over_time = df.groupby("month")["admin1"].nunique().reset_index(name="Regions Affected")
regions_over_time["month"] = regions_over_time["month"].dt.to_timestamp()

fig_regions = px.line(
    regions_over_time,
    x="month",
    y="Regions Affected",
    title="Geographic Spread of Violence Over Time"
)

fig_regions.update_traces(
    line=dict(color="#4cc9f0", width=3),
    hovertemplate="<b>%{x|%B %Y}</b><br>Regions affected: %{y}<extra></extra>"
)

fig_regions.add_shape(
    type="line",
    x0="2021-02-01",
    x1="2021-02-01",
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(color="white", dash="dash", width=2)
)

fig_regions.add_annotation(
    x="2021-02-01",
    y=1,
    xref="x",
    yref="paper",
    text="Military Coup",
    showarrow=False,
    yshift=12,
    font=dict(color="white")
)

fig_regions.update_layout(
    **dark_layout,
    xaxis=dict(title="Month", **time_axis),
    yaxis=dict(title="Number of Regions Affected", **value_axis)
)

# Graph 5: Average fatalities per event
avg_fatalities = df.groupby("period")["fatalities"].mean().reset_index(name="Average Fatalities")

fig_avg = px.bar(
    avg_fatalities,
    x="period",
    y="Average Fatalities",
    title="Average Fatalities per Event Before and After the Coup",
    color="period",
    color_discrete_sequence=["#4895ef", "#4cc9f0"]
)

fig_avg.update_traces(
    hovertemplate="<b>%{x}</b><br>Average fatalities per event: %{y:.2f}<extra></extra>"
)

fig_avg.update_layout(
    **dark_layout,
    xaxis_title="",
    yaxis_title="Average Fatalities per Event",
    showlegend=False,
    xaxis=dict(
        categoryorder="array",
        categoryarray=["Before Coup", "After Coup"]
    )
)

# Embed Plotly graphs directly into the report HTML
graph_events = fig_events.to_html(full_html=False, include_plotlyjs='cdn')
graph_fatalities = fig_fatalities.to_html(full_html=False, include_plotlyjs=False)
graph_event_types = fig_event_types.to_html(full_html=False, include_plotlyjs=False)
graph_regions = fig_regions.to_html(full_html=False, include_plotlyjs=False)
graph_avg = fig_avg.to_html(full_html=False, include_plotlyjs=False)

# Folium map
m = folium.Map(
    location=[21.9, 96.0],
    zoom_start=5,
    tiles="CartoDB Voyager"
)

sample_df = df.sample(min(2000, len(df)), random_state=42)

for _, row in sample_df.iterrows():
    color = "#4cc9f0" if row["period"] == "Before Coup" else "#f72585"
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=2,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=f"{row['period']}<br>{row['event_type']}<br>Fatalities: {row['fatalities']}"
    ).add_to(m)

map_html = m._repr_html_()

# Final report HTML
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Myanmar Political Violence Report</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
html {{
    scroll-behavior: smooth;
}}

body {{
    background-color: #0f1115;
    color: #e6e6e6;
    font-family: 'Poppins', Helvetica, Arial, sans-serif;
    max-width: 1080px;
    margin: auto;
    padding: 28px 34px 55px 34px;
    line-height: 1.75;
}}

.topnav {{
    position: sticky;
    top: 14px;
    z-index: 999;
    background: rgba(15, 17, 21, 0.92);
    backdrop-filter: blur(10px);
    border: 1px solid #242832;
    border-radius: 999px;
    padding: 12px 16px;
    margin-bottom: 55px;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
}}

.topnav a {{
    color: #aeb4bd;
    text-decoration: none;
    font-size: 14px;
    padding: 6px 10px;
    border-radius: 999px;
}}

.topnav a:hover {{
    color: #fff;
    background-color: #1c2230;
}}

h1 {{
    font-size: 48px;
    color: #fff;
    margin-bottom: 60px;
    margin-top: 40px;
}}

h2 {{
    font-size: 30px;
    margin-top: 70px;
    margin-bottom: 30px;
    border-left: 4px solid #4cc9f0;
    padding-left: 12px;
    scroll-margin-top: 120px;
}}

.section {{
    scroll-margin-top: 120px;
}}

.chart {{
    margin: 30px 0;
    border-radius: 12px;
    overflow: hidden;
}}

.map-title {{
    color: #ffffff;
    font-size: 22px;
    font-weight: 600;
    margin: 36px 0 14px 0;
}}

.map-subtitle {{
    color: #aeb4bd;
    font-size: 14px;
    margin: 0 0 16px 0;
}}

#topBtn {{
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 99999;
    background-color: #4cc9f0;
    color: #0f1115;
    border: none;
    border-radius: 50%;
    width: 52px;
    height: 52px;
    font-size: 24px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 10px 25px rgba(0,0,0,0.45);
    display: none;
}}

#topBtn.show {{
    display: block;
}}

#topBtn:hover {{
    background-color: #ffffff;
}}

</style>
</head>

<body>

<nav class="topnav">
<a href="#intro">Intro</a>
<a href="#method">Data</a>
<a href="#intensity">Intensity</a>
<a href="#lethality">Lethality</a>
<a href="#types">Types</a>
<a href="#geo">Geography</a>
<a href="#severity">Severity</a>
<a href="#conclusion">Conclusion</a>
</nav>

<h1>From Protest to Civil War: Political Violence in Myanmar After the 2021 Coup</h1>

<div id="intro" class="section">
<h2>Introduction</h2>
<p>The Myanmar Civil War, triggered by military officers’ 2021 coup d’ètat, is an ongoing conflict involving over a hundred armed groups. The war erupted between the State Administration Council (SAC), and the National Unity Government (NUG), a pro-democracy government led by ousted civilian leaders (McKenna, 2025).</p>
<p>This analysis argues that the 2021 coup transformed Myanmar from a low intensity and geographically contained conflict environment into a sustained and nationwide civil war. The escalation after February 2021 reflects a structural shift in the scale, intensity, and character of political violence.</p>
<p>First, it makes a substantive claim that the coup altered Myanmar’s conflict dynamics by increasing a) the frequency of violence b) the intensifying its lethality c) the diversifying forms of violence, and c) its expanding geographic scope.</p>
<p>To satisfy the argument, disaggregated event level data, specifically as Armed Conflict Location and Event Data (ACLED), is essential for identifying these transformations. Aggregate data can describe instability, but event level data makes it possible to trace how violence changed across time, space, and type.</p>
<p>Using ACLED data from 2019 to 2025, the analysis compares patterns of violence before and after the coup across five dimensions:</p>
<p>
1. Event frequency<br>
2. Fatalities<br>
3. Types of violence<br>
4. Geographic spread<br>
5. Average fatalities per event.
</p>
<p>Together, these indicators show that Myanmar entered a qualitatively more severe conflict environment after February 2021. The next section will explore how the project utilized python to process, and visualize ACLED data.</p>
</div>

<div id="method" class="section">
<h2>Data</h2>
<p>The project utilizes python to process event-level conflict data. Specifically, ACLED data for Myanmar from 2019 to 2025 was exported and processed in python, where variables such as time period, monthly trends, and fatalities were constructed and cleaned (as seen in 01_data_cleaning.ipynb). The dataset was then structured to allow comparison between pre- and post-coup dynamics.</p>
<p>Python was used to aggregate the data across multiple dimensions, including event frequency, fatalities, event types, and geographic spread. These outputs were visualized using interactive graphs and maps, allowing patterns to be observed over time and across space (as seen in 02_analysis.ipynb).</p>
<p>AI tools were used selectively to support coding and formatting, particularly in generating visualizations and structuring the report interface.</p>
</div>

<div id="intensity" class="section">
<h2>Intensity</h2>
<p>The frequency of political violence increased sharply after the coup. Before February 2021, monthly event counts remained relatively low and stable, usually below 200 events per month, with only occasional spikes. This suggests a contained and episodic pattern of violence.</p>
<p>After the coup, this pattern changed dramatically. Monthly event counts rise quickly, exceeding 500 events by mid 2021 and later reaching peaks of roughly 900 to 1000 events per month. These elevated levels persisted through 2022, 2023, and 2024. The evidence points to a new baseline of conflict rather than a temporary surge.</p>
<p>The intensity mirrors the rhythm of conflict. Before the coup, violence appeared  regionally bounded (see Geography section). After the coup, violence became continuous. The increase in event frequency suggests that both state and non state actors were repeatedly engaged in organized confrontation.</p>
<p>The coup functioned as a critical juncture, lowering the barriers to sustained violence and creating incentives for armed mobilization. The timing of the increase strengthens the claim of a structural change, and breakage. The shift appears abrupt, sustained, and closely tied to the political shock of February 2021.</p>
{graph_events}
</div>

<div id="lethality" class="section">
<h2>Lethality</h2>
<p>The fatality trend reinforces the argument that Myanmar’s conflict environment changed after the coup. Before February 2021, monthly fatalities were generally low, often far below 500 deaths per month, reflecting a conflict setting where violence existed but rarely produced large scale death totals.</p>
<p>After the coup, fatalities rose sharply. Monthly totals move into the thousands, with several peaks exceeding 3000 fatalities. Although the trend fluctuates, the post coup baseline remains far higher than the pre coup period. This shows that violence became more deadly as well as more frequent.</p>
<p>The simultaneous rise in events and fatalities is analytically important. Event frequency alone could reflect more unrest. Fatality increases show a deeper escalation in coercive force. The data point to a conflict environment involving heavier weaponry, more coordinated operations, and greater willingness by actors to inflict lethal harm.</p>
<p>This section strengthens the substantive argument. Myanmar’s post coup conflict was not only larger in scale. It became more destructive. It also strengthens the methodological argument because multiple indicators move in the same direction. Frequency and fatalities together provide stronger evidence of transformation than either measure alone.</p>
{graph_fatalities}
</div>

<div id="types" class="section">
<h2>Types</h2>
<p>The composition of violence also shifts after the coup. Before 2021, violent events were more limited in scale and diversity. After the coup, all major forms of violence increase, but the pattern is uneven.</p>
<p>Explosions and remote attacks show especially strong growth. This suggests a move toward more militarized and technologically mediated violence, including airstrikes, artillery, and explosive devices. These forms of violence require different capacities from ordinary street level confrontation. Their rise indicates a conflict environment shaped by heavier weapons and more strategic targeting.</p>
<p>Battles also increase substantially, pointing to sustained armed confrontation between organized actors. This reflects the growth of resistance forces capable of engaging state forces directly. At the same time, violence against civilians rises in absolute terms, showing that non combatants become increasingly exposed to the conflict. This points to repression, punishment, and territorial control as part of the post coup conflict dynamic.</p>
<p>The key point is that Myanmar’s violence becomes more complex. The growth of battles suggests organized military confrontation. The rise of remote attacks suggests escalation in tactics. The increase in violence against civilians reveals the human cost of that escalation. Disaggregating event types is therefore crucial. Total event counts show that violence increased, but event categories show how the conflict changed.</p>
{graph_event_types}
</div>

<div id="geo" class="section">
<h2>Geography</h2>
<p>The spatial distribution of violence provides another layer of evidence. Before the coup, violence was concentrated in specific regions, particularly long standing border conflict zones. These areas had established armed actors and historical patterns of conflict. Central Myanmar was comparatively less affected.</p>
<p>After February 2021, the number of affected administrative regions increases steadily. Violence spreads beyond traditional hotspots into central areas of the country. The conflict becomes geographically diffuse, affecting multiple regions at the same time.</p>
<p>This expansion reflects a breakdown in territorial containment. As opposition to the military regime intensified, resistance movements emerged across different parts of the country. The state’s response also expanded into these areas, creating new sites of confrontation. The result is a conflict that spreads through interaction between state repression and local resistance.</p>
<p>The map supports this argument visually. Before coup events appear more clustered. After coup events are distributed across a much wider area. The regional spread graph reinforces the same pattern by showing a broader number of affected administrative regions over time.</p>
<p>Geographic diffusion matters because a localized conflict can sometimes be contained. A nationwide conflict places heavier strain on state capacity and creates more durable instability. Methodologically, measuring affected regions captures the breadth of conflict rather than only its intensity.</p>
{graph_regions}
<div class="map-title">Spatial Distribution of Political Violence Events</div>
<p class="map-subtitle">Blue markers show events before the coup; pink markers show events after the coup.</p>
{map_html}
</div>

<div id="severity" class="section">
<h2>Severity</h2>
<p>Average fatalities per event provide a final measure of severity. Total fatalities show the overall human cost of conflict, but they do not reveal whether individual incidents became more deadly. Average fatalities per event helps isolate that question.</p>
<p>Before the coup, average fatalities per event remained relatively low. This fits a conflict environment marked by smaller scale incidents and localized clashes. After February 2021, the average increases, indicating that individual events became more lethal.</p>
<p>This finding matters because it separates two sources of escalation. Fatalities can rise because there are more events, or because each event is deadlier. In Myanmar’s case, both dynamics appear to be present. There are more incidents, and those incidents produce more deaths on average.</p>
<p>The increase in average fatalities also connects to the earlier findings on event types. The rise in battles and explosions provides a plausible mechanism for greater lethality per incident. More destructive tactics create higher casualty counts. This reinforces the larger argument that the post coup period represents a qualitative transformation in violence, not only a quantitative increase.</p>
{graph_avg}
</div>

<div id="conclusion" class="section">
<h2>Conclusion</h2>
<p>This essay has argued that the 2021 military coup in Myanmar represents a structural break in the country’s conflict dynamics. Substantively, the coup transformed political violence from a localized and low intensity pattern into a sustained nationwide civil war. Methodologically, the analysis shows that disaggregated event level data is necessary to trace how that transformation unfolded across time, space, and type.</p>
<p>The evidence is consistent across all indicators. Event frequency rises sharply and remains elevated. Fatalities increase to far higher levels, indicating greater lethality. The composition of violence shifts toward battles, explosions, and remote attacks, alongside increased violence against civilians. At the same time, conflict spreads geographically beyond traditional border regions into central Myanmar. Average fatalities per event also rise, suggesting that individual incidents became more destructive.</p>
<p>Taken together, these patterns show that the coup reorganized the structure of political violence in Myanmar. The conflict becomes persistent, geographically diffuse, and more lethal, reflecting a shift toward sustained armed confrontation involving multiple actors and more complex forms of violence.</p>
<p>There are, however, limitations. ACLED data relies on reported events, so coverage may vary across regions and time. Some areas may be underreported, and fatality figures are estimates. Event classification can also depend on available sources.</p>
<p>Despite this, the overall pattern remains clear. The alignment across multiple indicators supports the argument that Myanmar’s conflict underwent a genuine transformation. The coup did not simply increase instability. It produced a more sustained, widespread, and lethal form of violence.</p>
</div>

<div class="section" id="references">
<h2>References</h2>

<p>
Armed Conflict Location and Event Data (ACLED). (2025). <i>Exported Data from ACLED</i>.
</p>

<p>
Chen, H. & The University of Hong Kong. (2025). <i>Lectures in POLI3148</i>.
</p>

<p>
McKenna, A. (2022, July 12). 2021 Myanmar coup d'état. <i>Encyclopedia Britannica</i>.
<br>
https://www.britannica.com/event/2021-Myanmar-coup-d-etat
</p>

</div>

<button onclick="scrollToTop()" id="topBtn">↑</button>

<script>

const topBtn = document.getElementById('topBtn');

window.addEventListener('scroll', () => {{
    if (window.scrollY > 300) {{
        topBtn.classList.add('show');
    }} else {{
        topBtn.classList.remove('show');
    }}
}});

function scrollToTop() {{
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

</script>

</body>
</html>
"""

# Save the HTML report
report_path = DOCS_DIR / "index.html"

with open(report_path, "w", encoding="utf-8") as f:
    f.write(html_content)

webbrowser.open(report_path.resolve().as_uri())
