# Generated by Django 2.2.12 on 2020-07-10 09:55

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_auto_20190910_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedetailpage',
            name='accordions',
            field=wagtail.core.fields.StreamField([('satisfaction_panel', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('lead_text', wagtail.core.blocks.CharBlock(required=False)), ('intro_body', wagtail.core.blocks.RichTextBlock(blank=True)), ('teaching_stats_header', wagtail.core.blocks.CharBlock(required=False)), ('learning_opportunities_stats_header', wagtail.core.blocks.CharBlock(required=False)), ('assessment_stats_header', wagtail.core.blocks.CharBlock(required=False)), ('support_stats_header', wagtail.core.blocks.CharBlock(required=False)), ('organisation_stats_header', wagtail.core.blocks.CharBlock(required=False)), ('learning_resources_stats_header', wagtail.core.blocks.CharBlock(required=False)), ('learning_community_stats_header', wagtail.core.blocks.CharBlock(required=False)), ('student_voice_stats_header', wagtail.core.blocks.CharBlock(required=False)), ('nhs_placement_stats_header', wagtail.core.blocks.CharBlock(required=False)), ('data_source', wagtail.core.blocks.RichTextBlock(blank=True))], icon='collapse-down', required=True)), ('entry_information_panel', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('qualification_heading', wagtail.core.blocks.CharBlock(required=False)), ('qualification_intro', wagtail.core.blocks.CharBlock(required=False)), ('qualification_label_explanation_heading', wagtail.core.blocks.CharBlock(required=False)), ('qualification_label_explanation_body', wagtail.core.blocks.RichTextBlock(blank=True)), ('qualification_data_source', wagtail.core.blocks.RichTextBlock(blank=True)), ('tariffs_heading', wagtail.core.blocks.CharBlock(required=False)), ('tariffs_intro', wagtail.core.blocks.CharBlock(required=False)), ('tariffs_data_source', wagtail.core.blocks.RichTextBlock(blank=True))], icon='collapse-down', required=True)), ('after_one_year_panel', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('section_heading', wagtail.core.blocks.CharBlock(required=False)), ('intro', wagtail.core.blocks.CharBlock(required=False)), ('lead', wagtail.core.blocks.CharBlock(required=False)), ('label_explanation_heading', wagtail.core.blocks.CharBlock(required=False)), ('label_explanation_body', wagtail.core.blocks.RichTextBlock(blank=True)), ('data_source', wagtail.core.blocks.RichTextBlock(blank=True))], icon='collapse-down', required=True)), ('after_course_panel', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('section_heading', wagtail.core.blocks.CharBlock(required=False)), ('intro', wagtail.core.blocks.RichTextBlock(blank=True)), ('six_month_earnings_heading', wagtail.core.blocks.CharBlock(required=False)), ('six_month_earnings_explanation', wagtail.core.blocks.RichTextBlock(blank=True)), ('six_month_earnings_salary_range_heading', wagtail.core.blocks.CharBlock(required=False)), ('six_month_earnings_data_source', wagtail.core.blocks.RichTextBlock(blank=True)), ('three_years_earnings_heading', wagtail.core.blocks.CharBlock(required=False)), ('three_years_earnings_explanation', wagtail.core.blocks.RichTextBlock(blank=True)), ('three_years_earnings_salary_range_heading', wagtail.core.blocks.CharBlock(required=False)), ('three_years_earnings_data_source', wagtail.core.blocks.RichTextBlock(blank=True)), ('six_month_employment_heading', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_intro', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_lead', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_data_source', wagtail.core.blocks.RichTextBlock(blank=True)), ('six_month_employment_roles_heading', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_roles_intro', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_roles_label_explanation_heading', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_roles_label_explanation_body', wagtail.core.blocks.RichTextBlock(blank=True)), ('six_month_employment_roles_data_source', wagtail.core.blocks.RichTextBlock(blank=True)), ('common_jobs_heading', wagtail.core.blocks.CharBlock(required=False)), ('common_jobs_intro', wagtail.core.blocks.CharBlock(required=False)), ('common_jobs_data_source', wagtail.core.blocks.RichTextBlock(blank=True))], icon='collapse-down', required=True)), ('employment_after_course_panel', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_lead', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_data_source', wagtail.core.blocks.RichTextBlock(blank=True)), ('section_heading', wagtail.core.blocks.RichTextBlock(required=False)), ('intro', wagtail.core.blocks.CharBlock(blank=True)), ('six_month_employment_roles_heading', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_roles_label_explanation_heading', wagtail.core.blocks.CharBlock(required=False)), ('six_month_employment_roles_data_source', wagtail.core.blocks.RichTextBlock(blank=True))], icon='collapse-down', required=True)), ('accreditation_panel', wagtail.core.blocks.StructBlock([('heading', wagtail.core.blocks.CharBlock(required=False)), ('section_heading', wagtail.core.blocks.CharBlock(required=False))], icon='collapse-down', required=True))]),
        ),
    ]
