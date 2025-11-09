from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import traceback  # 🔴 ADICIONE ESTA LINHA NO TOPO
import sys       # 🔴 ADICIONE ESTA LINHA NO TOPO


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

def create_app(config_object='config.Config'):
    app = Flask(
        __name__, 
        template_folder='templates', 
        static_folder='static'
    )
    app.config.from_object(config_object)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    # register blueprints
    from app.routes.auth import auth
    app.register_blueprint(auth)

    return app

# 🔴 🔴 🔴 ADICIONE ESTE BLOCO NO FINAL DO ARQUIVO 🔴 🔴 🔴
if __name__ == "__main__":
    # Este bloco é para execução local (flask run)
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
else:
    # Este bloco é para o Render (produção)
    try:
        print("🔄 Inicializando aplicação Flask para produção...")
        app = create_app()
        print("✅ Aplicação Flask inicializada com sucesso!")
    except Exception as e:
        print("\n❌❌❌ ERRO FATAL AO INICIALIZAR O APP NO RENDER ❌❌❌", file=sys.stderr)
        print("Detalhes do erro:", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        print("\n💡 DICA: Verifique os logs acima para identificar o problema.", file=sys.stderr)
        sys.exit(1)  # Força a saída com código de erro
