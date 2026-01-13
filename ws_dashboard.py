"""
World Systems Theory Dashboard
Visualizes core, semi-periphery, and periphery countries based on:
- GDP per capita
- Global Militarization Index (GMI)
- Global Diplomacy Index (GDI)

Uses a ranking-based methodology with equal weighting (1:1:1)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="World Systems Theory Dashboard",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .category-core {
        background-color: #2166ac;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .category-semi {
        background-color: #92c5de;
        color: black;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .category-periphery {
        background-color: #f4a582;
        color: black;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA SECTION
# ============================================

# ISO 3166-1 alpha-3 country codes for mapping
# Data compiled from World Bank (GDP per capita), BICC (GMI), and Lowy Institute (GDI)

@st.cache_data
def load_data():
    """Load and prepare country data with all three indices"""
    
    # Comprehensive dataset with all three metrics
    # GDP per capita (2023/2024 World Bank data, nominal USD)
    # GMI scores (2022 BICC data - higher = more militarized)
    # GDI scores (2024 Lowy Institute - number of diplomatic posts)
    
    data = {
        'country': [
            'Ukraine', 'Israel', 'Armenia', 'Qatar', 'Bahrain', 'Saudi Arabia', 'Greece', 
            'Singapore', 'Azerbaijan', 'Russia', 'South Korea', 'Cyprus', 'Kuwait', 'Lebanon',
            'Jordan', 'Brunei', 'Taiwan', 'Vietnam', 'Oman', 'Turkey', 'Finland', 'Lithuania',
            'Estonia', 'Algeria', 'Norway', 'Morocco', 'Egypt', 'United States', 'France',
            'Serbia', 'Croatia', 'Bulgaria', 'Chile', 'Poland', 'Australia', 'Portugal',
            'Pakistan', 'Netherlands', 'Czechia', 'North Macedonia', 'Slovakia', 'Latvia',
            'Romania', 'Sri Lanka', 'Thailand', 'Ecuador', 'Myanmar', 'United Kingdom',
            'Italy', 'Sweden', 'Germany', 'Switzerland', 'Denmark', 'Spain', 'China',
            'Hungary', 'Bolivia', 'Canada', 'Japan', 'Uruguay', 'India', 'Belgium', 
            'Brazil', 'Slovenia', 'New Zealand', 'Cambodia', 'Austria', 'Peru',
            'Indonesia', 'Malaysia', 'Colombia', 'South Africa', 'Argentina',
            'Philippines', 'Tunisia', 'Ireland', 'Nigeria', 'Kenya', 'Mexico', 'Ethiopia',
            'Bangladesh', 'Ghana', 'Uganda', 'Tanzania', 'Nepal', 'Madagascar', 'Mali',
            'Senegal', 'Mozambique', 'Zambia', 'Zimbabwe', 'Rwanda', 'Congo', 'Cameroon',
            'Ivory Coast', 'Angola', 'Paraguay', 'Guatemala', 'Honduras', 'Dominican Republic',
            'Costa Rica', 'Panama', 'Venezuela', 'Cuba', 'Jamaica', 'Trinidad and Tobago',
            'Iceland', 'Luxembourg', 'Malta', 'Mauritius', 'Namibia', 'Botswana', 'Mongolia'
        ],
        'iso_alpha': [
            'UKR', 'ISR', 'ARM', 'QAT', 'BHR', 'SAU', 'GRC', 'SGP', 'AZE', 'RUS',
            'KOR', 'CYP', 'KWT', 'LBN', 'JOR', 'BRN', 'TWN', 'VNM', 'OMN', 'TUR',
            'FIN', 'LTU', 'EST', 'DZA', 'NOR', 'MAR', 'EGY', 'USA', 'FRA', 'SRB',
            'HRV', 'BGR', 'CHL', 'POL', 'AUS', 'PRT', 'PAK', 'NLD', 'CZE', 'MKD',
            'SVK', 'LVA', 'ROU', 'LKA', 'THA', 'ECU', 'MMR', 'GBR', 'ITA', 'SWE',
            'DEU', 'CHE', 'DNK', 'ESP', 'CHN', 'HUN', 'BOL', 'CAN', 'JPN', 'URY',
            'IND', 'BEL', 'BRA', 'SVN', 'NZL', 'KHM', 'AUT', 'PER', 'IDN', 'MYS',
            'COL', 'ZAF', 'ARG', 'PHL', 'TUN', 'IRL', 'NGA', 'KEN', 'MEX', 'ETH',
            'BGD', 'GHA', 'UGA', 'TZA', 'NPL', 'MDG', 'MLI', 'SEN', 'MOZ', 'ZMB',
            'ZWE', 'RWA', 'COG', 'CMR', 'CIV', 'AGO', 'PRY', 'GTM', 'HND', 'DOM',
            'CRI', 'PAN', 'VEN', 'CUB', 'JAM', 'TTO', 'ISL', 'LUX', 'MLT', 'MUS',
            'NAM', 'BWA', 'MNG'
        ],
        # GDP per capita (nominal USD, 2023/2024 estimates)
        'gdp_per_capita': [
            5181, 54930, 7918, 87661, 32205, 32586, 22340, 84734, 7762, 14403,
            33393, 32807, 38124, 4136, 4946, 37166, 33907, 4316, 23223, 13110,
            53983, 25064, 28247, 5188, 87925, 3795, 4295, 80412, 44408, 9538,
            20785, 13899, 16550, 22162, 64674, 26512, 1568, 57025, 30031, 6939,
            22525, 22264, 17647, 3354, 7066, 6323, 1173, 48913, 37146, 58532,
            54291, 99994, 68037, 33090, 12614, 21909, 3600, 54866, 33950, 22948,
            2731, 51767, 10413, 29533, 48826, 1758, 56802, 7769, 4919, 12570,
            7291, 6190, 13694, 3498, 4376, 106210, 2184, 2099, 13245, 1020,
            2688, 2445, 964, 1206, 1456, 519, 833, 1712, 539, 1430,
            1773, 2085, 2280, 1694, 2579, 3352, 5892, 5475, 3136, 10121,
            13198, 18798, 3897, 9500, 6047, 21037, 75180, 128259, 34127, 12297,
            4907, 7738, 5228
        ],
        # GMI Score (2022 BICC data - higher means more militarized)
        # Note: For ranking purposes, higher GMI = more "core-like" in military dimension
        'gmi_score': [
            335, 257, 223, 220, 215, 213, 211, 210, 204, 204,
            204, 204, 203, 200, 192, 190, 182, 178, 174, 168,
            162, 160, 160, 156, 154, 152, 149, 147, 144, 143,
            141, 139, 139, 138, 137, 137, 137, 137, 136, 135,
            135, 134, 131, 130, 128, 127, 127, 123, 123, 122,
            121, 118, 118, 118, 117, 116, 114, 114, 114, 112,
            111, 111, 110, 110, 109, 109, 109, 107, 106, 106,
            106, 103, 102, 102, 101, 101, 100, 100, 99, 98,
            96, 96, 94, 93, 92, 91, 91, 91, 90, 90,
            88, 87, 87, 87, 86, 86, 85, 85, 84, 83,
            81, 80, 80, 78, 74, 73, 73, 73, 72, 70,
            70, 69, 68
        ],
        # GDI Score (2024 Lowy Institute - number of diplomatic posts)
        # Higher = more diplomatic reach = more "core-like"
        'gdi_score': [
            75, 107, 45, 70, 45, 128, 134, 65, 55, 230,
            187, 45, 60, 50, 55, 40, 110, 94, 55, 252,
            90, 50, 45, 75, 91, 70, 85, 271, 249, 55,
            60, 55, 121, 135, 124, 127, 121, 149, 120, 40,
            70, 50, 65, 45, 97, 55, 35, 225, 206, 102,
            217, 141, 90, 190, 274, 65, 45, 157, 251, 55,
            194, 113, 205, 50, 65, 40, 104, 75, 130, 106,
            117, 114, 150, 94, 50, 98, 80, 55, 161, 55,
            80, 45, 40, 45, 45, 35, 40, 55, 40, 45,
            40, 40, 40, 45, 45, 50, 45, 45, 40, 50,
            55, 60, 55, 60, 45, 40, 35, 45, 35, 40,
            35, 35, 40
        ]
    }
    
    df = pd.DataFrame(data)
    return df


def calculate_rankings(df, use_gdp=True, use_gmi=True, use_gdi=True):
    """
    Calculate composite rankings based on selected categories.
    Lower rank = better/more "core-like" position.
    """
    df = df.copy()
    
    # Calculate individual rankings (lower is better for core status)
    # GDP: Higher GDP = lower rank (more core-like)
    df['gdp_rank'] = df['gdp_per_capita'].rank(ascending=False)
    
    # GMI: Higher militarization = lower rank (more core-like in terms of power projection)
    df['gmi_rank'] = df['gmi_score'].rank(ascending=False)
    
    # GDI: Higher diplomatic reach = lower rank (more core-like)
    df['gdi_rank'] = df['gdi_score'].rank(ascending=False)
    
    # Calculate composite score based on selected categories
    selected_ranks = []
    if use_gdp:
        selected_ranks.append('gdp_rank')
    if use_gmi:
        selected_ranks.append('gmi_rank')
    if use_gdi:
        selected_ranks.append('gdi_rank')
    
    if not selected_ranks:
        st.error("Please select at least one category!")
        return df
    
    # Sum the selected ranks (equal weighting)
    df['composite_rank_sum'] = df[selected_ranks].sum(axis=1)
    
    # Final ranking based on sum (lower sum = more core-like)
    df['final_rank'] = df['composite_rank_sum'].rank(method='min')
    
    # Divide into three quantiles (tertiles)
    n_countries = len(df)
    tertile_size = n_countries / 3
    
    def assign_category(rank):
        if rank <= tertile_size:
            return 'Core'
        elif rank <= 2 * tertile_size:
            return 'Semi-Periphery'
        else:
            return 'Periphery'
    
    df['category'] = df['final_rank'].apply(assign_category)
    
    return df


# ============================================
# MAIN APP
# ============================================

def main():
    # Header
    st.markdown('<h1 class="main-header">World Systems Theory Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('''<p class="sub-header">
        Visualizing Core, Semi-Periphery, and Periphery nations based on GDP per Capita, 
        Global Militarization Index, and Global Diplomacy Index
    </p>''', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar for controls
    st.sidebar.header("Configuration")
    
    st.sidebar.markdown("### Select Categories")
    st.sidebar.markdown("Toggle categories to see how the world system changes:")
    
    use_gdp = st.sidebar.checkbox("GDP per Capita", value=True, help="Economic output per person (World Bank 2023/2024)")
    use_gmi = st.sidebar.checkbox("Global Militarization Index", value=True, help="Military resources relative to society (BICC 2022)")
    use_gdi = st.sidebar.checkbox("Global Diplomacy Index", value=True, help="Number of diplomatic missions (Lowy Institute 2024)")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Methodology")
    st.sidebar.info("""
    **Ranking Formula:**
    1. Each country is ranked (1 = highest) in each selected category
    2. Ranks are summed with equal weighting (1:1:1)
    3. Countries are divided into tertiles:
       - **Core**: Top third
       - **Semi-Periphery**: Middle third
       - **Periphery**: Bottom third
    """)
    
    # Calculate rankings based on selections
    df_ranked = calculate_rankings(df, use_gdp, use_gmi, use_gdi)
    
    # Color mapping for categories
    category_colors = {
        'Core': '#2166ac',
        'Semi-Periphery': '#92c5de',
        'Periphery': '#f4a582'
    }
    
    # Main content area
    col1, col2, col3 = st.columns(3)
    
    with col1:
        core_count = len(df_ranked[df_ranked['category'] == 'Core'])
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="color: #2166ac;">Core</h3>
            <h2>{core_count} countries</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        semi_count = len(df_ranked[df_ranked['category'] == 'Semi-Periphery'])
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="color: #4a90a4;">Semi-Periphery</h3>
            <h2>{semi_count} countries</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        periphery_count = len(df_ranked[df_ranked['category'] == 'Periphery'])
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="color: #d16a48;">Periphery</h3>
            <h2>{periphery_count} countries</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # World Map
    st.subheader("World Systems Map")
    
    # Create the title based on selected categories
    selected_cats = []
    if use_gdp:
        selected_cats.append("GDP per Capita")
    if use_gmi:
        selected_cats.append("GMI")
    if use_gdi:
        selected_cats.append("GDI")
    
    map_title = f"World System Classification ({' + '.join(selected_cats)})"
    
    # Create choropleth map
    fig_map = px.choropleth(
        df_ranked,
        locations='iso_alpha',
        color='category',
        hover_name='country',
        hover_data={
            'iso_alpha': False,
            'category': True,
            'final_rank': True,
            'gdp_per_capita': ':,.0f',
            'gmi_score': True,
            'gdi_score': True
        },
        color_discrete_map=category_colors,
        category_orders={'category': ['Core', 'Semi-Periphery', 'Periphery']},
        title=map_title
    )
    
    fig_map.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        height=550,
        margin=dict(l=0, r=0, t=50, b=0),
        legend=dict(
            title="Category",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # Two-column layout for additional charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Category Distribution by Metric")
        
        # Create box plots for each metric by category
        metric_option = st.selectbox(
            "Select metric to visualize:",
            ["GDP per Capita", "GMI Score", "GDI Score"]
        )
        
        metric_map = {
            "GDP per Capita": "gdp_per_capita",
            "GMI Score": "gmi_score",
            "GDI Score": "gdi_score"
        }
        
        fig_box = px.box(
            df_ranked,
            x='category',
            y=metric_map[metric_option],
            color='category',
            color_discrete_map=category_colors,
            category_orders={'category': ['Core', 'Semi-Periphery', 'Periphery']},
            title=f"{metric_option} by World System Category",
            points="all"
        )
        
        fig_box.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Category",
            yaxis_title=metric_option
        )
        
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col_right:
        st.subheader("Ranking Comparison")
        
        # Scatter plot showing relationship between metrics
        scatter_x = st.selectbox(
            "X-axis:",
            ["GDP per Capita", "GMI Score", "GDI Score"],
            index=0
        )
        
        scatter_y = st.selectbox(
            "Y-axis:",
            ["GDP per Capita", "GMI Score", "GDI Score"],
            index=1
        )
        
        fig_scatter = px.scatter(
            df_ranked,
            x=metric_map[scatter_x],
            y=metric_map[scatter_y],
            color='category',
            color_discrete_map=category_colors,
            category_orders={'category': ['Core', 'Semi-Periphery', 'Periphery']},
            hover_name='country',
            title=f"{scatter_x} vs {scatter_y}",
            size_max=15
        )
        
        fig_scatter.update_layout(
            height=400,
            xaxis_title=scatter_x,
            yaxis_title=scatter_y
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # Data table section
    st.subheader("Complete Country Rankings")
    
    # Category filter
    category_filter = st.multiselect(
        "Filter by category:",
        options=['Core', 'Semi-Periphery', 'Periphery'],
        default=['Core', 'Semi-Periphery', 'Periphery']
    )
    
    # Filter data
    df_display = df_ranked[df_ranked['category'].isin(category_filter)].copy()
    
    # Sort by final rank
    df_display = df_display.sort_values('final_rank')
    
    # Prepare display columns
    display_cols = ['final_rank', 'country', 'category']
    col_names = {'final_rank': 'Overall Rank', 'country': 'Country', 'category': 'Category'}
    
    if use_gdp:
        display_cols.extend(['gdp_per_capita', 'gdp_rank'])
        col_names['gdp_per_capita'] = 'GDP per Capita ($)'
        col_names['gdp_rank'] = 'GDP Rank'
    
    if use_gmi:
        display_cols.extend(['gmi_score', 'gmi_rank'])
        col_names['gmi_score'] = 'GMI Score'
        col_names['gmi_rank'] = 'GMI Rank'
    
    if use_gdi:
        display_cols.extend(['gdi_score', 'gdi_rank'])
        col_names['gdi_score'] = 'Diplomatic Posts'
        col_names['gdi_rank'] = 'GDI Rank'
    
    df_table = df_display[display_cols].copy()
    df_table.columns = [col_names.get(c, c) for c in display_cols]
    
    # Format GDP column if present
    if 'GDP per Capita ($)' in df_table.columns:
        df_table['GDP per Capita ($)'] = df_table['GDP per Capita ($)'].apply(lambda x: f"${x:,.0f}")
    
    # Style the dataframe
    def highlight_category(row):
        if row['Category'] == 'Core':
            return ['background-color: #d4e6f1'] * len(row)
        elif row['Category'] == 'Semi-Periphery':
            return ['background-color: #e8f4f8'] * len(row)
        else:
            return ['background-color: #fdebd0'] * len(row)
    
    styled_df = df_table.style.apply(highlight_category, axis=1)
    
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Download button
    csv = df_ranked.to_csv(index=False)
    st.download_button(
        label="Download Full Dataset (CSV)",
        data=csv,
        file_name="world_systems_data.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # Theory explanation
    with st.expander("About World-Systems Theory"):
        st.markdown("""
        ### World-Systems Theory
        
        **World-systems theory**, developed by sociologist **Immanuel Wallerstein** in the 1970s, 
        analyzes the world economy as a single capitalist system divided into three zones:
        
        #### Core Countries
        - High-income, technologically advanced nations
        - Strong state institutions and military capabilities
        - Extensive diplomatic networks
        - Control of global financial systems
        - Examples: USA, Germany, Japan, France
        
        #### Semi-Periphery Countries
        - Middle-income nations with mixed characteristics
        - Growing industrial bases and emerging markets
        - Moderate military and diplomatic capacity
        - Bridge between core and periphery
        - Examples: Brazil, China, Turkey, India
        
        #### Periphery Countries
        - Lower-income, often resource-extracting economies
        - Limited industrialization
        - Smaller diplomatic footprints
        - Economic dependency on core nations
        - Examples: Many nations in Sub-Saharan Africa, Central America
        
        ---
        
        ### This Dashboard's Methodology
        
        This dashboard uses three key indicators to classify countries:
        
        1. **GDP per Capita** (World Bank) - Economic strength per person
        2. **Global Militarization Index** (BICC) - Military resources relative to society
        3. **Global Diplomacy Index** (Lowy Institute) - Extent of diplomatic network
        
        Each country is ranked in each category, and ranks are summed with equal weighting.
        Countries are then divided into **tertiles** (thirds) to create the three-zone classification.
        
        **Note:** This is a simplified pedagogical model. Real-world classifications involve 
        many more factors including trade relationships, capital flows, and historical context.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9rem;">
        <p>Data Sources: World Bank (GDP per Capita 2023/2024), 
        BICC (Global Militarization Index 2022), 
        Lowy Institute (Global Diplomacy Index 2024)</p>
        <p>Created for educational purposes | World Systems Theory Dashboard</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
