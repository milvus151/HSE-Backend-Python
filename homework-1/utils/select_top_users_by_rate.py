from models.user import User

def select_top_users_by_rate(users: list[User], top_size: int) -> list[User]:
    users_by_rate = users[:]
    users_by_rate.sort(key=lambda x: x.rate, reverse=True)
    top_users = users_by_rate[:top_size]
    return top_users

