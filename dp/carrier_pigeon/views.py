from datetime import datetime

from django.views.generic import ListView, DetailView
from django.utils.timezone import utc

from braces.views import LoginRequiredMixin, SetHeadlineMixin

from carrier_pigeon.models import Message


class InboxListView(LoginRequiredMixin, SetHeadlineMixin, ListView):
    headline = "Inbox"
    model = Message
    paginate_by = 30
    template_name = "carrier_pigeon/list.html"

    def get_queryset(self):
        """
        Return all inbox messages for this user.
        """
        return self.request.user.received_messages.filter(
            recipient_archived=False
        )


class ArchiveListView(InboxListView):
    headline = "Archive"

    def get_queryset(self):
        """
        Return all archived messages for this user.
        """
        return self.request.user.received_messages.filter(
            recipient_archived=True
        )


class MessageDetailView(LoginRequiredMixin, SetHeadlineMixin, DetailView):
    model = Message
    template_name = "carrier_pigeon/detail.html"

    def get_headline(self):
        return u"Set This Shit"

    def get_object(self):
        """
        Set read_at if this is the first time viewing a message.
        """
        obj = super(MessageDetailView, self).get_object()

        if not obj.read_at:
            obj.read_at = datetime.utcnow().replace(tzinfo=utc)
            obj.save()

        return obj
