# Generated by Django 2.2.6 on 2020-07-14 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_auto_20200713_1946'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.RemoveField(
            model_name='player',
            name='AC_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='CF_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='CL_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='CO_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='DM_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='DR_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='HF_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='LI_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='RA_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='SA_rating',
        ),
        migrations.RemoveField(
            model_name='player',
            name='SU_rating',
        ),
        migrations.RemoveField(
            model_name='playerrecord',
            name='best_survival_REC',
        ),
        migrations.AddField(
            model_name='player',
            name='AC_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='CF_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='CL_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='CO_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='DM_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='DR_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='HF_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='LI_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='RA_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='SA_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='SU_figures_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerrecord',
            name='best_survival_time_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_survival_time_REC', to='web.SingleGameRecord'),
        ),
        migrations.AlterField(
            model_name='playerrecord',
            name='best_countdown_score_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_countdown_score_REC', to='web.SingleGameRecord'),
        ),
        migrations.AlterField(
            model_name='playerrecord',
            name='best_distance_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_distance_REC', to='web.SingleGameRecord'),
        ),
        migrations.AlterField(
            model_name='playerrecord',
            name='best_lines_count_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_lines_count_REC', to='web.SingleGameRecord'),
        ),
        migrations.AlterField(
            model_name='playerrecord',
            name='best_score_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_score_REC', to='web.SingleGameRecord'),
        ),
        migrations.AlterField(
            model_name='playerrecord',
            name='best_speed_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_speed_REC', to='web.SingleGameRecord'),
        ),
        migrations.AlterField(
            model_name='playerrecord',
            name='best_time_acc_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_time_acc_REC', to='web.SingleGameRecord'),
        ),
        migrations.AlterField(
            model_name='playerrecord',
            name='best_time_climb_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_time_climb_REC', to='web.SingleGameRecord'),
        ),
        migrations.AlterField(
            model_name='playerrecord',
            name='best_time_drag_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_time_drag_REC', to='web.SingleGameRecord'),
        ),
        migrations.AlterField(
            model_name='playerrecord',
            name='best_time_lines_REC',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_time_lines_REC', to='web.SingleGameRecord'),
        ),
    ]
