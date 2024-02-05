# Generated by Django 5.0.1 on 2024-01-15 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('private_app', '0002_alter_address_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='study_program',
            field=models.ForeignKey(help_text='The program saved as a favorite by the user.', on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='private_app.studyprogram'),
        ),
        migrations.AlterField(
            model_name='link',
            name='link_type',
            field=models.CharField(choices=[('Website', 'Website'), ('ParcoursSuplink', 'ParcoursSup link'), ('SchoolWebsite', 'School Website'), ('Tiktok', 'Tiktok'), ('Instagram', 'Instagram'), ('Other', 'Other')], help_text='Type of website (Instagram, FB, etc.)', max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='about_me',
            field=models.TextField(blank=True, help_text='A profile description of the user.', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='student_at',
            field=models.ForeignKey(blank=True, help_text='FK to a program the student in which the student is or has enrolled.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='private_app.studyprogram'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='url_instagram',
            field=models.OneToOneField(blank=True, help_text="A url to the user's Instagram profile.", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_insta', to='private_app.link'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='url_tiktok',
            field=models.OneToOneField(blank=True, help_text="A url to the user's TikTok profile.", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_tiktok', to='private_app.link'),
        ),
    ]
