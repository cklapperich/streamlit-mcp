# Visualize data in Snowflake Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

In Snowflake Notebooks, you can use your favorite Python visualization
libraries, such as matplotlib and plotly, to develop your visualizations.

This topic shows how to visualize data in your notebooks using the following
libraries:

  * Altair

  * Matplotlib

  * Plotly

  * Seaborn

  * Streamlit

## The dataset¶

The examples in this topic use the following toy dataset that is based on the
[Palmer’s Penguin
dataset](https://allisonhorst.github.io/palmerpenguins/articles/intro.html).

species | measurement | value  
---|---|---  
adeli | bill_length | 37.3  
adeli | flipper_length | 187.1  
adeli | bill_depth | 17.7  
chinstrap | bill_length | 46.6  
chinstrap | flipper_length | 191.7  
chinstrap | bill_depth | 17.6  
gentoo | bill_length | 45.5  
gentoo | flipper_length | 212.7  
gentoo | bill_depth | 14.2  
  
You can create this dataset in your notebook with the following code:

    
    
    species = ["adelie"] * 3 + ["chinstrap"] * 3 + ["gentoo"] * 3
    measurements = ["bill_length", "flipper_length", "bill_depth"] * 3
    values = [37.3, 187.1, 17.7, 46.6, 191.7, 17.6, 45.5, 212.7, 14.2]
    df = pd.DataFrame({"species": species,"measurement": measurements,"value": values})
    df
    

Copy

### Visualize results with Altair¶

Altair is imported by default on Snowflake Notebooks as part of Streamlit.
Snowflake Notebooks currently support Altair version 4.0. For details on
available visualization types when using Altair, see [Vega-Altair: Declarative
Visualization in Python](https://altair-viz.github.io/index.html).

The following code plots a stacked bar chart of all the measurements in a
dataframe named `df` that contains the toy dataset:

    
    
    import altair as alt
    alt.Chart(df).mark_bar().encode(
        x= alt.X("measurement", axis = alt.Axis(labelAngle=0)),
        y="value",
        color="species"
    )
    

Copy

After you run the cell, the following visualization appears:

[![A stacked bar chart showing the stacked values of each of the measurements
for each penguin type.](../../_images/notebooks-altair-
heatmap.png)](../../_images/notebooks-altair-heatmap.png)

### Visualize results with matplotlib¶

To use matplotlib, install the matplotlib library for your notebook:

  1. From the notebook, select Packages.

  2. Locate the matplotlib library and select the library to install it.

The following code plots the toy dataset, `df`, using matplotlib:

    
    
    import matplotlib.pyplot as plt
    
    pivot_df = pd.pivot_table(data=df, index=['measurement'], columns=['species'], values='value')
    
    import matplotlib.pyplot as plt
    ax = pivot_df.plot.bar(stacked=True)
    ax.set_xticklabels(list(pivot_df.index), rotation=0)
    

Copy

After you run the cell, the following visualization appears:

[![A stacked bar chart showing the stacked values of each of the measurements
for each penguin type.](../../_images/notebooks-matplotlib-
viz.png)](../../_images/notebooks-matplotlib-viz.png)

For more details on using the `st.pyplot` chart element, see
[st.pyplot](https://docs.streamlit.io/library/api-reference/charts/st.pyplot).

### Visualize results with plotly¶

To use plotly, install the plotly library for your notebook:

  1. From the notebook, select Packages.

  2. Locate the plotly library and select the library to install it.

The following code plots a bar chart of the penguin measurements from the toy
dataset, `df`:

    
    
    import plotly.express as px
    px.bar(df, x='measurement', y='value', color='species')
    

Copy

After you run the cell, the following visualization appears:

[![A stacked bar chart showing the stacked values of each of the measurements
for each penguin type.](../../_images/notebooks-plotly-
viz.png)](../../_images/notebooks-plotly-viz.png)

### Visualize results with seaborn¶

To use seaborn, you must install the seaborn library for your notebook:

  1. From the notebook, select Packages.

  2. Locate the seaborn library and select the library to install it.

The following code plots a bar chart of the penguin measurements from the toy
dataset, `df`:

    
    
    import seaborn as sns
    
    sns.barplot(
        data=df,
        x="measurement", hue="species", y="value",
    )
    

Copy

After you run the cells, the following visualization appears:

[![Bar chart showing each of the measurement values for each penguin
type.](../../_images/notebooks-seaborn-viz.png)](../../_images/notebooks-
seaborn-viz.png)

For more examples of seaborn visualizations, see the seaborn [Example
gallery](https://seaborn.pydata.org/examples/index.html).

### Visualize results using Streamlit¶

Streamlit is imported by default in Snowflake Notebooks. You can use chart
elements supported by Streamlit version 1.26.0 to create a line chart, bar
chart, area chart, or a map with points on it. See [Chart
elements](https://docs.streamlit.io/library/api-reference/charts) .

Note

Some Streamlit chart elements are not supported in Snowflake or might be
subject to additional terms. See [Streamlit support in Notebooks](notebooks-
use-with-snowflake.html#label-notebooks-streamlit-support).

To visualize the toy dataset, `df`, in a bar chart, you can use the following
Python code:

    
    
    import streamlit as st
    
    st.bar_chart(df, x='measurement', y='value', color='species')
    

Copy

After you run both cells, the following visualization appears:

![Bar chart that stacks the penguin measurements for each penguin
species.](../../_images/notebooks-streamlit-barchart.png)

To learn more about how you can build interactive data apps with Streamlit,
see [Streamlit in notebooks](notebooks-use-with-snowflake.html#label-
notebooks-streamlit-in-nb).

