import logging
from logging.handlers import SMTPHandler

from flask import Flask


_log = logging.getLogger(__name__)


def create_app(settings=None):
    _log.info("Creating app")

    app = Flask(__name__, static_folder='frontend/static',
                template_folder='frontend/templates')
    app.config.from_object('reprof_rest.default_settings')
    if settings:
        app.config.update(settings)
    else:  # pragma: no cover
        app.config.from_envvar('REPROF_REST_SETTINGS')  # pragma: no cover

    # Ignore Flask's built-in logging
    # app.logger is accessed here so Flask tries to create it
    app.logger_name = "nowhere"
    app.logger

    # Configure email logging. It is somewhat dubious to get _log from the
    # root package, but I can't see a better way. Having the email handler
    # configured at the root means all child loggers inherit it.
    from reprof_rest import _log as root_logger
    if not app.debug and not app.testing:  # pragma: no cover
        mail_handler = SMTPHandler((app.config["MAIL_SERVER"],
                                    app.config["MAIL_SMTP_PORT"]),
                                    app.config["MAIL_FROM"],
                                    app.config["MAIL_TO"],
                                    "reprof-rest failed")
        mail_handler.setLevel(logging.ERROR)
        root_logger.addHandler(mail_handler)
        mail_handler.setFormatter(
            logging.Formatter("Message type: %(levelname)s\n" +
                              "Location: %(pathname)s:%(lineno)d\n" +
                              "Module: %(module)s\n" +
                              "Function: %(funcName)s\n" +
                              "Time: %(asctime)s\n" +
                              "Message:\n" +
                              "%(message)s"))
    else:
        root_logger.setLevel(logging.DEBUG)

    # Use ProxyFix to correct URL's when redirecting.
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Register blueprints
    from reprof_rest.frontend.api.endpoints import bp as api_bp
    app.register_blueprint(api_bp)

    return app
