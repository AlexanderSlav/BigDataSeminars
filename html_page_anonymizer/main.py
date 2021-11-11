from html_utils import HTMLHandler
from utils import parse_args, dump_results_to_csv, timeit
from presidio_anonymizer import AnonymizerEngine
from bs4.element import Comment
from tqdm import tqdm
from presidio_analyzer import AnalyzerEngine
import os.path as osp
import json

RESULTS_DIR = osp.join(osp.dirname(__file__), "results")


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


@timeit
def anonymize(html_handler):
    per_entity_result = {}
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    for text in tqdm(html_handler.soup.findAll(text=True)[:100]):
        if tag_visible(text):
            analyzer_results = analyzer.analyze(text=str(text), language="en")
            anonymizer_result = anonymizer.anonymize(
                text=str(text),
                analyzer_results=[result for result in analyzer_results]
            )
            if anonymizer_result.text in per_entity_result.keys():
                per_entity_result[anonymizer_result.text].append(str(text))
            else:
                per_entity_result[anonymizer_result.text] = [str(text)]
            text.string.replace_with(anonymizer_result.text)

    return per_entity_result


if __name__ == "__main__":
    args = parse_args()
    html_handler = HTMLHandler(args.link)
    per_entity_result, _ = anonymize(html_handler)
    with open(
            osp.join(RESULTS_DIR, f"{args.output_file}.json"),
            "w",
    ) as file:
        json.dump(per_entity_result, file, indent=4)

    html_handler.dump()
