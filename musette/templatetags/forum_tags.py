# encoding:utf-8
from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils import formats, timezone
from django.utils.text import Truncator

from hitcount.models import HitCount

from ..models import Comment, Forum, Topic, Notification
from .photo import get_photo
from ..utils import (
    get_photo_profile, get_datetime_topic
)

register = template.Library()


@register.filter
def in_category(category):
    '''
        This tag filter the forum for category
    '''
    return Forum.objects.filter(
        category_id=category,
        hidden=False
    )


@register.filter
def get_tot_comments(idtopic):
    '''
        This tag filter return the total
        comments of one topic
    '''
    return Comment.objects.filter(
        topic_id=idtopic,
    ).count()


@register.simple_tag
def get_tot_views(idtopic):
    '''
        This tag filter return the total
        views for topic or forum
    '''
    try:
        content = Topic.objects.get(idtopic=idtopic)
        idobj = ContentType.objects.get_for_model(content)

        hit = HitCount.objects.get(
            object_pk=idtopic,
            content_type_id=idobj
        )
        total = hit.hits
    except Exception:
        total = 0

    return total


@register.filter
def get_path_profile(user):
    '''
        Return tag a with profile
    '''
    username = getattr(user, "username")
    tag = "<a href='/profile/" + username + "'>" + username + " </a>"

    return tag


@register.filter
def get_tot_users_comments(topic):
    '''
        This tag filter return the total
        users of one topic
    '''
    idtopic = topic.idtopic
    users = Comment.objects.filter(topic_id=idtopic)

    data = ""
    lista = []
    for user in users:
        usuario = user.user.username
        if not usuario in lista:
            lista.append(usuario)

            photo = get_photo(user.user.id)

            tooltip = "data-toggle='tooltip' data-placement='bottom' "
            tooltip += "title='" + usuario + "'"
            data += "<a href='/profile/" + usuario + "' " + tooltip + ">"
            data += "<img class='img-circle' src='" + str(photo) + "' "
            data += "width=30, height=30></a>"

    if len(users) == 0:
        usuario = topic.user.username
        iduser = topic.user.id

        photo = get_photo(iduser)
        data += "<a href='/profile/" + usuario + "'>"
        data += "<img class='img-circle' src='" + str(photo) + "' "
        data += "width=30, height=30></a>"

    return data


@register.filter
def get_tot_topics_moderate(forum):
    '''
        This filter return info about
        Few topics missing for moderate
    '''
    topics_count = forum.topics_count
    idforum = forum.idforum

    moderates = Topic.objects.filter(
        forum_id=idforum,
        moderate=True).count()
    return topics_count - moderates


@register.filter
def get_item_notification(notification):
    '''
    This filter return info about
    one notification of one user
    '''
    idobject = notification.idobject
    is_comment = notification.is_comment

    html = ""
    if is_comment:

        try:
            comment = Comment.objects.get(idcomment=idobject)
            forum = comment.topic.forum.name
            slug = comment.topic.slug
            idtopic = comment.topic.idtopic
            username = comment.user.username

            url_topic = "/topic/" + forum + "/" + \
                slug + "/" + str(idtopic) + "/"

            title = "<h5><a href='" + url_topic + "'><u>" + \
                comment.topic.title + "</u></h5></a>"

            # Data profile
            photo = get_photo_profile(comment.user.id)
            date = get_datetime_topic(notification.date)

            # Notificacion
            html += '<a class="content" href="' + url_topic + '">'
            html += '   <div class="notification-item">'
            html += '    <h4 class="item-title">'
            html += '<img class="img-circle" src="' + photo + '"'
            html += ' width=25 height=25 />'
            html += username + " - " + str(date) + '</h4>'
            html += '    <p class="item-info"> ' + title + '</p>'
            html += '  </div>'
            html += '</a>'
        except Comment.DoesNotExist:
            html = ""
    else:
        html = ""

    return html


@register.filter
def get_pending_notifications(user):
    '''
        This method return total pending notifications
    '''
    return Notification.objects.filter(
        is_view=False, iduser=user).count()


@register.filter
def get_last_activity(idtopic):
    '''
        This method return last activity of topic
    '''
    try:
        comment = Comment.objects.filter(
            topic_id=idtopic).order_by("-date")
    except Exception:
        comment = None

    if comment:
        # Get timezone for datetime
        d_timezone = timezone.localtime(comment[0].date)
        # Format data
        date = formats.date_format(d_timezone, "SHORT_DATETIME_FORMAT")

        # Return format data more user with tag <a>
        html = ""
        # html += get_path_profile(comment[0].user)
        html += " <p>" + str(date) + "</p>"
        return html
    else:
        topic = Topic.objects.get(idtopic=idtopic)

        # Get timezone for datetime
        d_timezone = timezone.localtime(topic.date)
        # Format data
        date = formats.date_format(d_timezone, "SHORT_DATETIME_FORMAT")

        # Return format data more user with tag <a>
        html = ""
        # html += get_path_profile(topic.user)
        html += " <p>" + str(date) + "</p>"
        return html