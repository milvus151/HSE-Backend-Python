from models.comment import Comment
from models.user import User

def filter_comments_by_author(comments: list[Comment], author: User) -> list[Comment]:
    needed_comments = []
    for comment in comments:
        if comment.author_id == author.id:
            needed_comments.append(comment)
    return needed_comments