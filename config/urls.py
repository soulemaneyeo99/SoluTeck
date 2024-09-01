from django.contrib import admin  
from django.urls import path, include  
from django.conf import settings  
from django.conf.urls.static import static  
from django.views import defaults as default_views  

admin.site.site_header = "Dj-LMS Admin"  

urlpatterns = [  
    path("jet/", include("jet.urls", "jet")),  # URLS Django JET  
    path(  
        "jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")  
    ),  # URLS dashboard Django JET  
    path("", include("core.urls")),  
    path("comptes/", include("accounts.urls")),  # URL des comptes  
    path("programmes/", include("course.urls")),  # URL des programmes  
    path("resultats/", include("result.urls")),  # URL des résultats  
    path("recherche/", include("search.urls")),  # URL de recherche  
    path("quiz/", include("quiz.urls")),  # URL du quiz  
    path("paiements/", include("payments.urls")),  # URL des paiements  
    path("comptes/api/", include("accounts.api.urls", namespace="accounts-api")),  # URL API des comptes  
    path("admin/", admin.site.urls),  
]  

if settings.DEBUG:  
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

if settings.DEBUG:  
    # Cela permet de déboguer les pages d'erreur pendant le développement, il suffit de visiter  
    # ces URL dans le navigateur pour voir à quoi ressemblent ces pages d'erreur.  
    urlpatterns += [  
        path(  
            "400/",  
            default_views.bad_request,  
            kwargs={"exception": Exception("Mauvaise demande !")},  
        ),  
        path(  
            "403/",  
            default_views.permission_denied,  
            kwargs={"exception": Exception("Permission refusée")},  
        ),  
        path(  
            "404/",  
            default_views.page_not_found,  
            kwargs={"exception": Exception("Page non trouvée")},  
        ),  
        path("500/", default_views.server_error),  
    ]