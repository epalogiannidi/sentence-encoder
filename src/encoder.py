import torch
import os
import chardet
from typing import Dict, List
from sentence_transformers import SentenceTransformer, util
from src import logger


class SentenceEncoder:
    def __init__(self, config: Dict):
        self.config = config
        self.model = SentenceTransformer(config["pretrained_model"])
        self.embeddings = (
            torch.load(config["saved_embeddings"])
            if os.path.exists(config["saved_embeddings"])
            else None
        )

        if not os.path.exists(config["output_path"]):
            logger.info("Creating output directory")
            os.makedirs(config["output_path"])

    def _save_embeddings(
        self,
        embeddings: Dict[str, torch.Tensor],
        sentences: List[str],
        init: bool,
        saved_embeddings: Dict[str, torch.Tensor],
    ) -> None:
        if init:
            embedded_dict = {}
            for idx, sentence in enumerate(sentences):
                embedded_dict[sentence] = embeddings[sentence]
            torch.save(embedded_dict, self.config["saved_embeddings"])
        else:
            for idx, sentence in enumerate(sentences):
                saved_embeddings[sentence] = embeddings[sentence]
            torch.save(saved_embeddings, self.config["saved_embeddings"])

    def _load_embeddings(self):
        embeddings_file = self.config["saved_embeddings"]
        if os.path.exists(embeddings_file):
            try:
                return torch.load(embeddings_file)
            except Exception as e:
                logger.error(f"Failed to load embeddings file: {e}.")
        else:
            logger.warning(
                "No saved embeddings file found. Starting the process from scratch"
            )

    def encode(self, sentence: str) -> Dict[str, torch.Tensor]:
        saved_embeddings = self._load_embeddings()
        init = False
        if saved_embeddings is None:
            embeddings = self.model.encode(sentence, convert_to_tensor=True)
            init = True
        else:
            if sentence not in saved_embeddings.keys():
                embeddings = self.model.encode(
                    sentence,
                    convert_to_tensor=True,
                )
            else:
                embeddings = saved_embeddings[sentence]
        self._save_embeddings(
            {sentence: embeddings}, [sentence], init, saved_embeddings
        )
        return {sentence: embeddings}

    def batch_encode(self, sentences: List[str]) -> Dict[str, torch.Tensor]:
        saved_embeddings = self._load_embeddings()
        init = True if saved_embeddings is None else False
        new_sentences = (
            sentences
            if init
            else list(set(sentences).difference(set(saved_embeddings.keys())))
        )

        new_sentences_embeddings = dict()
        return_embeddings = dict()
        if len(new_sentences) > 0:
            embeddings = self.model.encode(new_sentences, convert_to_tensor=True)
            for idx, sentence in enumerate(new_sentences):
                new_sentences_embeddings[sentence] = embeddings[idx]
        else:
            logger.info("No new sentences found.")

        if init:
            saved_embeddings = {}
            return_embeddings = new_sentences_embeddings.copy()
        else:
            # in this case return_embeddings is the embeddings of the already saved sentences
            return_embeddings = {
                key: saved_embeddings[key] for key in sentences if key in saved_embeddings
            }
            return_embeddings.update(new_sentences_embeddings)

        self._save_embeddings(
            new_sentences_embeddings, new_sentences, init, saved_embeddings
        )

        return return_embeddings

    @staticmethod
    def compare(embeddings1: torch.Tensor, embeddings2: torch.Tensor):
        return util.pytorch_cos_sim(embeddings1, embeddings2)
