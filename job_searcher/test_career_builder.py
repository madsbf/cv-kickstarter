from job_searcher.career_builder import CareerBuilder
from job import Job
import os
import responses

test_path = os.path.dirname(__file__)
xml_path = os.path.join(test_path, 'career_builder_test_jobs.xml')

xml = open(xml_path).read()
jobs = [Job(title='Developer',
            company_name='Everett Kelley Associates, Inc.',
            teaser='Developer Large, Pennsylvania based, growing organization '
                   'has an immediate need for a ...  Developer Requirements '
                   'Microsoft SQL Server and associated...',
            job_url='http://api.careerbuilder.com/v1/joblink?TrackingID=UNTRKD'
                    '&HostSite=US&DID=JHR0PP5Z1YVB42FD92M'),
        Job(title='Software Developer',
            company_name='Meridian Staffing Services',
            teaser='Software Developer Role: You love working with a team of '
                   'hard-core product developers learning ...  Software '
                   'Developer Role: You love working with a...',
            job_url='http://api.careerbuilder.com/v1/joblink?TrackingID=UNTRKD'
                    '&HostSite=US&DID=JHP81K5XZMR1GDMXNL2')]


@responses.activate
def test_find_results():
    responses.add(responses.GET,
                  CareerBuilder.BASE_URL,
                  body=xml,
                  content_type="application/xml")

    found_jobs = CareerBuilder('developerkey').find_results(['developer'])
    for found_job, job in zip(found_jobs, jobs):
        assert found_job.title == job.title
        assert found_job.company_name == job.company_name
        assert found_job.teaser == job.teaser
        assert found_job.job_url == job.job_url


@responses.activate
def test_find_results_amount():
    responses.add(responses.GET,
                  CareerBuilder.BASE_URL,
                  body=xml,
                  content_type="application/xml")

    amount = CareerBuilder('developerkey').find_results_amount('developer')
    assert amount == 16892


def test_xml_to_jobs():
    found_jobs = CareerBuilder.xml_to_jobs(xml)
    for found_job, job in zip(found_jobs, jobs):
        assert found_job.title == job.title
        assert found_job.company_name == job.company_name
        assert found_job.teaser == job.teaser
        assert found_job.job_url == job.job_url
