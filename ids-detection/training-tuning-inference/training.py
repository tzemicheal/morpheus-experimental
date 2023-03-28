import json

import click
import pandas as pd
from loda import Loda
from util import NetFlowFeatureProcessing


@click.command()
@click.option('--input-name',
              help="Path to trained LODA IDS model",
              default="dataset/Monday-WorkingHours.pcap_ISCX.csv")
@click.option('--model-name', help="Input file name path", default="../model/loda_ids")
@click.option('--config-path', help="Path to JSON training configuration file", default="../model/config.json")
@click.option('--output-name', help="Path to csv training result", default="train_out.csv")
@click.option('--projections', help="Number of projections", default=1000)
def training(input_name, model_name, config_path, output_name, projections):

    # Load dataset and return preprocessed features along config file.
    feature_processor = NetFlowFeatureProcessing(input_name=input_name, config=None)
    X_train, config = feature_processor.process(apply_pca=True)

    # Train loda model
    loda_ids = Loda(n_random_cuts=projections)
    loda_ids.fit(X_train)
    scores = loda_ids.score(X_train)

    # Save model & training config
    loda_ids.save_model(model_name)
    json.dump(config, open(config_path, "w"))

    # Output training scores
    df = pd.DataFrame()
    df['scores'] = scores.get()
    df.to_csv(output_name, index=False)


if __name__ == "__main__":
    training()
