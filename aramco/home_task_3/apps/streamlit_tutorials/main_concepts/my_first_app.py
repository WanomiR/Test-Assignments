import streamlit as st
import pandas as pd

st.write("Here's our first attempt at using data to crate a table:")
st.write(pd.DataFrame({
    "first column": [1, 2, 3, 4],
    "second columns": [10, 20, 30, 40]
}))