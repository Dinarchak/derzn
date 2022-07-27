# Generated by Django 3.2.4 on 2022-07-27 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("drevo", "0017_categoryexpert"),
    ]

    operations = [
        migrations.CreateModel(
            name="InterviewAnswerExpertProposal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_yesno_answer_argument",
                    models.BooleanField(
                        default=False,
                        verbose_name="Аргумент вопроса Да-Нет? (нет - контраргумент)",
                    ),
                ),
                (
                    "is_incorrect_answer",
                    models.BooleanField(
                        default=False, verbose_name="некорректный ответ"
                    ),
                ),
                (
                    "согласен",
                    models.BooleanField(
                        default=True, verbose_name="Эксперт согласен с ответом?"
                    ),
                ),
                (
                    "comment",
                    models.JSONField(
                        default=dict, verbose_name="Аргументы и контраргументы (JSON)"
                    ),
                ),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "new_answer_text",
                    models.TextField(null=True, verbose_name="новый ответ от эксперта"),
                ),
                (
                    "admin_comment",
                    models.TextField(
                        default="", verbose_name="Комментарий администратора"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("APPRVE", "Принят"),
                            ("REJECT", "Не принят"),
                            ("ANSDPL", "Дублирует ответ"),
                            ("RESDPL", "Дублирует предложение"),
                        ],
                        max_length=6,
                        null=True,
                    ),
                ),
                (
                    "admin_reviewer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Администратор",
                    ),
                ),
                (
                    "answer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="answer_proposals",
                        to="drevo.znanie",
                        verbose_name="Ответ",
                    ),
                ),
                (
                    "expert",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="interview_results",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Ответивший эксперт",
                    ),
                ),
                (
                    "interview",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="interview_proposals",
                        to="drevo.znanie",
                        verbose_name="Интервью",
                    ),
                ),
                (
                    "new_answer",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="made_in_interview",
                        to="drevo.znanie",
                        verbose_name="Новый ответ",
                    ),
                ),
            ],
            options={
                "verbose_name": "Предложение эксперта",
                "verbose_name_plural": "Предложения эксперта",
                "ordering": ("-updated",),
            },
        ),
    ]
