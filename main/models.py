from django.utils.functional import cached_property
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class BaseUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="base_user")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Base Users"

    def __str__(self) -> str:
        return f"{self.user.username}"

    @cached_property
    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    @cached_property
    def username(self) -> str:
        return f"{self.user.username}"

    @cached_property
    def first_name(self) -> str:
        return f'{self.user.first_name}'

    @cached_property
    def last_name(self) -> str:
        return f'{self.user.last_name}'


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    title = models.TextField()
    user = models.ForeignKey(
        BaseUser, on_delete=models.SET_NULL, null=True, related_name="user_questions", db_index=True)
    tags = models.ManyToManyField(Tag, related_name="question_tags")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}"

    @cached_property
    def upvotes(self):
        return self.question_votes.filter(type=Vote.UPVOTE).count()

    @cached_property
    def downvotes(self):
        return self.question_votes.filter(type=Vote.DOWNVOTE).count()


class Answer(models.Model):
    answer = models.TextField()
    user = models.ForeignKey(
        BaseUser, on_delete=models.SET_NULL, null=True, related_name="user_answers", db_index=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_answers", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.question.title} : answered by => {self.user.username}"

    @cached_property
    def answered_by(self):
        return self.user.username


class Vote(models.Model):
    UPVOTE, DOWNVOTE = ("UPVOTE", "DOWNVOTE")

    vote_choices = ((UPVOTE, _("UPVOTE")), (DOWNVOTE, _("DOWNVOTE")))

    type = models.CharField(max_length=8, choices=vote_choices)
    user = models.ForeignKey(
        BaseUser, on_delete=models.SET_NULL, null=True, related_name="user_votes")
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="answer_votes", null=True, blank=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_votes", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "user", "question"], name="question_vote_constraints"),
            models.UniqueConstraint(
                fields=["type", "user", "answer"], name="answer_vote_constraints")
        ]

    def __str__(self) -> str:
        return f"Type: {self.type} || User: {self.user.username} || {'Q' if self.question else 'A'}: {self.question.title if self.question else self.answer.answer}"
