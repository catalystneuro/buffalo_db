import json
import pdb
from django.views.generic import (
    View,
    CreateView,
    TemplateView,
    FormView,
    DetailView,
    UpdateView,
)
from django.urls import reverse
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from .utils import get_mat_file_info

from actions.models import Session, Weighing
from misc.models import Lab
from subjects.models import Subject
from .models import (
    Task,
    SessionTask,
    SubjectFood,
    ChannelRecording,
    TaskCategory,
    BuffaloSubject,
    Electrode,
    StartingPoint,
)
from .forms import (
    TaskForm,
    SessionForm,
    SubjectForm,
    SessionTaskForm,
    TaskVersionForm,
    WeighingForm,
    SubjectFoodForm,
    ElectrodeBulkLoadForm,
)


class TaskCreateView(CreateView):
    template_name = "buffalo/task.html"
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["objects"] = Task.objects.exclude(name="").order_by("name")
        return context

    def get_success_url(self):
        return reverse("buffalo-tasks")


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse("buffalo-tasks")


class TaskCreateVersionView(CreateView):
    template_name = "buffalo/task_form.html"
    model = Task
    form_class = TaskVersionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.original_task = str(self.kwargs["pk"])
        form.instance.first_version = False
        form.instance.version = str(
            Task.objects.filter(original_task=self.kwargs["pk"]).count() + 2
        )
        form.save()

        return super(TaskCreateVersionView, self).form_valid(form)

    def get_form(self, form_class=None):
        if self.request.method == "GET":
            if "buffalo/task/" in self.request.environ["HTTP_REFERER"]:
                self.template_name = "buffalo/admin_task_form.html"
            task = Task.objects.get(pk=self.kwargs["pk"])
            form = TaskVersionForm(
                initial=(
                    {
                        "name": task.name,
                        "description": task.description,
                        "training": task.training,
                        "platform": task.platform,
                        "category": task.category,
                        "json": task.json,
                        "reward": task.reward,
                        "location": task.location,
                        "dataset_type": task.dataset_type,
                        "version": task.version,
                        "original_task": task.original_task,
                    }
                )
            )
            return form
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        return reverse("admin:index")


class subjectUpdateView(UpdateView):
    template_name = "buffalo/subject_form.html"
    model = Subject
    form_class = SubjectForm

    def get_context_data(self, **kwargs):
        context = super(subjectUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse("buffalo-subjects")


class SessionCreateView(CreateView):
    template_name = "buffalo/session.html"
    form_class = SessionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = Session.objects.exclude(name="")
        context["form_task"] = SessionTaskForm()

        return context

    def get_success_url(self):
        return reverse("buffalo-sessions")


class getTaskCategoryJson(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            task_category = request.GET.get("task_category_id")
            category = TaskCategory.objects.get(pk=task_category)
            data = category.json
            return JsonResponse({"category_json": data}, status=200)


class CreateTasksToSession(CreateView):
    template_name = "buffalo/tasks_selector_modal.html"
    form_class = SessionTaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sessions = Session.objects.all()
        context["objects"] = sessions.select_related("subject", "lab", "project")

        return context

    def get_success_url(self):
        return reverse("buffalo-sessions")


class SubjectDetailView(TemplateView):
    template_name = "buffalo/admin_subject_details.html"

    def get(self, request, *args, **kwargs):
        subject_id = self.kwargs["subject_id"]
        context = {
            "subject": Subject.objects.get(pk=subject_id),
            "sessions": Session.objects.filter(subject=subject_id).order_by('-start_time'),
            "weights": Weighing.objects.filter(subject=subject_id).order_by('-date_time'),
            "food": SubjectFood.objects.filter(subject=subject_id),
        }

        return self.render_to_response(context)


class SubjectWeighingCreateView(CreateView):
    template_name = "buffalo/subject_weight.html"
    form_class = WeighingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_success_url(self):
        return reverse("buffalo-subjects")


class SessionTaksDetails(TemplateView):
    template_name = "buffalo/admin_session_details.html"

    def get(self, request, *args, **kwargs):
        session_id = self.kwargs["session_id"]
        all_session_tasks = (
            SessionTask.objects.filter(session=session_id)
            .values(
                "id",
                "task__id",
                "task__name",
                "task__version",
                "session__name",
                "session__start_time",
                "date_time",
                "general_comments",
                "task_sequence",
                "dataset_type__name",
            )
            .order_by("task_sequence")
        )
        channels_recording = []
        session_task_dataset_type = {}
        session_tasks = []
        for session_task in all_session_tasks:
            session_task_id = session_task["task__id"]

            if session_task_id in session_task_dataset_type:

                session_task_dataset_type[session_task_id].append(
                    session_task["dataset_type__name"]
                )
            else:
                session_tasks.append(session_task)
                session_task_dataset_type.update(
                    {session_task_id: [session_task["dataset_type__name"]]}
                )
        channels_recording = ChannelRecording.objects.filter(session=session_id,)

        context = {
            "session": Session.objects.get(pk=session_id),
            "session_tasks": session_tasks,
            "channels_recording": list(channels_recording),
            "session_task_dataset_type": session_task_dataset_type,
        }

        return self.render_to_response(context)

class getTaskDatasetType(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            task_id = request.GET.get("task_id")
            task = Task.objects.filter(id=task_id).values("dataset_type__id")
            data = json.dumps(list(task), cls=DjangoJSONEncoder)
            return JsonResponse({"task_dataset_type": data}, status=200)
            
class ElectrodeBulkLoadView(FormView):
    form_class = ElectrodeBulkLoadForm
    template_name = "buffalo/electrode_bulk_load.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        subject_id = self.kwargs.pop('subject_id', None)
        if subject_id:
            kwargs['initial'] = {
                "subject": subject_id
            }
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            structure_name = form.cleaned_data['structure_name']
            subject_id = form.cleaned_data['subject']
            subject = BuffaloSubject.objects.get(pk=subject_id)
            if (not structure_name):
                structure_name = subject.nickname
            electrodes_info = get_mat_file_info(form.cleaned_data['file'], structure_name)
            for electrode_info in electrodes_info:
                electrode = Electrode.objects.filter(
                    subject=subject_id,
                    channel_number=str(electrode_info['channel'])
                ).first()
                if electrode:
                    electrode.create_new_starting_point_from_mat(electrode_info)
                else:
                    new_electrode = Electrode()
                    new_electrode.subject = subject
                    new_electrode.channel_number = str(electrode_info['channel'])
                    new_electrode.save()
                    new_electrode.create_new_starting_point_from_mat(electrode_info)
            messages.success(request, 'File loaded successful.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse("admin:buffalo_buffalosubject_changelist")
