import argparse
import yaml
import torch
import numpy as np
from typing import Dict
from src import logger
from src.encoder import SentenceEncoder
from src.utils import Timer, SetUpConfig

# TODO:
# Add unit tests
# check the types and styles
# Add docstrings and documents


class SetUpConfig:
    def __init__(self):
        self.config_path = "configs/encoder.yml"

        with open(self.config_path, "r") as cf:
            self.config_values = yaml.safe_load(cf)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Command Line Interface for sentence-encoder"
    )

    subparsers = parser.add_subparsers(
        description="Use different parser to distinguish between batch and single mode.",
        dest="mode",
    )

    batch = subparsers.add_parser(
        name="batch", help="Use this parser to trigger batch encoding calculation"
    )

    inference = subparsers.add_parser(
        name="inference",
        help="Use this parser to trigger inference encoding calculation",
    )

    poc = subparsers.add_parser(
        name="poc",
        help="Use this parser for poc purposes",
    )

    batch.add_argument(
        "-input_file",
        type=str,
        required=True,
        help="The path to the txt file with the sentences.",
    )

    inference.add_argument(
        "-sentence",
        type=str,
        required=True,
        help="The sentence to calculate the encoding ",
    )

    poc.add_argument(
        "-sentence",
        type=str,
        required=True,
        help="The sentence to calculate the encoding ",
    )

    return parser.parse_args()


def run_poc(model, sentence):
    knowledge_store = model._load_embeddings()
    knowledge_store_embeddings = torch.stack(list(knowledge_store.values()), dim=0)
    encodings = model.encode(sentence)
    sentence_embeddings = torch.stack(list(encodings.values()), dim=0).repeat(knowledge_store_embeddings.shape[0], 1)

    knowledge_sentences = list(knowledge_store.keys())
    cosine_scores = model.compare(sentence_embeddings, knowledge_store_embeddings)

    score_list = cosine_scores.numpy()[0, :]
    sorted_indices = np.argsort(score_list, kind='quicksort')[::-1]
    sorted_score_list = score_list[sorted_indices]

    with open(f"{model.config['output_path']}/{sentence}.txt", 'w') as f:
        logger.info(f"User input: {sentence}")
        for idx, score in enumerate(sorted_score_list):
            logger.info(f"Score: {score} \t {knowledge_sentences[sorted_indices[idx]]}")
            f.write(f"{score};;;{knowledge_sentences[sorted_indices[idx]]}\n")


if __name__ == "__main__":
    arguments = parse_arguments()
    config = SetUpConfig()

    with Timer() as t:
        model = SentenceEncoder(config.config_values)
    logger.info(f"Model loaded in {t.elapsed} seconds.")

    match arguments.mode:
        case "inference":
            with Timer() as t:
                encodings = model.encode(arguments.sentence)
            logger.info(f"One sentence encoded in {t.elapsed} seconds.")
            sentences = [arguments.sentence]
        case "batch":
            with open(arguments.input_file) as f:
                sentences = [line.rstrip() for line in f]

            with Timer() as t:
                encodings = model.batch_encode(sentences)
            logger.info(f"{len(sentences)} sentences encoded in {t.elapsed} seconds.")
        case "poc":
            run_poc(model, arguments.sentence)
            print('ok')
        case _:
            logger.error("Mode not recognised. Try one of: batch, inference")
