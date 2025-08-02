from django.contrib import admin
from .models import Book, Category, BookImage, SiteSettings
from django.contrib.auth.models import User, Group
from django.contrib.admin.sites import NotRegistered

# Unregister the default User and Group models to replace them later if needed
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

try:
    admin.site.unregister(Group)
except NotRegistered:
    pass

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 3  # Show 3 extra empty forms for uploading images by default.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the main list view of books
    list_display = ('title', 'author', 'category', 'price')
    # Add a search bar that searches these fields
    search_fields = ('title', 'author', 'description')
    # Add a filter sidebar for these fields
    list_filter = ('category',)
    # Use a searchable dropdown for selecting the category, which is better for many categories
    autocomplete_fields = ['category']
    # Add the ability to upload multiple images directly on the book page
    inlines = [BookImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__',) # Show the full path in the list display
    search_fields = ('name',)

# The BookImage model doesn't need its own separate admin page,
# as it's managed through the BookAdmin inline.
# If you wanted to manage them separately, you would register it like this:
# admin.site.register(BookImage)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Admin interface for site-wide settings.
    Implements singleton pattern - only allows editing the existing settings record.
    """
    list_display = ('site_title', 'hero_title', 'updated_at')
    fields = (
        'cover_image', 
        'site_title', 
        'hero_title', 
        'hero_subtitle',
        'updated_at'
    )
    readonly_fields = ('updated_at',)
    
    def has_add_permission(self, request):
        # Only allow adding if no settings exist yet
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Never allow deletion of settings
        return False
    
    def changelist_view(self, request, extra_context=None):
        # If settings exist, redirect directly to the edit page
        if SiteSettings.objects.exists():
            settings = SiteSettings.objects.first()
            return self.change_view(request, str(settings.pk), extra_context=extra_context)
        return super().changelist_view(request, extra_context=extra_context)
