from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from lesson.models import Lesson
from users.tests import UserModelTestCase


# Create your tests here.
class LessonCreateModelTestCase(APITestCase):
    def setUp(self) -> None:
        # Создание объектов Lesson
        self.lesson_1 = Lesson.objects.create(
            title='Python',
            description='Язык программирования. Помогаем с трудоустройством.',
            url_video='https://youtube.com/example12345'
        )
        self.lesson_1.save()

        self.lesson_2 = Lesson.objects.create(
            title='Математика',
            description='Осваиваем точную науку с нуля.',
            url_video='https://youtube.com/example6789'
        )
        self.lesson_2.save()

        # Данные для создания курса
        self.lesson_create_data = {
            'title': 'SQL',
            'description': 'Разбираемся с SQL-запросами',
            'url_video': 'https://youtube.com/example12345'
        }

        # Данные для обновления курса
        self.lesson_update_data = {
            'title': 'SQL 2.0',
            'description': 'С нуля до профи',
            "url_video": 'https://youtube.com/example12345'
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


class LessonTestCase(LessonCreateModelTestCase, UserModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.lesson_create_url = '/lesson/create_lesson/'
        self.lesson_list_url = '/lesson/'
        self.lesson_detail_url = f'/lesson/{self.lesson_1.pk}/'
        self.lesson_update_url = f'/lesson/update/{self.lesson_1.pk}/'
        self.lesson_delete_url = f'/lesson/delete/{self.lesson_1.pk}/'

        # Добавление пользователей к созданным урокам
        self.lesson_1.user_lesson = self.user_test
        self.lesson_1.save()
        self.lesson_2.user_lesson = self.user_2
        self.lesson_2.save()

    def test_user_cannot_create_lesson_without_authentication(self):
        """Только авторизованные пользователи могут создавать объекты Lesson."""

        response = self.client.post(
            self.lesson_create_url,
            self.lesson_create_data,
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

    def test_user_can_create_lesson_correctly(self):
        """Авторизованные пользователи могут создавать объекты Lesson. К тому же, создателем текущего объекта будет
        авторизованный пользователь."""

        response = self.client.post(
            self.lesson_create_url,
            self.lesson_create_data,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.count() == 3
        )

        self.assertEqual(
            Lesson.objects.select_related('user_lesson').get(title='SQL').user_lesson.email,
            'test@test.com'
        )

    def test_user_cannot_add_invalid_url_video(self):
        """Пользователи не могут указывать некорректные ссылки на видеоматериалы."""

        response = self.client.post(
            self.lesson_create_url,
            {
                'title': 'SQL',
                'description': 'Разбираемся с SQL-запросами',
                'url_video': 'qwdqwdqwq'
            },
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'url_video': {
                    'invalid_url': 'Некорректная ссылка на видеоматериал.'
                }
            }
        )

    def test_user_cannot_add_url_domain_not_is_youtube(self):
        """Пользователи могут размещать видеоматериалы только на видеохостинге <YouTube>."""

        response = self.client.post(
            self.lesson_create_url,
            {
                'title': 'SQL',
                'description': 'Разбираемся с SQL-запросами',
                'url_video': 'www.google.com'
            },
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'url_video': {
                    'invalid_domain': 'Видеоматериалы должны быть размещены на видеохостингe <Youtube>.'
                }
            }
        )

    def test_user_can_get_lessons_correctly(self):
        """Авторизованные пользователи могут просматривать информацию только о тех уроках, чьими владельцами
        они являются."""

        self.assertTrue(
            Lesson.objects.count() == 2
        )

        response = self.client.get(
            self.lesson_list_url,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            response.json().get('count') == 1
        )

    def test_user_cannot_get_lesson_without_authentication(self):
        """Только авторизованные пользователи могут просматривать информацию об уроках."""

        response = self.client.get(
            self.lesson_list_url,
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

    def test_user_cannot_get_detail_lesson_another_user(self):
        """Пользователи не могут просматривать информацию о чужих уроках."""

        response = self.client.get(
            self.lesson_detail_url,
            headers=self.headers_user_2,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_cannot_update_lesson_without_authentication(self):
        """Пользователи не могут изменять информацию об уроках без авторизации."""

        response = self.client.patch(
            self.lesson_update_url,
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

    def test_user_cannot_update_lesson_another_user(self):
        """Пользователи не могут изменять информацию о чужих уроках."""

        response = self.client.patch(
            self.lesson_update_url,
            headers=self.headers_user_2,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_can_update_lesson_correctly(self):
        """Авторизованные пользователи могут изменять информацию об уроках, владельцами которых они являются."""

        response = self.client.patch(
            self.lesson_update_url,
            {
                'title': 'Python 1',
                'description': 'Язык программирования. Помогаем с трудоустройством.',
                'url_video': 'https://youtube.com/example12345'
            },
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            response.json().get('title') == 'Python 1'
        )

    def test_user_cannot_update_lesson_with_invalid_url(self):
        """Авторизованные пользователи не могут изменять ссылки на видеоматериалы в объектах Lesson на
        некорректные."""

        response = self.client.patch(
            self.lesson_update_url,
            {
                'title': 'Python 1',
                'description': 'Язык программирования. Помогаем с трудоустройством.',
                'url_video': 'example12345'
            },
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'url_video': {
                    'invalid_url': 'Некорректная ссылка на видеоматериал.'
                }
            }
        )

    def test_user_cannot_update_lesson_url_domain_not_youtube(self):
        """Авторизованные пользователи не могут изменять ссылки на видеоматериалы, которые размещены не на видеохостинге
        <YouTube>."""

        response = self.client.patch(
            self.lesson_update_url,
            {
                'title': 'Python 1',
                'description': 'Язык программирования. Помогаем с трудоустройством.',
                'url_video': 'www.google.com'
            },
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'url_video': {
                    'invalid_domain': 'Видеоматериалы должны быть размещены на видеохостингe <Youtube>.'
                }
            }
        )

    def test_user_cannot_delete_lesson_without_authentication(self):
        """Пользователи не могут удалять информацию об уроках без авторизации."""

        response = self.client.delete(
            self.lesson_delete_url,
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

    def test_user_cannot_delete_lesson_another_user(self):
        """Пользователи не могут удалять информацию о чужих уроках."""

        response = self.client.delete(
            self.lesson_delete_url,
            headers=self.headers_user_2,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_can_delete_lesson_correctly(self):
        """Авторизованные пользователи могут удалять информацию об уроках, владельцами которых они являются."""

        self.assertTrue(
            Lesson.objects.count() == 2
        )

        response = self.client.delete(
            self.lesson_delete_url,
            headers=self.headers_user_1,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertTrue(
            Lesson.objects.count() == 1
        )