# Generated by Django 2.2.6 on 2020-07-14 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0017_auto_20200714_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='AC_figures_rating',
            new_name='AC_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='CF_figures_rating',
            new_name='CF_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='CL_figures_rating',
            new_name='CL_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='CO_figures_rating',
            new_name='CO_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='DM_figures_rating',
            new_name='DM_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='DR_figures_rating',
            new_name='DR_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='HF_figures_rating',
            new_name='HF_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='LI_figures_rating',
            new_name='LI_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='RA_figures_rating',
            new_name='RA_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='SA_figures_rating',
            new_name='SA_rating',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='SU_figures_rating',
            new_name='SU_rating',
        ),
    ]
