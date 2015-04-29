from main.views import *
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^new_user/$', new_user),
    url(r'^user_save/$', user_save),
    url(r'^update_profile/$', update_user),
    url(r'^profile/$', profile),
    url(r'^profile/(\w+)/$', profile_user),
    url(r'^all_user/$', all_user),
    url(r'^save/(\w+)/$', save_profile),
    url(r'^document/$', document),
    url(r'^new_document/$', document_new),
    url(r'^save_document/$', document_save),
  	url(r'^$', start_page_lgoin),
    url(r'^logout/', logout),
    url(r'^document_information/(?P<id_d>\d+)/$', document_information),
    url(r'^document_access/(?P<id_d>\d+)/$', document_access),
    url(r'^access_user/(?P<id_d>\d+)/$', access_user),
    url(r'^access_group/(?P<id_d>\d+)/$', access_group),
    url(r'^document_user_delete/(?P<id_document_user>\d+)/$', delet_document_user),
    url(r'^document_group_delete/(?P<id_document_group>\d+)/$', delet_document_group),
    url(r'^new_versia/(?P<id_d>\d+)/$', new_versia),
    url(r'^save_versia/(?P<id_d>\d+)/$', versia_save),
    url(r'^versia_document/(?P<id_d>\d+)/$', all_versia),
    url(r'^document_delete/(?P<id_d>\d+)/$', delete_document),
    url(r'^matching_new/$', matching_new),
    url(r'^matching_new/(?P<id_matching>\d+)/$', matching_write),
    url(r'^matching_document/(?P<id_matching>\d+)/$', matching_document),
    url(r'^matching_document_save/(?P<id_matching>\d+)/(?P<id_d>\d+)/$', matching_document_save),
    url(r'^matching_user_save/(?P<id_matching>\d+)/$', matching_user_save),
    url(r'^matching_user_delete/(?P<id_matching>\d+)/(?P<login>\w+)/$', matching_user_delete),
    url(r'^matching_document_delete/(?P<id_matching>\d+)/(?P<id_d>\d+)/$', matching_document_delete),
    url(r'^matching_not/(?P<id_matching>\d+)/$', matching_not),
    url(r'^all_matching_user/$', all_matching_user_status),
    url(r'^matching_start/(?P<id_matching>\d+)/$', matching_start),
    url(r'^matching_runing/(?P<id_matching>\d+)/$', matching_user_status),

   
    
    
  

   # url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
	urlpatterns += patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': settings.MEDIA_ROOT}),
	)