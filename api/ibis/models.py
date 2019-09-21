from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel

from users.models import User

# TODO: best way to handle this? maybe in settings?
CAT_MAX_LEN = 10
TITLE_MAX_LEN = 50
TX_MAX_LEN = 160
DESC_MAX_LEN = 320


class IbisUser(User):
    class Meta:
        verbose_name_plural = 'ibis user'

    following = models.ManyToManyField(
        'self',
        related_name='follower',
        symmetrical=False,
        blank=True,
    )
    profile_image = models.ImageField(upload_to='profile-photos/%Y/%m/%d/')
    score = models.PositiveIntegerField()

    def __str__(self):
        return '{}{}{}'.format(
            self.first_name,
            ' ' if self.first_name and self.last_name else '',
            self.last_name,
        )


class NonprofitCategory(models.Model):
    class Meta:
        verbose_name_plural = 'nonprofit categories'

    title = models.CharField(max_length=TITLE_MAX_LEN, unique=True)
    description = models.CharField(max_length=DESC_MAX_LEN)

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)


class TransactionCategory(models.Model):
    class Meta:
        verbose_name_plural = 'transaction categories'

    title = models.CharField(max_length=TITLE_MAX_LEN, unique=True)
    description = models.CharField(max_length=DESC_MAX_LEN)

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)


class PrivacyPolicy(models.Model):
    class Meta:
        verbose_name_plural = 'privacy policies'

    title = models.CharField(max_length=TITLE_MAX_LEN, unique=True)
    description = models.CharField(max_length=DESC_MAX_LEN)

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)


class NotificationReason(models.Model):
    title = models.CharField(max_length=TITLE_MAX_LEN, unique=True)
    description = models.CharField(max_length=DESC_MAX_LEN)

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)


class Settings(models.Model):
    class Meta:
        verbose_name_plural = 'settings'

    user = models.OneToOneField(
        IbisUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    follow_privacy = models.ForeignKey(
        PrivacyPolicy,
        related_name='follow_privacy_of',
        on_delete=models.PROTECT,
    )
    transfer_privacy = models.ForeignKey(
        PrivacyPolicy,
        related_name='transfer_privacy_of',
        on_delete=models.PROTECT,
    )
    blocked_users = models.ManyToManyField(
        IbisUser,
        related_name='blocked_user_of',
        blank=True,
    )
    push_notifications = models.ManyToManyField(
        NotificationReason,
        related_name='push_policy_of',
        blank=True,
    )
    email_notifications = models.ManyToManyField(
        NotificationReason,
        related_name='email_policy_of',
        blank=True,
    )

    def __str__(self):
        return 'settings {} ({})'.format(
            self.user.username,
            self.user.id,
        )


class Person(IbisUser):
    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    transaction_to = models.ManyToManyField(
        IbisUser,
        related_name='transaction_from',
        through='Transaction',
        symmetrical=False,
    )


class Nonprofit(IbisUser, TimeStampedModel, SoftDeletableModel):
    class Meta:
        verbose_name = "Nonprofit"

    title = models.CharField(max_length=TITLE_MAX_LEN, unique=True)
    category = models.ForeignKey(
        NonprofitCategory,
        on_delete=models.CASCADE,
    )
    description = models.TextField()
    link = models.TextField()

    donation_to = models.ManyToManyField(
        IbisUser,
        related_name='donation_from',
        through='Donation',
        symmetrical=False,
    )

    def __str__(self):
        return self.title


class Exchange(TimeStampedModel):
    amount = models.PositiveIntegerField()


class Deposit(Exchange):
    user = models.ForeignKey(
        IbisUser,
        on_delete=models.CASCADE,
    )


class Withdrawal(Exchange):
    user = models.ForeignKey(
        Nonprofit,
        on_delete=models.CASCADE,
    )


class Post(TimeStampedModel, SoftDeletableModel):
    user = models.ForeignKey(
        IbisUser,
        on_delete=models.CASCADE,
    )
    description = models.TextField()


class Transfer(Post):
    amount = models.PositiveIntegerField()
    like = models.ManyToManyField(
        IbisUser,
        related_name='likes_transfer',
        blank=True,
    )


class Donation(Transfer):
    target = models.ForeignKey(
        Nonprofit,
        on_delete=models.CASCADE,
    )


class Transaction(Transfer):
    target = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.CASCADE,
    )


class News(Post):
    class Meta:
        verbose_name_plural = 'news'

    title = models.CharField(max_length=TITLE_MAX_LEN)
    link = models.TextField()
    content = models.TextField()
    bookmark = models.ManyToManyField(
        IbisUser,
        related_name='bookmark_for',
        blank=True,
    )
    like = models.ManyToManyField(
        IbisUser,
        related_name='likes_news',
        blank=True,
    )
    header_image = models.ImageField(upload_to='news-photos/%Y/%m/%d/')
    score = models.PositiveIntegerField()

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)


class Event(Post):
    title = models.CharField(max_length=TITLE_MAX_LEN)
    link = models.TextField()
    rsvp = models.ManyToManyField(
        IbisUser,
        related_name='rsvp_for',
        blank=True,
    )
    like = models.ManyToManyField(
        IbisUser,
        related_name='likes_event',
        blank=True,
    )
    date = models.DateTimeField()
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    score = models.PositiveIntegerField()

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)


class Comment(Post):
    parent = models.ForeignKey(
        Post,
        related_name='parent_of',
        on_delete=models.CASCADE,
    )
    vote = models.ManyToManyField(
        IbisUser,
        through='UserCommentVote',
    )


class UserCommentVote(models.Model):
    user = models.ForeignKey(
        IbisUser,
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )
    is_upvote = models.BooleanField(default=True)
