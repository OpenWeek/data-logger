# Relation des url

URL | GET/POST | HTML | Est redirigé de | Fonction
----|----------|------|-----------------|---------
/   | GET      | index.html
/profile        | GET/POST  | profile.html  | /profile
/project/\<id>  | GET       | project.html  | /ADD/PROJECT
/projects       | GET       | projects.html |
/add/project    | GET/POST  | projects.html |
/project/\<id>/ask/sensor                       | POST      | /               |                           | ask_sensor(id)
/project/\<id>/client/\<client_id>              | GET       |                 | /project/<id>/client/<client_id>/add/sensor | client_show(id, client_id)
/project/\<id>/add/user                         | GET/POST  | addUser.html    |                           | project_add_user(id)
/project/\<id>/add/client                       | GET/POST  |                 | /project/\<id>/add/clien  | project_add_client(id)
/project/\<id>/client/\<client_id>/add/sensor   | GET/POST  | addSensor.html  |
/project/\<id>/edit/user/\<user_id>             | GET/POST  |                 | /project/\<id>/add/user /project/\<id>/edit/user/\<user_id> |  project_edit_user(id, user_id)
/remove/project/\<id>                           |           |                 |                           |
/project/\<id>/remove/user/\<user_id>     | | |
/project/\<id>/remove/client/\<client_id> | | |
/project/\<id>/client/\<client_id>/remove/sensor/<sensor_id> | | |
/admin  | | |
/admin/approve/project/\<project_id> | | |
/admin/reject/project/\<project_id>  | | |
/admin/approve/sensors/project/\<project_id> | | |
/admin/reject/sensors/project/\<project_id>  | | |
/admin/add/user  | post | | | ajoute un utilisateur (dans admin.html)(todo backend)
/logout | | |
