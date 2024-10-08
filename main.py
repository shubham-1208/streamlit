# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# st.title("Data Dashboard")

# upload_file = st.file_uploader("Choose a CSV file", type="csv")

# if upload_file is not None:
#     df = pd.read_csv(upload_file)

#     st.subheader("Data Preview")
#     st.write(df.head())

#     st.subheader("Data Summary")
#     st.write(df.describe())

#     st.subheader("Filter Data")
#     columns = df.columns.tolist()
#     selected_column = st.selectbox("Select which column to filter by", columns)
#     unique_values = df[selected_column].unique()
#     selected_value = st.selectbox("Select value", unique_values)


#     filtered_df = df[df[selected_column] == selected_value]
#     st.write(filtered_df)

#     st.subheader("Plot Data")
#     x_column = st.selectbox("Select x-axis column", columns)
#     y_column = st.selectbox("Select y-axis column", columns)

#     if st.button("Generate Plot"):
#         st.line_chart(filtered_df.set_index(x_column)[y_column])

# else:
#     st.write("Waiting for file upload...")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data Dashboard")

# Option to upload a file or provide a URL
upload_file = st.file_uploader("Choose a CSV file", type="csv")
url = st.text_input("Or enter the URL of a CSV file")

df = None

if upload_file is not None:
    df = pd.read_csv(upload_file)
elif url:
    try:
        df = pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading CSV from URL: {e}")

if df is not None:
    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("Data Summary")
    st.write(df.describe())

    st.subheader("Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select which column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot Data")
    x_column = st.selectbox("Select x-axis column", columns)
    y_column = st.selectbox("Select y-axis column", columns)

    if st.button("Generate Plot"):
        st.line_chart(filtered_df.set_index(x_column)[y_column])

else:
    st.write("Waiting for file upload or URL input...")
