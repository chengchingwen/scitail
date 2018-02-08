from typing import Tuple

from overrides import overrides

from allennlp.common.util import JsonDict
from allennlp.data import Instance
from allennlp.service.predictors.predictor import Predictor

@Predictor.register('tree_attention')
class TreeAttentionPredictor(Predictor):
    """"Predictor wrapper for the tree attention entailment classifier"""
    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Tuple[Instance, JsonDict]:
        premise = json_dict['premise']
        hypothesis = json_dict['hypothesis']
        hypothesis_structure = json_dict['hypothesis_structure']
        label = json_dict['label']
        instance = self._dataset_reader.text_to_instance(premise, hypothesis, hypothesis_structure,
                                                       label)

        # label_dict will be like {0: "ACL", 1: "AI", ...}
        label_dict = self._model.vocab.get_index_to_token_vocabulary('labels')
        # Convert it to list ["ACL", "AI", ...]
        all_labels = [label_dict[i] for i in range(len(label_dict))]

        return instance#, {"all_labels": all_labels}
