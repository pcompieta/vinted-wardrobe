from datetime import datetime, timezone
from pyVinted.requester import requester


class Item:
    def __init__(self, data):
        self.raw_data = data
        self.id = data.get("id")
        self.title = data.get("title")
        self.user_id = data.get("user_id")
        self.is_draft = data.get("is_draft")
        self.is_closed = data.get("is_closed")
        self.is_reserved = data.get("is_reserved")
        self.is_hidden = data.get("is_hidden")
        self.price = data.get("price")
        self.transaction_permitted = data.get("transaction_permitted")
        self.is_processing = data.get("is_processing")
        self.currency = data.get("currency")
        self.item_closing_action = data.get("item_closing_action")
        self.path = data.get("path")
        self.user = data.get("user")
        self.item_alert = data.get("item_alert")
        self.item_alert_type = data.get("item_alert_type")
        self.promoted = data.get("promoted")
        self.is_business_user = data.get("is_business_user")
        self.size = data.get("size")
        self.view_count = data.get("view_count")
        self.can_push_up = data.get("can_push_up")
        self.push_up = data.get("push_up")
        self.can_edit = data.get("can_edit")
        self.stats_visible = data.get("stats_visible")
        self.favourite_count = data.get("favourite_count")
        self.is_favourite = data.get("is_favourite")
        self.url = data.get("url")
        self.service_fee = data.get("service_fee")
        self.total_item_price = data.get("total_item_price")
        self.status = data.get("status")
        self.photos = data.get("photos", [])
        self.brand = data.get("brand")
        self.is_heavy_bulky = data.get("is_heavy_bulky")
        self.item_box = data.get("item_box")

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(('id', self.id))
