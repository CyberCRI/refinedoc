import json
from collections import Counter

from refinedoc.refined_document import RefinedDocument

dt_syntetic_0 = json.loads(open("../dataset/syntetic_chat_gpt_28_01_26.json").read())


class BenchMarkData:
    def __init__(self, document: list[list[str]], ground_truth: dict):
        self.document = document
        self.ground_truth_headers = ground_truth["headers"]
        self.ground_truth_footers = ground_truth["footers"]
        self.ground_truth_body = ground_truth["body"]


def percentage_similarity_list(lst1: list, lst2: list):
    # Convertit chaque sous-liste en tuple pour qu'elles soient hashables
    lst1_tuples = [tuple(x) if isinstance(x, list) else x for x in lst1]
    lst2_tuples = [tuple(x) if isinstance(x, list) else x for x in lst2]
    counter1 = Counter(lst1_tuples)
    counter2 = Counter(lst2_tuples)
    all_keys = set(counter1.keys()) | set(counter2.keys())
    intersection = sum(min(counter1[k], counter2[k]) for k in all_keys)
    union = sum(max(counter1[k], counter2[k]) for k in all_keys)
    if union == 0:
        return 1.0
    return intersection / union


def main():
    headers_scores = []
    footers_scores = []
    body_scores = []
    errors = []
    for dt in dt_syntetic_0:
        bm_data = BenchMarkData(document=dt["document"], ground_truth=dt["truth"])
        refined_doc = RefinedDocument(content=bm_data.document)
        refined_content = refined_doc.content
        header_score = percentage_similarity_list(
            refined_content.headers, bm_data.ground_truth_headers
        )
        footer_score = percentage_similarity_list(
            refined_content.footers, bm_data.ground_truth_footers
        )
        body_score = percentage_similarity_list(
            refined_content.body, bm_data.ground_truth_body
        )
        headers_scores.append(header_score)
        footers_scores.append(footer_score)
        body_scores.append(body_score)
        # Log errors for low similarity
        if header_score < 0.8 or footer_score < 0.8 or body_score < 0.8:
            errors.append(
                {
                    "id": dt["id"],
                    "header_expected": bm_data.ground_truth_headers,
                    "header_pred": refined_content.headers,
                    "footer_expected": bm_data.ground_truth_footers,
                    "footer_pred": refined_content.footers,
                    "body_expected": bm_data.ground_truth_body,
                    "body_pred": refined_content.body,
                    "header_score": header_score,
                    "footer_score": footer_score,
                    "body_score": body_score,
                }
            )
    total = len(dt_syntetic_0)
    mean_headers = sum(headers_scores) / total
    mean_footers = sum(footers_scores) / total
    mean_body = sum(body_scores) / total
    print(f"\n===== Résumé du benchmark =====")
    print(f"Headers similarity moyenne: {mean_headers:.3f}")
    print(f"Footers similarity moyenne: {mean_footers:.3f}")
    print(f"Body similarity moyenne: {mean_body:.3f}")
    print(f"\nNombre de documents testés: {total}")
    if errors:
        print(f"\nExemples d'erreurs (similarité < 0.8):")
        for err in errors[:3]:
            print(f"\n--- Document {err['id']} ---")
            print(f"Header attendu: {err['header_expected']}")
            print(f"Header prédit:  {err['header_pred']}")
            print(f"Score header:   {err['header_score']:.2f}")
            print(f"Footer attendu: {err['footer_expected']}")
            print(f"Footer prédit:  {err['footer_pred']}")
            print(f"Score footer:   {err['footer_score']:.2f}")
            print(f"Body attendu:   {err['body_expected'][:2]} ...")
            print(f"Body prédit:    {err['body_pred'][:2]} ...")
            print(f"Score body:     {err['body_score']:.2f}")
    else:
        print("\nAucune erreur majeure détectée (toutes les similarités >= 0.8)")


if __name__ == "__main__":
    main()
