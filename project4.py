import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns


df=pd.read_csv("D:\\project\\Airbnb_data.csv")


#st.set_page_config(page_title="Extracting Business Card Data with OCR",layout="wide")

with st.sidebar:
    st.header(":red[AIRBNB ANALYSIS]")
    options=["POWER BI","DATA EXPLORATION", "GEOSPATIAL ANALYSIS","TOP ANALYSIS"]
    default_option="POWER BI"
    selected = st.selectbox("Select an option:", options,options.index(default_option))

if selected=="POWER BI":
    st.title("Power BI Dashboard in Streamlit")

    

    # Power BI embed URL
    embed_url = "https://app.powerbi.com/view?r=eyJrIjoiYjI1ZmY0Y2YtNTUwOS00OWIwLWE2MWMtN2RhZDcwYjlkOGEzIiwidCI6IjEzNTY3YmQ4LTYzOGEtNGU4OS05MWU5LTk4ZjdkNDU1MmE5ZiJ9&pageName=cc652ac45468cae1fca0" 

    # Embed the Power BI report using an iframe
    st.markdown(f"""
    <iframe title="Airbnb_final" width="800" height="500" src="{embed_url}" frameborder="0" allowFullScreen="true"></iframe>
    """, unsafe_allow_html=True)

if selected=="DATA EXPLORATION":
    
    st.header("PRICE ANALYSIS")


    Country=df.groupby('Country')['Price'].mean().reset_index()
    # Bar plot for average price by location
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Country', y='Price', data=Country)
    plt.title('Average Price by Country')
    plt.xlabel('Country')
    plt.ylabel('Price')
    plt.xticks(rotation=90)
    st.pyplot(plt)

    st.write("HongKong has the highest average price this might be due to higher cost of living in these areas or  might be a popular tourist destination")


    col1,col2=st.columns(2)
    with col1:
        st.write("")
        st.write("")
        st.write("")
        country=st.selectbox("select the country",df["Country"].unique())
        df1=df[df["Country"]==country]
        room_type=st.selectbox("select the room type",df1["Room_type"].unique())
        df2=df1[df1["Room_type"]==room_type]
        df_bar= pd.DataFrame(df2.groupby("Property_type")[["Price","Review_rating","No_of_reviews"]].mean())
        df_bar.reset_index(inplace= True)
        fig_bar= px.bar(df_bar, x='Property_type', y= "Price", title= "PRICE VS PROPERTY TYPE",hover_data=["Review_rating","No_of_reviews"],color_discrete_sequence=px.colors.sequential.Redor_r, width=600, height=500)
        st.plotly_chart(fig_bar)

        st.write("Farm stay has the highest average price, indicating it may offer premium amenities or a luxurious experience")

    with col2:
        st.write("")
        st.write("")
        st.write("")
        
        property_type=st.selectbox("select the property type",df2["Property_type"].unique())
        
        
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        df3=df2[df2["Property_type"]==property_type]
        # Group by Host_name and aggregate
        df_bar = df3.groupby("Host_name").agg({
            "Price": "mean",
            "Host_neighbourhood": "first",
            "Review_rating": "mean"
        }).reset_index()
        # Sort by Price in descending order and select top 10
        df_bar = df_bar.sort_values(by="Price", ascending=False).head(10)
        #.head(10)
        fig_bar= px.bar(df_bar,x="Host_name", y= "Price", title= "HOST NAME VS PRICE",hover_data=["Host_neighbourhood","Review_rating"],
                        color_discrete_sequence=px.colors.sequential.Redor_r, width=600, height=500) 
        st.plotly_chart(fig_bar)

        st.write("camilo has the highest earning and is the most expensive airbnb")

    df_scatter=df.groupby("Price")['No_of_reviews'].mean().reset_index()
    fig = px.scatter(df_scatter,x="Price", y ="No_of_reviews", title = "No_of_reviews vs price")
    st.plotly_chart(fig)
    st.write("From the above visualization we can say that most number of people like to stay in less price and their reviews are higher in those area")

        

    st.header("AVAILABILITY ANALYSIS")
    
    col1,col2,col3=st.columns(3)
    with col1:
        country=st.selectbox("select the country",df["Country"].unique(),key="country_type_selectionbox")
        df1=df[df["Country"]==country]
    with col2:
        room_type=st.selectbox("select the room type",df1["Room_type"].unique(),key="room_type_selectionbox")
        df2=df1[df1["Room_type"]==room_type]
    with col3:
        property_type=st.selectbox("select the property type",df2["Property_type"].unique(),key="property_type_selectionbox")
        df3=df2[df2["Property_type"]==property_type]

    df_scatter=df3.groupby("Host_neighbourhood").agg({
            "Price": "mean",
            "Host_name": "first",            
            "Min_nights":"mean",
            "Availability_365":"mean",
            "Max_nights":"mean"
        }).reset_index()
    df_scatter=df_scatter.sort_values(by="Availability_365", ascending=False).head()
    fig_scatter=px.scatter(df_scatter,x="Host_neighbourhood",y="Host_name",title='Availability analysis on Location',
                           hover_data=["Max_nights","Min_nights","Price","Availability_365"],template='plotly_dark')
        
    st.plotly_chart(fig_scatter) 

    

    st.header("LOCATION ANALYSIS")

    #st.title("Sunburst Chart of Property Data")

    # Group by the hierarchical path and aggregate the Price values
    aggregated_df = df.groupby(['Country', 'Property_type', 'Room_type', 'Host_neighbourhood']).agg({
        'Price': 'sum'
    }).reset_index()

    # Create the sunburst plot
    fig = px.sunburst(
        aggregated_df,
        path=['Country','Room_type', 'Property_type',  'Host_neighbourhood'],
        values='Price',
        title="Sunburst Chart of host_neighbourhood"
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

if selected=="GEOSPATIAL ANALYSIS":
    col1, col2, col3 = st.columns(3)

    # Filters
    with col1:
        country = st.multiselect('Select a Country', df['Country'].unique())
    with col2:
        prop = st.multiselect('Select Property Type', df['Property_type'].unique())
    with col3:
        room = st.multiselect('Select Room Type', df['Room_type'].unique())

    # Constructing the query
    query_parts = []
    if country:
        query_parts.append(f"Country in {country}")
    if prop:
        query_parts.append(f"Property_type in {prop}")
    if room:
        query_parts.append(f"Room_type in {room}")
    query = ' & '.join(query_parts)

    # Filter dataframe
    if query:
        filtered_df = df.query(query)
    else:
        filtered_df = df

    # Check if the filtered dataframe is empty
    if filtered_df.empty:
        st.write("No listings match the selected criteria.")

    else:
        # Aggregation and visualization
        country_df = filtered_df.groupby('Country', as_index=False).agg({
            'Availability_365': 'mean',
            'Price': 'mean',
            'Review_rating': 'mean'
        })


        fig = px.scatter_geo(country_df,
                            locations='Country',
                            locationmode='country names',
                            color='Availability_365',
                            hover_name='Country',
                            hover_data={
                                'Price': True,
                                'Availability_365': True,
                                'Review_rating': True
                            },
                            size='Availability_365',
                            color_continuous_scale='blues')
        st.plotly_chart(fig, use_container_width=True)

if selected=="TOP ANALYSIS":
    col1,col2=st.columns(2)
    with col1:
        top_country = df['Country'].value_counts().head(10)
        # Create the plot
        fig = px.bar(
        x=top_country.index,
        y=top_country.values,
        title="Top Countries by Number of Airbnb Listings",
        labels={'x': 'Country', 'y': 'Count'})

        # Update axes labels
        fig.update_xaxes(title_text='Country')
        fig.update_yaxes(title_text='Count')

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        st.write("Airbnb data reveals that the United States stands out as the top country and indicates a high level of Airbnb activity and availability in the US")

    with col2:
        top_property_types = df['Property_type'].value_counts().head(10)
        # Create the plot
        fig = px.bar(
        x=top_property_types.index,
        y=top_property_types.values,
        title="Top 10 Property_types by Number of Airbnb Listings",
        labels={'x': 'Property Types', 'y': 'Count'})

        # Update axes labels
        fig.update_xaxes(title_text='Property types')
        fig.update_yaxes(title_text='Count')

        st.plotly_chart(fig)

        st.write("Apartment is the leading property type many prefer this due to space, amenities or guest preferences.")
           
    col1, empty_col, col2 = st.columns([1, 0.2, 1])
    with col1:
        avg_price_room_type = df.groupby('Room_type')['Price'].mean().reset_index()
        fig = px.pie(values=avg_price_room_type['Price'], names=avg_price_room_type['Room_type'],title="Analysis of Room_type based on Avg_price")
        st.plotly_chart(fig)

        

    with empty_col:
        st.empty()
      
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.dataframe(avg_price_room_type)
        st.write("The pie chart shows that the Shared room is prefered the most which has 39.9% where the preference of Entire home/apt and shared room is less")

        
    # Calculate the average price for each neighborhood
    avg_price_location = df.groupby('Host_neighbourhood')['Price'].mean().reset_index()

    # Sort the DataFrame by average price in descending order
    avg_price_location_sorted = avg_price_location.sort_values(by='Price', ascending=False)

    # Select the top 20 neighborhoods
    top_20_neighbourhoods = avg_price_location_sorted.head(20)

    fig=px.scatter(top_20_neighbourhoods,x='Host_neighbourhood', y='Price',color='Price',size='Price',
            title='Average Price by Location',template='plotly_dark')
    st.plotly_chart(fig)
    st.write("From the above scatter plot,Location Kwun Tong is having the highest average price ,Ho man Tim is on second position while Urca retains third position")
    st.write("")
    st.write("")
    st.write("Cheapest Airbnb")
    df_cheapest=df[['Host_name','Price','Country']].sort_values(by='Price').nsmallest(20,columns='Price')
        
    plt.figure(figsize=(12, 6))
    plt.barh(df_cheapest['Host_name'], df_cheapest['Price'])
    plt.title('cheapest airbnb')
    plt.ylabel('Price')
    plt.xlabel('Host_name')
    st.pyplot(plt)
    st.write("catarina is the cheapest airbnb and has low earnings")

    
    min_nights_count = df.groupby('Min_nights').size().reset_index(name = 'count')
    min_nights_count = min_nights_count.sort_values('count', ascending=False)
    min_nights_count = min_nights_count.head(15)
    min_nights_count = min_nights_count.reset_index(drop=True)
    minimum_nights = min_nights_count['Min_nights']
    count = min_nights_count['count']
    plt.figure(figsize=(12, 8))

    # Create the bar plot
    plt.bar(minimum_nights, count)

    # Add axis labels and a title
    plt.xlabel('Minimum Nights', fontsize='14')
    plt.ylabel('Count', fontsize='14')
    plt.title('Stay Requirement by Minimum Nights', fontsize='15')

    # Show the plot
    st.pyplot(plt)
    st.write('''The majority of listings on Airbnb have a minimum stay requirement of 1 or 2 nights, with 1700 and 1400 listings, respectively.
            The number of listings with a minimum stay requirement decreases as the length of stay increases''')
