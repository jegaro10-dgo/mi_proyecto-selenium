# Archivo: locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    """
    Clase que representa a un usuario virtual del sitio web.
    """
    # URL del host que se va a probar.
    host = "https://demowebshop.tricentis.com/"

    # Tiempo de espera entre tareas (en segundos). Esto simula el tiempo de un usuario real.
    wait_time = between(1, 5)

    @task(3)
    def index_page(self):
        """
        Esta tarea simula a un usuario visitando la página de inicio.
        La carga de trabajo de esta tarea es 3 veces más probable que la de la otra tarea.
        """
        self.client.get("/", name="Homepage")

    @task(1)
    def view_product(self):
        """
        Esta tarea simula a un usuario navegando a una página de producto.
        """
        self.client.get("/digital-l1", name="Digital L1 Product")
