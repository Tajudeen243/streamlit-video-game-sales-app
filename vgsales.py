import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from urllib.error import URLError

@st.cache_data
def get_data():
    path_ = "vgsales.csv"
    df = pd.read_csv(path_)
    
    # Drop NAN on Year & Publisher
    df.dropna(inplace=True)
    # Cleaning on Year Column
    df.Year = df.Year.astype('str')
    df.Year = df.Year.str.replace('.0','')
    return df

try:
    df = get_data()
    """ # Video sales game analysis"""
    # st.write(df)
    st.dataframe(df.head())

    """ # Sales Metrics """
    global_sales = round(np.sum(df.Global_Sales),2)
    eu_sales = np.round(np.sum(df.EU_Sales),2)
    na_sales = np.round(np.sum(df.NA_Sales),2)
    ja_sales = np.round(np.sum(df.JP_Sales),2)
    oth_sales = np.round(np.sum(df.Other_Sales),2)

    # create a series of columns
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)


    # Card
    col1.metric("Global Sales Total", global_sales,"USD")
    col2.metric("Europian Union Sales", eu_sales,"USD")
    col3.metric("North American Sales", na_sales,"USD")
    col4.metric("Japanese Union Total", ja_sales,"USD")
    col5.metric("Other Sales", oth_sales,"USD")

    # Filter (platforms)
    col6,col7 = st.columns(2)
    platforms = df.Platform.unique()
    selected_platform = col6.multiselect("Platforms",platforms, [platforms[0],platforms[1]])

    # Filter (Genre)
    
    genre = df.Genre.unique()
    selected_genre = col7.multiselect("Genres",genre, [genre[0],genre[1]])

    filtered_data = df[df["Platform"].isin(selected_platform) & df["Genre"].isin(selected_genre)]

    # table 
    
    if not selected_platform and selected_genre:
        st.error("Please select both filters from Platform and Genre")
    else:
        st.write("""Filtered result""")
        st.table(filtered_data.head())

    # Table end
    # Plot
    # Bar chart

    st.write("# Top Platforms Chart")
    bar0 = df.groupby(['Platform'])['Global_Sales'].sum().nlargest(n=10).sort_values()
    st.bar_chart(bar0, color="#d4af37")

    st.write(""" ## Global Sales per platform""")
    bar1 = filtered_data.groupby(['Platform'])['Global_Sales'].sum().sort_values(ascending=True)
    st.bar_chart(bar1)
    st.bar_chart(bar1, color='#d4af37',width=400,height=400)

    # Line Chart
    st.write(""" ## Global Sales over time""")
    chart = (
            alt.Chart(filtered_data)
            .mark_line()
            .encode(
                x="Year",
                y=alt.Y("Global_Sales", stack=None),
            )
        )
    st.altair_chart(chart,use_container_width=True)

    st.write(""" ## Global Sales over time""")
    chart = (
            alt.Chart(filtered_data)
            .mark_area(opacity=0.3)
            .encode(
                x="Year",
                y=alt.Y("Global_Sales", stack=None),
            )
        )
    st.altair_chart(chart,use_container_width=True)
    

    # countries = st.multiselect(
    #     "Choose countries", list(df.index), ["China", "United States of America"]
    # )
    # if not countries:
    #     st.error("Please select at least one country.")
    # else:
    #     data = df.loc[countries]
    #     data /= 1000000.0
    #     st.write("### Gross Agricultural Production ($B)", data.sort_index())

    #     data = data.T.reset_index()
    #     data = pd.melt(data, id_vars=["index"]).rename(
    #         columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    #     )
    #     chart = (
    #         alt.Chart(data)
    #         .mark_area(opacity=0.3)
    #         .encode(
    #             x="year:T",
    #             y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
    #             color="Region:N",
    #         )
    #     )
    #     st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    

)
