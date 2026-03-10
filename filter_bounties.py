import json
data = json.load(open('C:/Users/corra/Desktop/bounties.json'))
for item in data:
    repo = item['repository']['nameWithOwner']
    skip = ['rustchain', 'la-tanda', 'roxonn']
    if any(s in repo.lower() for s in skip):
        continue
    print(f"{repo} | {item['title'][:80]}")
    print(f"  {item['url']}")
