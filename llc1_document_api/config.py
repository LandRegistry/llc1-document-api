import os
from urllib.parse import quote_plus

FLASK_LOG_LEVEL = os.environ['LOG_LEVEL']
COMMIT = os.environ['COMMIT']
APP_NAME = os.environ['APP_NAME']
PDF_GENERATION_API = os.environ['PDF_GENERATION_API']

MAX_HEALTH_CASCADE = os.environ['MAX_HEALTH_CASCADE']
PDF_GENERATION_API_ROOT = os.environ['PDF_GENERATION_API_ROOT']
AUTHENTICATION_API_URL = os.environ['AUTHENTICATION_API_URL']
STORAGE_API = os.environ['STORAGE_API']
AUTHENTICATION_API_ROOT = os.environ['AUTHENTICATION_API_ROOT']
STORAGE_API_ROOT = os.environ['STORAGE_API_ROOT']

DEPENDENCIES = {
    "pdf-generation-api": PDF_GENERATION_API_ROOT,
    "storage-api": STORAGE_API_ROOT,
    'authentication-api': AUTHENTICATION_API_ROOT
}

SQL_HOST = os.environ['SQL_HOST']
SQL_DATABASE = os.environ['SQL_DATABASE']
SQL_PASSWORD = os.environ['SQL_PASSWORD']
APP_SQL_USERNAME = os.environ['APP_SQL_USERNAME']
ALEMBIC_SQL_USERNAME = os.environ['ALEMBIC_SQL_USERNAME']
REPORT_API_SQL_PASSWORD = os.environ['REPORT_API_SQL_PASSWORD']
REPORT_API_SQL_USERNAME = os.environ['REPORT_API_SQL_USERNAME']

if os.environ['SQL_USE_ALEMBIC_USER'] == 'yes':
    FINAL_SQL_USERNAME = ALEMBIC_SQL_USERNAME
else:
    FINAL_SQL_USERNAME = APP_SQL_USERNAME

SQLALCHEMY_DATABASE_URI = 'postgres://{0}:{1}@{2}/{3}'.format(
    FINAL_SQL_USERNAME, quote_plus(SQL_PASSWORD), SQL_HOST, SQL_DATABASE)
SQLALCHEMY_DATABASE_URI_ALEMBIC = 'postgres://{0}:{1}@{2}/{3}'.format(
    FINAL_SQL_USERNAME, SQL_PASSWORD, SQL_HOST, SQL_DATABASE)
SQLALCHEMY_POOL_RECYCLE = int(os.environ['SQLALCHEMY_POOL_RECYCLE'])

LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            '()': 'llc1_document_api.extensions.JsonFormatter'
        },
        'audit': {
            '()': 'llc1_document_api.extensions.JsonAuditFormatter'
        }
    },
    'filters': {
        'contextual': {
            '()': 'llc1_document_api.extensions.ContextualFilter'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        },
        'audit_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'audit',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'llc1_document_api': {
            'handlers': ['console'],
            'level': FLASK_LOG_LEVEL
        },
        'audit': {
            'handlers': ['audit_console'],
            'level': 'INFO'
        }
    }
}
