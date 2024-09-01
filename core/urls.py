from django.urls import path

from .views import (
    home_view,
    post_add,
    edit_post,
    delete_post,
    session_list_view,
    session_add_view,
    session_update_view,
    session_delete_view,
    semester_list_view,
    semester_add_view,
    semester_update_view,
    semester_delete_view,
    dashboard_view,
)

urlpatterns = [
    # URL des comptes
    path("", home_view, name="home"),
    path("ajouter_article/", post_add, name="add_item"),
    path("article/<int:pk>/modifier/", edit_post, name="edit_post"),
    path("article/<int:pk>/supprimer/", delete_post, name="delete_post"),
    path("session/", session_list_view, name="session_list"),
    path("session/ajouter/", session_add_view, name="add_session"),
    path("session/<int:pk>/modifier/", session_update_view, name="edit_session"),
    path("session/<int:pk>/supprimer/", session_delete_view, name="delete_session"),
    path("semestre/", semester_list_view, name="semester_list"),
    path("semestre/ajouter/", semester_add_view, name="add_semester"),
    path("semestre/<int:pk>/modifier/", semester_update_view, name="edit_semester"),
    path("semestre/<int:pk>/supprimer/", semester_delete_view, name="delete_semester"),
    path("tableau_de_bord/", dashboard_view, name="dashboard"),
]
