"""
DGIdbのinteractions.tsvをinteractions.jsonlに変換する

$ python convert.py {input} {output}
"""
import argparse
import json
from pathlib import Path

import pandas as pd


def convert_concept_id(concept_id: str) -> dict[str, str] | None:
    if concept_id is None:
        return None
    db_name, db_id = concept_id.split(":")
    return {
        f"{db_name}_id": db_id
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path, help='path to interactions.tsv')
    parser.add_argument('output', type=Path, help='path to interactions.jsonl')
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep='\t')
    df['interaction_score'] = df['interaction_score'].astype(object)
    df = df.where(pd.notnull(df), other=None)
    del df['gene_claim_name']
    del df['gene_name']
    del df['drug_claim_name']
    del df['drug_name']
    del df['approved']
    del df['immunotherapy']
    del df['anti_neoplastic']

    jsonl_data = []
    for _, row in df.iterrows():
        data = row.to_dict()
        data["gene_concept_id"] = convert_concept_id(data["gene_concept_id"])
        data["drug_concept_id"] = convert_concept_id(data["drug_concept_id"])
        jsonl_data.append(json.dumps(data))

    with open(args.output, "w") as f:
        f.write("\n".join(jsonl_data))


if __name__ == '__main__':
    main()
