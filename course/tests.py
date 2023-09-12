from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from course.models import Course, Subscription
from lesson.models import Lesson

from users.tests import UserModelTestCase


# Create your tests here.
class CourseCreateModelTestCase(APITestCase):
    def setUp(self) -> None:
        # Создание объекта Lesson
        self.lesson_object = Lesson.objects.create(
            title='Python',
            description='Язык программирования',
            url_video='https://youtube.com/example12345'
        )

        # Создание объектов модели Course
        self.course_1 = Course.objects.create(
            title='Python-разработчик',
            description='Разработка бекэнда',
            user_course=self.user_test
        )
        self.course_1.lesson.set([self.lesson_object])
        self.course_1.save()

        self.course_2 = Course.objects.create(
            title='Data science',
            description='Работа с данными',
            user_course=self.user_2
        )
        self.course_2.lesson.set([self.lesson_object])
        self.course_2.save()

        # Данные для обновления курса
        self.course_data = {
            'title': 'Python-разработчик 1',
            'description': 'Бекэнд',
            "lesson": [
                {
                    "title": "Python",
                    "description": "Язык программирования",
                    "url_video": "https://youtube.com/example12345"
                }
            ]
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


class CourseCreateTestCase(UserModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.course_url = '/courses/'

        # Данные для создания курса
        self.course_data = {
            'title': 'Python-разработчик',
            'description': 'Разработка бекэнда',
            'lesson': [
                {
                    'title': 'Python',
                    'description': 'Язык программирования',
                    'url_video': 'https://youtube.com/example12345'
                }
            ],
            'user_course': 'test@test.com'
        }

    def test_user_cannot_create_course_without_authentication(self):
        """Пользователь не может создавать объекты без авторизации."""

        response = self.client.post(
            self.course_url,
            self.course_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_can_create_course_correctly(self):
        """Пользователь может создавать объекты модели Course после авторизации. Если для поля <lesson> не существуют
        объекты модели Lesson, то они будут созданы автоматически. Создателем курса будет тот пользователь, который
        его создал."""

        response = self.client.post(
            self.course_url,
            self.course_data,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            list(response.json().keys()),
            ['id', 'title', 'description', 'count_lesson', 'lesson', 'user_course', 'subscription']
        )

        self.assertTrue(
            Course.objects.all().exists()
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

        creator = Course.objects.get(title='Python-разработчик')
        self.assertEqual(
            creator.user_course.email,
            'test@test.com'
        )

    def test_course_has_unique_title(self):
        """В модели Course находятся объекты с уникальным полем <title>."""

        response_1 = self.client.post(
            self.course_url,
            self.course_data,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response_1.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Course.objects.count(),
            1
        )

        response_2 = self.client.post(
            self.course_url,
            self.course_data,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response_2.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response_2.json(),
            {'title': ['курс с таким название уже существует.']}
        )


class CourseTestCase(UserModelTestCase, CourseCreateModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.course_url = '/courses/'
        self.detail_url = f'/courses/{self.course_1.pk}/'

    def test_user_can_get_course_correctly(self):
        """Пользователи могут получить только те объекты модели Course, чьими владельцами являются."""

        response = self.client.get(
            self.course_url,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            Course.objects.count() == 2,
        )

        self.assertTrue(
            response.json().get('count') == 1
        )

        self.assertEqual(
            response.json().get('results')[0]['user_course'],
            self.user_test.email
        )

    def test_user_can_get_detail_correctly(self):
        """Пользователи могут смотреть инфомацию о тех курсах, которые сами создали."""

        response = self.client.get(
            self.detail_url,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json().get('user_course'),
            self.user_test.email
        )

    def test_user_cannot_get_detail_another_courses(self):
        """Пользователи не могут смотреть курсы, создателем которых они не являются."""

        response = self.client.get(
            self.detail_url,
            headers=self.headers_user_2,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.json(),
            {'detail': "Страница не найдена."}
        )

    def test_user_cannot_get_course_without_authentication(self):
        """Информацию о курсе могут смотреть только авторизованные пользователи."""

        response = self.client.get(
            self.course_url,
            headers=None,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_update_course_without_authentication(self):
        """Пользователи не могут редактировать объекты Course без авторизации."""

        response = self.client.patch(
            self.detail_url,
            self.course_data,
            headers=None,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_can_update_course_correctly(self):
        """После могут редактировать свои объекты Course после авторизации."""

        response = self.client.patch(
            self.detail_url,
            self.course_data,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json().get('title'),
            'Python-разработчик 1'
        )

        self.assertEqual(
            response.json().get('description'),
            'Бекэнд'
        )

    def test_user_cannot_update_course_another_user(self):
        """Пользователи не могут редактировать модели Course других пользователей."""

        response = self.client.patch(
            self.detail_url,
            self.course_data,
            headers=self.headers_user_2,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertTrue(
            {'detail': 'Страница не найдена.'}
        )

    def test_user_can_delete_course_correctly(self):
        """Пользователи могут удалять свои курсе после авторизации."""

        self.assertTrue(
            Course.objects.count() == 2
        )

        response = self.client.delete(
            self.detail_url,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertTrue(
            Course.objects.count() == 1
        )

    def test_user_cannot_delete_course_another_user(self):
        """Пользователи не могут удалять курсы других пользователей"""

        self.assertTrue(
            Course.objects.count() == 2
        )

        response = self.client.delete(
            self.detail_url,
            headers=self.headers_user_2,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertTrue(
            Course.objects.count() == 2
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Страница не найдена.'}
        )


class SubscriptionCreateTestCase(UserModelTestCase, CourseCreateModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.subscription_url = '/courses/create_subscription/'
        self.course_url = '/courses/'

        # Получение данные для создания подписки
        self.subscription_data = {
            'course': self.course_1.title,
            'user': self.user_test.email
        }

    def test_user_can_create_subscription_correctly(self):
        """Авторизованные пользователи могут создавать подписки по названию курса и по email пользователя."""

        response = self.client.post(
            self.subscription_url,
            self.subscription_data,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Subscription.objects.count() == 1
        )

    def test_user_cannot_create_subscription_without_existing_course(self):
        """Пользователи не могут создавать подписки без существующего курса."""

        response = self.client.post(
            self.subscription_url,
            {'course': 'Меня нет', 'user': 'test@test.com'},
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'course': ['Объект с title=Меня нет не существует.']}
        )

    def test_user_cannot_create_subscription_without_authentication(self):
        """Пользователи не могут создавать подписки без авторизации."""

        response = self.client.post(
            self.subscription_url,
            self.subscription_data,
            headers=None,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_can_create_subscription_without_user(self):
        """Пользователи могут создавать подписки без указания пользователя. В этом случае пользователь будет присвоен
        автоматически."""

        response = self.client.post(
            self.subscription_url,
            {'course': 'Data science'},
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json().get('user')['email'],
            'test@test.com'
        )

    def test_user_has_flag_if_has_subscription(self):
        response_subscription = self.client.post(
            self.subscription_url,
            self.subscription_data,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response_subscription.status_code,
            status.HTTP_201_CREATED
        )

        response_course_test_user = self.client.get(
            self.course_url,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response_course_test_user.status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            response_course_test_user.json().get('results')[0]['subscription']
        )

        response_course_user_2 = self.client.get(
            self.course_url,
            headers=self.headers_user_2,
            format='json'
        )

        self.assertEqual(
            response_course_user_2.status_code,
            status.HTTP_200_OK
        )

        self.assertFalse(
            response_course_user_2.json().get('results')[0]['subscription']
        )


class UnsubscribeTestCase(UserModelTestCase, CourseCreateModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Создание подписки для тестового пользователя
        self.subscription_test_user = Subscription.objects.create(
            course=self.course_1,
            user=self.user_test
        )
        self.subscription_test_user.save()

        # Создание подписки для второго пользователя
        self.subscription_user_2 = Subscription.objects.create(
            course=self.course_1,
            user=self.user_2
        )
        self.subscription_user_2.save()

        # Получение маршрутов
        self.unsubscribe_url = f'/courses/unsubscribe/{self.subscription_test_user.pk}/'
        self.course_url = f'/courses/{self.course_1.pk}/'

    def test_user_cannot_unsubscribe_without_authentication(self):
        """Пользователи не могут отписаться от подписки без авторизации."""

        response = self.client.patch(
            self.unsubscribe_url,
            headers=None,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_user_cannot_unsubscribe_from_another_subscription(self):
        """Пользователи не могут отписаться от подписки, на которую не подписаны."""

        response = self.client.patch(
            self.unsubscribe_url,
            headers=self.headers_user_2,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Страница не найдена.'}
        )

    def test_user_can_unsubscribe_correctly(self):
        """Пользователи могут отписаться от подписки, которую создали."""

        # Проверка, что пользователь имеет подписку на текущий курс
        response_course = self.client.get(
            self.course_url,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response_course.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response_course.json().get('user_course'),
            'test@test.com'
        )

        self.assertTrue(
            response_course.json().get('subscription')
        )

        # Совершаем отписка пользователя от текущего курса
        response = self.client.patch(
            self.unsubscribe_url,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка, что пользователь не имеет подписку на текущий курс
        response_after = self.client.get(
            self.course_url,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response_after.status_code,
            status.HTTP_200_OK
        )

        self.assertFalse(
            response_after.json().get('subscription')
        )
