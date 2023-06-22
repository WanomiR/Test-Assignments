import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from etna.datasets import TSDataset
from etna.models import NaiveModel, CatBoostPerSegmentModel
from etna.metrics import SMAPE
from etna.analysis import plot_forecast
from etna.transforms import LagTransform, LogTransform
from etna.pipeline import Pipeline

# to make plots with ETNA models
st.set_option('deprecation.showPyplotGlobalUse', False)

# temporary styling
plt.style.use("dark_background")
plt.rcParams["grid.alpha"] = 0.25

st.title("Taxi orders forecasting")
st.caption("with ETNA and CatBoost")

# data loading
input_data = pd.read_csv("./src/app/taxi_hour.csv")
df = TSDataset.to_dataset(input_data)
# for now filter the data here manually
ts = TSDataset(df["2018-05-01":"2018-05-31"], freq="1H")


if st.checkbox("See raw data sample"):
  st.subheader("Raw data sample")
  st.write(ts)

if st.checkbox("See raw data graph"):
  st.subheader("Raw data graph")
  st.pyplot(
    ts.plot()
  )
  
# —————————————————————————————————— #
# model training part


# split the data
train_ts, test_ts = ts.train_test_split(
    train_start="2018-05-01",
    train_end="2018-05-30",
    test_start="2018-05-31",
    test_end="2018-05-31"
)

HORIZON = 24

transforms = [
    LagTransform(in_column="target", lags=[HORIZON * i for i in range(1, 6)]),
    LogTransform(in_column="target")
]

model = Pipeline(
    model=CatBoostPerSegmentModel(),
    transforms=transforms,
    horizon=HORIZON,
)

model.fit(train_ts)
forecast_ts = model.forecast()

smape = SMAPE()
score = smape(y_true=test_ts, y_pred=forecast_ts)

st.header("Forecast")
st.pyplot(
  plot_forecast(forecast_ts, test_ts, train_ts, n_train_samples=HORIZON*2)
)
st.subheader(f"SMAPE:  {score['main']:.2f}%")