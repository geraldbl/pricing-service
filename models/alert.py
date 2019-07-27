import uuid
from typing import Dict
from dataclasses import dataclass, field
from models.item import Item
from models.model import Model
from models.user import User
from libs.mailgun import Mailgun


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)


    def json(self) -> Dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price_limit": self.price_limit,
            "_id": self._id,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}.")
            Mailgun.send_mail(
                ['gerald@CRMSuite.estate'],
                f'Notification for {self.name}',
                f'Your alert {self.name} for the product {self.item.url} has reached a price under {self.price_limit}',
                f'<h1>HELLO</h1> <p>This is wonderful</p> <p>Click <a href="{self.item.url}">here</a> to purchase your item.</p>'
            )

