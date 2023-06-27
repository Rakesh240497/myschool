# Generated by Django 4.1.7 on 2023-06-09 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("singup", "0003_studentclass_alter_teacherclass_teacher"),
    ]

    operations = [
        migrations.CreateModel(
            name="Marks",
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
                ("classes", models.CharField(max_length=100)),
                ("username", models.CharField(max_length=100)),
                (
                    "exam_type",
                    models.CharField(
                        choices=[
                            ("Sem1", "Sem1"),
                            ("Sem2", "Sem2"),
                            ("Finals", "Finals"),
                        ],
                        max_length=10,
                    ),
                ),
                ("maths", models.DecimalField(decimal_places=2, max_digits=4)),
                ("science", models.DecimalField(decimal_places=2, max_digits=4)),
                ("labs", models.DecimalField(decimal_places=2, max_digits=4)),
                ("sports", models.DecimalField(decimal_places=2, max_digits=4)),
                (
                    "percentage",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                ("pf", models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name="studentclass",
            name="student",
            field=models.CharField(
                choices=[
                    ("test1", "test1"),
                    ("test3", "test3"),
                    ("test6", "test6"),
                    ("nanankal", "nanankal"),
                    ("ali", "ali"),
                    ("rakesh", "rakesh"),
                    ("test11", "test11"),
                    ("test12", "test12"),
                    ("test13", "test13"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="teacherclass",
            name="teacher",
            field=models.CharField(
                choices=[
                    ("test", "test"),
                    ("test4", "test4"),
                    ("admin", "admin"),
                    ("admin1", "admin1"),
                    ("test7", "test7"),
                    ("tanguturi", "tanguturi"),
                    ("somex", "somex"),
                    ("somexx", "somexx"),
                ],
                max_length=100,
            ),
        ),
    ]