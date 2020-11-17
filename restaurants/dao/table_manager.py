from restaurants.models.table import Table
from .manager import Manager


class TableManager(Manager):

    @staticmethod
    def create_table(table: Table):
        Manager.create(table=table)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return Table.query.get(id_)
    
    @staticmethod
    def retrieve_by_restaurant_id(restaurant_id):
        Manager.check_none(restaurant_id=restaurant_id)
        return Table.query.filter(Table.restaurant_id==restaurant_id).all()

    @staticmethod
    def update_table(table: Table):
        Manager.update(table=table)

    @staticmethod
    def delete_table(table: Table):
        Manager.delete(table=table)

    @staticmethod
    def delete_table_by_id(id_: int):
        table = TableManager.retrieve_by_id(id_)
        TableManager.delete_table(table)
