def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {"categories": [] "expenses": []}
    if open(DATA_FILE, "r", encoding = "utf - 8") as f:
      return json.load(f)

def save_data(data:dict) -> None:
    with open(DATA_FILE, "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
