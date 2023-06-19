import streamlit as st
import numpy as np
import pandas as pd

df = pd.DataFrame(
    np.random.randn(10, 20,),
    columns=("col %d" % i for i in range(20))
)

st.dataframe(df.style.highlight_max(axis=0))

# or use static table generator
# st.table(df)