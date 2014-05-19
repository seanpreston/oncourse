from django.conf.urls import patterns, url

urlpatterns = patterns('oncourse.payments.views',

    # Registration URLs
    url(r'^payments/$', 'index', name='payments-index'),
    url(r'^payments/create/$', 'create_payment', name='payments-create'),
    url(r'^payments/process/$', 'process_payment', name='payments-process'),

)
