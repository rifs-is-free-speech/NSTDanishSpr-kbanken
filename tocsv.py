import os
import json
import pandas
import regex as re
from num2words import num2words

def prepare_text(transcripts):
    if isinstance(transcripts, str):
        transcripts = [transcripts]
    transcripts = [line.strip() for line in transcripts]
    transcripts = [line + "." if not line.endswith(".") else line for line in transcripts]
    transcripts = " ".join(transcripts)
    transcripts = re.sub('[\,\?\!\-\;\:"]', "", transcripts)  # noqa: W605
    transcripts = " ".join(
        [num2words(w, lang="dk", to="year") if w.isdigit() else w for w in transcripts.split(" ")]
    )
    transcripts = [line.strip().lower() for line in transcripts.split(".")[:-1]]

    return transcripts

path = "json"
rows = []
for filename in os.listdir(path):
    if filename.endswith(".json"):
        with open(os.path.join(path, filename), 'r') as f:
            data = json.load(f)
            for record in data["val_recordings"]:
                wav = "dk/"+filename.replace(".json", "").split("_")[0]+"/"+filename.replace(".json", "").split("_")[0]+"_"+record["file"].lower().replace(".wav", "")
                row = {"id": wav, "text": prepare_text(record["text"])[0]}
                row.update(data["info"])
                rows.append(row)

df = pandas.DataFrame(rows)
df.to_csv("all.csv", index=False)
