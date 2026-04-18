from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='Managers').exists():
            return reverse_lazy('dashboard')

        elif user.groups.filter(name='Mechanics').exists():
            return reverse_lazy('job_list')

        return reverse_lazy('login')