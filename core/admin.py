from django.contrib import admin
from .models import Quiz, MultipleChoiceQuestion, WrittenQuestion, QuizView


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_public", "created_at", "updated_at")
    search_fields = ("title", "owner__username")
    list_filter = ("is_public", "created_at")
    ordering = ("-created_at",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("title", "description", "owner", "is_public")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "created_at", "updated_at")
    search_fields = ("text", "quiz__title")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ('quiz', )
    fieldsets = (
        (None, {"fields": ("text", "quiz", "choices", "correct_answer")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(WrittenQuestion)
class WrittenQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "created_at", "updated_at")
    search_fields = ("text", "quiz__title")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    autocomplete_fields = ("quiz",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("text", "quiz", "answer")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(QuizView)
class QuizViewAdmin(admin.ModelAdmin):
    list_display = ("quiz", "user", "viewed_at")
    search_fields = ("quiz__title", "user__username")
    list_filter = ("viewed_at",)
    ordering = ("-viewed_at",)
    autocomplete_fields = ("quiz",)
    readonly_fields = ("viewed_at",)

    fieldsets = (
        (None, {"fields": ("quiz", "user")}),
        ("Timestamps", {"fields": ("viewed_at",)}),
    )
