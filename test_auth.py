#!/usr/bin/env python3

import requests


BASE_URL = "http://localhost:8000/api"

def test_registration():
    """Тестирование регистрации пользователя"""
    print("Тестирование регистрации...")
    
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "SecurePass@9x7",
        "password_confirm": "SecurePass@9x7"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=data)
        print(f"Код статуса: {response.status_code}")
        print(f"Ответ: {response.json()}")
        
        if response.status_code == 201:
            print("Регистрация успешна!")
            return response.json()
        else:
            print("Регистрация не удалась!")
            return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def test_login():

    print("\nТестирование входа...")
    
    data = {
        "email": "test@example.com",
        "password": "SecurePass@9x7"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=data)
        print(f"Код статуса: {response.status_code}")
        print(f"Ответ: {response.json()}")
        
        if response.status_code == 200:
            print("Вход выполнен успешно!")
            return response.json()
        else:
            print("Вход не удался!")
            return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def test_profile(access_token):

    print("\nТестирование доступа к профилю...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
        print(f"Код статуса: {response.status_code}")
        print(f"Ответ: {response.json()}")
        
        if response.status_code == 200:
            print("Доступ к профилю успешен!")
            return True
        else:
            print("Доступ к профилю не удался!")
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def test_logout(access_token, refresh_token):
    """Тестирование выхода из системы"""
    print("\nТестирование выхода...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    data = {
        "refresh": refresh_token
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/logout/", json=data, headers=headers)
        print(f"Код статуса: {response.status_code}")
        print(f"Ответ: {response.json()}")
        
        if response.status_code == 200:
            print("Выход выполнен успешно!")
            return True
        else:
            print("Выход не удался!")
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def main():
    print("Тестирование эндпоинтов аутентификации")
    print("=" * 50)
    
    # Тестирование регистрации
    registration_result = test_registration()
    
    # Тестирование входа
    login_result = test_login()
    
    if login_result and 'access' in login_result:
        access_token = login_result['access']
        refresh_token = login_result['refresh']
        
        # Тестирование защищенного эндпоинта
        test_profile(access_token)
        
        # Тестирование выхода
        test_logout(access_token, refresh_token)
    
    print("\nТестирование завершено!")

if __name__ == "__main__":
    main()
