import datetime
from django.test import TestCase
from .models import Scene, Liker
from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.shortcuts import get_object_or_404
from .utils import get_video_id

class SceneTestCase(TestCase):

    def setUp(self):
        user = User(username='admin', email='admin@website.com')
        user.set_password('Random#18')
        user.save()

        user = get_object_or_404(User, pk=1)
        scene = Scene(url="xzioevairnu", text="Example text")
        scene.user = user
        scene.published = datetime.datetime.utcnow().replace(tzinfo=utc)
        scene.save()

        scene = get_object_or_404(Scene, pk=1)
        liker = Liker()
        liker.scene = scene
        liker.user = user
        liker.save()

    def test_user_exists(self):
        user = get_object_or_404(User, pk=1)
        self.assertTrue(user)
    
    def test_scene_exists(self):
        scene = get_object_or_404(Scene, pk=1)
        self.assertTrue(scene)
    
    def test_liker_exists(self):
        like = get_object_or_404(Liker, pk=1)
        self.assertTrue(like)

    def test_scene_deleted(self):
        scene = get_object_or_404(Scene, pk=1)
        scene.delete()
        try:
            scene = get_object_or_404(Scene, pk=1)
            scene = True
        except:
            scene = False
            
        self.assertFalse(scene)
    
    def test_liker_unliked(self):
        like = get_object_or_404(Liker, pk=1)
        like.delete()
        try:
            like = get_object_or_404(Liker, pk=1)
            like = True
        except:
            like = False

        self.assertFalse(like)

class VideoIdTestCase(TestCase):

    def test_video_parser(self):
        url = "https://www.youtube.com/watch?v=xzioevairnu&ab_channel=Google"
        video_id = get_video_id(url)
        self.assertEqual(len(video_id), 11)
