from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import (
    RelevanceFilters,
    TimeFilters,
    TypeFilters,
    ExperienceLevelFilters,
    OnSiteOrRemoteFilters
)

__all__ = ['construct_query']


def construct_query(
        search_query: str,
        locations: list[str],
        apply_link: bool = False,
        skip_promoted_jobs: bool = True,
        page_offset: int = 0,
        limit: int = 25,
        company_jobs_url: str = None,
        relevance: str = RelevanceFilters.RECENT,
        time: str = TimeFilters.MONTH,
        type: list[str] = [TypeFilters.FULL_TIME, TypeFilters.PART_TIME, TypeFilters.CONTRACT, TypeFilters.INTERNSHIP],
        on_site_or_remote: list[str] = [OnSiteOrRemoteFilters.ON_SITE, OnSiteOrRemoteFilters.HYBRID, OnSiteOrRemoteFilters.REMOTE],
        experience: list[str] = [ExperienceLevelFilters.ENTRY_LEVEL, ExperienceLevelFilters.MID_SENIOR, ExperienceLevelFilters.DIRECTOR]
):
    return Query(
        query=search_query,
        options=QueryOptions(
            locations=locations,
            apply_link=apply_link,
            skip_promoted_jobs=skip_promoted_jobs,
            page_offset=page_offset,
            limit=limit,
            filters=QueryFilters(
                company_jobs_url=company_jobs_url,
                relevance=relevance,
                time=time,
                type=type,
                on_site_or_remote=on_site_or_remote,
                experience=experience
            )
        )
    )
