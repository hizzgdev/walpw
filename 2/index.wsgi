from app.web.root import root as app
import sae

application = sae.create_wsgi_app(app)
