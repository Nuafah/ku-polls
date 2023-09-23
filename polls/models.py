import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """
    Question class represent their text and publication date
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('end date', null=True, default=None)

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Check if the poll is published or not

        :return: True if the poll is published, False
        if it is not.
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """
        Check if the poll is published and not close yet.

        :return: True if the poll still available,
        False if it is not
        """
        now = timezone.now()
        if self.is_published() and self.end_date is not None:
            return now <= self.end_date
        return self.is_published()


class Choice(models.Model):
    """
    Choice class represent a choice in a question with
    text and vote count.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """Count the votes for this choice"""
        return self.vote_set.count()

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    """Records a Vote of Choice by a User"""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
