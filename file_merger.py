import glob
import json

if __name__ == "__main__":
    total_count = len(glob.glob1("./", "output_*.json"))
    merge_profile = []

    for i in range(1, total_count + 1):
        filename = "./output_{}.json".format(i)
        with open(filename, "r", encoding="utf8") as f:
            merge_profile.extend(json.load(f))

    out = json.dumps(merge_profile, ensure_ascii=False)
    with open("./merge_output.json", "w", encoding="utf8") as f:
        f.write(out)