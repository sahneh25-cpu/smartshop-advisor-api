import importlib
m = importlib.import_module("app.stores.store_data")
stores = []
for name in dir(m):
    if name.isupper() and ("STORE" in name or "STORES" in name):
        obj = getattr(m, name)
        if isinstance(obj, list):
            for x in obj:
                if isinstance(x, dict) and "slug" in x:
                    stores.append(x["slug"])
        elif isinstance(obj, dict) and "slug" in obj:
            stores.append(obj["slug"])

if not stores:
    print("NO_STORES_FOUND")
else:
    from collections import Counter
    c = Counter(stores)
    dups = [k for k,v in c.items() if v>1]
    print("TOTAL_SLUGS:", len(stores))
    print("UNIQUE_SLUGS:", len(c))
    print("DUPLICATES:", dups if dups else "NONE")
