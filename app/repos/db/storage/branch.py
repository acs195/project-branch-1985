"""This is the repository module for branches"""

from typing import Optional

from app.core.logger import logger
from app.repos.db.models.branch import BranchDDB
from app.repos.db.storage.base import BaseRepo


class BranchRepo(BaseRepo):
    """This handles branch repository operations"""

    MODEL = BranchDDB
    TABLE_NAME = "branch-project-1985"
    PK_NAME = "branch_id"
    PK_TEMPLATE = "BRANCH#{}"
    SK_NAME = "data"
    SK_TEMPLATE = "METADATA"
    INDEX_BILL_ACCT = "bill_acct"
    SK_TEMPLATE_BILL_ACCT = "BILL_ACCT#{}"

    def get_by_bill_acct(self, bill_acct_id: str) -> Optional[BranchDDB]:
        """Get object by billing account id from DB"""
        # TODO: this is not finished
        try:
            lookup_key = {
                self.INDEX_BILL_ACCT: {"S": self.SK_TEMPLATE_BILL_ACCT.format(bill_acct_id)},
            }
            response = self.db.query(
                TableName=self.TABLE_NAME, IndexName=self.INDEX_BILL_ACCT, Key=lookup_key
            )
            item = response.get("Item")
            if item:
                parsed_item = {key: list(value.values())[0] for key, value in item.items()}
                return self.MODEL(**parsed_item)
            else:
                return None
        except Exception as e:
            logger.error(f"Error on get item: {e}")
            raise

    def update(self, id: str, obj_update: dict) -> BranchDDB:
        """Update an object into the DB"""
        bill_acct = obj_update.pop("bill_acct", None)
        if obj_update:
            super().update(id, obj_update)
        if bill_acct:
            self.create_bill_acct(id, bill_acct)

        return self.get(id)

    def create_bill_acct(self, id: str, bill_acct: str) -> None:
        """Create an object into the DB"""
        try:
            item_template = {
                self.PK_NAME: {"S": self.PK_TEMPLATE.format(id)},
                self.SK_NAME: {"S": self.SK_TEMPLATE_BILL_ACCT.format(bill_acct)},
            }
            self.db.put_item(TableName=self.TABLE_NAME, Item=item_template)
        except Exception as e:
            logger.error(f"Error on create item: {e}")
            raise
