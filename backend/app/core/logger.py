import time

from functools import wraps

def login_logger(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        user_data = kwargs.get("userData")
        username = user_data.username if user_data else "Unknown"

        print(f"--- Попытка входа:{username} ---")
        start_time = time.perf_counter()

        try:
           result = await func(*args,**kwargs)
           print(f"--- Успешный вход:{username} ---")
           return result
       
        except Exception as e:
           print(f"--- Ошибка входа для {username} --- {e}")
           raise e
        
        finally:
            end_time = time.perf_counter()
            print(f"Время обработки запроса - {end_time - start_time:.4f}")
            
    return wrapper