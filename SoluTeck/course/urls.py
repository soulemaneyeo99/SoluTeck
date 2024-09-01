from django.urls import path
from .views import *


urlpatterns = [
    # URLs des programmes
    path("", ProgramFilterView.as_view(), name="programs"),
    path("<int:pk>/detail/", program_detail, name="program_detail"),
    path("ajouter/", program_add, name="add_program"),
    path("<int:pk>/modifier/", program_edit, name="edit_program"),
    path("<int:pk>/supprimer/", program_delete, name="program_delete"),
    # URLs des cours
    path("cours/<slug>/detail/", course_single, name="course_detail"),
    path("<int:pk>/cours/ajouter/", course_add, name="course_add"),
    path("cours/<slug>/modifier/", course_edit, name="edit_course"),
    path("cours/supprimer/<slug>/", course_delete, name="delete_course"),
    # URLs d'allocation des cours
    path(
        "cours/assigner/", CourseAllocationFormView.as_view(), name="course_allocation"
    ),
    path(
        "cours/assignés/",
        CourseAllocationFilterView.as_view(),
        name="course_allocation_view",
    ),
    path(
        "cours_assigné/<int:pk>/modifier/",
        edit_allocated_course,
        name="edit_allocated_course",
    ),
    path("cours/<int:pk>/désallouer/", deallocate_course, name="course_deallocate"),
    # URLs de téléchargement de fichiers
    path(
        "cours/<slug>/documentations/télécharger/",
        handle_file_upload,
        name="upload_file_view",
    ),
    path(
        "cours/<slug>/documentations/<int:file_id>/modifier/",
        handle_file_edit,
        name="upload_file_edit",
    ),
    path(
        "cours/<slug>/documentations/<int:file_id>/supprimer/",
        handle_file_delete,
        name="upload_file_delete",
    ),
    # URLs de téléchargement de vidéos
    path(
        "cours/<slug>/tutoriels_vidéo/télécharger/",
        handle_video_upload,
        name="upload_video",
    ),
    path(
        "cours/<slug>/tutoriels_vidéo/<video_slug>/detail/",
        handle_video_single,
        name="video_single",
    ),
    path(
        "cours/<slug>/tutoriels_vidéo/<video_slug>/modifier/",
        handle_video_edit,
        name="upload_video_edit",
    ),
    path(
        "cours/<slug>/tutoriels_vidéo/<video_slug>/supprimer/",
        handle_video_delete,
        name="upload_video_delete",
    ),
    # Inscription aux cours
    path("cours/inscription/", course_registration, name="course_registration"),
    path("cours/abandonner/", course_drop, name="course_drop"),
    path("mes_cours/", user_course_list, name="user_course_list"),
]
