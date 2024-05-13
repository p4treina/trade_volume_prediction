import pickle

from config import (
    FEATURES,
    MODEL_NAME,
    MODELS_PATH,
    RANDOM_STATE,
    ROOT_DIR,
    VOLUME_DATA_PATH,
)
from etl.extract import DataExtractor
from etl.transform import DataTransformer
from model.model import VolumeForecastModel
from utils import get_mean_std, get_model_path, get_train_test_indexes

if __name__ == "__main__":
    # Load Data
    data_path = f"{ROOT_DIR}/{VOLUME_DATA_PATH}"
    extractor = DataExtractor(data_path)
    volume_df = extractor.extract_data()

    # Add target
    transformer = DataTransformer()
    volume_df = transformer.add_target(volume_df, "volume_gm")
    volume_df = volume_df.iloc[:-1]

    # Train test split
    train_indexes, test_indexes = get_train_test_indexes(volume_df, test_size=0.2)
    train_df = volume_df.loc[train_indexes]
    test_df = volume_df.loc[test_indexes]

    # Transform
    means, stds = get_mean_std(train_df)
    train_df = transformer.transform(train_df, means, stds)
    test_df = transformer.transform(test_df, means, stds)

    # Train
    X_train = train_df[FEATURES]
    y_train = train_df[["target"]]
    X_test = test_df[FEATURES]
    y_test = test_df[["target"]]

    volume_forecaster = VolumeForecastModel(
        learning_rate=0.2, max_depth=5, subsample=0.8, random_state=RANDOM_STATE
    )
    volume_forecaster.fit(X_train, y_train)

    # TODO: Do smth with the eval metrics
    # Evaluate
    eval_metrics = volume_forecaster.evaluate(X_test, y_test)

    # Save model
    model_path, _ = get_model_path(MODEL_NAME, MODELS_PATH)
    with open(model_path, "wb") as file:
        pickle.dump(volume_forecaster.model, file)
