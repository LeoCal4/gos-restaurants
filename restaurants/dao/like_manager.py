from restaurants.dao.manager import Manager
from restaurants.models.like import Like


class LikeManager(Manager):

    @staticmethod
    def create_like(user_id, restaurant_id):
        like = Like(
            liker_id=user_id,
            restaurant_id=restaurant_id
        )
        Manager.create(like=like)

    @staticmethod
    def delete_like(user_id, restaurant_id):
        like = LikeManager.get_like_by_id(user_id, restaurant_id)
        Manager.delete(like=like)

    @staticmethod
    def get_like_by_id(user_id, restaurant_id):
        like = Like.query.filter_by(liker_id=user_id, restaurant_id=restaurant_id).first()
        return like

    @staticmethod
    def like_exists(user_id, restaurant_id):
        return LikeManager.get_like_by_id(user_id, restaurant_id) is not None
