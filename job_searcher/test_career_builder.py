from career_builder import CareerBuilder
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
                    '&amp;HostSite=US&amp;DID=JHR0PP5Z1YVB42FD92M'),
        Job(title='Software Developer',
            company_name='Meridian Staffing Services',
            teaser='Software Developer Role: You love working with a team of '
                   'hard-core product developers learning ...  Software '
                   'Developer Role: You love working with a...',
            job_url='http://api.careerbuilder.com/v1/joblink?TrackingID=UNTRKD'
                    '&amp;HostSite=US&amp;DID=JHP81K5XZMR1GDMXNL2')]


@responses.activate
def test_find_results():
    responses.add(responses.GET,
                  CareerBuilder.BASE_URL,
                  body=xml,
                  content_type="application/xml")

    assert CareerBuilder('developerkey').find_results(['developer']) == jobs


@responses.activate
def test_find_results_amount():
    responses.add(responses.GET,
                  CareerBuilder.BASE_URL,
                  body=xml,
                  content_type="application/xml")

    assert CareerBuilder('developerkey').find_results_amount('developer') == 16892

def test_xml_to_jobs():
    assert CareerBuilder.xml_to_jobs(xml) == jobs
