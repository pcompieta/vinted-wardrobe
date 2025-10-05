# Vinted Wardrobe Refresher
Simple python package that uses the Vinted API to search new posts.

## Install
Install the package via pip:
```
pip install vinted-wardrobe-refresher
```
## Example

```py
from vinted-wardrobe-refresher import Vinted
vinted = Vinted()

items = vinted.items.wardrobe("https://www.vinted.fr", "143839772")
#returns a list of objects: Item

```
You can access each single Item's attributes as shown here:
```py
item.title
item.id
item.photo
item.brand
item.price
item.url
item.currency
```

