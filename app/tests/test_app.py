def test_home(client):
    """Проверяет, что домашняя страница возвращает статус код 200."""
    response = client.get('/')
    assert response.status_code == 200


# def test_login_page(client):
#     """Проверяет, что страница входа доступна и возвращает статус код 200."""
#     response = client.get('/login')
#     assert response.status_code == 200
