"""Scrapers __init__."""
from .common import make_job_code, parse_iso_date, relative_time, clean_text, freshness_score
from .remotive_api import fetch_remotive_api
from .arbeitnow_api import fetch_arbeitnow_api
from .himalayas_api import fetch_himalayas_api
from .rss_feeds import (
    fetch_wwr_rss, fetch_remotive_rss, fetch_jobscollider_rss,
    fetch_jobalign_rss, fetch_workingviral_rss, fetch_jobicy_rss,
    fetch_remoteca_rss, fetch_authenticjobs_rss
)
from .rss_feeds_extended import (
    fetch_stackoverflow_rss, fetch_github_rss, fetch_developerjob_rss,
    fetch_flexjobs_rss, fetch_nofluff_rss, fetch_weworkpython_rss,
    fetch_javascript_rss, fetch_rubyonrails_rss, fetch_golangjobs_rss,
    fetch_rustiocean_rss, fetch_javaremote_rss, fetch_devopsboard_rss,
    fetch_designjobs_rss, fetch_marketingjobs_rss, fetch_salesjobs_rss,
    fetch_contentjobs_rss, fetch_datajobs_rss, fetch_aijobs_rss,
    fetch_securityjobs_rss, fetch_vmjobs_rss, fetch_translatorjobs_rss,
    fetch_educationjobs_rss, fetch_businessjobs_rss, fetch_projectmgmt_rss
)

__all__ = [
    "make_job_code", "parse_iso_date", "relative_time", "clean_text", "freshness_score",
    "fetch_remotive_api", "fetch_arbeitnow_api", "fetch_himalayas_api",
    "fetch_wwr_rss", "fetch_remotive_rss", "fetch_jobscollider_rss",
    "fetch_jobalign_rss", "fetch_workingviral_rss", "fetch_jobicy_rss",
    "fetch_remoteca_rss", "fetch_authenticjobs_rss",
    "fetch_stackoverflow_rss", "fetch_github_rss", "fetch_developerjob_rss",
    "fetch_flexjobs_rss", "fetch_nofluff_rss", "fetch_weworkpython_rss",
    "fetch_javascript_rss", "fetch_rubyonrails_rss", "fetch_golangjobs_rss",
    "fetch_rustiocean_rss", "fetch_javaremote_rss", "fetch_devopsboard_rss",
    "fetch_designjobs_rss", "fetch_marketingjobs_rss", "fetch_salesjobs_rss",
    "fetch_contentjobs_rss", "fetch_datajobs_rss", "fetch_aijobs_rss",
    "fetch_securityjobs_rss", "fetch_vmjobs_rss", "fetch_translatorjobs_rss",
    "fetch_educationjobs_rss", "fetch_businessjobs_rss", "fetch_projectmgmt_rss"
]
