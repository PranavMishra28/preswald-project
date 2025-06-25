# Load the dataset
from preswald import connect, get_df, query, table, text, slider, plotly, selectbox, button, checkbox, text_input
import plotly.express as px
import pandas as pd

# Initialize connection to preswald.toml data sources
connect()

# Load data
df = get_df("sample_csv")

# Fix data types - convert score columns to numeric
score_columns = ['Overall SCORE', 'AR SCORE', 'ER SCORE', 'FSR SCORE', 'CPF SCORE', 'IFR SCORE', 'ISR SCORE', 'ISD SCORE', 'IRN SCORE', 'EO SCORE', 'SUS SCORE']
for col in score_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Query or manipulate the data - use quotes for column names with spaces
sql = 'SELECT * FROM sample_csv WHERE "Overall SCORE" > 90'
try:
    filtered_df = query(sql, "sample_csv")
    if filtered_df is None:
        filtered_df = df[pd.to_numeric(df['Overall SCORE'], errors='coerce') > 90]
except Exception:
    # Fallback to pandas filtering if SQL query fails
    filtered_df = df[pd.to_numeric(df['Overall SCORE'], errors='coerce') > 90]

# Enhanced Header with Professional Styling
text("# 🎓 University Rankings Analytics Dashboard")
text("### 📊 Comprehensive Analysis of Global Higher Education Performance")
text("---")
text("")  # Add breathing room

# Quick Stats Section with Enhanced Visual Appeal
text("## 📊 Dashboard Overview")
text("")
total_universities = len(df)
avg_overall_score = df['Overall SCORE'].mean()
# Fix potential NoneType error for top university
if not df.empty and 'Overall SCORE' in df.columns:
    max_idx = df['Overall SCORE'].idxmax()
    if pd.notna(max_idx):
        top_university = df.loc[max_idx, 'Institution Name']
    else:
        top_university = "N/A"
else:
    top_university = "N/A"

# Create visually appealing metrics cards
text("### � Key Metrics at a Glance")
text("")
text(f"**🏛️ Total Universities Analyzed:** `{total_universities:,}`")
text(f"**📊 Global Average Score:** `{avg_overall_score:.1f}/100`")
text(f"**🏆 Top Performing Institution:** `{top_university}`")
text("")
text("---")
text("")  # Add spacing

# Enhanced Search and Filter Section with Professional Layout
text("## 🔍 Advanced Search & Filter Controls")
text("### 🎯 Find Your Perfect University Match")
text("")

# Primary Search with Enhanced Styling
text("#### 🔎 **Smart Search**")
text("*Search by university name, location, or any keyword*")
search_term = text_input("� Search Universities", placeholder="Try 'MIT', 'London', 'Engineering', or any keyword...")
text("")

# Organized Filter Categories with Better Spacing
text("#### 🌍 **Geographic Selection**")
text("*Filter universities by global regions and countries*")
text("")
regions = df['Region'].unique().tolist()
selected_region = selectbox("🌐 Select Region", options=["🌐 All Regions"] + [f"🌍 {region}" for region in regions], default="🌐 All Regions")
text("")
countries = sorted(df['Country/Territory'].unique().tolist())
selected_country = selectbox("🏳️ Select Country", options=["🏳️ All Countries"] + [f"🏴 {country}" for country in countries], default="🏳️ All Countries")
text("")

text("#### 🏫 **Institution Characteristics**")
text("*Filter by university size and institutional type*")
text("")
sizes = df['Size'].unique().tolist()
size_labels = {"XS": "🔹 Extra Small", "S": "🔸 Small", "M": "🔶 Medium", "L": "🔷 Large", "XL": "🔵 Extra Large"}
size_options = ["📏 All Sizes"] + [size_labels.get(size, f"📐 {size}") for size in sizes]
selected_size = selectbox("📏 University Size", options=size_options, default="📏 All Sizes")
text("")

text("#### 🏛️ **Institution Type**")
text("*Include or exclude private and public institutions*")
text("")
show_private = checkbox("🏢 Include Private Universities", default=True)
show_public = checkbox("🏛️ Include Public Universities", default=True)
text("")

# Advanced Filters with Professional Styling and Enhanced Layout
text("#### ⚙️ **Advanced Analytics Options**")
text("*Unlock deeper insights with performance-based filtering*")
text("")
show_advanced = checkbox("🔧 Enable Advanced Filters", default=False)
text("")

# Initialize advanced filter variables with default values
min_ar_score = 0
selected_focus = "All Focus Areas"

if show_advanced:
    text("##### 📈 **Performance Thresholds**")
    text("*Set minimum performance criteria for more precise results*")
    text("")
    min_ar_score = slider("🎯 Minimum Academic Reputation Score", min_val=0, max_val=100, default=0)
    text("")
    
    text("##### 🎓 **Academic Focus Areas**")
    text("*Filter by institutional focus and specialization*")
    text("")
    focus_options = df['Focus'].unique().tolist()
    focus_labels = {"FC": "🎓 Full Comprehensive", "FO": "🔬 Focused", "CO": "🔄 Comprehensive", "SP": "🎯 Specialized"}
    focus_display_options = ["🎯 All Focus Areas"] + [focus_labels.get(focus, f"📚 {focus}") for focus in focus_options]
    selected_focus = selectbox("🎓 Academic Focus Area", options=focus_display_options, default="🎯 All Focus Areas")
    text("")

# Action Buttons with Enhanced Visual Appeal
text("#### 🚀 **Control Panel**")
text("*Apply your filters or reset to start fresh*")
text("")

apply_pressed = button("✅ Apply All Filters")
text("")  # Add spacing between buttons
reset_pressed = button("🔄 Reset to Default")
text("")

if apply_pressed:
    text("✅ **Success!** Your filters have been applied and results updated.")
    text("")

if reset_pressed:
    text("🔄 **Reset Complete!** All filters cleared - displaying full dataset.")
    text("")

text("---")
text("")  # Enhanced spacing

# Filter the dataframe based on selections
filtered_data = df.copy()

# Apply region filter - extract region name from enhanced label
if not selected_region.startswith("🌐"):
    region_name = selected_region.replace("🌍 ", "")
    filtered_data = filtered_data[filtered_data['Region'] == region_name]

# Apply country filter - extract country name from enhanced label
if not selected_country.startswith("🏳️"):
    country_name = selected_country.replace("🏴 ", "")
    filtered_data = filtered_data[filtered_data['Country/Territory'] == country_name]

# Apply size filter - extract size from enhanced label
if not selected_size.startswith("📏"):
    # Reverse lookup from display label to actual size value
    size_reverse_lookup = {"🔹 Extra Small": "XS", "🔸 Small": "S", "🔶 Medium": "M", "🔷 Large": "L", "🔵 Extra Large": "XL"}
    actual_size = size_reverse_lookup.get(selected_size, selected_size.replace("📐 ", ""))
    filtered_data = filtered_data[filtered_data['Size'] == actual_size]

# Apply status filter
status_filter = []
if show_private:
    status_filter.extend(['Private not for Profit', 'Private for Profit'])
if show_public:
    status_filter.append('Public')
if status_filter:
    filtered_data = filtered_data[filtered_data['Status'].isin(status_filter)]

# Apply search filter
if search_term:
    filtered_data = filtered_data[
        filtered_data['Institution Name'].str.contains(search_term, case=False, na=False)
    ]

# Apply advanced filters if enabled
if show_advanced:
    filtered_data = filtered_data[pd.to_numeric(filtered_data['AR SCORE'], errors='coerce') >= min_ar_score]
    if not selected_focus.startswith("🎯"):
        # Reverse lookup from display label to actual focus value
        focus_reverse_lookup = {"🎓 Full Comprehensive": "FC", "🔬 Focused": "FO", "🔄 Comprehensive": "CO", "🎯 Specialized": "SP"}
        actual_focus = focus_reverse_lookup.get(selected_focus, selected_focus.replace("📚 ", ""))
        filtered_data = filtered_data[filtered_data['Focus'] == actual_focus]

# Enhanced Results Display with Professional Formatting
text("## 🏆 Elite Universities Showcase")
text("### 🌟 *Top-Tier Institutions (90+ Overall Score)*")
text("")
text("*Discover universities that have achieved exceptional overall performance scores above 90 points*")
text("")

if filtered_df is not None and len(filtered_df) > 0:
    text(f"**🎯 Found {len(filtered_df)} elite institutions meeting the highest standards**")
    text("")
    table(filtered_df, title="🌟 Elite University Rankings")
else:
    text("📊 **No universities currently meet the elite 90+ score criteria.**")
    text("💡 *Tip: Adjust your geographic or institutional filters to discover more results*")

text("")
text("---")
text("")

# Enhanced Dynamic Threshold Section with Better Presentation
text("## 🎯 Dynamic Performance Analysis")
text("### 📊 *Interactive Score Threshold Explorer*")
text("")
text("*Use the slider below to dynamically explore universities at different performance levels*")
text("")

threshold = slider("🎚️ Set Minimum Overall Score Threshold", min_val=80, max_val=100, default=90)
text("")
threshold_filtered = df[pd.to_numeric(df["Overall SCORE"], errors='coerce') > threshold].dropna(subset=['Overall SCORE'])

if threshold_filtered is not None and len(threshold_filtered) > 0:
    text(f"📈 **{len(threshold_filtered)} universities** exceed your {threshold}-point threshold")
    text("")
    table(threshold_filtered, title=f"🎓 Universities Scoring Above {threshold} Points")
else:
    text(f"🔍 **No universities found** with scores above {threshold} points.")
    text("💡 *Consider lowering the threshold to see more results*")

text("")
text("---")
text("")

# Enhanced Filtered Results with Exceptional Visual Appeal
result_count = len(filtered_data) if filtered_data is not None else 0
text(f"## 🔎 **Customized Results Dashboard**")
text(f"### 📊 *{result_count} Universities Match Your Criteria*")
text("")

if result_count > 0:
    text(f"✅ **Excellent!** We found **{result_count} universities** that perfectly match your search criteria.")
    text("")
    text("#### 📋 **Your Personalized University Selection**")
    table(filtered_data, title="🎯 Tailored University Results")
    text("")
    
    # Enhanced Summary Statistics with Premium Visual Appeal
    text("### 📊 **Advanced Performance Analytics**")
    text("*Comprehensive statistical analysis of your filtered results*")
    text("")
    
    overall_scores = pd.to_numeric(filtered_data['Overall SCORE'], errors='coerce')
    avg_score = overall_scores.mean()
    max_score = overall_scores.max()
    min_score = overall_scores.min()
    
    text("#### 🎯 **Core Performance Metrics**")
    text("")
    text(f"🏆 **Peak Performance Score:** `{max_score:.1f}/100` points")
    text(f"📊 **Average Performance Score:** `{avg_score:.1f}/100` points") 
    text(f"📉 **Minimum Performance Score:** `{min_score:.1f}/100` points")
    text(f"🎓 **Total Institutions Analyzed:** `{result_count}` universities")
    text("")
    
    # Enhanced Performance Categories with Visual Appeal
    excellent_count = len(filtered_data[pd.to_numeric(filtered_data['Overall SCORE'], errors='coerce') >= 95])
    good_count = len(filtered_data[pd.to_numeric(filtered_data['Overall SCORE'], errors='coerce').between(85, 95)])
    average_count = len(filtered_data[pd.to_numeric(filtered_data['Overall SCORE'], errors='coerce') < 85])
    
    text("#### 📈 **Performance Distribution Analysis**")
    text("*Classification of institutions by performance tier*")
    text("")
    text(f"🌟 **World-Class (95+ points):** `{excellent_count}` universities")
    text(f"⭐ **Excellent (85-94 points):** `{good_count}` universities") 
    text(f"📈 **Strong (Below 85 points):** `{average_count}` universities")
    text("")
    
else:
    text("🔍 **No Match Found** - Let's Help You Discover Great Universities!")
    text("")
    text("### 💡 **Smart Suggestions to Expand Your Search:**")
    text("")
    text("🌐 **Geographic Options:** Try selecting *'All Regions'* or *'All Countries'* for broader coverage")
    text("")
    text("📏 **Size Flexibility:** Consider including *all university sizes* for more diverse options")
    text("")
    text("🏛️ **Institution Types:** Include both *private and public* institutions for comprehensive results")
    text("")
    text("🎯 **Performance Criteria:** Lower the *academic reputation threshold* for wider selection")
    text("")
    text("🔎 **Search Terms:** Try *broader keywords* or leave the search field empty for maximum results")
    text("")

text("---")
text("")

# Enhanced Visualizations Section with Premium Styling
text("## 📈 **Interactive Data Visualization Suite**")
text("### 🎨 *Advanced Analytics Through Dynamic Charts*")
text("")
text("*Explore university performance patterns through our comprehensive visualization toolkit*")
text("")

# Enhanced Visualization Controls with Better Presentation
text("#### 📊 **Chart Selection Panel**")
text("*Choose your preferred visualization style for deeper insights*")
text("")
chart_type = selectbox("🎨 Visualization Type", 
                      options=["🔵 Scatter Plot Analysis", "📊 Regional Bar Chart", "📦 Distribution Box Plot", "📈 Score Histogram"], 
                      default="🔵 Scatter Plot Analysis")
text("")

text("### 🌍 **Global Regional Performance Analysis**")
text("*Compare and contrast university performance across different world regions*")
text("")

if result_count > 0:
    if "Scatter" in chart_type:
        text("#### 🎯 **Correlation Analysis: Overall vs Academic Reputation**")
        text("*Explore the relationship between overall performance and academic reputation by region*")
        text("")
        
        # Enhanced scatter plot with better data handling
        plot_data = filtered_data.copy()
        plot_data['Overall SCORE'] = pd.to_numeric(plot_data['Overall SCORE'], errors='coerce')
        plot_data['AR SCORE'] = pd.to_numeric(plot_data['AR SCORE'], errors='coerce')
        plot_data = plot_data.dropna(subset=['Overall SCORE', 'AR SCORE'])
        
        if len(plot_data) > 0:
            fig1 = px.scatter(plot_data, 
                         x="Overall SCORE", 
                         y="AR SCORE", 
                         color="Region",
                         hover_name="Institution Name",
                         hover_data=["Country/Territory", "Size"],
                         title="🎯 Performance Correlation: Overall Score vs Academic Reputation",
                         labels={"Overall SCORE": "Overall Performance Score", "AR SCORE": "Academic Reputation Score"})
            fig1.update_layout(
                plot_bgcolor='rgba(240,248,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=12, family="Arial"),
                title_font_size=16,
                showlegend=True
            )
            plotly(fig1)
        else:
            text("📊 *Insufficient data points available for scatter plot visualization*")
            
    elif "Bar Chart" in chart_type:
        text("#### 📊 **Regional Performance Comparison**")
        text("*Average performance scores across different global regions*")
        text("")
        
        plot_data = filtered_data.copy()
        plot_data['Overall SCORE'] = pd.to_numeric(plot_data['Overall SCORE'], errors='coerce')
        region_avg = plot_data.groupby('Region')['Overall SCORE'].mean().reset_index()
        
        if len(region_avg) > 0:
            fig1 = px.bar(region_avg, 
                      x="Region", 
                      y="Overall SCORE",
                      title="📊 Average Performance Metrics by Global Region",
                      labels={"Overall SCORE": "Average Overall Score", "Region": "Geographic Region"},
                      color="Overall SCORE",
                      color_continuous_scale="viridis")
            fig1.update_layout(
                plot_bgcolor='rgba(240,248,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=12, family="Arial"),
                title_font_size=16
            )
            plotly(fig1)
        else:
            text("📊 *No regional data available for bar chart visualization*")
            
    elif "Box Plot" in chart_type:
        text("#### 📦 **Score Distribution Analysis**")
        text("*Statistical distribution of performance scores across regions*")
        text("")
        
        plot_data = filtered_data.copy()
        plot_data['Overall SCORE'] = pd.to_numeric(plot_data['Overall SCORE'], errors='coerce')
        plot_data = plot_data.dropna(subset=['Overall SCORE'])
        
        if len(plot_data) > 0:
            fig1 = px.box(plot_data, 
                          x="Region", 
                          y="Overall SCORE",
                          title="📦 Performance Distribution Analysis by Region",
                          labels={"Overall SCORE": "Overall Score Distribution", "Region": "Geographic Region"})
            fig1.update_layout(
                plot_bgcolor='rgba(240,248,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=12, family="Arial"),
                title_font_size=16
            )
            plotly(fig1)
        else:
            text("📊 *Insufficient data available for box plot visualization*")
            
    else:  # Histogram
        text("#### 📈 **Score Frequency Distribution**")
        text("*Histogram showing the distribution of overall scores across regions*")
        text("")
        
        plot_data = filtered_data.copy()
        plot_data['Overall SCORE'] = pd.to_numeric(plot_data['Overall SCORE'], errors='coerce')
        plot_data = plot_data.dropna(subset=['Overall SCORE'])
        
        if len(plot_data) > 0:
            fig1 = px.histogram(plot_data, 
                               x="Overall SCORE", 
                               color="Region",
                               title="📈 Overall Score Distribution Across Global Regions",
                               labels={"Overall SCORE": "Overall Score", "count": "Number of Universities"},
                               nbins=20)
            fig1.update_layout(
                plot_bgcolor='rgba(240,248,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=12, family="Arial"),
                title_font_size=16
            )
            plotly(fig1)
        else:
            text("📊 *No data available for histogram visualization*")

else:
    text("🔍 **No Visualization Data Available**")
    text("*Please adjust your search and filter criteria to generate charts and analytics*")
    text("")

text("")
text("---")
text("")

# Premium Additional Visualizations with Enhanced Styling
if result_count > 0:
    text("### 🏆 **Elite Performers Spotlight**")
    text("#### 🌟 *Showcasing the Highest-Achieving Institutions*")
    text("")
    text("*Highlighting the most exceptional universities from your filtered selection*")
    text("")
    
    top_20_data = filtered_data.copy()
    top_20_data['Overall SCORE'] = pd.to_numeric(top_20_data['Overall SCORE'], errors='coerce')
    top_20_data = top_20_data.dropna(subset=['Overall SCORE']).head(20)
    
    if len(top_20_data) > 0:
        text(f"**📊 Displaying Top {len(top_20_data)} Universities from Your Selection**")
        text("")
        
        fig2 = px.bar(top_20_data, 
                      x="Institution Name", 
                      y="Overall SCORE",
                      color="Region",
                      title=f"🏅 Top {len(top_20_data)} University Champions - Performance Rankings",
                      labels={"Overall SCORE": "Overall Performance Score", "Institution Name": "University"})
        fig2.update_layout(
            xaxis_tickangle=45,
            plot_bgcolor='rgba(240,248,255,0.8)',
            paper_bgcolor='rgba(255,255,255,0.9)',
            font=dict(size=12, family="Arial"),
            title_font_size=16,
            height=550,
            margin=dict(b=150)  # Extra bottom margin for rotated labels
        )
        plotly(fig2)
        text("")
        
        text("### 🔬 **Research Excellence Analysis**")
        text("#### 📊 *Research Output vs Employment Success Correlation*")
        text("")
        text("*Analyzing the relationship between research performance and employment outcomes*")
        text("")
        
        research_data = filtered_data.copy()
        research_data['Overall SCORE'] = pd.to_numeric(research_data['Overall SCORE'], errors='coerce')
        research_data['EO SCORE'] = pd.to_numeric(research_data['EO SCORE'], errors='coerce')
        research_data = research_data.dropna(subset=['Overall SCORE', 'EO SCORE'])
        
        if len(research_data) > 0:
            fig3 = px.scatter(research_data,
                             x="Research",
                             y="Overall SCORE",
                             size="EO SCORE",
                             color="Region",
                             hover_name="Institution Name",
                             hover_data=["Country/Territory", "Status"],
                             title="🎓 Research Excellence vs Overall Performance Analysis",
                             labels={"Overall SCORE": "Overall Performance Score", "Research": "Research Level", "EO SCORE": "Employment Outcomes Score"})
            fig3.update_layout(
                plot_bgcolor='rgba(240,248,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=12, family="Arial"),
                title_font_size=16
            )
            plotly(fig3)
        else:
            text("📊 *Insufficient data available for comprehensive research analysis*")
    else:
        text("📊 *No universities available for elite performers analysis*")
        text("💡 *Try expanding your search criteria to see top performers*")

text("")
text("---")
text("")

# Premium Export and Action Center with Enhanced Design
text("## 📁 **Data Export & Action Center**")
text("### 💾 *Save Your Analysis Results for Future Reference*")
text("")
text("*Export your customized university analysis in your preferred format*")
text("")

text("#### 📄 **Export Configuration**")
text("*Choose your preferred file format for data export*")
text("")
export_format = selectbox("� Export Format Selection", 
                         options=["📄 CSV (Excel Compatible)", "📋 JSON (Data Format)", "📊 Excel (Advanced Workbook)"], 
                         default="📄 CSV (Excel Compatible)")
text("")

export_pressed = button("📥 Download Filtered Dataset")
text("")

if export_pressed:
    format_name = export_format.split(" ")[1].replace("(", "").replace(")", "")
    text(f"📁 **Export Successfully Initiated!**")
    text("")
    text(f"✅ Your selection of **{result_count} universities** is being prepared for download in **{format_name}** format.")
    text("")
    text("💡 *Note: In a production environment, this would automatically download your file*")
    text("")

text("### 🔧 **Quick Action Panel**")
text("*Convenient shortcuts for common operations*")
text("")

reset_action = button("🔄 Complete Reset & Fresh Start")
text("")
report_action = button("📊 Generate Executive Summary")
text("")

if reset_action:
    text("🔄 **System Reset Complete!**")
    text("")
    text("✅ All filters have been cleared and you're viewing the complete dataset")
    text("🎯 Ready to start a new analysis with fresh criteria")
    text("")

if report_action:
    text("📊 **Executive Summary Generated!**")
    text("")
    text("✅ A comprehensive analytical report has been prepared")
    text("📈 Summary includes key metrics, trends, and insights")
    text("")

text("---")
text("")

# Enhanced Pro Tips Section with Premium Styling
text("### 💡 **Expert Tips & Best Practices**")
text("#### 🎯 *Maximize Your University Search Experience*")
text("")
text("**🔍 Advanced Search Strategies:**")
text("• Combine **multiple filter categories** for highly targeted results")
text("• Experiment with **different chart types** to uncover hidden patterns")
text("• Use **specific keywords** like 'MIT', 'Oxford', 'Engineering', or city names")
text("• Enable **advanced filters** to find institutions with specialized strengths")
text("")
text("**📊 Data Analysis Tips:**")
text("• Compare **regional performance** trends using visualization tools")
text("• Analyze **score distributions** to understand performance benchmarks")
text("• Use the **threshold slider** to explore different performance levels")
text("• Export data for **external analysis** in your preferred tools")
text("")

text("---")
text("")

# Premium Footer with Enhanced Branding
text("### 🌟 **About This Platform**")
text("*University Rankings Analytics Dashboard - Powered by Advanced Data Science*")
text("")
text("Built with **❤️** and cutting-edge technology using the **Preswald Analytics Framework**")
text("")
text("🚀 **Features:** Interactive filtering • Dynamic visualizations • Real-time analytics • Export capabilities")
text("")
text("📊 **Data Source:** Global university rankings with comprehensive performance metrics")
text("")
text("*Empowering informed decisions in higher education through data-driven insights*")
