from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test import tag


User = get_user_model()


class UserTestCasePositive(TestCase):
    def setUp(self):
        self.users = [
            User.objects.create_user(
                email='user1@test.ua',
                first_name='Ivan',
                last_name='Ivanov',
                password='StrongPassword1!'
            ),
            User.objects.create_user(
                email='user2@test.ua',
                first_name='Petr',
                last_name='Petrov',
                password='StrongPassword2!'
            ),
            User.objects.create_user(
                email='user3@test.ua',
                first_name='Anna',
                last_name='Ivanova',
                password='StrongPassword3!'
            )
        ]

    @tag('positive')
    def test_user_create_positive(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 3)

        user = User.objects.get(email='user1@test.ua')
        self.assertEqual(user.first_name, 'Ivan')
        self.assertEqual(user.last_name, 'Ivanov')
        self.assertTrue(user.check_password('StrongPassword1!'))

        user = User.objects.get(email='user2@test.ua')
        self.assertEqual(user.first_name, 'Petr')
        self.assertEqual(user.last_name, 'Petrov')
        self.assertTrue(user.check_password('StrongPassword2!'))

        user = User.objects.get(email='user3@test.ua')
        self.assertEqual(user.first_name, 'Anna')
        self.assertEqual(user.last_name, 'Ivanova')
        self.assertTrue(user.check_password('StrongPassword3!'))


class UserTestCaseNegative(TestCase):
    def test_user_create_with_numeric_password(self):
        with self.assertRaises(ValidationError) as context:
            validate_password("12345678")
        self.assertIn("This password is entirely numeric.", str(context.exception))

    def test_user_create_with_short_password(self):
        with self.assertRaises(ValidationError) as context:
            validate_password("short")
        self.assertIn("This password is too short", str(context.exception))

    def test_user_create_with_common_password(self):
        with self.assertRaises(ValidationError) as context:
            validate_password("password")
        self.assertIn("This password is too common.", str(context.exception))
