from locust import HttpUser, task, between, events
import json


# Добавляем опциональные аргументы командной строки.
# Пример запуска: locust -f locustfile.py --method POST --payload '{"key": "value"}' --headers '{"Content-Type": "application/json"}'
# Также эти аргументы можно прописывать в WEB-интерфейсе.
@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--method", type=str, choices=["GET", "POST"], default="GET")
    parser.add_argument("--payload", type=str, default="")
    parser.add_argument("--headers", type=str, default="")


class ExampleUser(HttpUser):

    # Метод `__init__` вызывается перед запуском каждого пользователя.
    # В нем можно инициализировать переменные, которые будут доступны во всех тасках данного пользователя.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если метод GET, то payload не передаем.
        if self.environment.parsed_options.method == "GET":
            self.environment.parsed_options.payload = None

        # Создаем переменную headers, которая будет содержать заголовки запроса.
        # Переменная имеет тип dict, то есть словарь.
        self.headers = {}
        # Если переданы заголовки, то добавляем их в переменную headers.
        if self.environment.parsed_options.headers:
            self.headers.update(json.loads(self.environment.parsed_options.headers))

        # Создаем переменную payload, которая будет содержать тело запроса.
        # Переменная payload также имеет тип dict.
        self.payload = json.loads(
            # Обратите внимание, как мы пользуемся конструкцией "if else" для передачи значения None, если payload пустой.
            # Да, можно использовать "if else" и нормально:
            #   if:
            #       self.environment.parsed_options.payload
            #   then:
            #       json.loads(self.environment.parsed_options.payload)
            #   else:
            #       None
            # Но такой код выглядит сложнее и менее читаемо.
            self.environment.parsed_options.payload) if self.environment.parsed_options.payload else {}

    # А вот и наш таск, который будет выполняться пользователем.
    @task
    def example_task(self):
        # В зависимости от метода запроса, создаем переменную request, которая будет содержать функцию для отправки запроса.
        # Если метод POST, то используем метод post, иначе get
        if self.environment.parsed_options.method == "POST":
            request = self.client.post
        else:
            request = self.client.get

        with request(
                "",
                headers=self.headers,
                json=self.payload,
                catch_response=True
        ) as response:
            self.environment.events.request.fire(**response.request_meta)
