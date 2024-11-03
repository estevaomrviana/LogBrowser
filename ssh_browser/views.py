from django.shortcuts import render
from django.views.generic import DetailView, View
import paramiko
from .models import SSHConnection
from .utils import transform_path


class ConnectionView(DetailView):
    model = SSHConnection
    template_name = 'connection/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subfolder = ''
        
        if self.request.GET.get('type') == 'file':
            context['file_content'] = self.get_object().read_file(self.request.GET.get('path'))
            context['file_name'] = self.request.GET.get('path')
        
        if self.request.GET.get('path'):
            subfolder = self.request.GET.get('path')
            context['subfolder'] = subfolder
            context['subfolder_list'] = transform_path(subfolder)

        context['file_list'] = self.get_object().get_file_list(subfolder)
        return context

