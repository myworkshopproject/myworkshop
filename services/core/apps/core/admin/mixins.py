from core.models import LogMixin


class HasLogAdminInlineMixin(object):
    def save_related(self, request, form, formsets, change):
        """Given the ``HttpRequest``, the parent ``ModelForm`` instance, the
        list of inline formsets and a boolean value based on whether the
        parent is being added or changed, save the related objects to the
        database. Note that at this point save_form() and save_model() have
        already been called.
        """

        for formset in formsets:
            if issubclass(formset.model, LogMixin):
                instances = formset.save(commit=False)

                for instance in instances:
                    instance.changed_by = request.user

                for added_obj in formset.new_objects:
                    added_obj.owner = request.user

                # for deleted_obj in formset.deleted_objects:
                #     pass

                # for changed_obj in formset.changed_objects:
                #     pass

        super(HasLogAdminInlineMixin, self).save_related(
            request, form, formsets, change
        )
