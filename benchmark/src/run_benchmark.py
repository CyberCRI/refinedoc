import json

from refinedoc.refined_document import RefinedDocument

dt_syntetic_0 = json.loads(open("../dataset/syntetic_chat_gpt_28_01_26.json").read())


class BenchMarkData:
    def __init__(self, document: list[list[str]], ground_truth: dict):
        self.document = document
        self.ground_truth_headers = ground_truth["headers"]
        self.ground_truth_footers = ground_truth["footers"]
        self.ground_truth_body = ground_truth["body"]


def main():
    headers_correct = 0
    footers_correct = 0
    body_correct = 0
    for dt in dt_syntetic_0:
        print(f"------------------- {dt['id']} ------------------")
        bm_data = BenchMarkData(document=dt["document"], ground_truth=dt["truth"])
        refined_doc = RefinedDocument(content=bm_data.document)
        refined_content = refined_doc.content
        if refined_content.headers == bm_data.ground_truth_headers:
            headers_correct += 1
        else:
            print(f"Expected headers: {bm_data.ground_truth_headers}")
            print(f"Headers returned : {refined_content.headers}")
        if refined_content.footers == bm_data.ground_truth_footers:
            footers_correct += 1
        else:
            print(f"Expected footers: {bm_data.ground_truth_footers},")
            print(f"Footers returned : {refined_content.footers}")
        if refined_content.body == bm_data.ground_truth_body:
            body_correct += 1
    total = len(dt_syntetic_0)
    print(
        f"Headers correct: {headers_correct}/{total} ({(headers_correct/total)*100:.2f}%)"
    )
    print(
        f"Footers correct: {footers_correct}/{total} ({(footers_correct/total)*100:.2f}%)"
    )
    print(f"Body correct: {body_correct}/{total} ({(body_correct/total)*100:.2f}%)")


if __name__ == "__main__":
    main()
