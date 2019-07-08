import logging

logger = logging.getLogger(__name__)


class ApiError:
    base_message = 'An error occurred whilst %s'

    def __init__(self, status_code, action):
        self.status_code = status_code
        self.action = action

        logger.error('An error occurred on the API during the execution of %s' % action)

    def get_error_message(self):
        return self.base_message % self.action


class InternalError:
    base_message = 'An error occurred whilst %s'

    def __init__(self, status_code, details):
        self.status_code = status_code
        self.details = details

        logger.error(self.get_error_message())

    def get_error_message(self):
        return self.base_message % self.details
