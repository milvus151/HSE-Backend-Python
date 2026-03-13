from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_mock_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Post = apps.get_model('posts', 'Post')
    Comment = apps.get_model('posts', 'Comment')

    user1 = User.objects.create(
        username='messi',
        email='messi@gmail.com',
        password=make_password('messi10')
    )
    user2 = User.objects.create(
        username='ronaldo',
        email='ronaldo@yandex.ru',
        password=make_password('ronaldo7')
    )

    post1 = Post.objects.create(
        title='How to win Balon Dior',
        text='First rule: Be the best',
        author=user1
    )
    post2 = Post.objects.create(
        title='How to be the best?',
        text='Be me',
        author=user2
    )

    Comment.objects.create(post=post1, author=user2, text='Thank you for your advice!')
    Comment.objects.create(post=post2, author=user1, text='No, I am the best, ron')

def reverse_mock_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username__in=['messi', 'ronaldo']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_commentlike_postlike'),
    ]
    operations = [
        migrations.RunPython(create_mock_data, reverse_mock_data),
    ]