import pytest
from django.urls import reverse
from Users.models import CustomUser as C
from django.contrib.messages import get_messages

@pytest.mark.django_db
def test_login_view_valid(client):
    # Create a test user
    C.objects.create_user(username='testuser', password='password123')

    # Perform a POST request to the login view
    response = client.post(reverse('users:login_user'), {
        'username': 'testuser',
        'password': 'password123'
    })

    # Assert the login was successful
    assert response.status_code == 302  # Redirect to home
    assert response.url == reverse('product_shop:home')

    # Check for the welcome message
    messages = list(get_messages(response.wsgi_request))
    assert any("Welcome testuser!" in str(message) for message in messages)

@pytest.mark.django_db
def test_login_view_invalid(client):
    # Perform a POST request with invalid credentials
    response = client.post(reverse('users:login_user'), {
        'username': 'wronguser',
        'password': 'wrongpassword'
    })

    # Assert the login failed and page is re-rendered
    assert response.status_code == 200
    assert "Invalid username or password." in response.content.decode()

@pytest.mark.django_db
def test_logout_view(client):
    # Create and log in a user
    user = C.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    # Perform a GET request to logout
    response = client.get(reverse('users:logout_user'))

    # Assert the logout was successful
    assert response.status_code == 302  # Redirect to login
    assert response.url == reverse('users:login_user')

    # Check for the logout success message
    messages = list(get_messages(response.wsgi_request))
    assert any("You have been logged out." in str(message) for message in messages)
