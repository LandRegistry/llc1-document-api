FROM hmlandregistry/dev_base_python_flask:3

RUN yum install -y postgresql-devel

ENV APP_NAME=llc1-document-api \
    LOG_LEVEL="DEBUG" \
    PDF_GENERATION_API="http://pdf-generation-api:8080/v1.0/llc1" \
    PDF_GENERATION_API_ROOT="http://pdf-generation-api:8080" \
    STORAGE_API="http://storage-api:8080/v1.0/storage" \
    SQL_HOST="postgres" \
    SQL_DATABASE="llc1_document_api_db" \
    SQL_PASSWORD="password" \
    APP_SQL_USERNAME="llc1_document_api_db_user" \
    SQL_USE_ALEMBIC_USER="false" \
    ALEMBIC_SQL_USERNAME="alembic_user" \
    MAX_HEALTH_CASCADE=6 \
    AUTHENTICATION_API_URL="http://dev-search-authentication-api:8080/v2.0" \
    AUTHENTICATION_API_ROOT="http://dev-search-authentication-api:8080" \
    STORAGE_API_ROOT="http://storage-api:8080" \
    REPORT_API_SQL_USERNAME="report_api_db_user" \
    REPORT_API_SQL_PASSWORD="password" \
    SQLALCHEMY_POOL_RECYCLE="3300" 

ADD requirements_test.txt requirements_test.txt
ADD requirements.txt requirements.txt

RUN pip3 install -q -r requirements.txt && \
    pip3 install -q -r requirements_test.txt
