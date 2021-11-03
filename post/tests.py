from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from post.models import Post, Comment
from users.models import UserProfile
from faker import Faker

faker = Faker()

# create a user in the db
def add_user_to_db():
    new_user = UserProfile.objects.create(
                                first_name= faker.first_name(),
                                last_name= faker.last_name(),
                                email= faker.email(),
                                avatar=faker.url(),
                                phone=faker.word()
                                )
    new_user.save()

# add a new post to db
def add_post_to_db():
    a_post = Post.objects.create(createdBy= UserProfile.objects.get(pk=1),
                                title= faker.word(),
                                body= faker.text(),
                                picture= faker.url()
                                )
    a_post.save()

# add a new comment to a post
def add_comment_to_db():
    a_comment = Comment.objects.create(createdBy=UserProfile.objects.get(pk=1),
                                        post = Post.objects.get(pk=1),
                                        body = faker.text() 
                                        )
    a_comment.save()


class PostTest(APITestCase):
    """
    This test class contains all CRUD operations on Post objects
    """

    def test_create_post(self):
        """
        Ensure we can create a new post object.
        """
        # add a user to the dabase
        add_user_to_db()
        # get url for creating a post
        url = reverse('post-list')
        data = {
            'createdBy':1,
            'title': faker.word(),
            'body': faker.text(),
            'picture': faker.url()
            }
        # create new post
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post(self):
        """
        Ensure we can get post instances from db.
        """
        # add a user to the database
        add_user_to_db()
        # add first predefined post
        add_post_to_db()
        # add second predefined post
        add_post_to_db()
        # Get url for getting list of posts
        url = reverse('post-list')
        #  get posts
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(Post.objects.count(), len(response.data))

    def test_get_detail_post(self):
        """
        Get detailed info of a post instance
        """
        add_user_to_db()
        add_post_to_db()
        url = reverse('post-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

    def test_update_post(self):
        """
        Update a post instance
        """
        # add a user instance
        add_user_to_db()
        # add a post instance
        add_post_to_db()
        new_body = faker.text()
        data = {
            'createdBy':1,           
            'body': new_body,
            }
        # get url for updating post
        url = reverse('post-detail', args=[1])
        # update post
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], new_body)

    def test_delete_post(self):
        """
        Delete a post instance
        """
        # add a user instance
        add_user_to_db()
        # add a post instance
        add_post_to_db()
        # url for delete post
        url = reverse('post-detail', args=[1])
        # delete request
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentTest(APITestCase):
    """
    This test class contains all CRUD operations on Comments objects
    """
    def test_add_comment(self):
        # add a user instance
        add_user_to_db()
        # add a post instance
        add_post_to_db()
        # comment data
        data = {
            'body': faker.text(),
            'post': 1,
            'createdBy': 1
        }
        # get url for commenting on a post
        url = reverse('comment-list', args=[1])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_comment(self):
        # add a user instance
        add_user_to_db()
        # add a post instance
        add_post_to_db()
        # add comment to post
        add_comment_to_db()
        # get url for deleting comment
        url = reverse('comment-detail', args=[1,1]) # args=[1,1] consist of post id and comment id
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_comment(self):
        # add a user instance
        add_user_to_db()
        # add a post instance
        add_post_to_db()
        # add comment to post
        add_comment_to_db()
        # new data to update
        new_body = faker.text()
        data = {
            'createdBy':1,
            'post':1,
            'body': new_body
        }
        # get url for deleting comment
        url = reverse('comment-detail', args=[1,1]) # args=[1,1] consist of post id and comment id
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], new_body)



