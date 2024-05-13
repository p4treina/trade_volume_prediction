import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd

from config import FEATURES, MODEL_NAME, MODELS_PATH, ROOT_DIR, VOLUME_DATA_PATH
from etl.extract import DataExtractor
from etl.transform import DataTransformer
from model.model import VolumeForecastModel
from utils import get_mean_std, get_model_path, get_train_test_indexes


def get_data():
    data_path = f"{ROOT_DIR}/{VOLUME_DATA_PATH}"
    extractor = DataExtractor(data_path)
    volume_df = extractor.extract_data()

    # Add target
    transformer = DataTransformer()
    volume_df = transformer.add_target(volume_df, "volume_gm")

    # Transform
    train_indexes, _ = get_train_test_indexes(volume_df, test_size=0.2)
    means, stds = get_mean_std(volume_df.loc[train_indexes])
    volume_df = transformer.transform(volume_df, means, stds)
    return volume_df


def get_forecast(date):
    volume_df = get_data()
    # Load_model
    _, model_version = get_model_path(MODEL_NAME, MODELS_PATH)
    model_path = f"{MODELS_PATH}/{MODEL_NAME}_v{model_version}.pkl"
    volume_forecaster = VolumeForecastModel()
    volume_forecaster.model = model_path

    input_df = pd.DataFrame(
        data={
            "date": date,
            "rolling_mean": [volume_df.loc[date]["rolling_mean"]],
            "volume_gm_lag_1": [volume_df.loc[date]["volume_gm_lag_1"]],
            "volume_gm": [volume_df.loc[date]["volume_gm"]],
        },
        columns=["date", "rolling_mean", "volume_gm_lag_1", "volume_gm"],
    )
    input_df = input_df.set_index("date")
    forecast = float(volume_forecaster.predict(input_df)[0])
    return forecast


def modelled_data():
    volume_df = get_data()
    volume_df = volume_df.iloc[:-1]

    # Load_model
    _, model_version = get_model_path(MODEL_NAME, MODELS_PATH)
    model_path = f"{MODELS_PATH}/{MODEL_NAME}_v{model_version}.pkl"
    volume_forecaster = VolumeForecastModel()
    volume_forecaster.model = model_path

    # Predictions
    predictions = volume_forecaster.predict(volume_df[FEATURES])
    volume_df["predictions"] = predictions
    fig = plt.figure()
    volume_df["target"].plot(figsize=[20, 8], legend=True)
    volume_df["predictions"].plot(figsize=[20, 8], legend=True)
    return fig


if __name__ == "__main__":
    # GUI
    with gr.Blocks() as demo:
        with gr.Row():
            gr.Label("Global Markets Volumes", label="")
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Row():
                    date = gr.Dropdown(
                        ["2/16/2021", "2/15/2021", "2/12/2021", "2/11/2021"],
                        label="Date",
                    )
                with gr.Row():
                    forecast = gr.Button("Forecast")
                with gr.Row():
                    output = gr.Textbox(type="text", lines=1, label="Forecast")
            with gr.Column(scale=3, variant="panel"):
                gr.Label("Traded Volumes", label="", scale=0.1)
                gr.Plot(modelled_data)
        forecast.click(
            get_forecast,
            inputs=date,
            outputs=output,
        )
    demo.launch()
