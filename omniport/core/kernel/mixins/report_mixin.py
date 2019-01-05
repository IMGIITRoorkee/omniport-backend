import swapper
from django.db import models
from django.db.models import Count, Model


class ReportMixin(Model):
    """
    This mixin adds information about the reports against any object
    """

    reporters = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Person'),
        blank=True,
    )

    class Meta:
        """
        Meta class for ReportMixin
        """

        abstract = True

    @classmethod
    def objects_filter(cls, max_reports):
        """
        Return a query set of objects that satisfy the specified report count
        :param max_reports: the maximum reports of objects to keep in the set
        :return: a query set of objects with the specified report count
        """

        if hasattr(cls, 'objects'):
            return cls.objects.annotate(
                reporter_count=Count('reporters')
            ).filter(
                reporter_count__lte=max_reports
            )
        else:
            raise AttributeError('Class does not have attribute \'objects\'')

    @property
    def reporter_count(self):
        """
        Return the number of reporters of the object
        :return: the count of the reports again the object
        """

        return self.reporters.count()

    def has_reported(self, person):
        """
        Return whether the specified person has reported the object
        :param person: the person whose report status is being checked
        :return: True if the person is a reporter, False otherwise
        """

        return self.reporters.filter(pk=person.pk).exists()

    def file_report(self, person):
        """
        File the report on behalf of the specified person
        :param person: the person filing the report
        """

        self.reporters.add(person)

    def withdraw_report(self, person):
        """
        Withdraw the report on behalf of the specified person
        :param person: the person withdrawing the report
        """

        self.reporters.remove(person)

    def toggle_report(self, person):
        """
        Toggle the report on behalf of the specified person
        :param person: the person toggling the report
        """

        if person in self.reporters.all():
            self.withdraw_report(person)
        else:
            self.file_report(person)
