from django.contrib import admin
from blog.models import Blog, Post, Picture


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    user_fieldsets = [(None, {"fields": ("title", "description")})]
    list_display = ["title", "user"]

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not request.user.is_superuser or not form.cleaned_data["user"]:
                obj.user = request.user
                obj.save()
            elif form.cleaned_data["user"]:
                obj.user = form.cleaned_data["user"]
                obj.save()

    def preprocess_list_display(self, request):
        if "user" not in self.list_display:
            self.list_display.insert(self.list_display.__len__(), "user")
        if not request.user.is_superuser:
            if "user" in self.list_display:
                self.list_display.remove("user")

    def changelist_view(self, request, extra_context=None):
        self.preprocess_list_display(request)
        return super().changelist_view(request)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = super().get_fieldsets(request, obj)
            return fieldsets
        return self.user_fieldsets

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            qs = super().get_queryset(request)
            return qs.filter(user=request.user)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    user_fieldsets = [
        (None, {"fields": (("title", "slug"), "description", "body", "date_created")})
    ]
    list_display = ["title", "description", "blog"]
    readonly_fields = ["date_created"]

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not request.user.is_superuser or not form.cleaned_data["blog"]:
                try:
                    obj.blog = Blog.objects.get(user=request.user)
                    obj.save()
                except:
                    pass
            elif form.cleaned_data["blog"]:
                obj.blog = form.cleaned_data["blog"]
                obj.save()

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = super().get_fieldsets(request, obj)
            return fieldsets
        return self.user_fieldsets

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            qs = super().get_queryset(request)
            return qs.filter(blog__user=request.user)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass