import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from etna.datasets import TSDataset
from etna.models import CatBoostPerSegmentModel
from etna.metrics import SMAPE
from etna.analysis import plot_forecast, plot_backtest
from etna.pipeline import Pipeline, FoldMask

# transforms
from etna.transforms import (
    LagTransform,
    MeanTransform, 
    LogTransform,
    DateFlagsTransform,
    DensityOutliersTransform,
    TrendTransform,
    )

# to make plots with ETNA models
st.set_option('deprecation.showPyplotGlobalUse', False)

# ---------------------------------------- #
# temporary styling
plt.style.use("dark_background")
plt.rcParams["grid.alpha"] = 0.25
# ---------------------------------------- #

st.title("Taxi orders forecasting")
st.caption("with ETNA and CatBoost")

# data loading
input_data = pd.read_csv("taxi_hour.csv")
df = TSDataset.to_dataset(input_data)
ts = TSDataset(df, freq="H")

HORIZON = 24

# ---------------------------------------- #
# for now filter the data here manually
ts = TSDataset(ts["2018-03-01":"2018-05-31"], freq="H")
# ---------------------------------------- #


if st.checkbox("See raw data sample"):
  st.subheader("Raw data sample")
  st.write(ts)

if st.checkbox("See raw data graph"):
  st.subheader("Raw data graph")
  st.pyplot(
    ts.plot()
  )

############################################
# ---------------------------------------- #
# model training part

# split the data
train_ts, test_ts = ts.train_test_split(
    train_start="2018-03-01",
    train_end="2018-05-30",
    test_start="2018-05-31",
    test_end="2018-05-31"
)

# ---------------------------------------- #
# backtest window selecting function
def sliding_window_splitter(window_size: int = 2, n_folds: int = 3):

  masks = []
  window_size *= HORIZON
  training_size = ts.index.__len__() - n_folds * window_size - HORIZON

  for n in range(n_folds):

    first_train_ts = ts.index.min() + np.timedelta64(n * window_size, "h")
    last_train_ts = first_train_ts + np.timedelta64(training_size, "h") + \
        np.timedelta64(window_size - 1, "h")
    target_ts = pd.date_range(start=last_train_ts +
                              np.timedelta64(1, "h"), periods=HORIZON, freq="h")
    mask = FoldMask(
        first_train_timestamp=first_train_ts,
        last_train_timestamp=last_train_ts,
        target_timestamps=target_ts,
    )
    masks.append(mask)

  return masks

# ---------------------------------------- #
# define transformations

st.header("Define model parameters")
# set the number of lags
st.subheader("Choose the number of lags")
number_of_lags = st.slider(
  "Select a number",
  min_value=1,
  max_value=10,
  value=7,
)

st.subheader("Decide rolling window size")
window_size = st.slider(
  "Select a number",
  min_value=3,
  max_value=24,
  value=3
)
  
st.subheader("Add transforms")
transform_options = st.multiselect(
  "Choose data transformations",
  ["LogTransform"],
  ["LogTransform"]
)
st.write("You selected: ", transform_options)


transforms = [
    LagTransform(
      in_column="target", 
      lags=[HORIZON * i for i in range(1, number_of_lags + 1)],
      out_column="target_lag"
      ),
    MeanTransform(in_column=f"target_lag_{HORIZON}", window=window_size),
    LogTransform(in_column="target"),
    DateFlagsTransform(week_number_in_month=True, out_column="date_flag"),
    TrendTransform(in_column="target", out_column="trend"),
    DensityOutliersTransform(in_column="target", distance_coef=3.0),
]

# ---------------------------------------- #
# fit the model
pipeline = Pipeline(
    model=CatBoostPerSegmentModel(allow_writing_files=False),
    transforms=transforms,
    horizon=HORIZON,
)

masks = sliding_window_splitter(window_size=2, n_folds=3)
metrics_df, forecast_ts, _ = pipeline.backtest(
  ts=ts, metrics=[SMAPE()], n_folds=masks
)
# model.fit(train_ts)
# forecast_ts = model.forecast()

# smape = SMAPE()
# score = smape(y_true=test_ts, y_pred=forecast_ts)
score = metrics_df["SMAPE"].mean()

st.header("Forecast")
st.pyplot(
  plot_backtest(forecast_ts, ts, history_len=HORIZON*3)
)
st.subheader(f"Averages SMAPE:  {score:.2f}%")