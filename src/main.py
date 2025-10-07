from model import Model
from views import AmicosApp

if __name__ == '__main__':
    model = Model()
    model.init_db()

    amicos_app = AmicosApp()
    amicos_app.set_model(model)
    amicos_app.run()