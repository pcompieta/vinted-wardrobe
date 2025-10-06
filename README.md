# Vinted Wardrobe client
Simple python package that uses the Vinted API to export Wardrobe.

## Install
Install the package via pip:
```
pip install vintedwardrobe
```
## Example

```py
from vintedwardrobe import Vinted

vinted = Vinted(locale="it")

items = vinted.wardrobe.dump("your_member_id_here")

for idx, item in enumerate(items, 1):
    print(f"  Processing item {idx}: {item.title} (ID: {item.id})")
    print(f"    Price: {item.price} {item.currency}")
    print(f"    URL: {item.url}")
    # etc.
```
