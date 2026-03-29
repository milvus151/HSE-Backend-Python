from models.comment import Comment

def get_ordered_comments_by_likes(comments: list[Comment]) -> list[Comment]:
    ordered_comments = comments[:]
    ordered_comments.sort(key=lambda c: c.like_count, reverse=True)
    return ordered_comments

