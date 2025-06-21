from django.contrib import admin
from .models import Book, Category, BookImage

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
