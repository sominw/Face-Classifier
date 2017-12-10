import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/precog_task/precog_task")

from precog_task import app as application
application.secret_key = 'for_precog_task'
