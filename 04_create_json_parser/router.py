from views import Router

class Route:
    def __init__(self) -> None:
        self.router = Router()
    def return_function(self, path, params=None):
        print(f'Executing return_function with path: {path}')
        routes = {
            '/hello': lambda : self.router.hello_function(),
            '/about': lambda: self.router.about_function(params),
        }
        response = routes.get(path, lambda :'404 Not Found')()
        return response