from apps.posts.models import Post, Community
from apps.posts.vk_publisher import (
    get_photo_server_link, save_photo_on_vk_server,
    upload_photo_to_server, post_to_vk_wall
)
from vk_poster.celery import app
from urllib.request import urlopen


@app.task()
def post_to_vk():
    for community in Community.objects.all():
        post = Post.objects.filter(is_posted=False, vk_community=community).first()
        if post:
            try:
                token = post.vk_community.token.pk
                group_id = post.vk_community.pk

                vk_link = get_photo_server_link(
                    post.vk_community.token.pk,
                    post.vk_community.pk
                )

                img = urlopen(post.url).read()
                upload_response = upload_photo_to_server(vk_link, img)

                photo_id, owner_id = save_photo_on_vk_server(
                    token,
                    group_id,
                    upload_response['photo'],
                    upload_response['hash'],
                    upload_response['server']
                )

                post_to_vk_wall(owner_id, group_id, photo_id, token, post.title)
            finally: # TODO refactor this with normal flow
                post.is_posted = True
                post.save()
