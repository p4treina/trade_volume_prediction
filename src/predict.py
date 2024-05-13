from src.config import (
    FEATURES,
    MODEL_NAME,
    MODELS_PATH,
    ROOT_DIR,
    VOLUME_DATA_PATH,
)
from src.etl.extract import DataExtractor
from src.etl.transform import DataTransformer
from src.model.model import VolumeForecastModel
from src.utils import get_mean_std, get_model_path, get_train_test_indexes

if __name__ == "__main__":
    # Load data
    data_path = f"{ROOT_DIR}/{VOLUME_DATA_PATH}"
    extractor = DataExtractor(data_path)
    volume_df = extractor.extract_data()

    # Add target
    transformer = DataTransformer()
    volume_df = transformer.add_target(volume_df, "volume_gm")

    # Transform
    train_indexes, test_indexes = get_train_test_indexes(volume_df, test_size=0.2)
    means, stds = get_mean_std(volume_df.loc[train_indexes])
    volume_df = transformer.transform(volume_df, means, stds)

    # Load_model
    _, model_version = get_model_path(MODEL_NAME, MODELS_PATH)
    model_path = f"{MODELS_PATH}/{MODEL_NAME}_v{model_version}.pkl"
    volume_forecaster = VolumeForecastModel()
    volume_forecaster.model = model_path

    # Predict
    input_df = volume_df[FEATURES].iloc[-1:]
    volume_forecaster.predict(input_df)
