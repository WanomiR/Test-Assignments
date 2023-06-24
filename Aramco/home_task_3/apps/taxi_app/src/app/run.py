import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import datetime

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
# plt.style.use("dark_background")
# plt.rcParams["grid.alpha"] = 0.25
# ---------------------------------------- #

st.title("Taxi orders forecasting")
st.caption("with ETNA and CatBoost")
st.text("Build your model to predict the number of taxi orders for the next 24 hours 🚕")
st.divider()

# data loading
input_data = pd.read_csv("taxi_hour.csv")
df = TSDataset.to_dataset(input_data)
ts = TSDataset(df, freq="H")

HORIZON = 24

# ---------------------------------------- #
# select the data range
st.header("Data range")
st.text("Pick a range of dates to model")

col1, col2 = st.columns(2)

with col1:
  date_start = st.date_input(
    "From",
    value=datetime.date(2018, 3, 1),
    min_value=datetime.date(2018, 3, 1),
    max_value=datetime.date(2018, 7, 1),
  )

with col2:
  date_end = st.date_input(
    "To",
    value=datetime.date(2018, 4, 30),
    min_value=datetime.date(2018, 4, 30),
    max_value=datetime.date(2018, 8, 31),
  )

# ---------------------------------------- #
# for now filter the data here manually
ts = TSDataset(ts[date_start:date_end], freq="H")
# ---------------------------------------- #


st.subheader("Your data sample")
st.pyplot(ts.plot())
st.write(
  "Sample of ",
  (ts.index.max() - ts.index.min()).days,
  " days total"
  )
st.divider()

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

st.header("Features")
st.text("Choose data transforms")

col1, col2 = st.columns(2)

with col1:
  # set the number of lags
  st.subheader("Lags")
  number_of_lags = st.slider(
    "Select the number of lags (days)",
    min_value=1,
    max_value=10,
    value=7,
  )

with col2:
  st.subheader("Rolling window size")
  window_size = st.slider(
    "Select the rolling mean window size (hours)",
    min_value=2,
    max_value=24,
    value=3
  )
  
st.subheader("Additional transforms")
transform_options = st.multiselect(
  "Choose transform methods",
  [
    "LogTransform",
    "DateFlagsTransform",
    "TrendTransform",
    "DensityOutliersTransform"
  ],
)


transforms_dict = dict(
    LagTransform=LagTransform(
      in_column="target", 
      lags=[HORIZON * i for i in range(1, number_of_lags + 1)],
      out_column="target_lag"
      ),
    MeanTransform=MeanTransform(in_column=f"target_lag_{HORIZON}", window=window_size),
    LogTransform=LogTransform(in_column="target"),
    DateFlagsTransform=DateFlagsTransform(week_number_in_month=True, out_column="date_flag"),
    TrendTransform=TrendTransform(in_column="target", out_column="trend"),
    DensityOutliersTransform=DensityOutliersTransform(in_column="target", distance_coef=3.0),
)

transform_options += ["LagTransform", "MeanTransform"]# st.write(" ", transforms_dict)
transforms = [t for k, t in transforms_dict.items() if k in transform_options]

st.divider()

# ---------------------------------------- #
# fit the model
st.header("Model performance")
st.text("Decide validation parameters and see results")

pipeline = Pipeline(
    model=CatBoostPerSegmentModel(allow_writing_files=False),
    transforms=transforms,
    horizon=HORIZON,
)

st.subheader("Validation setup")

col1, col2 = st.columns(2)

with col1:
  window_size = st.number_input(
    "Select the backtest window size",
    min_value=1,
    max_value=5,
    value=2,
  )

with col2:
  n_folds = st.number_input(
    "Select the number of folds",
    min_value=1,
    max_value=5,
    value=3,
  )

masks = sliding_window_splitter(window_size=window_size, n_folds=n_folds)
metrics_df, forecast_ts, _ = pipeline.backtest(
  ts=ts, metrics=[SMAPE()], n_folds=masks
)
score = metrics_df["SMAPE"].mean()

st.subheader("Your forecast")

st.pyplot(
  plot_backtest(forecast_ts, ts, history_len=HORIZON*3)
)
st.subheader(f"Averages SMAPE:  {score:.2f}%")