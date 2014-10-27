PyCampus
========

Data Mining using Python project repository

# Jobs

This library allows simply job search and keyword evaluation in Danish and English. The library integrates with Go.dk for Danish jobs, and CareerBuilder.com for US jobs. The results are wrapped into a unified data structure.

For documentation of CareerBuilder API, see:
http://developer.careerbuilder.com/endpoints/index
(Note: A developer key is needed in order to use the CareerBuilder API)

Go.dk does not provide any API documentation. Instead, we used Charles (http://www.charlesproxy.com/) to discover the web service calls.

Example of usage:

A simple job search on Career Builder

    >>> searcher = jobs.careerbuilder('DEVELOPER_KEY')
    >>> jobs = jobsearcher.find_results(keywords=['developer','python'], amount=25)
    
To find the amount of results for a specific keyword

    >>> amount = jobsearcher.find_results_amount(keyword='python')
    
With a job searcher, we can also perform keyword evaluation

    >>> eval = jobs.keyword_evaluator(searcher)
    >>> eval.evaluate_keyword('python')
