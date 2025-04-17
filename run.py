import os
from app import createApp, startProcessQueueService

# Only start the queue *after* the reloader has launched the actual server
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    queue = startProcessQueueService()
else:
    queue = None  # Just a placeholder during the reloader's watcher phase

app = createApp(queue)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)