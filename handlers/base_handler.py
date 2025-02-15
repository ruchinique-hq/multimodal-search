import tornado


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def options(self, path):
        self.set_status(204)
        self.finish()
        
    def send_error_response(self, code: int, message: str) -> None:
        self.set_status(code)
        self.write({'message': message})
        self.finish()