AirChat - By SubPyAi

AirChat is a chatting web application made from python, using flask.
It is directed towards making an actually safe and more encrypted messaging service.

Release Notes:
  AirChat 0.1
    - Enabled a basic id login authentication.
    - Established a socket connection using flask-socketio.

  AirChat 0.2
    - More flat UI.
    - Added a neon glower at the header which animates on website start and does glow when a new message pops up.
    - Fixed the ugly looking floating header.
    - Messages are now logged with datetime on the server under static/air.log .
  
  AirChat 1.0
    - No major UI changes
    - Shifted the whole data structure onto mysql (schema @ ./.sqlschema).
    - Enabled password authentication.
    - Uses uuid4 encryption.
    - Created session handling.
    - The server now actually logs events to the logfile.
    - The top header on the chat page now responds to accent color changes and to new messages popping up.
    - This update however does not enable a lot of new features, but was a big structural backend change.

Expected features in the next release:
  - A lot better, customisable and responsive UI.
  - Chat rooms
  - A more customisable server.
  - Datetime support.
