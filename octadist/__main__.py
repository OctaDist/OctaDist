import os
import octadist.main

app = octadist.main.OctaDist()
app.start_app()

# Delete icon after closing app
if app.octadist_icon is not None:
    os.remove(app.octadist_icon)

