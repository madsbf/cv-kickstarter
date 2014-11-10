PyCampus
========

Data Mining using Python project repository

# Jobs

This library allows simply job search and keyword evaluation in Danish and English. The library integrates with Go.dk for Danish jobs, and CareerBuilder.com for US jobs. The results are wrapped into a unified data structure.

For documentation of the CareerBuilder API, see:
http://developer.careerbuilder.com/endpoints/index
(Note: A developer key is needed in order to use the CareerBuilder API. Obtain one here: http://developer.careerbuilder.com)

For documentation of the Go.dk API, see:
http://moveon.dk/webservice/mobile.asmx
(Note: A GUID is needed in order to use the Go.dk API. You can obtain one by downloading the Android or iOS app, and monitoring the http requests to the server (F.x. using Charles - http://www.charlesproxy.com/).

Example of usage:

A simple job search on Career Builder

    >>> searcher = jobs.careerbuilder('DEVELOPER_KEY')
    >>> jobs = jobsearcher.find_results(keywords=['developer','python'], amount=25)
    
To find the amount of results for a specific keyword

    >>> amount = jobsearcher.find_results_amount(keyword='python')
    
With a job searcher, we can also perform keyword evaluation

    >>> eval = jobs.keyword_evaluator(searcher)
    >>> eval.evaluate_keyword('python')
