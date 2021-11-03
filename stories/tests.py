from django.http import response
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import UserProfile
from stories.models import Story
from faker import Faker

faker = Faker()

# add a user to the userprofile model
def add_user_to_db():
    new_user = UserProfile.objects.create(
                                first_name= faker.first_name(),
                                last_name= faker.last_name(),
                                email= faker.email(),
                                avatar=faker.url(),
                                phone=faker.word()
                                )
    new_user.save()

# add a story to story model
def add_story_to_db():
    a_story = Story.objects.create( title = faker.word(),
                                    body = faker.text(),
                                    image = faker.url(),
                                    createdBy = UserProfile.objects.get(pk = 1)
                                )
    a_story.save()


class StoryTest(APITestCase):
    """
    This class contains tests to all story endpoint provided in the stories app
    """
    def test_get_stories(self):
        # add a user to db
        add_user_to_db()
        # add 3 instances of story object to db
        add_story_to_db()
        add_story_to_db()
        add_story_to_db()
        # obtain get url endpoint
        url = reverse('story-list')
        # make get request to endpoint
        response = self.client.get(url)
        # assert that request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that number of retrieved data is equal to number of instances in db
        self.assertEqual(len(response.data), Story.objects.count())
    
    def test_get_single_story(self):
        # add a user to db
        add_user_to_db()
        # add 3 instances of story object to db
        add_story_to_db()
        add_story_to_db()
        add_story_to_db()
        # obtain get url endpoint
        url = reverse('story-detail', args=[2])  # args=[2], the '2' represent the id of the story to be retrieved
        # make get request to endpoint
        response = self.client.get(url)
        # assert that request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that the id of retrieved story is equal to the id '2' passed as argument to the url
        self.assertEqual(response.data['id'], 2)

    def test_create_new_story(self):
        # add a user to db
        add_user_to_db()
        # create new story object
        data = {
            "title" : faker.word(),
            "body" : faker.text(),
            "image" : faker.url(),
            "createdBy" : 1
        }
        # obtain post url
        url = reverse('story-list')
        # make post request to endpoint
        response = self.client.post(url, data)
        # assert that response status code is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # assert that returned object is same as posted object
        self.assertEqual(response.data['title'], data['title'])

    def test_update_story(self):
        # add a user to db
        add_user_to_db()
        # add 2 stories to db
        add_story_to_db()
        add_story_to_db()
        # create updated story object for story with id = 1
        a_story = Story.objects.get(pk=1)
        data = {
            "id": a_story.id,
            "title": a_story.title,
            "body": faker.text(),
            "createdBy": a_story.createdBy.id
        }
        # obtain post url
        url = reverse('story-detail', args=[1])
        # make post request to endpoint
        response = self.client.put(url, data)
        # assert that response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that returned object is same as posted object
        self.assertEqual(response.data['body'], data['body'])

    def test_delete_story(self):
        # add a user to db
        add_user_to_db()
        # add a story object to db
        add_story_to_db()
        # obtain post url
        url = reverse('story-detail', args=[1])
        # make post request to endpoint
        response = self.client.delete(url)
        # assert that response status code is 204
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # assert that there's no story in the db 
        # self.assertEqual(Story.objects.count, 0)
